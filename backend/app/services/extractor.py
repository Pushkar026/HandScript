from pathlib import Path


def extract_text(file_path: Path, file_type: str) -> str:
    """
    Extract text from uploaded input files.
    Currently supports only digital text (.txt).

    Args:
        file_path (Path): Path to uploaded file
        file_type (str): Type of file ("text" or "handwritten")

    Returns:
        str: Extracted plain text

    Raises:
        ValueError: If file type is unsupported
    """

    if file_type == "text":
        return _extract_from_txt(file_path)

    elif file_type == "handwritten":
        # OCR will be added later
        raise NotImplementedError("OCR for handwritten images not implemented yet")

    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def _extract_from_txt(file_path: Path) -> str:
    """
    Read text content from a .txt file.
    """

    if not file_path.exists():
        raise FileNotFoundError("Uploaded text file not found")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return text.strip()
