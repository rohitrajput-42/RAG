from fastapi import APIRouter, Body
from app.services.query import get_llm_response

router = APIRouter()

@router.post("")
def ask_question(payload: dict = Body(...)):
    question = payload.get("question", "")
    if not question:
        return {"error": "Question is required"}
    
    answer = get_llm_response(question)
    return {"response": answer}
