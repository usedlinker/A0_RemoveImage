# main.py - Minimal safe Bepu server
import os, io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse

app = FastAPI(title="Bepu AI (safe)")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Bepu AI (safe) - running"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Safe BG remove:
    - If REMOVE_BG_API_KEY is set in env, proxy to remove.bg (paid).
    - Otherwise returns 501 (so server build never fails).
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")
    key = os.getenv("REMOVE_BG_API_KEY", "").strip()
    if not key:
        raise HTTPException(status_code=501, detail="Background removal not configured. Set REMOVE_BG_API_KEY in Render Environment or install rembg locally.")
    import requests
    resp = requests.post("https://api.remove.bg/v1.0/removebg",
                         files={"image_file": ("upload", contents)},
                         data={"size": "auto"},
                         headers={"X-Api-Key": key}, timeout=30)
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"remove.bg failed: {resp.status_code}")
    return StreamingResponse(io.BytesIO(resp.content), media_type="image/png")
