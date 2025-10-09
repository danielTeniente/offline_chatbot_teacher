# cli/main.py

from cli.cli_options.chat_experience import run_chat_experience
from cli.cli_options.generate_chunks import run_chunk_generation
from cli.cli_options.summarize_book import run_summary_generation
from cli.cli_options.book_qa import run_book_question_answering

def show_menu() -> None:
    """
    Displays the main CLI menu.
    """
    print("\n📋 Menú Principal")
    print("1. 🤖 Iniciar Chat con LLM")
    print("2. 📚 Generar Chunks y Embeddings desde un libro PDF")
    print("3. 📝 Generar resumen del libro basado en chunks")
    print("4. 📖 Preguntar sobre un libro procesado")
    print("0. ❌ Salir")

def main() -> None:
    """
    Main entry point for the CLI menu.
    """
    while True:
        show_menu()
        choice: str = input("\nSeleccione una opción: ").strip()

        if choice == "1":
            run_chat_experience()
        elif choice == "2":
            run_chunk_generation()
        elif choice == "3":
            run_summary_generation()
            
        elif choice == "4":
            run_book_question_answering()

        elif choice == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
