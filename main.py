# main.py - Step 2: Upload + List/Download/Delete
import os, time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from typing import List

app = FastAPI(title="Step2 - Upload + Manage")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Step2 Server Running - Upload + Manage"

def _safe_name(name: str) -> str:
    # 간단 sanitizing (디렉토리 traversal 방지)
    return os.path.basename(name).replace("..", "_")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # 파일명 유니크 처리 (타임스탬프 접두사)
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
    files = sorted([f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))])
    return files

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
