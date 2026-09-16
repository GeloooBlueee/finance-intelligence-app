from sqlalchemy.orm import Session
from sqlalchemy import case, func, select

from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate

def create_account(db: Session, account: AccountCreate):
    new_account = Account(
        name = account.name,
        type = account.type,
        initial_balance = account.initial_balance
    )

    try:
        db.add(new_account)
        db.commit()
        db.refresh(new_account)

    except:
        db.rollback()
        raise

    current_balance = get_current_balance(db, new_account.id)

    return {
        "id": new_account.id,
        "name": new_account.name,
        "type": new_account.type,
        "initial_balance": new_account.initial_balance,
        "current_balance": current_balance,
        "is_active": new_account.is_active,
        "created_at": new_account.created_at
    }

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        return None

    current_balance = get_current_balance(db, account_id)

    return {
        "id": account.id,
        "name": account.name,
        "type": account.type,
        "initial_balance": account.initial_balance,
        "current_balance": current_balance,
        "is_active": account.is_active,
        "created_at": account.created_at
    }

def get_current_balance(db: Session, account_id: int):
    transaction_effect = case(
        (
            (Transaction.account_id == account_id) & (Transaction.type == "income"),
            Transaction.amount
        ),
        (
            (Transaction.account_id == account_id) & (Transaction.type == "expense"),
            -Transaction.amount
        ),
        (
            Transaction.to_account_id == account_id,
            Transaction.amount
        ),
        (
            Transaction.from_account_id == account_id,
            -Transaction.amount
        ),
        else_=0
    )

    transaction_total = db.execute(
        select(
            func.coalesce(
                func.sum(transaction_effect),
                0
            )
        )
    ).scalar()

    account = db.query(Account).filter(Account.id == account_id).first()
    return account.initial_balance + transaction_total


def get_accounts(db: Session):
    transaction_effect = case(
        (
            (Transaction.account_id == Account.id) & (Transaction.type == "income"),
            Transaction.amount
        ),
        (
            (Transaction.account_id == Account.id) & (Transaction.type == "expense"),
            -Transaction.amount
        ),
        (
            Transaction.to_account_id == Account.id,
            Transaction.amount
        ),
        (
            Transaction.from_account_id == Account.id,
            -Transaction.amount
        ),
        else_=0
    )

    transaction_total = func.coalesce(
        func.sum(transaction_effect),
        0
    )

    accounts = (
        db.query(
            Account,
            (Account.initial_balance + transaction_total).label("current_balance")
        )
        .outerjoin(
            Transaction,
            (Transaction.account_id == Account.id)
            | (Transaction.from_account_id == Account.id)
            | (Transaction.to_account_id == Account.id)
        )
        .filter(Account.is_active == True)
        .group_by(
            Account.id,
            Account.name,
            Account.type,
            Account.initial_balance,
            Account.is_active,
            Account.created_at
        )
        .all()
    )

    return [
        {
            "id": account.id,
            "name": account.name,
            "type": account.type,
            "initial_balance": account.initial_balance,
            "current_balance": current_balance,
            "is_active": account.is_active,
            "created_at": account.created_at
        }
        for account, current_balance in accounts
    ]

def update_account(db: Session, account_id: int, account_data: AccountUpdate):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return None

    if account_data.name is not None:
        account.name = account_data.name

    if account_data.type is not None:
        account.type = account_data.type

    if account_data.initial_balance is not None:
        account.initial_balance = account_data.initial_balance

    try:
        db.commit()
        db.refresh(account)

    except:
        db.rollback()
        raise

    current_balance = get_current_balance(db, account.id)

    return {
        "id": account.id,
        "name": account.name,
        "type": account.type,
        "initial_balance": account.initial_balance,
        "current_balance": current_balance,
        "is_active": account.is_active,
        "created_at": account.created_at
    }

def delete_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        return None

    account.is_active = False

    try:
        db.commit()
        db.refresh(account)
    except:
        db.rollback()
        raise

    current_balance = get_current_balance(db, account.id)

    return {
        "id": account.id,
        "name": account.name,
        "type": account.type,
        "initial_balance": account.initial_balance,
        "current_balance": current_balance,
        "is_active": account.is_active,
        "created_at": account.created_at
    }