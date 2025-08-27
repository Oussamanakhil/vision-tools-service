# Small, GPU-capable base with Python 3.10 + CUDA/cuDNN
FROM runpod/base:0.6.0-cuda11.8.0

# System deps for video/image/ocr
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ffmpeg \
    tesseract-ocr \
    mediainfo \
 && rm -rf /var/lib/apt/lists/*

# Copy code
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

# Serverless entry
CMD ["python", "-u", "handler.py"]
