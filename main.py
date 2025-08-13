from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
from io import BytesIO
from PIL import Image
from rembg import remove

app = FastAPI(title="A0 Remove Image API")

# ✅ CORS (필요 시 allow_origins에 실제 도메인만 넣어 제한하세요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImgReq(BaseModel):
    image_base64: str  # 입력 이미지를 base64로 전달

def _remove_bg_from_bytes(img_bytes: bytes) -> bytes:
    # rembg로 배경 제거 → 투명 PNG로 반환
    out = remove(img_bytes)  # RGBA 포맷 bytes
    # 안전하게 PNG로 강제 인코딩
    img = Image.open(BytesIO(out)).convert("RGBA")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@app.get("/")
def index():
    return {
        "service": "A0 Remove Image",
        "health": "/health",
        "remove_json": "/remove_bg",
        "remove_multipart": "/remove_bg_multipart"
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/remove_bg")
def remove_bg(req: ImgReq):
    try:
        raw = base64.b64decode(req.image_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64: {e}")
    try:
        result = _remove_bg_from_bytes(raw)
        return {"image_base64": base64.b64encode(result).decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background removal failed: {e}")

@app.post("/remove_bg_multipart")
async def remove_bg_multipart(file: UploadFile = File(...)):
    try:
        raw = await file.read()
        result = _remove_bg_from_bytes(raw)
        return {"image_base64": base64.b64encode(result).decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background removal failed: {e}")