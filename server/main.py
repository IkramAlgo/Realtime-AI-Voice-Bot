from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from stt_processor import speech_to_text
from llm_processor import process_query
from tts_processor import text_to_speech
import logging
import io

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://127.0.0.1:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process_audio(audio: UploadFile = File(...)):
    try:
        logger.info("Received audio file: %s", audio.filename)
        # Validate audio file
        if audio.content_type not in ["audio/wav", "audio/webm"]:
            raise HTTPException(400, "Invalid audio format. Use WAV/WEBM.")
        audio_bytes = await audio.read()
        if len(audio_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(413, "Audio file too large (max 10MB)")
        # Process audio
        text = speech_to_text(io.BytesIO(audio_bytes))
        logger.info("STT Output: %s", text[:50] + "...")
        response_text = process_query(text)
        logger.info("LLM Response: %s", response_text[:50] + "...")
        output_audio = text_to_speech(response_text)
        return {
            "audio": output_audio,
            "text": response_text
        }
    except Exception as e:
        logger.error("Processing Error: %s", str(e), exc_info=True)
        raise HTTPException(500, "Internal server error")