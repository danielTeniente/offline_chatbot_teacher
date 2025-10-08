# cli/cli_options/generate_chunks.py

import os
from document_ingestion.file_selector import discover_books
from document_ingestion.chunking_book import process_pdf_for_llm

def run_chunk_generation() -> None:
    """
    CLI option to generate text chunks and embeddings from a selected PDF book.
    """
    print("\n📚 Generate Chunks and Embeddings")
    print("This option scans a PDF book, extracts text (using OCR if necessary), chunks it, and generates embeddings.")
    print("These chunks are saved as JSON files in a dedicated folder.")
    print("You can later use these embeddings for searching and summarization.\n")

    books_folder: str = "books"
    if not os.path.exists(books_folder):
        print(f"❌ La carpeta '{books_folder}' no existe.")
        return

    books = discover_books(books_folder)
    if not books:
        print("⚠️ No se encontraron libros disponibles en la carpeta 'books'.")
        return

    print("📖 Libros disponibles:")
    for idx, book_name in enumerate(books.keys(), start=1):
        print(f"{idx}. {book_name}")

    try:
        choice: int = int(input("\nSeleccione el número del libro: ").strip())
        selected_book = list(books.values())[choice - 1]
        print(f"\n🔄 Procesando el libro: {selected_book["name"]}...")
        process_pdf_for_llm(selected_book["path"])
        print("✅ Embeddings generados y almacenados correctamente.")
        print(f"Los datos se encuentran en 'text_data/{selected_book['name'].replace('.pdf','')}'")
    except (ValueError, IndexError):
        print("⚠️ Selección inválida. Intente nuevamente.")
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")