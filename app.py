# app.py
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Instancia modelo
chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Interface
st.set_page_config(page_title="Chatbot com LangChain", layout="centered")
st.title("🤖 Chatbot com LangChain")

# Prompt inicial do sistema
system_prompt = SystemMessage(
    content="Você é um assistente especialista em atendimento ao cliente de uma empresa de tecnologia."
)

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# Input do usuário
user_input = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar") and user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.spinner("Processando resposta..."):
        response = chat(st.session_state.messages)
        st.session_state.messages.append(response)
        st.success(response.content)

    # Log
    with open("logs/conversas.txt", "a") as f:
        f.write(f"Usuário: {user_input}\nBot: {response.content}\n\n")
