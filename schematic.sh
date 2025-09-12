                             ┌───────────────────────────┐
                             │          Client           │
                             │ (curl / Postman / UI)     │
                             └─────────────▲─────────────┘
                                           │ REST (HTTP)
                                           │
                                           ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                        Docker Compose Project (rag-api)                       │
│                       Shared network: rag-api_default                         │
│                                                                               │
│   ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐  │
│   │       API        │       │     Qdrant       │       │      Ollama      │  │
│   │ (FastAPI app)    │       │ (Vector DB)      │       │ (LLM + Embeds)  │  │
│   │ Port: 8080→8000  │       │ Port: 6333       │       │ Port: 11434      │  │
│   │ Vol: ./data:/data│       │ Vol: qdrant_storage │    │ Vol: ollama_models ││
│   │ Image: rag-api   │       │ Image: qdrant    │       │ Vol: ./models:/models│
│   │ Controllers +    │<─────▶│ Stores embeddings│       │ Models:            │ │
│   │ Services layer   │       │ & metadata       │       │  • nomic-embed-text │ │
│   │                  │       │                  │       │  • zephyr-7b-beta   │ │
│   └──────────────────┘       └──────────────────┘       └──────────────────┘  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ Ingest from
                                           ▼
                               ┌───────────────────────────┐
                               │      Data Sources         │
                               │  • arXiv (API reader)     │
                               │  • Local PDFs (./data)    │
                               └───────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                   Client                                    │
│                 (curl / Postman / simple web front-end)                     │
└───────────────────────────────▲──────────────────────────────────────────────┘
                                │  REST (HTTP)
                                │
                                │
┌────────────────────────────────┴────────────────────────────────────────────┐
│                                   API                                       │
│                          (FastAPI in Docker)                                │
│ Port: 8080→8000                                                            │
│ Image: local/rag-api:0.1.0                                                 │
│ Volume: ./data → /data  (optional PDFs)                                     │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │  Controllers: kb_controller, query_controller                           │ │
│ │  Services:    KBService, QueryService, QdrantService, OllamaService     │ │
│ │  Responsibilities:                                                      │ │
│ │   • Ingest (arXiv / PDFs) → embed → write vectors to Qdrant             │ │
│ │   • Query → retrieve top-k from Qdrant → prompt Zephyr LLM              │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└───────────────┬───────────────────────────────┬──────────────────────────────┘
                │                               │
                │ gRPC/HTTP (SDK)               │ HTTP (REST)
                │                               │
┌───────────────▼───────────────┐   ┌─────────────────────────────────────────┐
│            Qdrant             │   │                 Ollama                  │
│         (Vector DB)           │   │        (LLM + Embedding server)         │
│ Port: 6333:6333               │   │ Port: 11434:11434                       │
│ Image: qdrant/qdrant:v1.11.0  │   │ Image: ollama/ollama:0.3.14             │
│ Volume: qdrant_storage:/qdrant│   │ Vol: ollama_models:/root/.ollama        │
│ /storage                      │   │ Vol: ./models → /models:ro              │
│ Responsibilities:             │   │ Models:                                  │
│  • Store embeddings & metadata│   │  • LLM:  zephyr-7b-beta (local GGUF)     │
│  • Similarity search (top-k)  │   │  • Embed: nomic-embed-text              │
└───────────────────────────────┘   │ Responsibilities:                        │
                                    │  • Serve embeddings for ingestion        │
                                    │  • Generate final answers (LLM)          │
                                    └──────────────────────────────────────────┘

           ┌───────────────────────────────────────────────────────────────┐
           │                      Data Sources / Files                      │
           │  • arXiv (via reader)                                         │
           │  • Local PDFs in ./data (mounted as /data)                    │
           └───────────────────────────────────────────────────────────────┘

           ┌───────────────────────────────────────────────────────────────┐
           │                      Model Artifacts                           │
           │  ./models/zephyr-7b-beta/                                     │
           │    ├─ Modelfile  (FROM ./zephyr-7b-beta.Q5_K_M.gguf, params)  │
           │    └─ zephyr-7b-beta.Q5_K_M.gguf (local LLM weights)          │
           └───────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────────────┐
│                               Host (Ubuntu)                                   │
│  Files:                                                                        │
│   - docker-compose.yml                                                         │
│   - .env                                                                       │
│   - models/zephyr-7b-beta/{ Modelfile, zephyr-7b-beta.Q5_K_M.gguf }           │
│   - api/{ Dockerfile, requirements.txt, app/... }                              │
│   - data/  (optional PDFs)                                                     │
└───────────────┬───────────────────────────────────────────────────────────────┘
                │  docker compose up -d
                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                            Docker Network: rag-api_default                    │
└───────────────┬───────────────────────┬───────────────────────┬──────────────┘
                │                       │                       │
                │                       │                       │
        (1) QDRANT service       (2) OLLAMA service        (3) API service
        ─────────────────        ─────────────────         ────────────────
Service name: qdrant            Service name: ollama       Service name: api
Image: qdrant/qdrant:v1.11.0    Image: ollama/ollama:0.3.14 Image: local/rag-api:0.1.0
Ports: 6333:6333                Ports: 11434:11434          Ports: 8080:8000
Volume: qdrant_storage:/qdrant/  Volume: ollama_models:/root/.ollama
        storage                 Binds: ./models:/models:ro  Bind: ./data:/data (optional)
Env: —                          Env:
                                - OLLAMA_MODELS=/root/.ollama
                                - OLLAMA_NO_GPU=1
                                (models visible under /models/...)

                │                       │                       │
                │                       │                       │
                │     ┌─────────────────┴───────────────┐       │
                │     │   One-time helper service       │       │
                │     │  (optional but recommended)     │       │
                │     └─────────────────┬───────────────┘       │
                │                       │                       │
                │               Service: model-create            │
                │               Image: ollama/ollama:0.3.14      │
                │               Command:                         │
                │                `ollama create zephyr-7b-beta   │
                │                    -f /models/zephyr-7b-beta/  │
                │                         Modelfile`             │
                │               Volumes:                         │
                │                - ollama_models:/root/.ollama   │
                │                - ./models:/models              │
                │               Purpose: register local GGUF as  │
                │                        Ollama model tag        │
                │
                ▼
      ┌──────────────────────────────────────────────────────────┐
      │                         Data Flow                        │
      └──────────────────────────────────────────────────────────┘

 Ingestion path:
   Client → API (/api/kb/load_arxiv or /api/kb/ingest_pdfs)
     → KBService (uses OllamaEmbedding: OLLAMA_EMBED) → embeds chunks
     → Qdrant (stores vectors + metadata)

 Query path:
   Client → API (/api/query) → QueryService
     → Qdrant similarity search (top_k)
     → Ollama LLM (zephyr-7b-beta) with retrieved context
     ← Answer + source snippets to client
     

                             ┌───────────────────────────┐
                             │          Client           │
                             │  (curl / Postman / UI)    │
                             └─────────────▲─────────────┘
                                           │  REST
                        ┌──────────────────┴───────────────────┐
                        │ 1) Ingest: /api/kb/*                 │
                        │ 2) Query:  /api/query                │
                        └──────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                        Docker Compose Project (rag-api)                       │
│                       (shared network: rag-api_default)                       │
│                                                                               │
│   ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐│
│   │       API        │        │     Qdrant       │        │      Ollama      ││
│   │ (FastAPI)        │        │ (Vector DB)      │        │ (LLM + Embeds)   ││
│   │ Port: 8080→8000  │        │ Port: 6333       │        │ Port: 11434      ││
│   │ Vol: ./data:/data│        │ Vol: qdrant_...  │        │ Vol: ollama_...  ││
│   │ Controllers/     │        │ Stores vectors   │        │ Models:          ││
│   │ Services layer   │        │ + metadata       │        │  • nomic-embed    ││
│   └─────────┬────────┘        └─────────┬────────┘        │  • zephyr-7b     ││
│             │                           │                 └─────────┬────────┘│
│             │ Ingestion Flow            │ Retrieval Flow              │ Gen/Embed│
│             │                           │                             │          │
│   (1) /api/kb/load_arxiv or /ingest_pdfs│                             │          │
│             │                           │                             │          │
│             ▼                           │                             ▼          │
│   Chunk + Embed (via Ollama: nomic-embed) ───────────────────────────▶Embed vecs │
│             │                                                          (POST /api/embeddings)
│             │                                                          ▲          │
│             └──────────────────────────────▶  Upsert vectors  ─────────┘          │
│                                             (Qdrant upsert)                       │
│                                                                                   │
│   (2) /api/query ────────────────────────────────────────────────────────────────▶ │
│             │                                                                     │
│             ▼                                                                     │
│   Retrieve top-k from Qdrant ◀────────────────────────────────────────────────────┘
│             │
│             ▼
│   Call LLM w/ context (Ollama: zephyr-7b-beta)
│             │
│             ▼
│   Answer + Sources → Client
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

                 ┌────────────────────────────┐          ┌────────────────────┐
                 │        arXiv (external)    │          │  Local PDFs (host) │
                 │  API fetch via reader      │          │  ./data → /data    │
                 └──────────────▲─────────────┘          └──────────▲─────────┘
                                │                                    │
                                └───────── Ingestion into API ───────┘

