import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from app.model import cargar_modelo, generar_respuesta
from app.prompt import construir_prompt, limpiar_respuesta
from app.utils import contar_palabras
from app.types import Turno
from app.interface import mostrar_mensaje, actualizar_respuesta

class ChatbotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Profesor 24/7 - Aprendizaje sin límites")
        self.root.geometry("600x500")

        self.historial: list[Turno] = []
        self.llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Contenedor horizontal para entrada + botón
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Text(input_frame, height=4, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vincular tecla Enter al envío
        self.entry.bind("<Return>", self.enviar_mensaje_evento)
        self.entry.bind("<Shift-Return>", lambda e: None)  # Permitir salto de línea con Shift+Enter

        self.send_button = tk.Button(
            input_frame,
            text="➡️",
            command=self.enviar_mensaje,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=4,
            height=2
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        mostrar_mensaje(self.chat_area, "Profesor 24/7", "👋 ¡Hola! Soy tu profesor disponible 24/7. Estoy aquí para ayudarte a aprender. ¿Qué quieres saber hoy?")

    def enviar_mensaje_evento(self, event):
        self.enviar_mensaje()
        return "break"  # Evita que se agregue una nueva línea al presionar Enter

    def enviar_mensaje(self):
        user_input = self.entry.get("1.0", tk.END).strip()
        self.entry.delete("1.0", tk.END)

        if not user_input:
            return

        if contar_palabras(user_input) > 150:
            messagebox.showwarning("Límite de palabras", "Has escrito más de 150 palabras.")
            return

        mostrar_mensaje(self.chat_area, "Usuario", user_input)
        mostrar_mensaje(self.chat_area, "Profesor 24/7", "⏳ Pensando...")

        Thread(target=self.generar_y_mostrar_respuesta, args=(user_input,), daemon=True).start()

    def generar_y_mostrar_respuesta(self, user_input: str):
        prompt = construir_prompt(self.historial, user_input)
        try:
            respuesta = generar_respuesta(self.llm, prompt)
            respuesta = limpiar_respuesta(respuesta)
            self.historial.append({"usuario": user_input, "respuesta": respuesta})
            actualizar_respuesta(self.chat_area, respuesta)
        except Exception as e:
            if "exceed context window" in str(e):
                messagebox.showwarning("Contexto excedido", "Se borrará el historial.")
                self.historial = []
                actualizar_respuesta(self.chat_area, "⚠️ Se borró el historial por exceso de contexto.")
            else:
                messagebox.showerror("Error", str(e))
                actualizar_respuesta(self.chat_area, "❌ Hubo un error al generar la respuesta.")

def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()