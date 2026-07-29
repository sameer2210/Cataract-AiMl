FROM python:3.11-slim AS runtime

# Enforce secure Python runtime flags and default environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860 \
    TEMP_DIR=/tmp/cataract_temp

# Create unprivileged system user/group (UID/GID 1000) without login shell
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /usr/sbin/nologin appuser

WORKDIR /app

# Step 1: Install Python dependencies (Cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy application code and model weights
COPY app /app/app
COPY weights /app/weights

# Step 3: Hardened file permissions (Read-only source code to prevent runtime code tampering - CIS Benchmark 4.1)
RUN chown -R root:appgroup /app && \
    chmod -R 755 /app && \
    chmod -R 555 /app/app /app/weights

# Step 4: Prepare writable temporary directory in /tmp for Cloud Run Read-Only Root Filesystem compatibility
RUN mkdir -p /tmp/cataract_temp && \
    chown -R appuser:appgroup /tmp/cataract_temp && \
    chmod 700 /tmp/cataract_temp

USER appuser

EXPOSE 7860

# Container Healthcheck (Probes /health endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; port = os.environ.get('PORT', '7860'); urllib.request.urlopen(f'http://127.0.0.1:{port}/health')"

# Exec form via shell wrapper for dynamic PORT evaluation and SIGTERM propagation
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]