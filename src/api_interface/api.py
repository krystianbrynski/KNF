# src/api_interface/api.py

from fastapi import FastAPI, APIRouter, HTTPException

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}
