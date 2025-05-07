from fastapi import APIRouter
from app.db.mongo import get_database

router = APIRouter()

@router.get("/health")
async def health_check():
    db = get_database()
    try:
        await db.command("ping")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
