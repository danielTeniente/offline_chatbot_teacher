import os
import glob
from typing import List
from pypdf import PdfReader


def get_dirs(path: str = '.') -> List[str]:
    """Get list of directories in the given path."""
    all_files = os.listdir(path)
    return [name for name in all_files if os.path.isdir(os.path.join(path, name))]


def get_PDFs(path: str = '.') -> List[str]:
    """Get list of PDF files in the given path."""
    ls_pdfs = glob.glob(os.path.join(path, "*.pdf"))
    return [pdf.replace('\\', '/') for pdf in ls_pdfs]


def get_PDF_numPages(path: str = './test.pdf') -> int:
    """Get number of pages in a PDF file."""
    reader = PdfReader(path)
    return len(reader.pages)


def get_book_name(book_path: str) -> str:
    """Extract book name from its path."""
    book_name = os.path.basename(book_path)
    return book_name.replace('.pdf', '')


def get_PDF_content(path: str = './test.pdf', page: int = 0) -> str:
    """Extract text content from a specific page of a PDF file."""
    reader = PdfReader(path)
    if 0 <= page < len(reader.pages):
        content = reader.pages[page].extract_text()
        if content:
            return content.strip().replace('\n\n', '\n')
    return ''


def has_selectable_text(path: str) -> bool:
    """Check if a PDF has selectable text."""
    try:
        text = get_PDF_content(path, 0)
        return bool(text and text.strip())
    except Exception:
        return False


def write_text(content: str = '', path: str = '.', name: str = 'book_references.txt') -> bool:
    """Write content to a text file."""
    file_path = os.path.join(path, name)
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
            f.write('\n\n\n')
        return True
    except Exception as e:
        print(e)
        return False


def get_paragraph(phrase: str = '', text: str = '') -> str:
    """Extract paragraphs containing a specific phrase from text."""
    paragraph = ''
    phrase_lower = phrase.lower()
    text_lower = text.lower()
    resultados = text_lower.split(phrase_lower)
    num_resultados = len(resultados)
    if num_resultados > 1:
        for i in range(num_resultados):
            add_char = 100
            if i != 0:
                paragraph += phrase.upper()
                paragraph += resultados[i][:add_char]
                add_char = len(resultados[i]) - add_char
                if add_char < 1:
                    add_char = 0
            if i != num_resultados - 1:
                paragraph += resultados[i][-add_char:]
    return paragraph


def scan_book(path: str, phrase: str) -> str:
    """Scan a PDF book for a specific phrase and return context information."""
    num_pages = get_PDF_numPages(path)
    info = ''
    for page in range(num_pages):
        current_page = page + 1
        print(f"Procesando página {current_page}/{num_pages}", end='\r')
        book_content = get_PDF_content(path, page)
        match = get_paragraph(phrase, text=book_content)
        if match:
            info += f'Página {current_page}\n...{match}...\n\n'
    return info