# A0 Remove Image - FastAPI (rembg) for Render

## Files
- main.py
- requirements.txt
- runtime.txt  # MUST be named exactly like this and live in the repo root

## Render config
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

If your build log still shows Python 3.13.x, check:
1) `runtime.txt` is exactly at the **repo root** (not in a subfolder)
2) File name is exactly `runtime.txt` (no spaces, no Korean name, no extension)
3) The Render service Root Directory points to the repo root.
