# cli/cli_options/chat_experience.py

from app.utils import contar_palabras
from app.prompt import construir_prompt, limpiar_respuesta
from app.model import cargar_modelo, generar_respuesta
from common.types import Turno
from app.data.roles import roles

def run_chat_experience() -> None:
    """
    Launches the interactive chatbot session.
    """
    llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")
    print("💻 Welcome to your LLM assistant!")
    # choose a role for the chatbot
    print("Choose a role for the chatbot:")
    while True:
        for idx, role in enumerate(roles, start=1):
            print(f"{idx}. {role}")
        role_choice = input("Enter the number of your choice: ").strip()
        if role_choice.isdigit() and 1 <= int(role_choice) <= len(roles):
            rol = roles[int(role_choice) - 1]
            break

    historial: list[Turno] = []

    while True:
        user_input = input("\n🧑 Usuario: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("👋 ¡Hasta luego!")
            break

        if contar_palabras(user_input) > 150:
            print("⚠️ Has escrito demasiadas palabras. Máximo permitido: 150.")
            continue

        prompt = construir_prompt(historial, user_input, rol=rol)
        try:
            respuesta = generar_respuesta(llm, prompt)
            respuesta = limpiar_respuesta(respuesta)
            historial.append({"usuario": user_input, "respuesta": respuesta})
            print(f"🤖 Teacher: {respuesta}")
        except Exception as e:
            if "exceed context window" in str(e):
                print("⚠️ Se excedió la ventana de contexto. Se borrará el historial.")
                historial = []
            else:
                print(f"❌ Error: {e}")
