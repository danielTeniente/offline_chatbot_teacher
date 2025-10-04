import tkinter as tk
from typing import Callable

def create_send_button(parent: tk.Misc, command: Callable[[], None]) -> tk.Button:
    """
    Creates a green send button with an arrow icon.
    """
    return tk.Button(
        parent,
        text="➡️",
        command=command,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        width=4,
        height=2
    )