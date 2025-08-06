from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pyttsx3
import base64
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str

@app.post("/generate-voice")
def generate_voice(request: TTSRequest):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)

        buf = BytesIO()
        engine.save_to_file(request.text, 'output.mp3')
        engine.runAndWait()

        with open('output.mp3', 'rb') as f:
            audio_data = f.read()
        encoded_audio = base64.b64encode(audio_data).decode("utf-8")
        return {"audio": encoded_audio}
    except Exception as e:
        return {"error": str(e)}
