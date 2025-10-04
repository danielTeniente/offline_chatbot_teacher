import pytest
from app.model import cargar_modelo, generar_respuesta

def test_cargar_modelo():
    model = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")
    assert model is not None

def test_generar_respuesta():
    model = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")
    prompt = "Eres un profesor. Usuario: ¿Qué es la inflación?\nProfesor:"
    response = generar_respuesta(model, prompt)
    assert isinstance(response, str)
    assert len(response) > 0