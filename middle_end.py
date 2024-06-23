from fastapi import FastAPI
import json

app = FastAPI()
def get_summary(case_data):
    return "SUMMARY"

@app.get("/test")
async def test_route():
    return {"message": "Hey the server seems to be working!"}


def get_similar(case_data):
    return "SIMILAR CASES"


@app.get("/req")
async def request(case_data):
    summary = get_summary(case_data)
    similar_case = get_similar(case_data)
    return {"summary": summary, "similar": similar_case}


# fastapi dev middle_end.py