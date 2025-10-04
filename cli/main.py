# cli/main.py
from app.utils import contar_palabras
from app.prompt import construir_prompt, limpiar_respuesta
from app.model import cargar_modelo, generar_respuesta
from common.types import Turno

def main():
    print("💻 Bienvenido a TecniZip Chat (modo consola)")
    llm = cargar_modelo("./Phi-3-mini-4k-instruct-q4.gguf")
    historial: list[Turno] = []

    while True:
        user_input = input("\n🧑 Usuario: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("👋 ¡Hasta luego!")
            break

        if contar_palabras(user_input) > 150:
            print("⚠️ Has escrito demasiadas palabras. Máximo permitido: 150.")
            continue

        prompt = construir_prompt(historial, user_input)
        try:
            respuesta = generar_respuesta(llm, prompt)
            respuesta = limpiar_respuesta(respuesta)
            historial.append({"usuario": user_input, "respuesta": respuesta})
            print(f"🤖 TecniZip: {respuesta}")
        except Exception as e:
            if "exceed context window" in str(e):
                print("⚠️ Se excedió la ventana de contexto. Se borrará el historial.")
                historial = []
            else:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()