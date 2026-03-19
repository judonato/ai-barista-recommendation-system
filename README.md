AI Barista – Context-Aware Coffee Recommendation System

Este projeto é um sistema de recomendação inteligente que combina análise de dados reais com um Large Language Model (LLM) para simular um barista especialista.

O sistema utiliza injeção dinâmica de contexto para adaptar recomendações com base no horário do dia e no comportamento histórico de vendas.


# Features
- Context-aware coffee recommendations
- Integration with real sales data
- Time-based personalization (morning, afternoon, evening)
- LLM-powered conversational interface
- Data-driven decision making


# O Problema
Menus de cafeterias de especialidade podem ser complexos para o cliente médio. A escolha entre diferentes métodos (V60, AeroPress, Prensa) e grãos (notas sensoriais, acidez, corpo) muitas vezes gera fricção no momento da compra.


# A Solução: Context Engineering
O sistema não é apenas um chatbot genérico. Ele opera em três camadas:

1. Data Layer
Processa dados reais de vendas com Pandas para identificar os produtos mais populares por período do dia (morning, afternoon, evening).

2. Time Awareness Layer
Captura o horário atual do sistema para adaptar o contexto da recomendação.

3. LLM Inference Layer
Utiliza um prompt estruturado que injeta dinamicamente os dados filtrados, garantindo recomendações relevantes, contextuais e baseadas em evidência.


# Arquitetura do sistema (System Architecture)

User Input
↓
Context Detection (time of day)
↓
Data Retrieval (top products by period)
↓
Prompt Construction (context injection)
↓
LLM Response (Gemini)
↓
Final Recommendation


# Tecnologias Utilizadas
- Python
- Pandas (data analysis)
- Google Gemini 2.0 Flash Lite (LLM)
- python-dotenv (environment management)
- pytz (timezone handling)
- Streamlit


# Estrutura do Projeto
Project Structure

├── data/
│   └── coffee_sales_clean.csv
├── src/
│   ├── barista_ai.py
│   └── recommender.py
├── app.py
├── .env
├── requirements.txt
└── streamlit_app.py


# Configuração e Instalação
1. Clone o repositório:

Bash
git clone https://github.com/seu-usuario/ai-barista.git
cd ai-barista

2. Crie um ambiente virtual e instale as dependências:

Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure sua API Key:
Crie um arquivo .env na raiz do projeto e adicione:

Snippet de código
GEMINI_API_KEY=sua_chave_aqui

4. Execute a aplicação:
Opção 1: Interface Web
    streamlit run streamlit_app.py
    Então abra:
    http://localhost:8501
    
Opção 2: Versão CLI
    Bash
    python app.py


# Exemplo de Uso
CLIENTE: "Quero algo para acompanhar meu café agora à tarde."

BARISTA VIRTUAL: "Boa tarde! Para este momento, recomendo nosso Scone artesanal — um pãozinho amanteigado de origem escocesa que harmoniza perfeitamente com a acidez vibrante do nosso café filtrado mais pedido de hoje. Aceita essa sugestão?"

# Evoluções Futuras
- RAG (Retrieval-Augmented Generation): Incluir PDFs de manuais técnicos de grãos para respostas ainda mais profundas.

- API de Clima: Ajustar recomendações baseadas na temperatura externa (ex: sugerir Cold Brews em dias de calor).

---
Desenvolvido por Juliana Donato – Engenheira de IA e LLMs.