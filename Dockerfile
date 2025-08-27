# GPU-capable base with Python 3.10 (good for vision tasks)
FROM runpod/base:0.6.0-cuda11.8.0

# System deps for video/image/OCR
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    mediainfo \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY handler.py .

# Serverless entry
CMD ["python", "-u", "handler.py"]
