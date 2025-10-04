import tkinter as tk
from app.widgets.send_button import create_send_button

def test_create_send_button():
    root = tk.Tk()
    root.withdraw()  # Hide the window during testing

    def dummy_command(): pass
    button = create_send_button(root, dummy_command)

    assert button["text"] == "➡️"
    assert button["bg"] == "#4CAF50"
    assert button["fg"] == "white"
    assert button["font"] == "Arial 12 bold"
    assert button["width"] == 4
    assert button["height"] == 2

    root.destroy()