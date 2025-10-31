FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
 && apt-get install --no-install-recommends -y build-essential git curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
 && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
 CMD curl -fsS http://127.0.0.1:$PORT/docs || exit 1

 CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker",  "--preload", "--workers", "1", "--bind", "0.0.0.0:8000", "src.main.server.server:app"]