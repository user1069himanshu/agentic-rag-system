# backend-python-app/backend_server.py

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from utility.prompts import generate_specific_section
from utility.gemini import call_gemini_api
import json
import uuid
from pathlib import Path
from utility.logger import logger

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


# @app.post("/generate_guidance"  )
# async def generate_guidance_endpoint(payload: GuidanceInput, request: Request):
#     if not payload.question.strip():
#         raise HTTPException(status_code=400, detail="Question is required")

#     try:
#         logger.info(f"Generating guidance for section '{payload.section}'")
#         guidance = generate_upsc_guidance_logic(payload.question, payload.wordLimit)
#         return {"guidance": guidance}
#     except Exception as e:
#         logger.error(f"An error occurred in {request.url.path}: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.post("/generate_section"  )
async def generate_section_guidance(payload: SectionInput, request: Request):
    if not payload.question.strip() or not payload.section.strip():
        raise HTTPException(status_code=400, detail="Both question and section are required")

    try:
        logger.info(f"Generating guidance for section '{payload.section}'")
        guidance = generate_specific_section(payload.question, payload.section, payload.wordLimit)
        return {"guidance": guidance}
    except Exception as e:
        logger.error(f"An error occurred in {request.url.path}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.post("/translate"  )
async def translate_text_endpoint(payload: TranslationInput, request: Request):

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
        logger.error(f"An error occurred in {request.url.path}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
    
@app.post("/submit_feedback"  )
async def submit_feedback(payload: FeedbackEntry, request: Request):
    if not payload.question.strip() or not payload.section.strip() or not payload.guidance.strip():
        raise HTTPException(status_code=400, detail="Please rate the generated guidance out of 10")
    
    try:
        logger.info(f"Generating guidance for section '{payload.section}'")
        if FEEDBACK_FILE.is_file():
            feedback_data = json.loads(FEEDBACK_FILE.read_text())
        else:
            feedback_data = []

        new_feedback = {
            'id':str(uuid.uuid4()),
            'question': payload.question,
            'guidance': payload.guidance,
            'section': payload.section,
            'rating': payload.rating,
            'comment': payload.comment,
            'status': 'unverified'
        }

        feedback_data.append(new_feedback)

        FEEDBACK_FILE.write_text(json.dumps(feedback_data, indent=2))
        logger.info(f"New feedback submitted with ID: {new_feedback['id']}")
        return {"message": "Feedback submitted sucessfully!!"}
    
    except Exception as e:
        logger.error(f"An error occurred in {request.url.path}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
    
@app.get("/pending_feedback"  )
async def get_pending_feedback(request: Request):
    try:
        if not FEEDBACK_FILE.is_file():
            return [] # Return empty list if file doesn't exist
        
        all_feedback = json.loads(FEEDBACK_FILE.read_text())
        pending = [fb for fb in all_feedback if fb.get('status') == 'unverified']
        logger.info(f"Fetched {len(pending)} pending feedback items.")
        return pending
    except:
        logger.error(f"An error occured in {request.url.path}: {Exception}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(Exception))

@app.post("/moderate_feedback"  )
async def moderate_feedback(id: str, action: str, request: Request):
    try:
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
        logger.info(f"Feedback has been updated")
        return {"message": f"Feedback {id} has been {action}d."}
    
    except Exception as e:
        logger.error(f"Error in {request.url.path}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback_stats"  )
async def get_feedback_stats(request: Request):
    try:
        if not FEEDBACK_FILE.is_file():
            return {"approved": 0, "rejected": 0}

        all_feedback = json.loads(FEEDBACK_FILE.read_text())
        approved_count = sum(1 for fb in all_feedback if fb.get('status') == 'approve')
        rejected_count = sum(1 for fb in all_feedback if fb.get('status') == 'reject')
        
        return {"approved": approved_count, "rejected": rejected_count}
    except Exception as e:
        logger.error(f"Error in {request.url.path}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# --- Run the Flask App ---
if __name__ == '__main__':
    # You can specify host='0.0.0.0' to make it accessible from other devices on your network
    # For local development, '127.0.0.1' or just no host argument (defaults to 127.0.0.1) is fine.
    app.run(debug=True, port=8000) # debug=True enables auto-reloading and better error messages

    # X-api key