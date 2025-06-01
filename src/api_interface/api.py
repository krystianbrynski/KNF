from fastapi import FastAPI, HTTPException
from src.create_db.reports_loading import load_report
from src.create_db.structure_loading import create_structure

app = FastAPI()


@app.post("/load/structure")
def upload_structure():
    try:
        if create_structure():
            return "Struktura została załadaowana do bazydanych."
        else:
            return "Sprawdz logi w api, nie udało się załadowac struktury do bazydanych"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/load/reports")
def upload_reports():
    try:
        if load_report():
            return "Raport został pomyślnie rozładowany do bazydanych"
        else:
            return "Sprawdz logi w api, niestety nie udało się załadować danych do bazydanych"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
