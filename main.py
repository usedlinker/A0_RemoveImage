# main.py - Safe minimal Bepu AI server
import os, io, time, requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel
from gtts import gTTS

APP_VERSION = os.getenv("BF_APP_VERSION", "A1-3-safe-package")
app = FastAPI(title="Bepu AI (safe)", version=APP_VERSION)

# CORS - allow all origins by default (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    user_id: str = "guest"
    message: str

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Bepu AI (safe) - running. See /docs for API."

@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}

@app.post("/chat")
def chat(inp: ChatIn):
    # This endpoint demonstrates reading OPENAI_API_KEY but will fall back to a simple reply if not set.
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        # No OpenAI key configured - return a safe fallback reply
        return {"reply": f"(fallback) I understood: {inp.message}", "mode": "fallback"}
    # If you set OPENAI_API_KEY in env, you can wire OpenAI calls here.
    return {"reply": f"(placeholder) OpenAI configured but this template does not call it directly.", "mode": "stub"}

@app.post("/tts")
async def tts(file: UploadFile = File(...)):
    # Use gTTS to synthesize incoming small text files (or a text field). This is a tiny example.
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")[:5000]
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text required in uploaded file (utf-8).")
    buf = io.BytesIO()
    try:
        gTTS(text=text, lang="ko").write_to_fp(buf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")
    buf.seek(0)
    return StreamingResponse(buf, media_type="audio/mpeg", headers={"Content-Disposition": 'inline; filename="voice.mp3"'})

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Safe background-removal endpoint *without* rembg binary dependency.
    Two options:
     - If you set REMOVE_BG_API_KEY env var, this will proxy to remove.bg REST API (paid service).
     - Otherwise, returns 501 with instructions (so the server won't fail during build).
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    removebg_key = os.getenv("REMOVE_BG_API_KEY", "").strip()
    if removebg_key:
        # Proxy to remove.bg API
        try:
            resp = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": ("upload", contents)},
                data={"size": "auto"},
                headers={"X-Api-Key": removebg_key},
                timeout=30
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=502, detail=f"remove.bg failed: {resp.status_code} {resp.text[:200]}")
            return StreamingResponse(io.BytesIO(resp.content), media_type="image/png", headers={"Content-Disposition": 'inline; filename="no-bg.png"'})
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"remove.bg request failed: {e}")
    # No remove.bg key and no rembg dependency - return clear instruction so build does not break.
    raise HTTPException(status_code=501, detail="Background removal not configured. Provide REMOVE_BG_API_KEY (remove.bg) in environment or install rembg locally and add it to requirements for worker builds.")