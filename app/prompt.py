# app/prompt.py
from app.types import Turno

def construir_prompt(historial: list[Turno], user_input: str, rol: str = "profesor de economía") -> str:
    prompt = f"Eres un {rol}. No puedes hablar de otros temas. Concéntrate en la enseñanza\n"
    for turno in historial[-2:]:
        prompt += f"Usuario: {turno['usuario']}\nProfesor 24/7: {turno['respuesta']}\n"
    prompt += f"Usuario: {user_input}\nProfesor 24/7:"
    return prompt

def limpiar_respuesta(texto: str) -> str:
    if "Usuario:" in texto:
        texto = texto.split("Usuario:")[0]
    return texto.strip()