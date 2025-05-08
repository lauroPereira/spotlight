# ✨ Spotlight: IA para Agrupamento Inteligente de Reclamações

O **Spotlight** 🔦 é uma prova de conceito que utiliza **Inteligência Artificial Generativa** para identificar padrões recorrentes em grandes volumes de reclamações, incidentes ou tickets de suporte. Com base em textos livres coletados de múltiplas fontes, o sistema aplica embeddings semânticos e técnicas de clusterização para **organizar, entender e priorizar os assuntos mais críticos**. 


## 🧠 Tecnologias Utilizadas
- Python 3.10+
- LangChain 
- OpenAI / HuggingFace Embeddings
- MongoDB Vector Search ou FAISS
- KMeans / HDBSCAN
- (Opcional) Streamlit para visualização


## 📚 Como Usar
1. Adicione reclamações no arquivo `data/sample_complaints.json`
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. Veja no terminal os **clusters gerados** e **recomendações semânticas** baseadas em similaridade textual


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
