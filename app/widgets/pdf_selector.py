import tkinter as tk
from typing import Callable

def create_pdf_selector(parent: tk.Misc, pdfs: list[str], on_select: Callable[[str], None]) -> tuple[tk.Frame, tk.StringVar]:
    selected_pdf = tk.StringVar(value="Selecciona un libro")

    frame = tk.Frame(parent)

    label = tk.Label(frame, text="Libro seleccionado:", font=("Arial", 10))
    label.pack(side=tk.LEFT)

    display = tk.Entry(frame, textvariable=selected_pdf, font=("Arial", 10), state="readonly", width=40)
    display.pack(side=tk.LEFT, padx=(5, 0))

    def update_selection(event):
        selection = listbox.get(listbox.curselection())
        selected_pdf.set(selection)
        on_select(selection)

    listbox = tk.Listbox(frame, height=5)
    for pdf in pdfs:
        listbox.insert(tk.END, pdf)
    listbox.pack(side=tk.LEFT, padx=(10, 0))
    listbox.bind("<<ListboxSelect>>", update_selection)

    return frame, selected_pdf