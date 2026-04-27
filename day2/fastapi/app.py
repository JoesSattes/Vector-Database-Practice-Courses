"""
Day 2 | FastAPI RAG Service
============================
Production-grade RAG API using RedisVL.

Pipeline: Intent Route → Semantic Cache → PDR Retrieval → Guard → Response
Features: Async connection pool, request timing, structured stats, graceful shutdown
"""

import os
import time
import logging
import statistics
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorQuery
from redisvl.extensions.llmcache import SemanticCache
from redisvl.extensions.message_history import SemanticMessageHistory
from redisvl.utils.vectorize import HFTextVectorizer

# ─── Configuration ────────────────────────────────────────────────────────────
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CACHE_THRESHOLD = 0.25      # Semantic similarity threshold for cache hits
GUARD_THRESHOLD = 0.35      # Max vector distance (lower = more relevant)
FAITHFULNESS_MIN = 0.4      # Min faithfulness score before refusing answer
CACHE_TTL = 300             # Cache TTL in seconds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-api")

# ─── Schema Definitions ───────────────────────────────────────────────────────
PDR_SCHEMA = {
    "index": {"name": "pdr_knowledge", "prefix": "chunk:", "storage_type": "json"},
    "fields": [
        {"name": "parent_id", "type": "tag"},
        {"name": "proposition", "type": "text"},
        {"name": "embedding", "type": "vector",
         "attrs": {"dims": 384, "algorithm": "flat", "distance_metric": "cosine"}}
    ]
}

INTENT_SCHEMA = {
    "index": {"name": "intent_router", "prefix": "route:", "storage_type": "json"},
    "fields": [
        {"name": "intent", "type": "tag"},
        {"name": "embedding", "type": "vector",
         "attrs": {"dims": 384, "algorithm": "flat", "distance_metric": "cosine"}}
    ]
}

# ─── Intents for Router ───────────────────────────────────────────────────────
INTENT_EXAMPLES = [
    {"intent": "product_specs",   "example": "What are the specs of the Aether laptop?"},
    {"intent": "product_specs",   "example": "Does it have a good GPU?"},
    {"intent": "pricing",         "example": "How much does the X1 cost?"},
    {"intent": "pricing",         "example": "What is the price of the Nebula tablet?"},
    {"intent": "technical_support", "example": "My GPU is overheating"},
    {"intent": "technical_support", "example": "The screen is flickering"},
    {"intent": "battery",         "example": "How long does the battery last?"},
    {"intent": "battery",         "example": "How do I calibrate the battery?"},
    {"intent": "shipping",        "example": "When will my order arrive?"},
    {"intent": "shipping",        "example": "My package is delayed"},
]

# ─── Global State ─────────────────────────────────────────────────────────────
class AppState:
    model: SentenceTransformer = None
    vectorizer: HFTextVectorizer = None
    pdr_index: AsyncSearchIndex = None
    intent_index: AsyncSearchIndex = None
    cache: SemanticCache = None
    raw_knowledge: dict = {}   # parent_id → full_text (in-memory)
    request_latencies: list = []
    cache_hits: int = 0
    cache_misses: int = 0
    total_requests: int = 0

state = AppState()


# ─── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting RAG service...")

    # Load embedding model
    state.model = SentenceTransformer(EMBED_MODEL)
    state.vectorizer = HFTextVectorizer(EMBED_MODEL)
    logger.info("✅ Embedding model loaded")

    # Create PDR index
    from redisvl.schema import IndexSchema
    pdr_schema = IndexSchema.from_dict(PDR_SCHEMA)
    state.pdr_index = AsyncSearchIndex(pdr_schema, redis_url=REDIS_URL)
    await state.pdr_index.create(overwrite=False)

    # Create Intent Router index
    intent_schema = IndexSchema.from_dict(INTENT_SCHEMA)
    state.intent_index = AsyncSearchIndex(intent_schema, redis_url=REDIS_URL)
    await state.intent_index.create(overwrite=True)

    # Seed intent router
    intent_docs = [
        {"intent": item["intent"],
         "embedding": state.model.encode(item["example"]).tolist()}
        for item in INTENT_EXAMPLES
    ]
    await state.intent_index.load(intent_docs)
    logger.info("✅ Intent router seeded with %d examples", len(intent_docs))

    # Create Semantic Cache
    state.cache = SemanticCache(
        name="rag_cache",
        redis_url=REDIS_URL,
        distance_threshold=CACHE_THRESHOLD,
        vectorizer=state.vectorizer,
        ttl=CACHE_TTL,
        overwrite=False
    )
    logger.info("✅ Semantic cache ready (threshold=%.2f, TTL=%ds)",
                CACHE_THRESHOLD, CACHE_TTL)
    logger.info("🟢 RAG service online at %s", REDIS_URL)

    yield

    # Shutdown cleanup
    await state.pdr_index.client.aclose()
    logger.info("👋 RAG service shutdown complete")


# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Day 2 RAG Service",
    description="Production RAG API powered by RedisVL",
    version="2.0.0",
    lifespan=lifespan
)


# ─── Middleware: Request Timing ────────────────────────────────────────────────
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Response-Time-Ms"] = str(latency_ms)
    if request.url.path == "/chat":
        state.request_latencies.append(latency_ms)
        state.total_requests += 1
    return response


# ─── Pydantic Models ──────────────────────────────────────────────────────────
class IngestRequest(BaseModel):
    parent_id: str
    text: str

class ChatRequest(BaseModel):
    user_id: str
    question: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    source: Optional[str]
    confidence: Optional[float]
    intent: Optional[str]
    cache_hit: bool
    latency_ms: float


# ─── Helper: Local LLM Simulation ────────────────────────────────────────────
def simulate_llm(question: str, context: str) -> str:
    """Simulates an LLM response using context. Replace with real LLM call."""
    excerpt = context[:300].strip()
    return (
        f"Based on our product documentation:\n\n"
        f"{excerpt}\n\n"
        f"To answer your question about '{question}': "
        f"the information above directly addresses this. "
        f"Please refer to the full product specification for details."
    )


# ─── Helper: Faithfulness Score ──────────────────────────────────────────────
def check_faithfulness(answer: str, context: str) -> float:
    """Simple faithfulness: fraction of answer tokens found in context."""
    context_words = set(context.lower().split())
    answer_words = [w for w in answer.lower().split() if len(w) > 3]
    if not answer_words:
        return 0.0
    hits = sum(1 for w in answer_words if w in context_words)
    return hits / len(answer_words)


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Liveness + readiness check."""
    try:
        client = state.pdr_index.client
        await client.ping()
        return {
            "status": "online",
            "redis": "connected",
            "model": EMBED_MODEL,
            "version": app.version
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis offline: {e}")


@app.post("/ingest")
async def ingest(req: IngestRequest):
    """
    Ingest a document into the PDR index.
    Decomposes text into atomic propositions and indexes each one.
    """
    try:
        # Propositional decomposition
        propositions = [s.strip() for s in req.text.split(". ") if len(s.strip()) > 10]
        if not propositions:
            raise HTTPException(status_code=400, detail="Text too short to decompose")

        # Store full text as parent
        state.raw_knowledge[req.parent_id] = req.text

        # Embed and index each proposition
        docs = []
        for prop in propositions:
            vec = state.model.encode(prop).tolist()
            docs.append({
                "parent_id": req.parent_id,
                "proposition": prop,
                "embedding": vec
            })

        await state.pdr_index.load(docs)
        logger.info("Ingested parent_id=%s → %d propositions", req.parent_id, len(docs))

        return {
            "status": "indexed",
            "parent_id": req.parent_id,
            "propositions_indexed": len(docs)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Ingest error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Full RAG pipeline:
    1. Route intent
    2. Check semantic cache
    3. PDR retrieval (if cache miss)
    4. Faithfulness guard
    5. Cache store + memory update
    """
    t_start = time.perf_counter()

    # ── Step 1: Intent Detection ──────────────────────────────────────────────
    q_vec = state.model.encode(req.question).tolist()
    intent_q = VectorQuery(q_vec, "embedding", return_fields=["intent"], num_results=1)
    intent_results = await state.intent_index.query(intent_q)
    detected_intent = intent_results[0]["intent"] if intent_results else "general"

    # ── Step 2: Semantic Cache Check ──────────────────────────────────────────
    cache_hit_list = state.cache.check(prompt=req.question)
    if cache_hit_list:
        state.cache_hits += 1
        cached = cache_hit_list[0]
        latency_ms = round((time.perf_counter() - t_start) * 1000, 2)
        return ChatResponse(
            answer=cached["response"],
            source=cached.get("metadata", {}).get("parent_id"),
            confidence=float(cached.get("metadata", {}).get("confidence", 1.0)),
            intent=detected_intent,
            cache_hit=True,
            latency_ms=latency_ms
        )

    state.cache_misses += 1

    # ── Step 3: PDR Retrieval ─────────────────────────────────────────────────
    vq = VectorQuery(
        q_vec, "embedding",
        return_fields=["parent_id", "proposition"],
        num_results=1
    )
    results = await state.pdr_index.query(vq)

    if not results or float(results[0]["vector_distance"]) > GUARD_THRESHOLD:
        latency_ms = round((time.perf_counter() - t_start) * 1000, 2)
        return ChatResponse(
            answer="🚨 I could not find reliable information to answer that question. "
                   "Please contact support or rephrase your query.",
            source=None,
            confidence=0.0,
            intent=detected_intent,
            cache_hit=False,
            latency_ms=latency_ms
        )

    parent_id = results[0]["parent_id"]
    matched_prop = results[0]["proposition"]
    confidence = round(1.0 - float(results[0]["vector_distance"]), 4)

    # Fetch full parent context
    full_context = state.raw_knowledge.get(
        parent_id, matched_prop  # fallback to proposition if parent not in memory
    )

    # ── Step 4: Generate Answer ───────────────────────────────────────────────
    answer = simulate_llm(req.question, full_context)

    # ── Step 5: Faithfulness Guard ────────────────────────────────────────────
    faithfulness = check_faithfulness(answer, full_context)
    if faithfulness < FAITHFULNESS_MIN:
        latency_ms = round((time.perf_counter() - t_start) * 1000, 2)
        return ChatResponse(
            answer="🚨 HALLUCINATION GUARD: The generated answer could not be verified "
                   "against source documents. Please contact support.",
            source=parent_id,
            confidence=faithfulness,
            intent=detected_intent,
            cache_hit=False,
            latency_ms=latency_ms
        )

    # ── Step 6: Cache Store ───────────────────────────────────────────────────
    state.cache.store(
        prompt=req.question,
        response=answer,
        metadata={"parent_id": parent_id, "confidence": confidence}
    )

    # ── Step 7: Agent Memory (if session provided) ────────────────────────────
    if req.session_id:
        try:
            memory = SemanticMessageHistory(
                name=f"session:{req.session_id}",
                redis_url=REDIS_URL,
                distance_threshold=0.3,
                session_tag=req.user_id
            )
            memory.add_messages([
                {"role": "user", "content": req.question},
                {"role": "assistant", "content": answer}
            ])
        except Exception as mem_err:
            logger.warning("Memory store failed (non-critical): %s", mem_err)

    latency_ms = round((time.perf_counter() - t_start) * 1000, 2)
    logger.info("chat: user=%s intent=%s cache=MISS conf=%.2f latency=%.0fms",
                req.user_id, detected_intent, confidence, latency_ms)

    return ChatResponse(
        answer=answer,
        source=parent_id,
        confidence=confidence,
        intent=detected_intent,
        cache_hit=False,
        latency_ms=latency_ms
    )


@app.get("/stats")
async def get_stats():
    """Real-time performance statistics."""
    total = state.cache_hits + state.cache_misses
    hit_rate = state.cache_hits / total if total > 0 else 0.0
    latencies = state.request_latencies[-1000:]  # Last 1000 requests

    p50 = statistics.median(latencies) if latencies else 0
    p95 = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
    p99 = sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0

    try:
        pdr_info = await state.pdr_index.info()
        doc_count = pdr_info.get("num_docs", "N/A")
    except Exception:
        doc_count = "N/A"

    return {
        "total_requests": state.total_requests,
        "cache_hits": state.cache_hits,
        "cache_misses": state.cache_misses,
        "cache_hit_rate": round(hit_rate, 4),
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_p99_ms": round(p99, 2),
        "pdr_docs_indexed": doc_count,
        "cache_threshold": CACHE_THRESHOLD,
        "guard_threshold": GUARD_THRESHOLD,
    }


@app.delete("/cache")
async def flush_cache():
    """Invalidate the entire semantic cache (useful for testing)."""
    try:
        state.cache.clear()
        state.cache_hits = 0
        state.cache_misses = 0
        return {"status": "cache_flushed", "message": "Semantic cache cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
