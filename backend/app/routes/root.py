from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/")
def root(db = Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM accounts"))
    account_count = result.scalar()


    return {
        "message": "Finance Intelligence API is running",
        "account_count": account_count
    }