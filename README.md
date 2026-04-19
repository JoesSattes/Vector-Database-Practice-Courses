# 🛰️ Vector Database Mastery: From Math to Production

Welcome to the definitive hands-on curriculum for Vector Databases and Semantic Search. This course is designed to take you from the geometric foundations of embeddings to deploying high-performance, containerized AI services.

---

## 🗺️ Curriculum Roadmap

### 📅 Day 1: The Core Foundations
Master the math, the algorithms, and the industrial indexers.

| Notebook | Topic | Description |
| :--- | :--- | :--- |
| **0. Docker Environment** | `docker/` | Master Multi-Container architecture, DNS networking, and data persistence. |
| **1. Vector Foundations** | `foundation/` | The math of Cosine Similarity, Dot Product, and Product Quantization (PQ). |
| **2. FAISS Deep Dive** | `foundation/` | Benchmarking IVF, HNSW, and Radius Search using industry-standard C++ builders. |
| **3. Redis-Vector-DB** | `redis/` | Deploying RedisVL for hybrid filtering, under-the-hood processing, and semantic caching. |
| **Capstone Assignment** | `redis/` | Build a "VIP Recommendation Sandbox" from scratch with automated verifiers. |

### 📅 Day 2: AI-Agent & RAG Services
*Coming Soon: Building end-to-end services with LLM integration.*

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
