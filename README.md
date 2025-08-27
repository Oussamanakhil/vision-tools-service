# Vision Tools Service

Tasks (single endpoint, RunPod Serverless):
- `saliency` — returns heatmap (PNG base64)
- `ocr` — returns text
- `extract_frames` — returns list of JPEG base64 frames
- `parse_metadata` — returns MediaInfo JSON

## Build & Deploy on RunPod
1. New Endpoint → **Serverless → From Git Repo**
2. Repo path: this repo, Branch: `main`, Dockerfile path: `Dockerfile`
3. Worker Type: **GPU** (1 × 16–24 GB), Queue
4. Disk: 10 GB, Idle Timeout: 5s, Exec Timeout: 600s, FlashBoot: ON
5. Deploy → copy Endpoint `https://api.runpod.ai/v2/<ID>/run`

## Sample payloads

**Saliency**
```json
{"input": {"task": "saliency", "image": "https://.../image.jpg"}}
