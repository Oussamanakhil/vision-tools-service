FROM runpod/worker-py:3.10-1

# System deps for OpenCV, Tesseract, and media probing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "handler.py"]
