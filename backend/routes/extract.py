from fastapi import APIRouter, HTTPException
from backend.services.text_extraction import extract_text_from_file

router = APIRouter()


@router.get("/extract")
def extract_text(file_path: str):
    try:
        text = extract_text_from_file(file_path)

        return {
            "file_path": file_path,
            "characters": len(text),
            "preview": text[:500]
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
