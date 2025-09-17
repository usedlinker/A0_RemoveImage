# A0 Remove Image - FastAPI (rembg)

## Endpoints
- `GET /` → 서비스 정보
- `GET /health` → {"ok": true}
- `POST /remove_bg` → JSON {"image_base64": "..."} → {"image_base64": "<b64-png>"}
- `POST /remove_bg_multipart` → multipart file upload

## Local Run
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
