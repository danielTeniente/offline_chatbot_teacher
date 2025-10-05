from pathlib import Path
from common.types import BookMetadata
from . import pdf_utils

def discover_books(folder_path: str) -> dict[str, BookMetadata]:
    """Recursively finds PDFs and returns metadata."""
    folder = Path(folder_path)
    pdf_paths = list(folder.rglob("*.pdf"))
    books = {}
    for path in pdf_paths:
        name = path.name
        has_text = pdf_utils.has_selectable_text(str(path))
        books[name] = {
            "name": name,
            "path": str(path),
            "has_selectable_text": has_text
        }
    return books
