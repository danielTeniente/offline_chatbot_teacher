from app.prompt import construir_prompt, limpiar_respuesta
from app.types import Turno

def test_construir_prompt():
    historial: list[Turno] = [
        {"usuario": "¿Qué es la inflación?", "respuesta": "La inflación es el aumento general de precios."},
        {"usuario": "¿Cómo se mide?", "respuesta": "Se mide con el IPC."}
    ]
    user_input = "¿Qué causa la inflación?"
    prompt = construir_prompt(historial, user_input)
    assert "Usuario: ¿Qué causa la inflación?" in prompt
    assert prompt.startswith("Eres")

def test_limpiar_respuesta():
    raw = "La inflación es causada por varios factores. Usuario: ¿Qué más?"
    cleaned = limpiar_respuesta(raw)
    assert "Usuario:" not in cleaned
    assert cleaned.startswith("La inflación")