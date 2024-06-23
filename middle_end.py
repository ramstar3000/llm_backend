from fastapi import FastAPI
import json

app = FastAPI()
def get_response(case_data):
    pass

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}

@app.get("/req")
async def request(case_data):
    response = get_response(case_data)
    return {"response": response}


# fastapi dev middle_end.py