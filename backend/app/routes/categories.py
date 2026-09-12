from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from app.services.category_service import (
    create_category as create_category_service,
    get_category as get_category_service,
    get_categories as get_categories_service,
    update_category as update_category_service,
    delete_category as delete_category_service
)

router = APIRouter()

@router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return get_categories_service(db)

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_service(db, category)

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category_service(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = update_category_service(db, category_id, category_data)

    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = delete_category_service(db, category_id)

    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category