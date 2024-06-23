from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}

@app.get("/")
async def test_root():
    return {"hello": "world"}

# fastapi dev middle_end.py
