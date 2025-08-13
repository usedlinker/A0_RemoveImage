# A0 Remove Image - FastAPI (rembg enabled)

## Endpoints
- `GET /` → service info
- `GET /health` → `{"ok": true}`
- `POST /remove_bg` → JSON: `{"image_base64": "<b64>"}` → returns `{"image_base64": "<b64-png>"}`
- `POST /remove_bg_multipart` → multipart file field `file` → returns base64 PNG

## Local Run
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Render Deploy
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Python: 3.11 recommended
- Notes:
  - First request on free plan can be slow due to cold start.
  - Consider upgrading to avoid spin-downs.
```

**Performance tips**
- If model download latency occurs on first call, let Render finish first warmup via `/health` or an initial `/remove_bg` call.
- You can pin `onnxruntime` cpu-only build as above to avoid GPU deps.