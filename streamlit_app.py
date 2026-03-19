import streamlit as st
from src.barista_ai import ask_barista, get_service_context

# Configurações da página
st.set_page_config(page_title="AI Barista - Coffee Now", page_icon="☕")

# Estilização básica
st.title("☕ AI Barista")
st.caption("Recomendações de café sensíveis ao contexto, impulsionadas por dados e inteligência artificial")
st.markdown("---")

# Inicializa o histórico de chat no estado da sessão (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de input do usuário
if prompt := st.chat_input("Como posso ajudar com seu café hoje?"):
    
    # Adiciona a mensagem do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do Barista
    with st.chat_message("assistant"):
        with st.spinner("Preparando sua recomendação..."):
            try:
                response = ask_barista(prompt)
            except Exception as e:
                response = "⚠️ Ocorreu um erro ao gerar a recomendação. Tente novamente."

            st.markdown(response)
    
    # Adiciona a resposta da IA ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("⚙️ Status do Sistema")
    ctx = get_service_context()
    
    st.info(f"📍 Período: {ctx['periodo'].capitalize()}")
    st.info(f"👤 Persona: {ctx['persona']}")
    st.write("Dados de vendas carregados com sucesso. ✅")