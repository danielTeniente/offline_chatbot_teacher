import tkinter as tk
from typing import Callable, Optional

def create_send_button(
    parent: tk.Misc,
    command: Callable[[], None],
    text: Optional[str] = "➡️",
    bg: str = "#4CAF50",
    fg: str = "white",
    font: tuple = ("Arial", 12, "bold"),
    width: int = 4,
    height: int = 2
) -> tk.Button:
    """
    Creates a styled send button. Defaults to a green arrow button,
    but allows customization for other use cases.
    """
    safe_text = text if text is not None else ""  # Ensure it's a string
    return tk.Button(
        parent,
        text=safe_text,
        command=command,
        bg=bg,
        fg=fg,
        font=font,
        width=width,
        height=height
    )