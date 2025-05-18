import streamlit as st
import sys, os
# Garante que o diretório raiz esteja no PYTHONPATH
print(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import logging

# configura logger para plugins
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("front-end")


st.set_page_config(page_title="🔦 Spotlight – Reclamações e processos", layout="wide")


# Configura o a barra lateral com o nome da empresa
st.session_state.setdefault("empresa_cache", "")
# garante que exista
if "empresa_cache" not in st.session_state:
    st.session_state["empresa_cache"] = ""
# Sidebar
st.sidebar.title("🔦 Spotlight")
st.sidebar.markdown(
    "Coleta e agrupa reclamações e processos de empresas. "
    "Escolha uma empresa na barra lateral para começar."
)
# Sidebar - parâmetros
with st.sidebar:
    st.header("⚙️ Parâmetros")
    empresa = st.text_input(
        "🏢 Empresa", 
        value=st.session_state["empresa_cache"], 
        key="empresa_sidebar"
    )
     # 👉 Bullet sempre visível informando a empresa selecionada
    if st.session_state["empresa_cache"]:
        st.markdown(f"- **Empresa selecionada:** {st.session_state['empresa_cache']}")
        
    if st.button("🚀 Definir Empresa"):
        # atualiza o cache e recarrega para as outras páginas
        st.session_state["empresa_cache"] = empresa.strip()
        st.rerun()
        
# lê o parâmetro fixo da sidebar
empresa = st.session_state["empresa_cache"]
if not empresa:
    st.warning("▶️ Defina a empresa desejada na barra lateral.")
    st.stop()
else:
    st.markdown(
       f"**🤖 **Chat**: Conversar com o agente sobre os dados da empresa **{empresa.upper()}**"
    )
