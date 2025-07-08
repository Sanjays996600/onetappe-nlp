FROM python:3.8-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_md && \
    python -m spacy download xx_ent_wiki_sm

# Production stage
FROM python:3.8-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 nlpuser && \
    useradd -u 1001 -g nlpuser -s /bin/bash -m nlpuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment path to use virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production

# Copy application code
COPY --chown=nlpuser:nlpuser . /app/

# Expose port
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Switch to non-root user
USER nlpuser

# Run the application
CMD ["python", "api_integration.py", "--framework", "flask", "--host", "0.0.0.0", "--port", "5000"]