# 🧠 Profesor 24/7

**Profesor 24/7** is an **offline chatbot** application built with Python that integrates a local **LLM (Large Language Model)** such as `Phi-3-mini-4k-instruct-q4`.  
It provides a **Tkinter-based GUI** for chatting, managing roles, and interacting with local PDF documents using both **text extraction** and **OCR** when needed.

---

## 🚀 Features

- 💬 **Offline Chatbot** powered by a local model (Phi-3, Llama, etc.)
- 🪶 **Prompt management** with roles and chat history
- 📚 **PDF integration** — select and scan books from a folder
- 🔍 **OCR support** using Tesseract for image-based PDFs
- 🧩 **Modular architecture** with clear separation between logic, GUI, and utilities
- 🧪 **Unit tests** for each component

---

## Create and activate a virtual environment
python -m venv .venv
### On Windows:
.venv\Scripts\activate
### On macOS/Linux:
source .venv/bin/activate

## Install dependencies
pip install -r requirements.txt

## Model 
This project is designed to work offline using a local model such as Phi-3-mini-4k-instruct-q4 from Hugging Face.

## Launch the application GUI
The GUI interfacte is easy to use for chatbot experience, the PDF tools need some improvements.
python -m cli.gui_main

This opens a Tkinter window with two panels:

Chatbot Panel: interact with the model, select roles, and send messages.

PDF Panel: select a directory with PDFs, preview, and process them with OCR.

## Launch the application CLI
This is a simple command-line to use all the features of the app.
python -m cli.main

📚 LLM‑Powered Book Assistant CLI
A small command‑line interface that lets you:

* Chat with a large language model (LLM).
* Generate chunks & embeddings from a PDF book (necessary for the next steps).
* Sumarise the book using the generated chunks.
* Ask questions about a processed book (Q&A).

## 🧾 OCR Setup (Tesseract)

1. Install Tesseract
2. Update config.json if needed

## 🧪 Running Test
python -m pytest --cov=apps

## Next Steps
* Improve PDF reading with OCR: currently, the app uses pypdf to extract text from PDFs.

## Previous Work
This project was built over a previous one called [pdfSearch](https://github.com/danielTeniente/pdfSearch) that was a simple GUI to search keywords in a book using regex and computer vision to improve text extraction from scanned PDFs.

