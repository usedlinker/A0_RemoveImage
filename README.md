# A0 Remove Image - FastAPI (rembg with Render fix)

## What's changed
- Pin Python version for Render: **runtime.txt → python-3.11.9**
- Use a newer `rembg` compatible with current wheels: **rembg==2.0.66**
- Keep `onnxruntime==1.17.3` (CPU) and Pillow 10.4

## Deploy on Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Make sure `runtime.txt` is at repo root so Render uses Python 3.11.9.
