# FastAPI 서버 (/remove_bg 표준화 + /health + CORS)

## 파일
- main.py
- requirements.txt

## 로컬 실행
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Render 배포
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment: Python 3.11 (권장)

## 엔드포인트
- GET `/health` → {"ok": true}
- POST `/remove_bg` → {"image_base64": "..."}
  - Request: {"image_base64": "<base64-encoded image>"}
  - Response: {"image_base64": "<base64-encoded processed image>"}
