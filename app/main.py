from fastapi import FastAPI
from api import general, telegram

app = FastAPI()

app.include_router(general.router)
app.include_router(telegram.router)