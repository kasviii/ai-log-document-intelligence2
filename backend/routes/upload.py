from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.validators import validate_file
from backend.services.file_ingestion import save_uploaded_file

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        validate_file(file.filename, len(content))

        # Reset file pointer after reading
        file.file.seek(0)

        file_path = save_uploaded_file(file)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "path": file_path
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
