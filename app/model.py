from typing import Any
from llama_cpp import Llama
import os
import json
from document_ingestion.ocr_utils import sanitize_name
from document_ingestion.chunk_search import rank_chunks_by_similarity  # You’ll create this next

def cargar_modelo(ruta: str, n_ctx = 1024) -> Any:
    return Llama(model_path=ruta, n_ctx=n_ctx)

def generar_respuesta(llm: Any, prompt: str, max_tokens: int = 200, temperature: float = 0.6) -> str:
    resultado = llm(prompt, max_tokens=max_tokens, temperature=temperature)
    return resultado["choices"][0]["text"]


def interpret_book_ideas(
    llm: Any,
    prompt: str,
    max_tokens: int = 200,
    temperature: float = 0.6,
    max_retries: int = 3
) -> str:
    """
    Attempts to interpret book ideas using a language model.
    If the input prompt exceeds token limits, retries by trimming the first 100 characters,
    up to `max_retries` times.

    Parameters:
    - llm: The language model callable.
    - prompt: The input prompt string.
    - max_tokens: Maximum number of tokens for the response.
    - temperature: Sampling temperature for the model.
    - max_retries: Number of times to retry by trimming the prompt.

    Returns:
    - A string with the model's response or an error message if the context is too large.
    """

    def try_prompt(current_prompt: str) -> str:
        """Helper function to call the model and handle errors."""
        try:
            result = llm(current_prompt, max_tokens=max_tokens, temperature=temperature)
            return result["choices"][0]["text"]
        except Exception as e:
            if "token" in str(e).lower() or "length" in str(e).lower():
                return ""  # Signal to retry
            return f"Unexpected error: {e}"

    for attempt in range(max_retries + 1):
        response = try_prompt(prompt)
        if response != "":
            return response
        # Trim the first 100 characters and retry
        print(f"Attempt {attempt + 1}: Prompt too long, trimming and retrying...")
        print(f"Current prompt length: {len(prompt)} characters")
        prompt = prompt[1000:]

    return "The context is too large to process. Please reduce the input size."

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


def answer_question_about_book(llm: Any, book_name: str, question: str) -> str:
    """
    Answers a question based on the most relevant chunks from a processed book.
    """
    book_path: str = os.path.join("text_data", book_name)

    chunks: list[dict] = []

    # Load all chunks with their embeddings
    for file_name in sorted(os.listdir(book_path)):
        if file_name.startswith("chunk_") and file_name.endswith(".json"):
            with open(os.path.join(book_path, file_name), "r", encoding="utf-8") as f:
                chunk_data = json.load(f)
                if "text" in chunk_data and "vector" in chunk_data:
                    chunks.append({
                        "text": chunk_data["text"],
                        "vector": chunk_data["vector"]
                    })

    # Rank chunks by relevance
    top_chunks: list[str] = rank_chunks_by_similarity(question, chunks, top_k=3)

    # Build prompt
    context: str = "\n\n".join(top_chunks)
    prompt: str = f"""Usa el siguiente contenido del libro para responder la pregunta del usuario.

        Contenido relevante:
        {context}

        Pregunta del usuario:
        {question}

        Respuesta:"""

    return generar_respuesta(llm, prompt, 350)
