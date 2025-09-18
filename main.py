import os, time, io
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import PlainTextResponse, FileResponse, StreamingResponse
from PIL import Image

app = FastAPI(title="Step4 - Upload + Manage + Process")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Step4 Server Running - Upload + Manage + Process"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ts = int(time.time() * 1000)
    save_name = f"{ts}_{os.path.basename(file.filename)}"
    save_path = os.path.join(UPLOAD_DIR, save_name)
    with open(save_path, "wb") as f:
        f.write(await file.read())
    return {"message": "Upload successful", "filename": save_name}

@app.get("/files", response_model=List[str])
def list_files():
    return sorted([
        f for f in os.listdir(UPLOAD_DIR)
        if os.path.isfile(os.path.join(UPLOAD_DIR, f))
    ])

@app.get("/files/{name}")
def download_file(name: str):
    safe = os.path.basename(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/octet-stream", filename=safe)

@app.delete("/files/{name}")
def delete_file(name: str):
    safe = os.path.basename(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(path)
    return {"message": "Deleted", "filename": safe}

# ------- 새로 추가: 이미지 처리 --------
@app.get("/process/{name}")
def process_image(
    name: str,
    op: str = Query(..., description="grayscale 또는 resize"),
    w: Optional[int] = Query(None, description="resize일 때 너비"),
    h: Optional[int] = Query(None, description="resize일 때 높이"),
):
    safe = os.path.basename(name)
    src_path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(src_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with Image.open(src_path) as img:
            if op == "grayscale":
                out_img = img.convert("L")
            elif op == "resize":
                if not (w and h):
                    raise HTTPException(status_code=400, detail="resize에는 w,h 둘 다 필요")
                out_img = img.resize((w, h))
            else:
                raise HTTPException(status_code=400, detail="op는 grayscale 또는 resize")

            buf = io.BytesIO()
            out_img.save(buf, format="PNG")
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

