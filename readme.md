Estructure of the Project
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
│   │   └── construir_prompt(historial, user_input, rol)   # Builds a prompt using conversation history and a role
│   │   └── limpiar_respuesta(...)  # Cleans up the model's raw output
│
│   ├── utils.py                    # [Helper Functions]
│   │   └── contar_palabras(...)    # Counts the number of words in a string
│
│   ├── types.py                    # [Type Definitions]
│   │   └── Turno                   # TypedDict for a conversation turn (user + response)
│
│   |── widgets/                     # Custom Tkinter widgets
│   │   └── send_button.py          # Widget for the send button
|   |   └── create_send_button(...)    # Function to create a styled send button
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
│   ├── test_send_button.py         # Tests for button widget creation
│
├── requirements.txt                # Python dependencies
└── README.md                       # Project overview and usage instructions