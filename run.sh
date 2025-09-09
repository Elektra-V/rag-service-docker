docker compose down -v
docker compose build --no-cache --pull
docker compose up -d

# watch the init jobs finish, then the main ollama service:
docker compose logs -f ollama-init-llm
docker compose logs -f ollama-init-embed
docker compose logs -f ollama

# sanity checks
curl http://localhost:11434/            # Ollama welcome text
curl http://localhost:11434/api/tags    # should list your models
curl http://localhost:6333/readyz       # "OK"
curl http://localhost:8000/health/ready # API ready (after both are healthy)
