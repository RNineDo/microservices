FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip setuptools && pip install --no-cache-dir .

COPY services/ services/

ENV PYTHONPATH=/app
