from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Hello Server")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Server is running"

@app.get("/health")
def health():
    return {"status": "ok"}

