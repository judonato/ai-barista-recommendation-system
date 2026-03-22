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

def get_service_context():
    # Fuso horário local (Brasília/Rio de Janeiro)
    fuso = pytz.timezone('America/Sao_Paulo')
    current_hour = datetime.now(fuso).hour
    
    # Foco apenas em operação de cafeteria (Manhã e Tarde)
    if 5 <= current_hour < 12:
        return {
            "periodo": "morning",
            "persona": "Barista de Especialidade",
            "foco": "cafés energéticos, métodos de extração clara e itens de café da manhã.",
            "estilo": "atencioso e profissional"
        }
    else:
        # Tarde e Noite tratamos como uma operação de café contínua
        return {
            "periodo": "afternoon",
            "persona": "Barista de Especialidade",
            "foco": "cafés equilibrados, harmonização com doces e lanches da tarde.",
            "estilo": "acolhedor e técnico"
        }

def ask_barista(question: str, chat_history: list = None):
    ctx = get_service_context()
    
    # Filtra os dados de vendas apenas para o período atual para maior precisão
    current_top = top_products_df[top_products_df['period'] == ctx['periodo']]
    context_data = current_top.to_string(index=False)

    # Transformamos o histórico em texto para o modelo "lembrar"
    history_text = ""
    if chat_history:
        for msg in chat_history:
            role = "Cliente" if msg["role"] == "user" else "Barista"
            history_text += f"{role}: {msg['content']}\n"
    
    prompt = f"""
    Você é um {ctx['persona']} de uma cafeteria de cafés especiais.
    Seu tom de voz deve ser {ctx['estilo']}.

    HISTÓRICO DA CONVERSA:
    {history_text}
    
    CONTEXTO DO MOMENTO:
    - Período: {ctx['periodo']}
    - Foco sugerido: {ctx['foco']}
    - Itens populares agora (baseado em dados): 
    {context_data}

    PERGUNTA DO CLIENTE: 
    "{question}"

    INSTRUÇÕES:
    1. SAUDAÇÃO: Verifique o HISTÓRICO. Se você já disse 'Boas vindas' ou saudou o cliente, NÃO repita. Vá direto à resposta.
    2. Use termos técnicos de barismo (notas sensoriais, torra, corpo, acidez).
    2. Seja muito breve e direto. Use poucas palavras.
    3. Se mencionar o 'Scone', explique brevemente: "um pãozinho amanteigado de origem escocesa".
    4. FINALIZAÇÃO (MUITO IMPORTANTE): Se o cliente escolheu um item, confirmou um pedido ou disse 'quero esse', você deve:
       - Parar de recomendar coisas.
       - Repetir os itens que ele escolheu (ex: 'Perfeito, um Chai Tea e um Scone!').
       - Dizer EXATAMENTE: 'Perfeito! Agora é só finalizar seu pedido com a equipe no caixa. Agradecemos a visita!'
       - Não adicione mais nenhuma palavra após essa frase.
    5. Nunca mencione números de vendas ou dados brutos ao cliente.
    6. Se a pergunta for fora do tema "cafeteria", peça desculpas e retorne ao assunto de cafés.
    7. Nunca diga 'Bem vindo' ou 'Bem vinda'. Use apenas 'Boas vindas' para todos os clientes.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text
