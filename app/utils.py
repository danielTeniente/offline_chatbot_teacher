import os
import re
from document_ingestion.ocr_utils import sanitize_name
from document_ingestion.pdf_utils import get_book_name

# app/utils.py
def contar_palabras(texto: str) -> int:
    return len(texto.split())


def is_book_analyzed(book_path: str) -> bool:
    """
    Checks if a book has already been analyzed by verifying the existence
    of chunked JSON files in the corresponding text_data folder.
    """
    book_name = get_book_name(book_path)
    sanitized_name = sanitize_name(book_name)

    book_folder = os.path.join('document_ingestion', 'text_data', sanitized_name)
    if not os.path.isdir(book_folder):
        return False

    # Look for files matching chunk_{i}.json
    chunk_files = [f for f in os.listdir(book_folder) if re.match(r'chunk_\d+\.json', f)]
    return len(chunk_files) > 0
