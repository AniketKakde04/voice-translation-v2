import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from twilio_utils import download_audio_file
from transcriber import transcribe_audio_bytes
from gemini_utils import send_to_gemini

load_dotenv()
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    num_media = int(request.form.get("NumMedia", 0))
    resp = MessagingResponse()

    if num_media == 0:
        resp.message("Please send a voice message in any Indian language.")
        return str(resp)

    media_url = request.form.get("MediaUrl0")
    media_content_type = request.form.get("MediaContentType0", "")

    if not any(fmt in media_content_type for fmt in ["audio", "mp3", "wav", "ogg"]):
        resp.message("Unsupported audio format. Please send MP3, WAV or OGG voice note.")
        return str(resp)

    try:
        audio_data = download_audio_file(media_url)

        # STEP 1: Transcribe using Whisper + encrypt sensitive data
        result = transcribe_audio_bytes(audio_data)
        transcript = result["transcript"]
        sanitized = result["sanitized"]

        # STEP 2: Send sanitized text to Gemini
        gemini_reply = send_to_gemini(sanitized)

        # STEP 3: Send reply to user
        resp.message(f"🧾 Gemini Response:\n\n{gemini_reply}")

    except Exception as e:
        print("Error:", e)
        resp.message("Sorry, could not process your voice note. Try again.")

    return str(resp)
