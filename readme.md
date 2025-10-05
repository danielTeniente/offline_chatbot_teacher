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
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

## Install dependencies
pip install -r requirements.txt

## Model 
This project is designed to work offline using a local model such as Phi-3-mini-4k-instruct-q4 from Hugging Face.

## Launch the application
python -m cli.gui_main

This opens a Tkinter window with two panels:

Chatbot Panel: interact with the model, select roles, and send messages.

PDF Panel: select a directory with PDFs, preview, and process them with OCR.

## 🧾 OCR Setup (Tesseract)

1. Install Tesseract
2. Update config.json if needed

## 🧪 Running Test
python -m pytest --cov=apps

