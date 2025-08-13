from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from io import BytesIO
from PIL import Image
from rembg import remove
import base64

app = FastAPI(title="A0 Remove Image Server", version="1.0.0")

# CORS (필요 시 allow_origins를 실제 도메인으로 제한하세요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImgReq(BaseModel):
    image_base64: str  # 입력 이미지를 base64로 전달

def _png_bytes_with_alpha(input_bytes: bytes) -> bytes:
    """입력 이미지를 로드하고 배경 제거 후 투명 PNG 바이트로 반환"""
    # 원본 로드
    img = Image.open(BytesIO(input_bytes)).convert("RGBA")
    # 배경 제거
    out = remove(img)  # PIL.Image 전달 가능
    # PNG로 저장
    buf = BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue()

@app.get("/")
def index():
    return {
        "service": "A0 Remove Image",
        "health": "/health",
        "remove_json": "/remove_bg (POST, {image_base64})",
        "remove_multipart": "/remove_bg_multipart (POST, file=@image)",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/remove_bg")
def remove_bg(req: ImgReq):
    # JSON base64 입력 → 투명 PNG base64 출력
    try:
        input_bytes = base64.b64decode(req.image_base64)
        png_bytes = _png_bytes_with_alpha(input_bytes)
        return {"image_base64": base64.b64encode(png_bytes).decode("utf-8")}
    except Exception as e:
        return {"error": f"processing_failed: {e}"}

@app.post("/remove_bg_multipart")
async def remove_bg_multipart(file: UploadFile = File(...)):
    # multipart 업로드 → 투명 PNG base64 출력
    try:
        input_bytes = await file.read()
        png_bytes = _png_bytes_with_alpha(input_bytes)
        return {"image_base64": base64.b64encode(png_bytes).decode("utf-8")}
    except Exception as e:
        return {"error": f"processing_failed: {e}"}