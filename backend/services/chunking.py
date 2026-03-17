from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
    file_type: str = "default"
) -> List[str]:
    """
    Smart chunking based on file type:
    - logs: line-based chunking
    - pdf/txt: paragraph-based chunking
    - default: character-based chunking with overlap
    """
    if file_type == "log":
        return _chunk_by_lines(text)
    elif file_type in ["pdf", "txt"]:
        return _chunk_by_paragraphs(text, chunk_size, overlap)
    else:
        return _chunk_by_characters(text, chunk_size, overlap)


def _chunk_by_lines(text: str, lines_per_chunk: int = 20) -> List[str]:
    """For log files — group lines into chunks."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    chunks = []
    for i in range(0, len(lines), lines_per_chunk):
        chunk = "\n".join(lines[i:i + lines_per_chunk])
        chunks.append(chunk)
    return chunks


def _chunk_by_paragraphs(text: str, chunk_size: int, overlap: int) -> List[str]:
    """For PDFs/TXT — split by paragraphs, merge small ones."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) <= chunk_size:
            current += "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current)
            # If single paragraph exceeds chunk_size, split it further
            if len(para) > chunk_size:
                sub_chunks = _chunk_by_characters(para, chunk_size, overlap)
                chunks.extend(sub_chunks[:-1])
                current = sub_chunks[-1] if sub_chunks else ""
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def _chunk_by_characters(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Fallback: fixed-size character chunks with overlap."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0

    return chunks