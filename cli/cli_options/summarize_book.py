# cli/cli_options/summarize_book.py

import os
from app.model import cargar_modelo, interpret_book_ideas
from document_ingestion.summarizer_utils import get_central_chunks


def run_summary_generation() -> None:
    """
    CLI option to generate a summary of a book based on its central chunks.
    """
    print("\n📝 Generate a summary from book chunks")
    print("Esta opción utiliza los fragmentos centrales del libro para generar un resumen legible con ayuda del modelo LLM.")
    print("⚠️ Asegúrese de haber generado los chunks previamente usando la opción 2.\n")

    text_data_path: str = "text_data"
    if not os.path.exists(text_data_path):
        print("❌ La carpeta 'text_data' no existe.")
        return

    available_books: list[str] = [
        name for name in os.listdir(text_data_path)
        if os.path.isdir(os.path.join(text_data_path, name)) and
           os.path.exists(os.path.join(text_data_path, name, "chunk_0.json"))
    ]

    if not available_books:
        print("⚠️ No hay libros con chunks disponibles. Use la opción 2 primero.")
        return

    print("📖 Libros con chunks disponibles:")
    for idx, book_name in enumerate(available_books, start=1):
        print(f"{idx}. {book_name}")

    try:
        choice: int = int(input("\nSeleccione el número del libro: ").strip())
        if choice < 1 or choice > len(available_books):
            print("⚠️ Selección inválida. Intente nuevamente.")
            return
        selected_book: str = available_books[choice - 1]
        print(f"\n📚 You chose: {selected_book}")
        chunks_path: str = os.path.join(text_data_path, selected_book)

        print(f"\n🔍 Extrayendo ideas centrales del libro: {selected_book}...")
        central_chunks_path: str = get_central_chunks(chunks_path)

        if central_chunks_path == "":
            print("⚠️ No se encontraron fragmentos centrales para este libro.")
            return

        with open(central_chunks_path, "r", encoding="utf-8") as f:
            central_ideas: str = f.read()

        llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")
        prompt: str = (
            "These are central ideals of a book:\n\n"
            f"{central_ideas}\n\n"
            "Please provide a clear and concise summary of the book."
        )

        print("\n🧠 The model is thinking...")
        resumen: str = interpret_book_ideas(llm, prompt, max_tokens=400)
        print("\n📘 Resumen del libro:")
        print("--------------------------------------------------")
        print(resumen)
        print("--------------------------------------------------")

    except Exception as e:
        print(f"❌ Error durante el resumen: {e}")