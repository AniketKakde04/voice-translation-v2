import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def send_to_gemini(text: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash") # Updated model name

    prompt = [
        "You are an AI assistant. The following text is a transcription of a voice message. Please translate it to English and provide a helpful, concise response based on the content. Ignore or redact any encrypted content like [ENCRYPTED:...]. If the input is already in English, just provide a helpful response.",
        text
    ]

    response = model.generate_content(prompt)
    return response.text.strip()
