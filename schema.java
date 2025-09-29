┌────────────────────┐          push/PR           ┌──────────────────────┐
│   App Repo (API)   │  ───────────────────────▶  │   GitLab CI (App)    │
│  code + Dockerfile │                            │ test → integration → │
└─────────┬──────────┘                            │   build (Kaniko)     │
          │                                       └─────────┬────────────┘
          │               build & push                        │
          │         (sha-, branch, latest)                    │
          ▼                                                   ▼
   ┌──────────────────────┐                         ┌──────────────────────┐
   │ GitLab Container     │   image tags:           │  “Bump Manifests”    │
   │ Registry (OCI)       │  api:sha-abcdef1,       │  Job (in App CI)     │
   └─────────┬────────────┘  api:main, latest       └─────────┬────────────┘
             │                                               edits & MR
             │                                               (GitLab API)
             ▼                                                   ▼
   ┌──────────────────────┐                         ┌──────────────────────┐
   │ Manifests Repo       │ ◀────────────────────── │   Merge Request      │
   │ (CI config only)     │     updates image tag   │  (in Manifests repo) │
   └─────────┬────────────┘                         └─────────┬────────────┘
             │                                                │ triggers
             │                                                ▼
             │                                    ┌─────────────────────────┐
             │                                    │ GitLab CI (Manifests)   │
             │                                    │  • Job image = your API │
             │                                    │  • Services: Qdrant,    │
             │                                    │    Ollama               │
             │                                    │  • Start uvicorn        │
             │                                    │  • Curl /healthz        │
             │                                    └───────────┬─────────────┘
             │                                                │
             ▼                                                ▼
      (optional)                                          Merge MR
   ┌──────────────────────┐                             (green = passed)
   │ Deploy/Prod repo or  │
   │ env (future)         │
   └──────────────────────┘
