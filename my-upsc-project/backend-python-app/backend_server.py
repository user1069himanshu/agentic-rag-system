# backend-python-app/backend_server.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from utility.prompts import generate_upsc_guidance_logic, generate_specific_section
from utility.gemini import call_gemini_api
import json
import uuid
from pathlib import Path
import traceback


app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
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

class FeedbackEntry(BaseModel):
    question: str
    section: str
    guidance: str
    rating: int = Field(..., ge=1, le=10)
    comment: str


FEEDBACK_FILE = Path("feedback_log.json")

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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_section")
async def generate_section_guidance(payload: SectionInput):
    if not payload.question.strip() or not payload.section.strip():
        raise HTTPException(status_code=400, detail="Both question and section are required")

    try:
        guidance = generate_specific_section(payload.question, payload.section, payload.wordLimit)
        return {"guidance": guidance}
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/submit_feedback")
async def submit_feedback(payload: FeedbackEntry):
    if not payload.question.strip() or not payload.section.strip() or not payload.guidance.strip():
        raise HTTPException(status_code=400, detail="Please rate the generated guidance out of 10")
    
    try:
        if FEEDBACK_FILE.is_file():
            feedback_data = json.loads(FEEDBACK_FILE.read_text())
        else:
            feedback_data = []

        feedback_data.append({
            'id':str(uuid.uuid4()),
            'question': payload.question,
            'guidance': payload.guidance,
            'section': payload.section,
            'rating': payload.rating,
            'comment': payload.comment,
            'status': 'unverified'
        })

        FEEDBACK_FILE.write_text(json.dumps(feedback_data, indent=2))
        return {"message": "Feedback submitted sucessfully!!"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/pending_feedback")
async def get_pending_feedback():
    if not FEEDBACK_FILE.is_file():
        return [] # Return empty list if file doesn't exist
    
    all_feedback = json.loads(FEEDBACK_FILE.read_text())
    pending = [fb for fb in all_feedback if fb.get('status') == 'unverified']
    return pending
@app.post("/moderate_feedback")
async def moderate_feedback(id: str, action: str):
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'approve' or 'reject'.")

    if not FEEDBACK_FILE.is_file():
        raise HTTPException(status_code=404, detail="Feedback file not found.")

    all_feedback = json.loads(FEEDBACK_FILE.read_text())
    
    feedback_found = False
    for fb in all_feedback:
        if fb.get('id') == id:
            fb['status'] = action
            feedback_found = True
            break
            
    if not feedback_found:
        raise HTTPException(status_code=404, detail="Feedback ID not found.")

    FEEDBACK_FILE.write_text(json.dumps(all_feedback, indent=2))
    return {"message": f"Feedback {id} has been {action}d."}

@app.get("/feedback_stats")
async def get_feedback_stats():
    if not FEEDBACK_FILE.is_file():
        return {"approved": 0, "rejected": 0}

    all_feedback = json.loads(FEEDBACK_FILE.read_text())
    approved_count = sum(1 for fb in all_feedback if fb.get('status') == 'approve')
    rejected_count = sum(1 for fb in all_feedback if fb.get('status') == 'reject')
    
    return {"approved": approved_count, "rejected": rejected_count}

# --- Run the Flask App ---
if __name__ == '__main__':
    # You can specify host='0.0.0.0' to make it accessible from other devices on your network
    # For local development, '127.0.0.1' or just no host argument (defaults to 127.0.0.1) is fine.
    app.run(debug=True, port=8000) # debug=True enables auto-reloading and better error messages