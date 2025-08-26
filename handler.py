import base64, io, os, json, subprocess, tempfile, uuid, requests
from PIL import Image
import numpy as np
import cv2
import pytesseract
from pymediainfo import MediaInfo
import runpod

# ---------- helpers ----------
def _read_image(input_obj):
    """Accepts base64 string or URL -> returns RGB np.array"""
    if isinstance(input_obj, str) and input_obj.startswith("http"):
        b = requests.get(input_obj, timeout=30).content
    elif isinstance(input_obj, str):
        b = base64.b64decode(input_obj)
    else:
        raise ValueError("image must be base64 string or URL")
    img = Image.open(io.BytesIO(b)).convert("RGB")
    return np.array(img)

def task_saliency(image):
    img = _read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    spectrum = np.fft.fft2(gray)
    log_ampl = np.log(np.abs(spectrum) + 1e-8)
    avg = cv2.GaussianBlur(log_ampl, (7,7), 0)
    spectral_residual = log_ampl - avg
    saliency = np.abs(np.fft.ifft2(np.exp(spectral_residual + 1j*np.angle(spectrum))))
    saliency = (saliency - saliency.min()) / (saliency.max() - saliency.min() + 1e-8)
    saliency_u8 = (saliency * 255).astype(np.uint8)
    # return heatmap as base64 PNG
    pil = Image.fromarray(saliency_u8)
    buf = io.BytesIO(); pil.save(buf, format="PNG")
    return {"saliency_map_b64": base64.b64encode(buf.getvalue()).decode()}

def task_ocr(image):
    img = _read_image(image)
    pil = Image.fromarray(img)
    text = pytesseract.image_to_string(pil)
    return {"text": text}

def _save_temp(data_bytes, suffix):
    p = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}{suffix}")
    with open(p, "wb") as f: f.write(data_bytes)
    return p

def task_extract_frames(video, every_n=30, max_frames=50):
    """video: URL or base64; returns JPEG frames as b64 list"""
    if video.startswith("http"):
        data = requests.get(video, timeout=60).content
    else:
        data = base64.b64decode(video)
    inpath = _save_temp(data, ".mp4")
    # extract as sequence of JPEGs
    outdir = tempfile.mkdtemp()
    # Use ffmpeg to extract every_n-th frame
    cmd = ["ffmpeg","-i", inpath, "-vf", f"select='not(mod(n\\,{int(every_n)}))'",
           "-vsync","vfr", os.path.join(outdir, "frame-%05d.jpg")]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    frames = []
    for name in sorted(os.listdir(outdir))[:max_frames]:
        with open(os.path.join(outdir, name), "rb") as f:
            frames.append(base64.b64encode(f.read()).decode())
    return {"frames_b64": frames}

def task_parse_metadata(media):
    """Return container/stream metadata using MediaInfo"""
    if media.startswith("http"):
        data = requests.get(media, timeout=60).content
    else:
        data = base64.b64decode(media)
    path = _save_temp(data, ".bin")
    info = MediaInfo.parse(path)
    return {"metadata": json.loads(info.to_json())}

# ---------- handler ----------
def handler(event):
    inp = event.get("input", {})
    task = inp.get("task")
    try:
        if task == "saliency":
            return task_saliency(inp["image"])
        elif task == "ocr":
            return task_ocr(inp["image"])
        elif task == "extract_frames":
            return task_extract_frames(inp["video"], inp.get("every_n", 30), inp.get("max_frames", 50))
        elif task == "parse_metadata":
            return task_parse_metadata(inp["media"])
        else:
            return {"error": "unknown task", "accepted": ["saliency","ocr","extract_frames","parse_metadata"]}
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})
