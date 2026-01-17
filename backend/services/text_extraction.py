from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# points to ai-log-document-intelligence/


def extract_text_from_file(file_path: str) -> str:
    full_path = BASE_DIR / file_path
    extension = full_path.suffix.lower()

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {full_path}")

    if extension in [".txt", ".log"]:
        return _extract_from_text_file(full_path)

    if extension == ".pdf":
        return _extract_from_pdf(full_path)

    raise ValueError("Unsupported file type for extraction")


def _extract_from_text_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_from_pdf(path: Path) -> str:
    reader = PdfReader(path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)
