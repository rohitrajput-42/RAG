from fastapi import APIRouter, UploadFile, File
from app.services.upload_document import save_document

router = APIRouter()

@router.post("")
async def upload_document_api(file: UploadFile = File(...)):
    result = await save_document(file)
    return result