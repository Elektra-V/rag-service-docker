# ollama.Dockerfile
ARG OLLAMA_BASE_TAG=0.3.14
FROM ollama/ollama:${OLLAMA_BASE_TAG}

# Create non-root user and a writable models dir.
ARG APP_UID=1002
ARG APP_GID=1002
RUN addgroup --system --gid ${APP_GID} app \
 && adduser  --system --uid ${APP_UID} --ingroup app app
ENV OLLAMA_MODELS=/models
RUN mkdir -p /models && chown -R ${APP_UID}:${APP_GID} /models

# IMPORTANT: keep upstream ENTRYPOINT ["ollama"] and CMD ["serve"]
USER app