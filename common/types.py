from typing import TypedDict

class Turno(TypedDict):
    usuario: str
    respuesta: str

class BookMetadata(TypedDict):
    name: str
    path: str
    has_selectable_text: bool

