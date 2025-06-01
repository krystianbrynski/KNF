from fastapi import FastAPI, HTTPException
from src.create_db.reports_loading import load_report
from src.create_db.structure_loading import create_structure

app = FastAPI()


@app.post("/load/structure")
def upload_structure():
    try:
        create_structure()
        return {"status": "success", "message": "Structure loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/load/reports")
def upload_reports():
    try:
        load_report()
        return {"status": "success", "message": "Reports loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
