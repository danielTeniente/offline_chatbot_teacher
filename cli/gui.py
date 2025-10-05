import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from threading import Thread
from typing import List, Dict
from app.data.roles import roles
from app.model import cargar_modelo, generar_respuesta
from app.prompt import construir_prompt, limpiar_respuesta
from app.utils import contar_palabras
from app.interface import mostrar_mensaje, actualizar_respuesta
from app.widgets.send_button import create_send_button
from app.widgets.role_selector import create_role_selector
from app.widgets.book_path_selector import create_book_path_selector
from document_ingestion.file_selector import discover_books
from common.types import Turno, BookMetadata

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CHAT_WIDTH_RATIO = 0.5
FUNCTIONALITY_WIDTH_RATIO = 1 - CHAT_WIDTH_RATIO

class ChatbotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Profesor 24/7 - Aprendizaje sin límites")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.historial: List[Turno] = []
        self.llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")

        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # === Left Frame: Chat ===
        chat_frame = tk.Frame(main_pane, width=int(WINDOW_WIDTH * CHAT_WIDTH_RATIO))
        main_pane.add(chat_frame)

        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state="disabled", font=("Arial", 15))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.role_var = tk.StringVar()
        role_frame = tk.Frame(chat_frame)
        role_frame.pack(padx=10, pady=(0, 5), fill=tk.X)
        role_label = tk.Label(role_frame, text="Selecciona el rol:", font=("Arial", 10))
        role_label.pack(side=tk.LEFT)
        self.role_selector = create_role_selector(role_frame, self.role_var, roles)
        self.role_selector.pack(side=tk.LEFT, padx=(5, 0))

        input_frame = tk.Frame(chat_frame)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Text(input_frame, height=4, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", self.enviar_mensaje_evento)
        self.entry.bind("<Shift-Return>", lambda e: None)

        self.send_button = create_send_button(input_frame, self.enviar_mensaje)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        mostrar_mensaje(self.chat_area, "Profesor 24/7", "👋 ¡Hola! Soy tu profesor disponible 24/7. Estoy aquí para ayudarte a aprender. ¿Qué quieres saber hoy?")

        # === Right Frame: Functionalities ===
        right_frame = tk.Frame(main_pane, width=int(WINDOW_WIDTH * FUNCTIONALITY_WIDTH_RATIO))
        main_pane.add(right_frame)

        self.book_path_var: tk.StringVar
        book_path_frame, self.book_path_var = create_book_path_selector(right_frame, self.on_book_path_change)
        book_path_frame.pack(padx=10, pady=(10, 5), fill=tk.X)

        self.book_path: str = self.book_path_var.get()
        self.books_metadata: Dict[str, BookMetadata] = discover_books(self.book_path)
        pdf_names: List[str] = list(self.books_metadata.keys())

        # PDF Selector as Combobox
        self.pdf_var: tk.StringVar = tk.StringVar()
        self.pdf_selector_frame = tk.Frame(right_frame)
        self.pdf_selector_frame.pack(padx=10, pady=(5, 10), fill=tk.X)
        pdf_label = tk.Label(self.pdf_selector_frame, text="Selecciona el PDF:", font=("Arial", 10))
        pdf_label.pack(side=tk.LEFT)
        self.pdf_combobox = ttk.Combobox(self.pdf_selector_frame, textvariable=self.pdf_var, values=pdf_names, state="readonly")
        self.pdf_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pdf_combobox.bind("<<ComboboxSelected>>", self.on_pdf_selected_event)

        self.selected_book_path: str = ""

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

    def on_book_path_change(self, new_path: str):
        self.book_path = new_path
        self.books_metadata = discover_books(new_path)
        pdf_names: List[str] = list(self.books_metadata.keys())
        self.pdf_combobox["values"] = pdf_names
        self.pdf_var.set("")

    def on_pdf_selected_event(self, event):
        pdf_name: str = self.pdf_var.get()
        selected_metadata = self.books_metadata.get(pdf_name)
        if selected_metadata:
            self.selected_book_path = selected_metadata["path"]

def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()