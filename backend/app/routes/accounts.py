from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.account import AccountResponse, AccountCreate, AccountUpdate
from app.services.account_service import (
    create_account as create_account_service,
    get_account as get_account_service,
    get_accounts as get_accounts_service,
    update_account as update_account_service,
    delete_account as delete_account_service
)

router = APIRouter()

@router.get("/accounts", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return get_accounts_service(db)

@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account_service(db, account)

@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = get_account_service(db, account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account

@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, account_data: AccountUpdate, db: Session = Depends(get_db)):
    updated_account = update_account_service(db, account_id, account_data)

    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")

    return updated_account

@router.delete("/accounts/{account_id}", response_model=AccountResponse)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    deleted_account = delete_account_service(db, account_id)

    if not deleted_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return deleted_account