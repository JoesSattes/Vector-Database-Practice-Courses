# 🛰️ Vector Database Mastery: From Math to Production

Welcome to the definitive hands-on curriculum for Vector Databases and Semantic Search. This course is designed to take you from the geometric foundations of embeddings to deploying high-performance, containerized AI services.

---

## 🗺️ Curriculum Roadmap

### 📅 Day 1: Foundations & Core RedisVL
Master the math and the basics of Vector Databases with granular, step-by-step labs.

| Notebook | Topic | Description |
| :--- | :--- | :--- |
| **0. Environment** | `docker/` | Master Multi-Container Architecture and Internal DNS. |
| **1. Math & Theory** | `foundation/` | Euclidean vs Cosine, IVF/PQ algorithms from scratch. |
| **2. FAISS Deep-Dive** | `foundation/` | Benchmarking HNSW and detecting near-duplicates. |
| **3. Redis-Vector-DB** | `redis/` | Hybrid schemas, Geo-discovery, and Semantic Caching. |
| **Capstone Project** | `redis/` | Build a "VIP Recommendation Sandbox" with auto-verifiers. |

### 📅 Day 2: Production RAG Engineering (Micro-Lesson Format)
Step-by-step workshops with `SHOW_INSIGHTS` instructor toggle and end-of-notebook assignments.

| Notebook | Location | Description |
| :--- | :--- | :--- |
| **D2-NB00. RAG Foundations** | `day2/notebooks/` | Theory: RAG taxonomy, chunking strategies, RAGAS metrics, failure modes. |
| **D2-NB01. Async & Scale** | `day2/notebooks/` | `AsyncSearchIndex`, `asyncio.gather`, throughput benchmarking, retry logic. |
| **D2-NB02. Hybrid Search + RRF** | `day2/notebooks/` | `VectorQuery` with `Tag`/`Num`/`Text` filters; Reciprocal Rank Fusion from scratch. |
| **D2-NB03. Agent Memory** | `day2/notebooks/` | `SemanticMessageHistory`, token budgeting, TTL expiry, multi-user sessions. |
| **D2-NB04. Production RAG** | `day2/notebooks/` | `HFTextVectorizer`, `SemanticCache`, PDR pattern, intent routing, 3-layer pipeline. |
| **D2-NB05. RAG Evaluation** | `day2/notebooks/` | RAGAS-style metrics from scratch, golden dataset, hallucination guard, regression testing. |
| **D2-NB06. FastAPI Server** | `day2/notebooks/` | Interactive FastAPI development directly inside Jupyter using `uvicorn.run`. |
| **D2-NB07. FastAPI Client** | `day2/notebooks/` | Call the running RAG API, cache warmup, latency analysis, load testing. |

---

## 🛠️ Technology Stack

- **Vector Database**: [Redis Stack](https://redis.io/docs/latest/develop/interact/search-and-query/vector-search/) (Native Vector + Geo-Spatial + JSON)
- **Indexing Engines**: [FAISS](https://github.com/facebookresearch/faiss) (C++ High Performance Search)
- **Python Framework**: [RedisVL](https://redisvl.com) (Redis Vector Library)
- **Embeddings**: [Sentence-Transformers](https://www.sbert.net/) (all-MiniLM-L6-v2)
- **Environment**: [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

For installation guide, please refer to [INSTALLATION GUIDE](https://docs.google.com/document/d/1H8pMuY0zIUZilTgAcXnI8vzflfOIh8cR2SAALI0VEj0).

### 1. Prerequisites
- [Docker & Docker Compose](https://www.docker.com/get-started) installed.
- Python 3.9+ (Optional: Only if running the generator script).

### 2. Launch the Environment

**Day 1** — Jupyter + Redis only:
```bash
cd docker
docker compose up -d
```

**Day 2** — Add the FastAPI RAG service:
```bash
cd docker
docker compose --profile day2 up -d
```
> The `--profile day2` flag starts the `fastapi-service` container in addition to Jupyter and Redis.
> Day 1 notebooks are unaffected — the `fastapi-service` only activates when explicitly requested.

### 3. Access the Tools
- **Jupyter Notebooks**: Open [http://localhost:8888](http://localhost:8888)
- **Redis Insight (GUI)**: Open [http://localhost:8001](http://localhost:8001) to visually inspect your Vector Graphs and JSON records.

---

## 🔍 Why this course?

We move beyond "Hello World" RAG applications. This curriculum focuses on the **Engineering Rigor** required for production:
- **Hybrid Filtering**: Learn why filtering before searching is the key to 100M+ scale.
- **Semantic Caching**: Reduce LLM costs and latency to < 1ms.
- **Graph Topology**: Visualize HNSW layers to understand why your search is fast.
- **Geo-Semantic Discovery**: Blend physical proximity with semantic intent.

## Contribution
- Sattaya Singkul

---

*Built for engineers, by engineers. Let's build the future of retrieval.*
