# Stage 1: Build Python dependencies
FROM python:3.13-slim AS python-deps

ARG BUILD_VERSION=undefined
ARG BUILD_TIME=undefined

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project

# Stage 2: Final Python runtime
FROM python:3.13-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG BUILD_VERSION=undefined
ARG BUILD_TIME=undefined

LABEL maintainer="Robert Olechowski <robertolechowski@gmail.com>"
LABEL license="Apache License 2.0"
LABEL org.opencontainers.image.authors="Robert Olechowski <robertolechowski@gmail.com>"
LABEL org.opencontainers.image.url="https://github.com/RobertOlechowski/k2000_visa_generator"
LABEL org.opencontainers.image.source="https://github.com/RobertOlechowski/k2000_visa_generator"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    FLASK_DEBUG=0 \
    VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV RR_BUILD_VERSION=$BUILD_VERSION \
    RR_BUILD_TIME=$BUILD_TIME

RUN groupadd -g 1000 appuser && \
    useradd -m -u 1000 -g 1000 appuser && \
    mkdir -p /app/.logs && \
    chown -R appuser:0 /app && \
    chmod -R g+rwX /app

COPY --from=python-deps --chown=appuser:0 /app/.venv /app/.venv

COPY --chown=appuser:0 app/ /app/app/
COPY --chown=appuser:0 config/ /app/config/
COPY --chown=appuser:0 static/ /app/static/
COPY --chown=appuser:0 wsgi.py /app/

RUN chmod -R g+rwX /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "1", \
     "--threads", "1", \
     "--worker-tmp-dir", "/tmp", \
     "--no-control-socket", \
     "wsgi:app"]
