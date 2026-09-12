from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.exceptions import AccountNotFoundError, CategoryNotFoundError, CategoryTypeMismatchError
from app.database import get_db
from app.services.transaction_service import (
    create_transaction,
    get_transactions,
    get_transaction,
    delete_transaction,
    update_transaction,
)
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate

router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction_route(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return create_transaction(db, transaction)

    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except CategoryTypeMismatchError as e:
        raise HTTPException(status_code=422, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions_route(db:Session = Depends(get_db)):

    return get_transactions(db)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction_route(transaction_id: int, db: Session = Depends(get_db)):
    transaction = get_transaction(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.delete("/transactions/{transaction_id}", response_model=TransactionResponse)
def delete_transaction_route(transaction_id: int, db: Session = Depends(get_db)):
    deleted_transaction = delete_transaction(db, transaction_id)

    if not deleted_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return deleted_transaction

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction_route(transaction_id: int, transaction_data: TransactionUpdate, db: Session = Depends(get_db)
):
    try:
        updated_transaction = update_transaction(db, transaction_id, transaction_data)

        if not updated_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return updated_transaction

    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoryTypeMismatchError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))