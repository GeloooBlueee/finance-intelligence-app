from sqlalchemy.orm import Session

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

    return new_account

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    return account

def get_accounts(db: Session):
    accounts = db.query(Account).all()
    return accounts

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

    return account

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

    return account