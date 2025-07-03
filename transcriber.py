# transcriber.py
import torch
import whisper
from crypto_utils import encrypt_4digit_numbers
import tempfile
import os
import logging

# Get a logger instance
logger = logging.getLogger(__name__)

torch.set_num_threads(1)
# Load model once at the top
logger.info("Loading Whisper model (tiny)...")
model = whisper.load_model("tiny")
logger.info("Whisper model loaded.")

def transcribe_audio_bytes(audio_bytes: bytes) -> dict:
    temp_audio_path = None  # Initialize path variable
    try:
        logger.info("Starting audio transcription process...")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        logger.info(f"Temporary audio file created: {temp_audio_path}")

        logger.info(f"Calling model.transcribe() for {temp_audio_path}...")
        # Transcribe the audio using Whisper
        result = model.transcribe(
            temp_audio_path,
            task="transcribe",
            # language="hi"  # Auto-detect language
        )
        raw_text = result.get("text", "").strip()
        logger.info(f"model.transcribe() successful. Raw text length: {len(raw_text)}")

        logger.info("Sanitizing text...")
        sanitized_text = encrypt_4digit_numbers(raw_text)
        logger.info(f"Text sanitized. Sanitized text length: {len(sanitized_text)}")
        
        return {
            "transcript": raw_text,
            "sanitized": sanitized_text
        }
    except Exception as e:
        logger.error(f"Error during transcribe_audio_bytes: {e}", exc_info=True)
        # Re-raise the exception to be caught by the caller in app.py
        # This allows app.py to send a specific error message to the user.
        raise
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            logger.info(f"Deleting temporary audio file: {temp_audio_path}")
            os.remove(temp_audio_path)
            logger.info(f"Temporary audio file deleted: {temp_audio_path}")
