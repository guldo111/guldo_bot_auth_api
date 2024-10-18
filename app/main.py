from fastapi import FastAPI
from app.api import general, telegram

app = FastAPI()

app.include_router(general.router)
app.include_router(telegram.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}