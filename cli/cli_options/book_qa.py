import os
from app.model import cargar_modelo, answer_question_about_book

def run_book_question_answering() -> None:
    """
    CLI option to ask questions based on a processed book's chunks.
    """
    print("\n📖 Preguntar sobre un libro procesado")
    print("Esta opción permite hacer preguntas sobre libros previamente procesados usando el modelo LLM.")
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
        print("⚠️ No hay libros disponibles. Genere los chunks primero.")
        return

    print("📚 Libros disponibles:")
    for idx, book in enumerate(available_books, start=1):
        print(f"{idx}. {book}")

    selected_index: str = input("\nSeleccione el número del libro: ").strip()
    if not selected_index.isdigit() or int(selected_index) not in range(1, len(available_books) + 1):
        print("⚠️ Selección inválida.")
        return

    selected_book: str = available_books[int(selected_index) - 1]
    question: str = input("\nEscriba su pregunta sobre el libro: ").strip()

    llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")  # Ajusta según tu configuración
    answer: str = answer_question_about_book(llm, selected_book, question)

    print(f"\n🧠 Respuesta:\n{answer}")
