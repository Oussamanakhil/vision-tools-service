# vision-tools-service
CPU microservice for **saliency**, **OCR**, **video frame extraction**, and **metadata parsing** on RunPod Serverless.

## Tasks / Inputs
- `task: "saliency"` + `image: <url|base64>`
- `task: "ocr"` + `image: <url|base64>`
- `task: "extract_frames"` + `video: <url|base64>` (+ optional `every_n`, `max_frames`)
- `task: "parse_metadata"` + `media: <url|base64>`

## RunPod
- **Worker Type:** CPU (e.g., `cpu3c-2-4`)
- **Start Command:** `python -u handler.py`
- **Autoscaling:** Min 0, Max 1–2, Autosuspend 5–10 min
- **Env Vars:** none required
