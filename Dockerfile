# EnforceAI - Multi-Agent Governance Platform
# Production-ready Docker image

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r enforceai && useradd -r -g enforceai enforceai

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R enforceai:enforceai /app

# Switch to non-root user
USER enforceai

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "demo_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Multi-stage build for production
FROM base as production

# Install additional production dependencies
RUN pip install --no-cache-dir gunicorn

# Copy production configuration
COPY docker/production.conf /app/production.conf

# Production command
CMD ["gunicorn", "--config", "production.conf", "app:app"]

# Development stage
FROM base as development

# Install development dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install development tools
RUN pip install --no-cache-dir \
    jupyter \
    ipython \
    debugpy

# Expose additional ports for development
EXPOSE 8888 5678

# Development command
CMD ["streamlit", "run", "demo_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]

# Testing stage
FROM development as testing

# Copy test files
COPY tests/ ./tests/

# Run tests
RUN python -m pytest tests/ --cov=agents --cov-report=html

# Lambda deployment stage
FROM public.ecr.aws/lambda/python:3.11 as lambda

# Copy requirements and install
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy application code
COPY agents/ ${LAMBDA_TASK_ROOT}/agents/
COPY policies/ ${LAMBDA_TASK_ROOT}/policies/
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]