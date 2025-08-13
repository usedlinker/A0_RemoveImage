# A0 Remove Image — FastAPI + rembg (Render 배포용, v2)

## 변경점
- `runtime.txt` 추가 (Python 3.11.9 고정)
- `render.yaml` 추가 (빌드/시작 커맨드 고정)
- `requirements.txt`에 `numpy<2.0.0` 고정 (호환성 이슈 예방)

## 배포 순서
1) GitHub 저장소 루트에 아래 파일 업로드/커밋
   - `main.py`
   - `requirements.txt`
   - `runtime.txt`
   - `render.yaml`
2) Render 대시보드 → 새 Web Service (또는 연결된 서비스 자동 배포)
   - 빌드 로그에서 `pip install -r requirements.txt` 완료 확인
3) 배포 완료 후
   - `GET /health` → `{"ok": true}` 확인
   - `POST /remove_bg` 테스트

## 로컬 실행
```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```