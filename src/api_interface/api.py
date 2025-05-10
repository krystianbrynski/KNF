from fastapi import FastAPI, HTTPException
from src.create_db.connection import connect
from src.config.paths import FILE_PATH

app = FastAPI()

@app.post("/upload")
def upload():
    try:
        connect(FILE_PATH)
        return {"status": "success", "message": "Dane załadowane do bazy."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
