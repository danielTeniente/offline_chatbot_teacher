import os
import shutil
import json
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

from document_ingestion.pdf_utils import get_PDF_numPages, get_book_name, get_PDF_content
from document_ingestion.ocr_utils import sanitize_name, there_are_imgs, create_book_images, ocr_img
from document_ingestion.text_chunking import chunk_text


def extract_text_chunks_from_pdf(path: str, num_pages: int) -> List[str]:
    """Extracts and chunks text from a PDF with selectable text."""
    full_text = ''
    for page in range(num_pages):
        print(f"Procesando página {page + 1}/{num_pages}", end='\r')
        full_text += get_PDF_content(path, page) + '\n'
    return chunk_text(full_text, max_length=200)


def extract_text_chunks_from_ocr(path: str, book_name: str, num_pages: int, temp_img_folder: str) -> List[str]:
    """Extracts and chunks text from a PDF using OCR."""
    if not there_are_imgs(path):
        if not create_book_images(path, output_folder=temp_img_folder):
            raise RuntimeError('Failed to generate images for OCR.')

    all_chunks: List[str] = []

    for page_num in range(1, num_pages + 1):
        img_path = os.path.join(temp_img_folder, f"{book_name}_page_{page_num}.jpg")
        if not os.path.exists(img_path):
            continue
        text = ocr_img(img_path)
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    shutil.rmtree(temp_img_folder)
    return all_chunks


def save_chunks_with_embeddings(chunks: List[str], book_folder: str) -> None:
    """Generates embeddings and saves each chunk as a JSON file."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = model.encode(chunks, convert_to_numpy=True)
    vectors = np.asarray(vectors, dtype=np.float32)

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        data = {
            "text": chunk,
            "vector": vector.tolist()
        }
        chunk_path = os.path.join(book_folder, f"chunk_{i}.json")
        with open(chunk_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def process_pdf_for_llm(path: str, use_ocr: bool = False) -> str:
    """
    Processes a PDF for LLM ingestion.
    If use_ocr is True, uses OCR to extract text from images.
    Otherwise, extracts text directly from the PDF.
    """
    num_pages = get_PDF_numPages(path)
    book_name = get_book_name(path)
    sanitized_name = sanitize_name(book_name)

    book_folder = os.path.join('text_data', sanitized_name)
    os.makedirs(book_folder, exist_ok=True)

    # Check if chunks already exist
    if any(fname.endswith('.json') for fname in os.listdir(book_folder)):
        return f"Chunks already exist for '{book_name}' in '{book_folder}'."

    # Extract chunks
    if use_ocr:
        temp_img_folder = os.path.join(book_folder, 'temp_imgs')
        os.makedirs(temp_img_folder, exist_ok=True)
        chunks = extract_text_chunks_from_ocr(path, book_name, num_pages, temp_img_folder)
    else:
        chunks = extract_text_chunks_from_pdf(path, num_pages)

    # Save chunks and embeddings
    save_chunks_with_embeddings(chunks, book_folder)

    return f"Processed {len(chunks)} chunks from '{book_name}' and saved to '{book_folder}'."