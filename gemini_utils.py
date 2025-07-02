import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def send_to_gemini(text: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = [
        "You are an AI assistant.Translate, Transcibe and Respond helpfully to the following user message. Ignore or redact any encrypted content like [ENCRYPTED:...]",
        text
    ]

    response = model.generate_content(prompt)
    return response.text.strip()
