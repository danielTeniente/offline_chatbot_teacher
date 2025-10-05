import tkinter as tk
from cli.chatbot_panel import create_chatbot_panel
from cli.pdf_panel import create_pdf_panel

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
CHAT_WIDTH_RATIO = 0.5
FUNCTIONALITY_WIDTH_RATIO = 1 - CHAT_WIDTH_RATIO

def main():
    root = tk.Tk()
    root.title("Profesor 24/7 - Aprendizaje sin límites")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Panel izquierdo: Chatbot
    chat_frame = create_chatbot_panel(main_pane, int(WINDOW_WIDTH * CHAT_WIDTH_RATIO))
    main_pane.add(chat_frame)

    # Panel derecho: Funcionalidades PDF
    pdf_frame = create_pdf_panel(main_pane, int(WINDOW_WIDTH * FUNCTIONALITY_WIDTH_RATIO))
    main_pane.add(pdf_frame)

    root.mainloop()

if __name__ == "__main__":
    main()