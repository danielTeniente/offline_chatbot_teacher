from typing import Any
from llama_cpp import Llama
import os
from document_ingestion.ocr_utils import sanitize_name


def cargar_modelo(ruta: str) -> Any:
    return Llama(model_path=ruta, n_ctx=1024)

def generar_respuesta(llm: Any, prompt: str, max_tokens: int = 200, temperature: float = 0.6) -> str:
    resultado = llm(prompt, max_tokens=max_tokens, temperature=temperature)
    return resultado["choices"][0]["text"]


def generate_summary_book(llm: Any, book_path: str) -> str:
    """Generates a summary for the book located at book_path using the provided LLM model.
    returns the summary as a string.
    """
    book_name = sanitize_name(os.path.splitext(os.path.basename(book_path))[0])
    book_folder = os.path.join('document_ingestion', 'text_data', book_name)
    summary_path = os.path.join(book_folder, 'summary.txt')

    try:
        with open(summary_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        prompt = (
            "Por favor, traduce y resume el siguiente contenido al español de forma clara y concisa:\n\n"
            f"{content}"
        )
        
        resumen = generar_respuesta(llm, prompt, max_tokens=400, temperature=0.6)
        return resumen.strip()
    
    except FileNotFoundError:
        return "Error: No se encontró el archivo en la ruta especificada."
    except Exception as e:
        return f"Error al generar el resumen: {str(e)}"
