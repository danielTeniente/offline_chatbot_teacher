tecni_zip_chat/
│
├── app/                            # Core chatbot logic and utilities
│   ├── __init__.py                 # Marks this directory as a Python package
│
│   ├── model.py                    # [LLM Integration]
│   │   └── cargar_modelo(ruta)     # Loads the Llama model from a file path
│   │   └── generar_respuesta(...)  # Generates a response from the model using a prompt
│
│   ├── prompt.py                   # [Prompt Construction]
│   │   └── construir_prompt(...)   # Builds a prompt using conversation history
│   │   └── limpiar_respuesta(...)  # Cleans up the model's raw output
│
│   ├── utils.py                    # [Helper Functions]
│   │   └── contar_palabras(...)    # Counts the number of words in a string
│
│   ├── types.py                    # [Type Definitions]
│   │   └── Turno                   # TypedDict for a conversation turn (user + response)
│
├── cli/                            # User interfaces (console and GUI)
│   ├── main.py                     # [Console Interface]
│   │   └── Runs the chatbot in terminal mode
│
│   ├── gui.py                      # [Graphical Interface]
│   │   └── Tkinter-based GUI for interacting with the chatbot
│
├── tests/                          # Unit tests for each module
│   ├── test_model.py               # Tests for model loading and response generation
│   ├── test_prompt.py              # Tests for prompt construction and cleaning
│   ├── test_utils.py               # Tests for utility functions
│
├── requirements.txt                # Python dependencies
└── README.md                       # Project overview and usage instructions