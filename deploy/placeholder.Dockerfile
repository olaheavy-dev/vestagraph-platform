# Placeholder app image (stage 5b group A). Standard library only, so there is no pip install.
# Build from the repository root:
#   docker build -f deploy/placeholder.Dockerfile --build-arg VESTAGRAPH_COMMIT=<sha> .
FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f

LABEL org.opencontainers.image.source="https://github.com/olaheavy-dev/vestagraph-platform"

ARG VESTAGRAPH_COMMIT=unknown
ENV VESTAGRAPH_COMMIT=$VESTAGRAPH_COMMIT \
    PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY packages/vestagraph-placeholder/src/ /app/src/

USER 10001:10001
EXPOSE 8080
CMD ["python", "-m", "vestagraph_placeholder"]
