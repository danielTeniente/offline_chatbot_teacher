import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from typing import List, Dict, Any
from app.data.roles import roles
from app.model import cargar_modelo, generar_respuesta, generate_summary_book
from app.prompt import construir_prompt, limpiar_respuesta
from app.utils import contar_palabras
from app.interface import mostrar_mensaje, actualizar_respuesta
from app.widgets.send_button import create_send_button
from app.widgets.role_selector import create_role_selector
from common.types import Turno

class ChatbotPanel:
    def __init__(self, parent: tk.Misc, width: int, shared_state: Dict[str, Any]):
        self.frame = tk.Frame(parent, width=width)
        self.shared_state = shared_state
        
        self.previous_book_summarized = False
        self.frame.after(1000, self.check_book_summarized_state)

        self.historial: List[Turno] = []
        self.llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")

        self.chat_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, state="disabled", font=("Arial", 15))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.role_var = tk.StringVar()
        role_frame = tk.Frame(self.frame)
        role_frame.pack(padx=10, pady=(0, 5), fill=tk.X)
        role_label = tk.Label(role_frame, text="Selecciona el rol:", font=("Arial", 10))
        role_label.pack(side=tk.LEFT)
        self.role_selector = create_role_selector(role_frame, self.role_var, roles)
        self.role_selector.pack(side=tk.LEFT, padx=(5, 0))

        input_frame = tk.Frame(self.frame)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Text(input_frame, height=4, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", self.enviar_mensaje_evento)
        self.entry.bind("<Shift-Return>", lambda e: None)

        
        self.send_button = create_send_button(
            input_frame,
            command=self.enviar_mensaje,
            text="➡️",
            width=10,
            height=2,
            font=("Arial", 10, "bold")
        )

        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        mostrar_mensaje(self.chat_area, "Profesor 24/7", "👋 ¡Hola! Soy tu profesor disponible 24/7. Estoy aquí para ayudarte a aprender. ¿Qué quieres saber hoy?")

    def enviar_mensaje_evento(self, event):
        self.enviar_mensaje()
        return "break"

    def enviar_mensaje(self):
        user_input: str = self.entry.get("1.0", tk.END).strip()
        self.entry.delete("1.0", tk.END)

        if not user_input:
            return

        if contar_palabras(user_input) > 150:
            messagebox.showwarning("Límite de palabras", "Has escrito más de 150 palabras.")
            return

        mostrar_mensaje(self.chat_area, "Usuario", user_input)
        mostrar_mensaje(self.chat_area, "Profesor 24/7", "⏳ Pensando...")

        rol: str = self.role_var.get()
        Thread(target=self.generar_y_mostrar_respuesta, args=(user_input, rol), daemon=True).start()

    def generar_y_mostrar_respuesta(self, user_input: str, rol: str):
        prompt: str = construir_prompt(self.historial, user_input, rol)
        try:
            respuesta: str = generar_respuesta(self.llm, prompt)
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


    def check_book_summarized_state(self):
        current_state = self.shared_state.get("book_summarized", False)
        if current_state and not self.previous_book_summarized:
            self.previous_book_summarized = True
            self.mostrar_resumen_libro()

        elif not current_state:
            self.previous_book_summarized = False

        # Check again after 1 second
        self.frame.after(1000, self.check_book_summarized_state)

    def mostrar_resumen_libro(self):
        mostrar_mensaje(self.chat_area, "Profesor 24/7", "📖 Leyendo el libro para generar el resumen...")

        def generar_y_mostrar():
            try:
                resumen = generate_summary_book(self.llm, self.shared_state.get("summarized_book_path", ""))
                mostrar_mensaje(self.chat_area, "Resumen del libro", resumen)
            except Exception as e:
                messagebox.showerror("Error al generar resumen", str(e))

        # Run in a separate thread to avoid freezing the UI
        Thread(target=generar_y_mostrar, daemon=True).start()

    

def create_chatbot_panel(parent: tk.Misc, width: int, shared_state: Dict[str, Any]) -> tk.Frame:
    panel = ChatbotPanel(parent, width, shared_state)
    return panel.frame