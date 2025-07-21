import os
import json
from fastapi import APIRouter, File, UploadFile, HTTPException
from groq import Groq
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/speechtotext",
    tags=["speechtotext"],
)

# Initialize the Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@router.post("/transcribe-audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        suffix = os.path.splitext(file.filename)[-1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Open and transcribe the audio file
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                prompt="Specify context or spelling",
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language="en",
                temperature=0.0
            )

        return transcription  # returns full transcription with timestamps

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
