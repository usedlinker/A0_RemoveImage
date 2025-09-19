import os, time
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse

app = FastAPI(title="Upload + File Management")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Server Running - Upload + File Management"

@app.get("/health")
def health():
    return {"status": "ok"}

def _safe(name: str) -> str:
    # 경로 탈출 방지
    return os.path.basename(name).replace("..", "_")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ts = int(time.time() * 1000)
    save_name = f"{ts}_{_safe(file.filename)}"
    path = os.path.join(UPLOAD_DIR, save_name)
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")
    with open(path, "wb") as f:
        f.write(data)
    return {"message": "Upload successful", "filename": save_name}

@app.get("/files", response_model=List[str])
def list_files():
    return sorted(
        f for f in os.listdir(UPLOAD_DIR)
        if os.path.isfile(os.path.join(UPLOAD_DIR, f))
    )

@app.get("/files/{name}")
def download_file(name: str):
    safe = _safe(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/octet-stream", filename=safe)

@app.delete("/files/{name}")
def delete_file(name: str):
    safe = _safe(name)
    path = os.path.join(UPLOAD_DIR, safe)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(path)
    return {"message": "Deleted", "filename": safe}
