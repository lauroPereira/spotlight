# 🔦 Spotlight – Inteligência Artificial para Reclamações

Uma prova de conceito que utiliza técnicas modernas de **NLP, LLMs e IA Generativa para coletar, processar, clusterizar e explorar** reclamações e processos de diferentes fontes públicas.


## 🛠️ Tecnologias Utilizadas
Python 3.10+

- Streamlit: Interface web multiplataforma
- Pydantic v2: Validação de dados via schemas
- LangChain + langchain-community + langchain-openai: Orquestração de LLMs e RAG
- Transformers/HuggingFace: Pipeline de análise de sentimentos (nlptown/bert-base-multilingual-uncased-sentiment)
- Sentence-Transformers: Geração de embeddings (all-MiniLM-L6-v2)
- FAISS: Indexação vetorial em memória
- Scikit-Learn (DBSCAN): Algoritmo de clusterização de textos
- Streamlit Config: Arquivo de tema e parâmetros em .streamlit/config.toml


## 🚀 Como Rodar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/spotlight.git
cd spotlight
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv .venv

# Ative:
# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate

```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure sua chave OpenAI
Crie um arquivo `.env` na raiz com o seguinte conteúdo:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
> Nunca suba esse arquivo para o GitHub.

### 5. Execute a interface Streamlit
```bash
streamlit run streamlit_app/app.py
```


## 🗂️ Estrutura do Projeto
```bash
spotlight/
├── assets/                         # Pasta para arquivos estáticos utilizados
│   ├── salesforce-logo.png         
│   ├── service-now-logo.png         
│   ├── siebel-logo.png 
├── clustering/                     # Lógica de clusterização (DBSCAN, embeddings)
│   ├── embedding.py                # Funções para geração de vetores
│   └── cluster.py                  # Funções de agrupamento de textos
├── data/                           # Arquivos JSON com resultados de plugins
├── plugins/                        # Módulos de ingestão de reclamações/processos
│   ├── base.py                     # Classe abstrata IngestPlugin
│   ├── schema.py                   # Pydantic v2 schemas: Complaint, PluginResult
│   ├── ingest_anatel.py            # Plugin: Anatel (ZIP → CSV em chunks)
│   ├── ingest_consumidor_gov.py    # Plugin: Consumidor.gov.br (CSV)
│   ├── ingest_procon.py            # Plugin: Procon (XLSX)
│   └── ingest_cvm.py               # Plugin: CVM (ZIP → CSVs)
├── streamlit_app/                  # Interface Streamlit com páginas multi-app
│   ├── app.py                      # Roteamento das páginas
│   ├── pages/      
│   │   ├── 01_discover.py          # 🔦 Discover (ingestão)
│   │   ├── 02_feelings.py          # 💖 Mood Explorer (sentimento)
│   │   ├── 03_explorer.py          # 🔢 Data Explorer (clusterização + visual)
│   │   ├── 04_chat.py              # 💭 Chat RAG com histórico por empresa
│   │   └── 05_helpdesk.py          # 🛠️ HelpDesk (mock CRMs)
│   └── .streamlit/                 # Configurações nativas de tema e parâmetros
│       └── config.toml     
├── .env                            # Variáveis de ambiente (não versionar)
├── .gitignore
├── LICENSE                         # Este arquivo
├── README.md                       # Este arquivo
└── requirements.txt                # Dependências pip
```


## 📥 Fontes de Dados Integradas

* ✅ Consumidor.gov.br (CSV público)
* ✅ Procon/RS (XLSX oficial)
* ✅ Anatel (ZIP público)
* ✅ CVM (ZIP público)
* 🔜 ReclameAqui (em análise)
* 🔜 Banco Central (BACEN)


## 🖥️ Páginas e Funcionalidades

* 🔦 Discover: Coleta e agrupa reclamações/processos com plugins e cards atualizáveis.
* 💖 Mood Explorer: Classificação de sentimento (Positive/Neutral/Negative).
* 🔢 Data Explorer: Clusterização de textos (embeddings + DBSCAN).
* 💭 Chat: Conversa RAG com LLM, histórico por empresa.
* 🛠️ HelpDesk: Mock de integração com CRMs corporativos.

## 🛣️ Roadmap
### 🛹 Lançado

- Plugins de ingestão: Consumidor.gov, Procon, Anatel, CVM
- App Multi-Page: Discover, Mood Explorer, Data Explorer, Chat, HelpDesk
- Clusterização (DBSCAN + embeddings) e RAG com LangChain

### 🚴🏼‍♂️ Em breve

- Ingestão de novas fontes de dados abertos
- Dashboard de métricas avançadas
- Autenticação de usuários / API REST

### 🏎️ Futuro

- Integrações com CRMs reais e importação automática
- Alertas e notificações em tempo real
- Suporte multi-idioma


## ✨ Origem
Este projeto é uma evolução de um **Trabalho de Conclusão de Curso (2018)**, originalmente implementado em PHP com K-means. Agora, ele é reimaginado com ferramentas modernas de IA e NLP para atender cenários reais de tomada de decisão e eficiência operacional.

© 2025 **Lauro Pereira**. Se você compartilhar ou propagar este projeto, por favor cite a fonte:
https://github.com/lauroPereira/spotlight