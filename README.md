# ✨ Spotlight: IA para Agrupamento Inteligente de Reclamações

O **Spotlight** 🔦 é uma prova de conceito que utiliza **Inteligência Artificial Generativa** para identificar padrões recorrentes em grandes volumes de reclamações, incidentes ou tickets de suporte. Com base em textos livres coletados de múltiplas fontes, o sistema aplica embeddings semânticos e técnicas de clusterização para **organizar, entender e priorizar os assuntos mais críticos**. 


## 🧰 Tecnologias Utilizadas
- Python 3.10+
- LangChain + langchain-community + langchain-openai
- OpenAIEmbeddings
- FAISS (para busca vetorial)
- KMeans (via Scikit-learn)
- Streamlit (interface interativa)


## 🔧 Como Executar Localmente

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


## 🧪 Funcionalidades
- Inserir nome de uma empresa e importar reclamações de múltiplas fontes públicas
- Ingestão real dos dados do [Consumidor.gov.br](https://dados.mj.gov.br/)
- Processamento e clusterização com embeddings + IA
- Interface interativa para explorar os clusters gerados


## 📥 Fontes de Dados (implementadas)
- ✅ **Consumidor.gov.br** (CSV oficial com download e filtro por empresa)
- 🔜 Banco Central (Bacen)
- 🔜 Procon/RS


## 🔄 Roadmap
- [x] Ingestão via CSV do Consumidor.gov.br por empresa
- [x] Interface com campo para nome da empresa e botões por origem
- [ ] Scraping ou ingestão automatizada de ReclameAqui e Bacen
- [ ] Visualização de métricas dos clusters
- [ ] API REST para integração com outros sistemas


## ✨ Origem
Este projeto é uma evolução de um **Trabalho de Conclusão de Curso (2018)**, originalmente implementado em PHP com K-means. Agora, ele é reimaginado com ferramentas modernas de IA e NLP para atender cenários reais de tomada de decisão e eficiência operacional.