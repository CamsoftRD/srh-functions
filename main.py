from fastapi import FastAPI
from client  import main as m
import asyncio

app = FastAPI()

@app.get("/")
def read_root():
    asyncio.run(m())
    return {"message": "Hello World!"}