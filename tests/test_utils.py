from app.utils import contar_palabras

def test_contar_palabras():
    assert contar_palabras("Hola mundo") == 2
    assert contar_palabras("") == 0
    assert contar_palabras("Uno dos tres cuatro cinco") == 5