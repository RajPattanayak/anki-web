from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import tempfile, shutil
from pathlib import Path
from app.services.import_wrapper import ImportWrapper

router = APIRouter()
importer = ImportWrapper()


@router.post("/", summary="Upload and import a file (.apkg, .csv, .txt)")
async def import_file(file: UploadFile = File(...)):
    temp_path = None
    try:
        suffix = Path(file.filename).suffix if file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = Path(tmp.name)

        result = importer.run_import(temp_path)
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "Import failed"))
        return {"message": "Import completed", "details": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if temp_path and temp_path.exists():
            try:
                os.remove(temp_path)
            except Exception:
                pass