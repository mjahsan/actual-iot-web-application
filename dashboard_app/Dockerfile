# Use a modern, explicit, secure base image
FROM python:3.11-slim-bookworm

# Prevent Python from writing .pyc files to disk and ensure logs dump immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip and install build dependencies safely (Debian-based slim images already have pip)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix Layer Caching: Copy requirements first so dependencies are cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Security Hardening: Create a non-privileged system user for execution
RUN groupadd -r devopsuser && useradd -r -g devopsuser devopsuser
# Copy application code and transfer ownership
COPY --chown=devopsuser:devopsuser . .

# Drop root privileges completely
USER devopsuser

# Document the port the application listens on
EXPOSE 5000

CMD ["python", "app.py"]