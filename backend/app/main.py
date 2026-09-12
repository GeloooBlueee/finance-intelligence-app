from fastapi import FastAPI
from app.routes.root import router
from app.routes.accounts import router as accounts_router
from app.routes.categories import router as categories_router
from app.routes.transaction import router as transactions_router

app = FastAPI()

app.include_router(router)
app.include_router(accounts_router)
app.include_router(categories_router)
app.include_router(transactions_router)