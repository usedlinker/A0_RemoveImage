# A0 Remove Image — FastAPI + rembg (Render 배포용)

## 엔드포인트
- `GET /` : 서비스 안내
- `GET /health` : 헬스 체크 (200 / {"ok": true})
- `POST /remove_bg` : JSON body로 base64 이미지 전달 → 배경 제거 PNG(base64) 반환
  - Request: `{"image_base64": "<base64>"}`
  - Response: `{"image_base64": "<base64_png>"}`
- `POST /remove_bg_multipart` : `file=@image` 멀티파트 업로드 → 배경 제거 PNG(base64) 반환

## Render 설정
- **Build Command**
```
pip install -r requirements.txt
```
- **Start Command**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
- **Environment**
  - Python 3.11 권장
  - 무료 플랜은 유휴 시 콜드스타트로 지연될 수 있음 (유료 전환 시 해소)

## 로컬 실행
```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 테스트 (예시)
### PowerShell (JSON base64)
```
$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("test.png"))
$body = "{""image_base64"":""$b64""}"
curl.exe -X POST -H "Content-Type: application/json" -d $body http://127.0.0.1:8000/remove_bg
```

### curl (multipart)
```
curl -X POST -F "file=@test.png" http://127.0.0.1:8000/remove_bg_multipart
```