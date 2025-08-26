# Public base image
FROM python:3.10-slim

# System deps for OpenCV, Tesseract and media probing
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr libtesseract-dev \
    ffmpeg \
    libgl1 libglib2.0-0 libsm6 libxext6 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Helpful runtime flags
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Start the RunPod serverless worker
CMD ["python", "-m", "runpod.serverless.worker", "handler.main"]
