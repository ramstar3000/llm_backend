from fastapi import FastAPI
from pydantic import BaseModel
import json

class UserCreate(BaseModel):
    username: str

app = FastAPI()
def get_summary(case_data):
    return "SUMMARY"

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}


def get_similar(case_data):
    return "SIMILAR CASES"


@app.post("/req/")
async def request(case_data: UserCreate):
    summary = get_summary(case_data)
    similar_case = get_similar(case_data)
    return {"summary": summary, "similar": similar_case}


# fastapi dev middle_end.py