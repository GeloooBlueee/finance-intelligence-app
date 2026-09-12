from sqlalchemy.orm import Session

from app.exceptions import AccountNotFoundError, CategoryNotFoundError, CategoryTypeMismatchError
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if account is None:
        raise AccountNotFoundError("Account not found")

    return account

def get_valid_category(db: Session, category_id: int, transaction_type: str):
    category = db.query(Category).filter(Category.id == category_id, Category.is_active == True).first()

    if category is None:
        raise CategoryNotFoundError("Category not found")

    if category.type != transaction_type:
        raise CategoryTypeMismatchError("Category type does not match transaction type")

    return category

def validate_transaction(db: Session, transaction_type: str, category_id: int | None, account_id: int | None, from_account_id: int | None, to_account_id: int | None):
    if transaction_type in ("expense", "income"):
        if from_account_id is not None or to_account_id is not None:
            raise ValueError(f"{transaction_type.capitalize()} cannot have transfer accounts")

        if account_id is None:
            raise ValueError(f"{transaction_type.capitalize()} requires account_id")

        if category_id is None:
            raise ValueError(f"{transaction_type.capitalize()} requires category_id")

        get_account(db, account_id)
        get_valid_category(db, category_id, transaction_type)

    elif transaction_type == "transfer":
        if category_id is None:
            raise ValueError("Transfer requires category_id")

        if account_id is not None:
            raise ValueError("Transfer cannot have account_id")

        if from_account_id is None:
            raise ValueError("Transfer requires from_account_id")

        if to_account_id is None:
            raise ValueError("Transfer requires to_account_id")

        if from_account_id == to_account_id:
            raise ValueError("Transfer source and destination accounts must be different")

        get_valid_category(db, category_id, transaction_type)
        get_account(db, from_account_id)
        get_account(db, to_account_id)


def create_transaction(db: Session, transaction: TransactionCreate):
    validate_transaction(db, transaction.type, transaction.category_id, transaction.account_id, transaction.from_account_id, transaction.to_account_id)

    new_transaction = Transaction(
        date=transaction.date,
        type=transaction.type,
        amount=transaction.amount,
        description=transaction.description,
        category_id=transaction.category_id,
        account_id=transaction.account_id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except Exception:
        db.rollback()
        raise

    return new_transaction

def get_transactions(db: Session):
    transactions = db.query(Transaction).all()

    return transactions

def update_transaction(db: Session, transaction_id: int, transaction_data: TransactionUpdate):
    transaction = get_transaction(db, transaction_id)

    if not transaction:
        return None

    updates = transaction_data.model_dump(exclude_unset=True)

    new_type = updates.get("type", transaction.type)
    new_category_id = updates.get("category_id", transaction.category_id)
    new_account_id = updates.get("account_id", transaction.account_id)
    new_from_account_id = updates.get("from_account_id", transaction.from_account_id)
    new_to_account_id = updates.get("to_account_id", transaction.to_account_id)

    try:
        validate_transaction(db, new_type, new_category_id, new_account_id, new_from_account_id, new_to_account_id)

        for field, value in updates.items():
            setattr(transaction, field, value)

        db.commit()
        db.refresh(transaction)

    except Exception:
        db.rollback()
        raise

    return transaction

def get_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    return transaction
def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        return None

    db.delete(transaction)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return transaction