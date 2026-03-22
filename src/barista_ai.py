import os
import pytz
import streamlit as st
from google import genai
from dotenv import load_dotenv
from datetime import datetime
from .recommender import load_sales_data, top_products_by_period

load_dotenv()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Carregamento global dos dados
df = load_sales_data()
top_products_df = top_products_by_period(df)


# -------------------------
# CONTEXTO
# -------------------------
def get_service_context():
    fuso = pytz.timezone('America/Sao_Paulo')
    current_hour = datetime.now(fuso).hour
    
    if 5 <= current_hour < 12:
        return {
            "periodo": "morning",
            "persona": "Barista de Especialidade",
            "foco": "cafés energéticos, métodos de extração clara e itens de café da manhã.",
            "estilo": "atencioso e profissional"
        }
    
    elif 12 <= current_hour < 18:
        return {
            "periodo": "afternoon",
            "persona": "Barista de Especialidade",
            "foco": "cafés equilibrados, harmonização com doces e lanches da tarde.",
            "estilo": "acolhedor e técnico"
        }
    
    else:
        return {
            "periodo": "evening",
            "persona": "Barista de Especialidade",
            "foco": "bebidas mais suaves, opções descafeinadas e experiências relaxantes.",
            "estilo": "calmo e acolhedor"
        }


# -------------------------
# LÓGICA DE CONTROLE
# -------------------------
def is_order_final(user_input: str):
    keywords = ["quero", "vou querer", "esse", "pode ser", "sim", "fechado"]
    return any(word in user_input.lower() for word in keywords)


def build_history(messages):
    # pega só últimas 5 mensagens pra não poluir
    history = messages[-5:]
    return "\n".join([f"{m['role']}: {m['content']}" for m in history])


# -------------------------
# FUNÇÃO PRINCIPAL
# -------------------------
def ask_barista(question: str, messages: list):
    ctx = get_service_context()

    # CONTROLE DE ESTADO
    if "stage" not in st.session_state:
        st.session_state.stage = "greeting"

    stage = st.session_state.stage

    # FINALIZAÇÃO (ANTES DO LLM)
    if is_order_final(question) and stage != "finished":
        st.session_state.stage = "finished"

        return f"""
Perfeito! Pedido confirmado.

Agora é só finalizar seu pedido com a equipe no caixa.
Agradecemos a visita!
"""

    # CONTEXTO DE DADOS
    current_top = top_products_df[top_products_df['period'] == ctx['periodo']]
    context_data = current_top.to_string(index=False)

    # HISTÓRICO
    history_text = build_history(messages)

    # CONTROLE DE SAUDAÇÃO
    greeting_rule = (
        "Comece com 'Boas vindas'"
        if stage == "greeting"
        else "NÃO faça saudação. Vá direto ao ponto."
    )

    # PROMPT
    prompt = f"""
    Você é um {ctx['persona']} de uma cafeteria de cafés especiais.
    Seu tom deve ser {ctx['estilo']}.

    REGRAS:
    - {greeting_rule}
    - Seja breve e direto
    - Não repita explicações
    - Use termos de barismo (acidez, torra, corpo, notas)
    - Se o cliente já decidiu, NÃO sugira mais nada
    - Nunca diga 'Bem vindo', apenas 'Boas vindas' na primeira mensagem
    - Nunca mencione números de vendas ou dados brutos ao cliente
    - Se a pergunta for fora do tema "cafeteria", peça desculpas e retorne ao assunto de cafés
    - Se mencionar o 'Scone', explique brevemente: "um pãozinho amanteigado de origem escocesa"
    - Após oferecer opções, pergunte qual delas a pessoa gostaria.

    CONTEXTO:
    Período: {ctx['periodo']}
    Foco: {ctx['foco']}

    ITENS POPULARES:
    {context_data}

    HISTÓRICO:
    {history_text}

    CLIENTE:
    {question}

    Responda como barista:
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    # muda estado depois da primeira resposta
    if stage == "greeting":
        st.session_state.stage = "ordering"

    return response.text
