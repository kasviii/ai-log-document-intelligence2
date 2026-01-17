ALLOWED_EXTENSIONS = {".txt", ".log", ".pdf"}
MAX_FILE_SIZE_MB = 5


def validate_file(filename: str, file_size: int):
    extension = "." + filename.split(".")[-1]

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError("File size exceeds limit")
