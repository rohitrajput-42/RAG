from fastapi import APIRouter, HTTPException
from typing import List
from app.services.list_document import fetch_all_documents

router = APIRouter()

@router.get("", tags=["Documents"])
def get_all_documents():
    documents = fetch_all_documents()
    return {"documents": documents}