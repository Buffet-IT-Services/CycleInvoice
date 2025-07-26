
FROM python:3.12-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libcairo2 \
    libgirepository-1.0-1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY requirements/base.txt requirements/base.txt
COPY requirements/local.txt requirements/local.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m cycleinvoice && \
    mkdir -p /code/staticfiles && \
    chown -R cycleinvoice:cycleinvoice /code/staticfiles

USER cycleinvoice

EXPOSE 8000