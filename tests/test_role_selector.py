import tkinter as tk
from app.widgets.role_selector import create_role_selector

def test_create_role_selector():
    root = tk.Tk()
    root.withdraw()

    roles = ["math teacher", "economics teacher", "technology teacher"]
    selected_role = tk.StringVar()
    selector = create_role_selector(root, selected_role, roles)

    assert isinstance(selector, tk.OptionMenu)
    assert selected_role.get() == roles[0]

    root.destroy()