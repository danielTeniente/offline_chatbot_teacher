import unittest
from unittest.mock import MagicMock
from app.interface import mostrar_mensaje, actualizar_respuesta

class TestInterfaceFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_text = MagicMock()
        self.mock_text.get.return_value = "Profesor 24/7: ⏳ Pensando...\n\n"

    def test_mostrar_mensaje(self):
        mostrar_mensaje(self.mock_text, "User", "Hello, world!")
        self.mock_text.config.assert_any_call(state="normal")
        self.mock_text.insert.assert_called_with("end", "User: Hello, world!\n\n")
        self.mock_text.config.assert_any_call(state="disabled")
        self.mock_text.see.assert_called_with("end")

    def test_actualizar_respuesta_replaces_placeholder(self):
        actualizar_respuesta(self.mock_text, "This is the answer.")
        self.mock_text.config.assert_any_call(state="normal")
        self.mock_text.delete.assert_called_with("1.0", "end")
        self.mock_text.insert.assert_called_with("end", "Profesor 24/7: This is the answer.\n\n")
        self.mock_text.config.assert_any_call(state="disabled")
        self.mock_text.see.assert_called_with("end")

    def test_actualizar_respuesta_appends_if_no_placeholder(self):
        self.mock_text.get.return_value = "Some previous message\n\n"
        actualizar_respuesta(self.mock_text, "Another answer.")
        self.mock_text.insert.assert_called_with("end", "Profesor 24/7: Another answer.\n\n")

if __name__ == "__main__":
    unittest.main()