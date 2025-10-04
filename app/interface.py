# app/interface.py
import tkinter as tk

def mostrar_mensaje(area: tk.Text, autor: str, mensaje: str) -> None:
    area.config(state="normal")
    area.insert(tk.END, f"{autor}: {mensaje}\n\n")
    area.config(state="disabled")
    area.see(tk.END)

def actualizar_respuesta(area: tk.Text, nueva_respuesta: str) -> None:
    area.config(state="normal")
    contenido = area.get("1.0", tk.END)
    if "Profesor 24/7: ⏳ Pensando..." in contenido:
        contenido = contenido.replace("Profesor 24/7: ⏳ Pensando...\n\n", f"Profesor 24/7: {nueva_respuesta}\n\n")
        area.delete("1.0", tk.END)
        area.insert(tk.END, contenido)
    else:
        area.insert(tk.END, f"Profesor 24/7: {nueva_respuesta}\n\n")
    area.config(state="disabled")
    area.see(tk.END)