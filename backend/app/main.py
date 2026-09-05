from fastapi import FastAPI
from app.routes.root import router

app = FastAPI()
app.include_router(router)