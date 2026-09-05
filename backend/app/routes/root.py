from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Finance Intelligence API is running"}