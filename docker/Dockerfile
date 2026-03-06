FROM python:3.14-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG BUILD_TIME=undefined
ARG BUILD_VERSION=undefined

LABEL maintainer="Robert Olechowski <robertolechowski@gmail.com>"
LABEL license="Apache License 2.0"
LABEL org.opencontainers.image.authors="Robert Olechowski <robertolechowski@gmail.com>"

LABEL org.opencontainers.image.url="https://github.com/RobertOlechowski/k2000_visa_generator"
LABEL org.opencontainers.image.source="https://github.com/RobertOlechowski/k2000_visa_generator"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production \
    RR_BUILD_TIME=$BUILD_TIME \
    RR_BUILD_VERSION=$BUILD_VERSION

RUN groupadd -g 1000 appuser && useradd -m -u 1000 -g 1000 appuser

COPY ../requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

COPY --chown=appuser:appuser ./.. /app

RUN mkdir -p /app/logs /tmp/gunicorn && \
    chown -R appuser:appuser /app /tmp/gunicorn

USER appuser

EXPOSE 8000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "1", \
     "--threads", "1", \
     "--worker-class", "gthread", \
     "--worker-tmp-dir", "/tmp/gunicorn", \
     "app:app"]

