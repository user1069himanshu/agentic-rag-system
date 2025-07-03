# backend-python-app/backend_server.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utility.prompts import generate_upsc_guidance_logic, generate_specific_section
from utility.gemini import call_gemini_api

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideally restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class GuidanceInput(BaseModel):
    question: str
    wordLimit: int = 150

class SectionInput(BaseModel):
    question: str
    section: str
    wordLimit: int = 150

class TranslationInput(BaseModel):
    text: str
    language: str


# Routes

@app.get("/")
async def home():
    return {"message": "Ajayvision PoC Backend (FastAPI) is running!"}


@app.post("/generate_guidance")
async def generate_guidance_endpoint(payload: GuidanceInput):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        guidance = generate_upsc_guidance_logic(payload.question, payload.wordLimit)
        return {"guidance": guidance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_section")
async def generate_section_guidance(payload: SectionInput):
    if not payload.question.strip() or not payload.section.strip():
        raise HTTPException(status_code=400, detail="Both question and section are required")

    try:
        guidance = generate_specific_section(payload.question, payload.section, payload.wordLimit)
        return {"guidance": guidance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/translate")
async def translate_text_endpoint(payload: TranslationInput):
    if not payload.text.strip() or not payload.language.strip():
        raise HTTPException(status_code=400, detail="Text and target language are required")

    try:
        prompt = (
            f"Translate the following text into {payload.language}. "
            f"Maintain the original markdown formatting (like '###', '**', and bullet points):\n\n{payload.text}"
        )
        messages = [{"role": "user", "parts": [{"text": prompt}]}]
        translated_text = call_gemini_api(messages)
        return {"translatedText": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# --- Run the Flask App ---
if __name__ == '__main__':
    # You can specify host='0.0.0.0' to make it accessible from other devices on your network
    # For local development, '127.0.0.1' or just no host argument (defaults to 127.0.0.1) is fine.
    app.run(debug=True, port=5000) # debug=True enables auto-reloading and better error messages