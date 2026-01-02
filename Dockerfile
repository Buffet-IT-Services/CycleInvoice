FROM python:3.12-slim@sha256:8fbd0afc32e6cb14696c2fc47fadcda4c04ca0e766782343464bd716a6dc3f96
LABEL maintainer="Buffet IT Services GmbH"

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libcairo2 \
    libffi-dev \
    libgirepository-1.0-1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash cycleinvoice

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

RUN mkdir -p /code/staticfiles && \
    chown -R cycleinvoice:cycleinvoice /code

USER cycleinvoice

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/api/healthcheck/ || exit 1

EXPOSE 8000