from typing import Any
from llama_cpp import Llama

def cargar_modelo(ruta: str) -> Any:
    return Llama(model_path=ruta)

def generar_respuesta(llm: Any, prompt: str) -> str:
    resultado = llm(prompt, max_tokens=200, temperature=0.5)
    return resultado["choices"][0]["text"]