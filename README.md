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

### 📅 Day 2: Advanced Engineering & RAG Blueprint
The production masterclass consolidated into two high-density sessions.

| Notebook | Topic | Description |
| :--- | :--- | :--- |
| **4. Advanced Engineering** | `redis/` | **Masterclass**: Async Pipelines, Hybrid RRF, Semantic Memory, Intent Routing, and Index DevOps/CLI. |
| **5. Production RAG** | `app/` | **Blueprint**: Deep Ingestion (Propositions), Multi-Modal CLIP Search, and RAG Evaluators. |
| **6. API Deployment** | `app/` | **Scaling**: Building a production-grade **FastAPI** service with Async Connection Pooling. |

---

## 🛠️ Technology Stack

- **Vector Database**: [Redis Stack](https://redis.io/docs/latest/develop/interact/search-and-query/vector-search/) (Native Vector + Geo-Spatial + JSON)
- **Indexing Engines**: [FAISS](https://github.com/facebookresearch/faiss) (C++ High Performance Search)
- **Python Framework**: [RedisVL](https://redisvl.com) (Redis Vector Library)
- **Embeddings**: [Sentence-Transformers](https://www.sbert.net/) (all-MiniLM-L6-v2)
- **Environment**: [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### 1. Prerequisites
- [Docker & Docker Compose](https://www.docker.com/get-started) installed.
- Python 3.9+ (Optional: Only if running the generator script).

### 2. Launch the Environment
Everything is pre-configured. Run the following command from the root directory:

```bash
cd docker
docker-compose up -d
```

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
