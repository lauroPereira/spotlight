# ✨ Spotlight: IA para Agrupamento Inteligente de Reclamações

O **Spotlight** 🔦 é uma prova de conceito que utiliza **Inteligência Artificial Generativa** para identificar padrões recorrentes em grandes volumes de reclamações, incidentes ou tickets de suporte. Com base em textos livres coletados de múltiplas fontes, o sistema aplica embeddings semânticos e técnicas de clusterização para **organizar, entender e priorizar os assuntos mais críticos**. 


## 🧠 Tecnologias Utilizadas
- Python 3.10+
- LangChain + langchain-community + langchain-openai
- OpenAIEmbeddings
- FAISS (para busca vetorial)
- KMeans (via Scikit-learn)


## 📚 Como Usar
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

### 5. Execute o projeto
```bash
python main.py
```

Você verá:
- Reclamações similares por busca semântica
- Clusters de assuntos agrupados automaticamente
- Resposta gerada pela IA com base nas reclamações


## 📊 Casos de Uso
- Priorizacão de correções em sistemas com base em feedbacks reais
- Análise de reputação a partir de dados públicos (ReclameAqui, ouvidorias, redes sociais)
- Insights operacionais a partir de logs e registros de atendimento


## 🔄 Roadmap
- [ ] Conectar a fontes de dados reais (APIs, scraping, etc.)
- [ ] Adicionar visualização com Streamlit 
- [ ] Criar API REST para consumo dinâmico


## ✨ Origem
Este projeto é uma evolução de um **Trabalho de Conclusão de Curso (2018)**, originalmente implementado em PHP com K-means. Agora, ele é reimaginado com ferramentas modernas de IA e NLP para atender cenários reais de tomada de decisão e eficiência operacional.
