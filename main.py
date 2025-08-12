from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64

app = FastAPI()

# ✅ CORS (필요 시 allow_origins에 실제 도메인을 넣어 제한하세요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImgReq(BaseModel):
    image_base64: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/remove_bg")
def remove_bg(req: ImgReq):
    # TODO: 여기에 실제 배경 제거 엔진 연결
    # 일단은 받은 이미지를 그대로 돌려보냅니다.
    try:
        input_bytes = base64.b64decode(req.image_base64)
    except Exception:
        return {"image_base64": req.image_base64}
    return {"image_base64": base64.b64encode(input_bytes).decode("utf-8")}
