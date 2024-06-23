from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class UserCreate(BaseModel):
    username: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_summary(case_data):
    return "SUMMARY"

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}


def get_similar(case_data):
    return "SIMILAR CASES"


@app.post("/req")
async def request(case_data: UserCreate):
    print(case_data)
    print("hello")
    summary = get_summary(case_data)
    similar_case = get_similar(case_data)
    return {"summary": summary, "similar": similar_case}

# fastapi dev middle_end.py