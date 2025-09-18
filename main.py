import os, time
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse

app = FastAPI(title="Step3 - Upload + File Management")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Step3 Server Running - Upload + File Management"

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
