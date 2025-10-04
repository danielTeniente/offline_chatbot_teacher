import tkinter as tk
from typing import Callable

def create_role_selector(parent: tk.Misc, variable: tk.StringVar, options: list[str]) -> tk.OptionMenu:
    """
    Creates a dropdown menu for selecting the chatbot's role.

    Args:
        parent: The parent widget.
        variable: A StringVar to hold the selected role.
        options: A list of role options.

    Returns:
        A configured OptionMenu widget.
    """
    variable.set(options[0])  # Set default value
    return tk.OptionMenu(parent, variable, *options)