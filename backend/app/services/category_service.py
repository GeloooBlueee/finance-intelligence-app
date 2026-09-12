from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate):
    new_category = Category(
        name = category.name,
        type = category.type
    )

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except:
        db.rollback()
        raise

    return new_category

def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    return category

def get_categories(db: Session):
    categories = db.query(Category).filter(Category.is_active == True).all()
    return categories

def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return None

    if category_data.name is not None:
        category.name = category_data.name

    if category_data.type is not None:
        category.type = category_data.type

    try:
        db.commit()
        db.refresh(category)
    except:
        db.rollback()
        raise
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return None

    category.is_active = False

    try:
        db.commit()
        db.refresh(category)
    except:
        db.rollback()
        raise
    return category