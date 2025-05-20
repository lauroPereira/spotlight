import sys, os
from pathlib import Path
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document, HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Ajusta PYTHONPATH para importar plugins/schema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import logging
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("chatbot-page")

from plugins.schema import PluginResult

# Configuração de página
st.set_page_config(page_title="Chat", page_icon="💭", layout="wide")
st.title(f"💭 Descubra ainda mais sobre: {st.session_state.get('empresa_cache','N/D').upper()}")

# Sidebar: mostra empresa
st.sidebar.markdown("**Empresa:** " + st.session_state.get("empresa_cache", "N/D").upper())

# --- Helpers ---
@st.cache_data(show_spinner=False)
def load_documents(empresa: str) -> list[Document]:
    docs = []
    for f in Path("data").glob(f"*_{empresa}.json"):
        pr = PluginResult.model_validate_json(f.read_text(encoding="utf-8"))
        for c in pr.complaints:
            docs.append(Document(page_content=c.description, metadata={"source": pr.plugin, "category": c.category}))
    return docs

# Identificador da empresa
empresa = st.session_state.get("empresa_cache", "").strip().upper()
if not empresa:
    st.error("Nenhuma empresa selecionada.")
    st.stop()

# Chaves dinâmicas
history_key = f"chat_history_{empresa}"
initial_key = f"initial_messages_{empresa}"
vector_key = f"vectorstore_chat_{empresa}"
init_flag = f"initialized_{empresa}"

# Inicializa vector store para cada empresa
if vector_key not in st.session_state:
    docs = load_documents(empresa)
    if not docs:
        st.error("Nenhum dado disponível para chat.")
        st.stop()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    st.session_state[vector_key] = FAISS.from_documents(chunks, OpenAIEmbeddings())

# Setup LLM e chain
llm = ChatOpenAI(temperature=0)
chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=st.session_state[vector_key].as_retriever(),
    return_source_documents=False
)

# Inicializa histórico e mensagens iniciais por empresa
st.session_state.setdefault(history_key, [])
if not st.session_state.get(init_flag):
    sys_prompt = (
        f"Olá! Hoje você é o assistente virtual de atendimento da empresa {empresa}. "
        "Use as reclamações para fornecer insights e melhorar produtos e experiência do cliente."
    )
    init_q = "Quem é você?"
    persona = llm([SystemMessage(content=sys_prompt), HumanMessage(content=init_q)])
    st.session_state[initial_key] = [(init_q, persona.content)]
    st.session_state[init_flag] = True

# --- UI de chat ---
# Exibe histórico real
for user, bot in st.session_state[history_key]:
    st.markdown(f"**Você:** {user}")
    st.markdown(f"**Agente:** {bot}")

# Entrada de nova mensagem
user_input = st.text_input("Faça sua pergunta:", key=f"input_{empresa}")
if user_input:
    full_history = st.session_state[initial_key] + st.session_state[history_key]
    result = chain({"question": user_input, "chat_history": full_history})
    reply = result["answer"]
    st.session_state[history_key].append((user_input, reply))
    # limpa o campo de entrada
    st.session_state[f"input_{empresa}"] = ""
