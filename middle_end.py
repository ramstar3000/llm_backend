from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}

# fastapi dev middle_end.py
