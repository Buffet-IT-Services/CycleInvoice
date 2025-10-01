FROM python:3.12-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc curl \
    libpq-dev \
    libcairo2 \
    libgirepository-1.0-1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

RUN useradd -m cycleinvoice && \
    mkdir -p /code/staticfiles && \
    chown -R cycleinvoice:cycleinvoice /code/staticfiles

USER cycleinvoice

EXPOSE 8000