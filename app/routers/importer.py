from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile, shutil
from pathlib import Path
from app.services.import_wrapper import ImportWrapper

router = APIRouter()
importer = ImportWrapper()

@router.post("/")
async def import_file(file: UploadFile = File(...)):
    """
    Upload a file (.apkg, .txt, .csv) and import it into the collection.
    """
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = Path(tmp.name)

        result = importer.run_import(temp_path)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"] or "Import failed")

        return {"message": "Import completed", "details": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
