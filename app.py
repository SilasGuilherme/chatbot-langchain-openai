# app.py

import streamlit as st
from openai import OpenAI
from vet_prompt import SYSTEM_PROMPT

# Configure sua chave da OpenAI no ambiente ou direto aqui (temporário)
client = OpenAI()

# Inicializa estado da conversa
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

st.set_page_config(page_title="Veterinário Virtual", page_icon="🐶🐱")

st.title("🐶🐱 Veterinário Virtual")
st.caption("Um assistente informativo para a saúde de cães e gatos. Não substitui uma consulta veterinária!")

with st.chat_message("ai"):
    st.markdown("Olá! Sou um veterinário virtual. Em que posso ajudar você hoje?")

# Exibe o histórico da conversa
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de input do usuário
if prompt := st.chat_input("Digite sua pergunta sobre seu pet..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        with st.spinner("Consultando literatura veterinária..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
