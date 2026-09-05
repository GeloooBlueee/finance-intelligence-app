from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Finance Intelligence API is running"}