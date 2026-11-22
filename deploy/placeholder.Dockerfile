# Placeholder app image (stage 5b group A). Standard library only, so there is no pip install.
# Build from the repository root:
#   docker build -f deploy/placeholder.Dockerfile --build-arg VESTAGRAPH_COMMIT=<sha> .
FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

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
