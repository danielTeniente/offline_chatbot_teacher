import tkinter as tk
from tkinter import filedialog
from typing import Callable

DEFAULT_PATH = "./books"

def create_book_path_selector(parent: tk.Misc, on_path_change: Callable[[str], None]) -> tuple[tk.Frame, tk.StringVar]:
    path_var = tk.StringVar(value=DEFAULT_PATH)

    frame = tk.Frame(parent)

    label = tk.Label(frame, text="Ruta de libros:", font=("Arial", 10))
    label.pack(side=tk.LEFT)

    path_display = tk.Entry(frame, textvariable=path_var, font=("Arial", 10), state="readonly", width=40)
    path_display.pack(side=tk.LEFT, padx=(5, 0))

    def select_folder():
        selected = filedialog.askdirectory(initialdir=DEFAULT_PATH)
        if selected:
            path_var.set(selected)
            on_path_change(selected)

    change_button = tk.Button(frame, text="Cambiar", command=select_folder)
    change_button.pack(side=tk.LEFT, padx=(5, 0))

    return frame, path_var

