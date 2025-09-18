# main.py - Step 1: Image Upload Only
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Step1 - Upload Only")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Step1 Server Running - Upload Only"

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # 저장 경로 지정
    save_path = os.path.join(UPLOAD_DIR, file.filename)

    # 파일 저장
    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {"message": "Upload successful", "filename": file.filename, "path": save_path}
