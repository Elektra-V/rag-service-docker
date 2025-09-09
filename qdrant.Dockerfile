# qdrant.Dockerfile
FROM qdrant/qdrant:v1.11.0

ARG APP_UID=1001
ARG APP_GID=1001
RUN addgroup --system --gid ${APP_GID} qd \
 && adduser  --system --uid ${APP_UID} --ingroup qd qd

ENV QDRANT__STORAGE__STORAGE_PATH=/qdrant/storage
RUN mkdir -p /qdrant/storage && chown -R ${APP_UID}:${APP_GID} /qdrant

USER qd
