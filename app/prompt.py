# app/prompt.py
from common.types import Turno

def construir_prompt(historial: list[Turno], user_input: str, rol: str = "profesor de economía") -> str:
    prompt = ""
    for turno in historial[-2:]:
        prompt += f"{turno['respuesta']}\n"
    # getting just last 500 characters from previous context to avoid exceeding context window
    prompt = f"Context:{prompt[-500:]} \n"
    prompt += f"You are a {rol}. Don't speak about other topics\n"
    prompt += f"Usuario: {user_input}\nTeacher 24/7:"
    return prompt

def limpiar_respuesta(texto: str) -> str:
    if "Usuario:" in texto:
        texto = texto.split("Usuario:")[0]
    return texto.strip()