from fastapi import FastAPI, HTTPException
from src.create_db.structure_loading import create_structure
from src.create_db.reports_loading import load_reports
from src.config.constants import STRUCTURE_JSON_PATH
from src.config.constants import REPORTS_JSON_PATH
from src.config.constants import TAXONOMY_INF_PATH


app = FastAPI()

@app.on_event("startup")
def upload():
    try:
        create_structure(STRUCTURE_JSON_PATH,TAXONOMY_INF_PATH)
        load_reports(REPORTS_JSON_PATH)
        return {"status": "success", "message": "Data are loaded to thw database."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
