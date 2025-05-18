import sys, os
# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path
import streamlit as st
from typing import List, Optional
from plugins.schema import PluginResult
from plugins.base import IngestPlugin

# LangChain imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="Spotlight – Exploração", layout="wide")

@st.cache_data(show_spinner=False)
def load_records(empresa: str) -> List[dict]:
    """
    Carrega todos os JSONs de reclamações/processos de uma empresa na pasta data/. Retorna lista de dicts.
    """
    data_dir = Path("data")
    records = []
    for file in data_dir.glob(f"*_{empresa}.json"):
        pr: PluginResult = PluginResult.model_validate_json(file.read_text(encoding="utf-8"))
        for comp in pr.complaints:
            records.append({
                "plugin": pr.plugin,
                "date": comp.date.isoformat(),
                "category": comp.category,
                "description": comp.description,
                "source": pr.plugin
            })
    return records

@st.cache_resource(show_spinner=False)
def create_vectorstore(records: List[dict]) -> FAISS:
    """
    Cria ou carrega FAISS vectorstore a partir de descrições.
    """
    texts = [r["description"] for r in records]
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts, embeddings)

@st.cache_resource(show_spinner=False)
def create_qa_chain(vstore: FAISS) -> ConversationalRetrievalChain:
    """
    Cria cadeia de QA conversacional usando ChatOpenAI e vetor store.
    """
    llm = ChatOpenAI(temperature=0)
    return ConversationalRetrievalChain.from_llm(llm, vstore.as_retriever())

st.title("🗺️ Explorar Dataset Spotlight")
empresa = st.text_input("🏢 Nome da empresa para exploração", key="explore_empresa")

if st.button("📂 Carregar e Preparar Dados"):
    if not empresa:
        st.warning("Digite o nome da empresa antes de carregar.")
    else:
        with st.spinner("Carregando registros e gerando embeddings..."):
            records = load_records(empresa)
            if not records:
                st.error("Nenhum registro encontrado para essa empresa.")
                st.stop()
            vstore = create_vectorstore(records)
            qa_chain = create_qa_chain(vstore)
            st.session_state["records"] = records
            st.session_state["qa_chain"] = qa_chain
        st.success(f"Dados prontos: {len(records)} registros carregados.")

if "qa_chain" in st.session_state and "records" in st.session_state:
    st.markdown("---")
    st.header(f"🔍 Pergunte sobre dados de {empresa.strip().upper()}")
    query = st.text_input("❓ Sua pergunta:", key="explore_query")
    if st.button("🤖 Responder"):
        if not query:
            st.warning("Digite uma pergunta para receber uma resposta.")
        else:
            with st.spinner("Gerando resposta..."):
                result = st.session_state["qa_chain"].run(question=query)
            st.subheader("Resposta:")
            st.write(result)

    if st.checkbox("Mostrar registros brutos", key="show_raw"):
        import pandas as pd
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)
