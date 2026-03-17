from fastapi import APIRouter, HTTPException
from backend.services.text_extraction import extract_text_from_file
from backend.services.chunking import chunk_text

router = APIRouter()


@router.get("/chunk")
def chunk_document(file_path: str):
    try:
        text = extract_text_from_file(file_path)

        # Detect file type from extension
        extension = file_path.rsplit(".", 1)[-1].lower()
        file_type = extension if extension in ["pdf", "txt", "log"] else "default"

        chunks = chunk_text(text, file_type=file_type)

        return {
            "file_path": file_path,
            "file_type": file_type,
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0][:300] if chunks else ""
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))