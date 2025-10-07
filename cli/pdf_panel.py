import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from typing import Optional, cast
from document_ingestion.summarizer_utils import summarize_book
from tkinter import ttk, messagebox, Toplevel, Label
from typing import Dict, List, Optional, cast, Any
from app.widgets.book_path_selector import create_book_path_selector
from app.widgets.send_button import create_send_button
from document_ingestion.file_selector import discover_books
from app.utils import is_book_analyzed  
from common.types import BookMetadata
from document_ingestion.pdf_utils import has_selectable_text, get_PDF_content
from document_ingestion.chunking_book import process_pdf_for_llm
from common.types import BookMetadata


class PDFPanel:
    def __init__(self, parent: tk.Misc, width: int, shared_state: Dict[str, Any]):
        
        self.parent_window = parent  # Store the parent window
        self.shared_state = shared_state
        self.frame = tk.Frame(parent, width=width)

        self.book_path_var: tk.StringVar
        book_path_frame, self.book_path_var = create_book_path_selector(self.frame, self.on_book_path_change)
        book_path_frame.pack(padx=10, pady=(10, 5), fill=tk.X)

        self.book_path: str = self.book_path_var.get()
        self.books_metadata: Dict[str, BookMetadata] = discover_books(self.book_path)
        pdf_names: List[str] = list(self.books_metadata.keys())

        self.pdf_var: tk.StringVar = tk.StringVar()
        self.pdf_selector_frame = tk.Frame(self.frame)
        self.pdf_selector_frame.pack(padx=10, pady=(5, 10), fill=tk.X)
        pdf_label = tk.Label(self.pdf_selector_frame, text="Selecciona el PDF:", font=("Arial", 10))
        pdf_label.pack(side=tk.LEFT)
        self.pdf_combobox = ttk.Combobox(self.pdf_selector_frame, textvariable=self.pdf_var, values=pdf_names, state="readonly")
        self.pdf_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pdf_combobox.bind("<<ComboboxSelected>>", self.on_pdf_selected_event)

        self.selected_book_path: str = ""
        self.analyzer_button: tk.Button = create_send_button(
            parent,
            command=self.on_analyzer_click,
            text="Analizador",
            width=10,
            height=2,
            font=("Arial", 10, "bold")
        )
        
        self.simple_read_button: Optional[tk.Button] = None
        self.smart_read_button: Optional[tk.Button] = None

        
        self.summary_button: Optional[tk.Button] = create_send_button(
            parent=self.frame,
            command=self.on_summary_click,
            text="Resumen",
            width=14,
            height=2,
            font=("Arial", 10, "bold")
        )
        self.summary_button.pack(pady=(2, 10))
        self.summary_button.config(state="disabled")  # Initially disabled



    def on_book_path_change(self, new_path: str):
        self.book_path = new_path
        self.books_metadata = discover_books(new_path)
        pdf_names: List[str] = list(self.books_metadata.keys())
        self.pdf_combobox["values"] = pdf_names
        self.pdf_var.set("")

        # Hide analyzer button if path changes
        if self.analyzer_button:
            self.analyzer_button.pack_forget()

    def on_pdf_selected_event(self, event):
        pdf_name: str = self.pdf_var.get()
        selected_metadata = self.books_metadata.get(pdf_name)
        if selected_metadata:
            self.selected_book_path = selected_metadata["path"]
            self.show_analyzer_button()

    def show_analyzer_button(self):
        if self.analyzer_button:
            self.analyzer_button.pack_forget()

        self.analyzer_button = tk.Button(self.frame, text="Analizador", command=self.on_analyzer_click)
        self.analyzer_button.pack(pady=(5, 10))


    def on_analyzer_click(self) -> None:
        if not self.selected_book_path:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún libro.")
            return

        analyzed: bool = is_book_analyzed(self.selected_book_path)

        if analyzed:
            messagebox.showinfo("Estado del análisis", "Este libro ya fue analizado.")
            
            if self.summary_button is not None:
                self.summary_button.config(state="normal")
            return

        # Remove previous buttons if they exist (optional cleanup)
        if hasattr(self, "simple_read_button") and self.simple_read_button:
            self.simple_read_button.destroy()
        if hasattr(self, "smart_read_button") and self.smart_read_button:
            self.smart_read_button.destroy()

        # Show message in the interface (could be a label if preferred)
        messagebox.showinfo("Estado del análisis", "Este libro aún no ha sido analizado. Elige una opción para continuar:")

        # Create "Lectura simple" button
        self.simple_read_button: Optional[tk.Button] = create_send_button(
            parent=self.frame,
            command=self.on_simple_read_click,
            text="Lectura simple",
            width=14,
            height=2,
            font=("Arial", 10, "bold")
        )
        self.simple_read_button.pack(pady=(5, 2))

        # Enable only if the book has selectable text
        if has_selectable_text(self.selected_book_path):
            self.simple_read_button.config(state="normal")
        else:
            self.simple_read_button.config(state="disabled")

        # Create "Lectura inteligente" button
        self.smart_read_button: Optional[tk.Button] = create_send_button(
            parent=self.frame,
            command=self.on_smart_read_click,
            text="Lectura inteligente",
            width=14,
            height=2,
            font=("Arial", 10, "bold")
        )
        self.smart_read_button.pack(pady=(2, 10))

    def on_simple_read_click(self) -> None:
        """
        Handler for the 'Lectura simple' button.
        Shows a preview of the first page and asks for confirmation before processing.
        Displays a temporary 'processing' window during the operation.
        """
        try:
            preview_text: str = get_PDF_content(path=self.selected_book_path, page=0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo extraer el contenido del PDF.\nDetalles: {str(e)}")
            return

        preview_snippet: str = preview_text[:100].strip()
        if not preview_snippet:
            messagebox.showwarning("Texto no útil", "El texto extraído no parece ser útil para el análisis.")
            return

        confirm: bool = messagebox.askyesno(
            "Confirmar lectura simple",
            f"Texto extraído:\n\n\"{preview_snippet}...\"\n\n¿Deseas continuar con la lectura simple?"
        )

        if not confirm:
            return

        # Disable buttons
        if self.simple_read_button is not None:
            self.simple_read_button.config(state="disabled")
        if self.smart_read_button is not None:
            self.smart_read_button.config(state="disabled")
        self.analyzer_button.config(state="disabled")

        self.frame.update_idletasks()

        # Show processing window
        loading_window = Toplevel(self.frame)
        loading_window.title("Procesando")
        loading_window.geometry("250x100")
        loading_window.transient(cast(tk.Toplevel, self.parent_window))
        loading_window.grab_set()
        Label(loading_window, text="Procesando el libro...\nPor favor espera.", font=("Arial", 10)).pack(expand=True, pady=20)
        loading_window.update()

        try:
            result_message: str = process_pdf_for_llm(path=self.selected_book_path, use_ocr=False)
            loading_window.destroy()
            messagebox.showinfo("Lectura completada", result_message)
        except Exception as e:
            loading_window.destroy()
            messagebox.showerror("Error en el procesamiento", f"Ocurrió un error durante la lectura.\nDetalles: {str(e)}")
        finally:
            # Re-enable buttons
            if self.simple_read_button is not None:
                self.simple_read_button.config(state="normal")
            if self.smart_read_button is not None:
                self.smart_read_button.config(state="normal")
            self.analyzer_button.config(state="normal")

    def on_smart_read_click(self) -> None:
        """
        Handler for the 'Lectura inteligente' button.
        Displays a placeholder message indicating future development.
        """
        messagebox.showinfo("Lectura inteligente", "Esta funcionalidad está en desarrollo. ¡Pronto estará disponible!")


    def on_summary_click(self) -> None:
        """
        Handler for the 'Resumen' button.
        Displays a temporary 'processing' window while generating the summary.
        Shows the result message returned by summarize_book.
        """
        if not self.selected_book_path:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún libro.")
            return

        # Disable buttons during processing
        if self.summary_button is not None:
            self.summary_button.config(state="disabled")
        self.frame.update_idletasks()

        # Show processing window
        loading_window = Toplevel(self.frame)
        loading_window.title("Procesando")
        loading_window.geometry("250x100")
        loading_window.transient(cast(tk.Toplevel, self.parent_window))
        loading_window.grab_set()
        Label(loading_window, text="Generando el resumen...\nPor favor espera.", font=("Arial", 10)).pack(expand=True, pady=20)
        loading_window.update()

        try:
            # Call the summarization function and get the result message
            result_message: str = summarize_book(self.selected_book_path)
            loading_window.destroy()

            # Show result to the user
            messagebox.showinfo("Resumen generado", result_message)
            # Update shared state to indicate the book has been summarized
            self.shared_state["book_summarized"] = True
            self.shared_state["summarized_book_path"] = self.selected_book_path
            print(self.shared_state)
            
        except Exception as e:
            loading_window.destroy()
            messagebox.showerror("Error al resumir", f"No se pudo generar el resumen.\nDetalles: {str(e)}")
        finally:
            # Re-enable the summary button
            if self.summary_button is not None:
                self.summary_button.config(state="normal")


def create_pdf_panel(parent: tk.Misc, width: int, shared_state: Dict[str, Any]) -> tk.Frame:
    panel = PDFPanel(parent, width, shared_state)
    return panel.frame
