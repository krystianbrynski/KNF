from fastapi import FastAPI, HTTPException
from src.create_db.structure_loading import structure
from src.create_db.reports_loading import reports
from src.config.constants import FILE_PATH
from src.config.constants import REPORTS_PATH

app = FastAPI()

@app.on_event("startup")
def upload():
    try:
        structure(FILE_PATH)
        reports(REPORTS_PATH)
        return {"status": "success", "message": "Data are loaded to thw database."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
