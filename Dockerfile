# =============================================================================
# CookShare Chatbot - Docker Image
# Deployment với llama-cpp-python + GGUF model
# =============================================================================

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
# Note: llama-cpp-python cần build từ source
RUN pip install --no-cache-dir --upgrade pip && \
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api.py .
COPY model.py .
COPY app.py .

# Tạo thư mục models (file sẽ được upload sau qua Railway CLI)
RUN mkdir -p models

# Environment variables
ENV GGUF_MODEL_PATH=models/cookshare.gguf
# PORT sẽ được Railway tự động set khi deploy

# Expose port (Railway sẽ tự động map PORT từ env variable)
# EXPOSE không thể dùng biến, nhưng Railway sẽ tự động detect
EXPOSE 7860

# Health check
# Railway sẽ tự động set PORT, app.py sẽ đọc từ env
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-7860}/health || exit 1

# Run the application
# Railway sẽ tự động set PORT, app.py sẽ đọc từ env
CMD ["python", "app.py"]
