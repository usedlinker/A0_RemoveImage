# main.py - Step 3: Upload + Manage + Simple Process (grayscale/resize)
import os, time, io
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import PlainTextResponse, FileResponse, StreamingResponse
from PIL import Image

app = FastAPI(title="Step3 - Upload + Manage + Process")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Step3 Server Running - Upload + Manage + Process"

def _safe_name(name: str) -> str:
    return os.path.basename(name).replace("..", "_")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ts = int(time.time() * 1000)
    safe_name = _safe_name(file.filename)
    save_name = f"{ts}_{safe_name}"
    save_path = os.path.join(UPLOAD_DIR, save_name)
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")
    with open(save_path, "wb") as f:
        f.write(contents)
    return {"message": "Upload successful", "filename": save_name, "path": save_path, "size": len(contents)}

@app.get("/files", response_model=List[str])
def list_files():
    return sorted([f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))])

@app.get("/files/{name}")
def download_file(name: str):
    safe = _safe_name(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/octet-stream", filename=safe)

@app.delete("/files/{name}")
def delete_file(name: str):
    safe = _safe_name(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(path)
    return {"message": "Deleted", "filename": safe}

# ------- 새로 추가: 간단 처리 엔드포인트 --------
@app.get("/process/{name}")
def process_image(
    name: str,
    op: str = Query(..., description="grayscale 또는 resize"),
    w: Optional[int] = Query(None, description="resize일 때 너비"),
    h: Optional[int] = Query(None, description="resize일 때 높이"),
    download: bool = Query(False, description="처리 결과를 파일로 저장 후 다운로드할지 여부"),
):
    """
    예)
    - 흑백:   GET /process/<filename>?op=grayscale
    - 리사이즈: GET /process/<filename>?op=resize&w=512&h=512
    """
    safe = _safe_name(name)
    src_path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(src_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with Image.open(src_path) as img:
            if op == "grayscale":
                out_img = img.convert("L")  # 흑백
            elif op == "resize":
                if not (w and h) or w <= 0 or h <= 0:
                    raise HTTPException(status_code=400, detail="resize에는 양수 w,h가 필요")
                out_img = img.convert("RGB").resize((w, h))
            else:
                raise HTTPException(status_code=400, detail="op는 grayscale 또는 resize")

            if download:
                # 파일로 저장 후 다운로드
                base, ext = os.path.splitext(safe)
                out_name = f"processed_{op}_{base}.png"
                out_path = os.path.join(UPLOAD_DIR, out_name)
                out_img.save(out_path, format="PNG")
                return FileResponse(out_path, media_type="image/png", filename=out_name)

            # 메모리로 바로 반환(미저장)
            buf = io.BytesIO()
            out_img.save(buf, format="PNG")
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"processing failed: {e}")
