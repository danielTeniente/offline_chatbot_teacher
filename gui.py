# gui
# archivo: tecni_zip_chat.py
import streamlit as st
from llama_cpp import Llama

# --- CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="TecniZip Chat", page_icon="💻")
st.title("TECNIZIP")  # Logo / palabra fija

# --- CARGA DEL MODELO ---
model_path = "./Phi-3-mini-4k-instruct-q4.gguf"  # Cambia a tu ruta
llm = Llama(model_path=model_path)

# --- HISTORIAL DE CONVERSACIÓN ---
if "historial" not in st.session_state:
    st.session_state.historial = []

# --- FORMULARIO DE ENTRADA ---
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_area(
        "Escribe tu mensaje (máximo 150 palabras):",
        height=100
    )
    submitted = st.form_submit_button("Enviar")

    # Contar palabras
    palabras = len(user_input.split())
    if palabras > 150:
        st.warning(f"Has escrito {palabras} palabras. Máximo permitido: 150.")
        submitted = False

# --- GENERAR RESPUESTA ---
if submitted and user_input.strip():
    # Tomar solo los últimos 2 intercambios como contexto
    contexto = st.session_state.historial[-2:] if len(st.session_state.historial) >= 2 else st.session_state.historial

    # Construir prompt con contexto
    #prompt = "Eres TecniZip, un asistente técnico simpático en español. Sólo puedes hablar de temas tecnológicos."
    prompt = "Eres TecniZip, un profesor amable de matemáticas que habla español. No puedes hablar de otros temas.\n"
    for turno in contexto:
        prompt += f"Usuario: {turno['usuario']}\nTecniZip: {turno['respuesta']}\n"
    prompt += f"Usuario: {user_input}\nTecniZip:"

    # Llamada al modelo
    respuesta_modelo = llm(prompt, max_tokens=200, temperature=0.3)
    respuesta_texto = respuesta_modelo["choices"][0]["text"].strip()

    # Guardar en historial
    st.session_state.historial.append({
        "usuario": user_input,
        "respuesta": respuesta_texto
    })

# --- MOSTRAR HISTORIAL ---
for turno in st.session_state.historial:
    st.markdown(f"**Usuario:** {turno['usuario']}")
    st.markdown(f"**TecniZip:** {turno['respuesta']}")
    st.markdown("---")
