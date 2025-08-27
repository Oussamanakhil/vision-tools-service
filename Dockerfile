FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1

# (Optional for later) System binaries you’ll eventually need:
# ffmpeg, tesseract-ocr, mediainfo
# For the very first test, you can comment this block out.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg tesseract-ocr mediainfo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# This is the “start command” for RunPod when deploying from GitHub
CMD ["python","-u","handler.py"]
