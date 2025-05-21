import sys, os
import streamlit as st

# Ajusta PYTHONPATH para importar plugins/schema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import logging
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("helpdesk-page")

# Página de mock de integrações com CRMs
st.set_page_config(page_title="HelpDesk", page_icon="🛠️", layout="wide")
st.title("🛠️ HelpDesk – Integrações com CRMs")

st.markdown(
    "Nesta página você pode sincronizar e consultar tickets de diferentes sistemas de CRM corporativo. "
    "Clique em '🔎 Buscar' para simular a conexão e recuperação de dados." 
)

# Layout em três colunas para cada CRM
cols = st.columns(3, gap="large")

with cols[0]:
    st.subheader("Salesforce")
    st.image("assets\salesforce-logo.png", use_container_width=True)
    if st.button("🔎 Buscar", key="search_salesforce"):
        st.info("Buscando tickets no Salesforce...")
        # Aqui entraria a lógica real de integração

with cols[1]:
    st.subheader("Siebel")
    st.image("assets\siebel-logo.png", use_container_width=True)
    if st.button("🔎 Buscar", key="search_siebel"):
        st.info("Buscando tickets no Siebel...")
        # Aqui entraria a lógica real de integração

with cols[2]:
    st.subheader("ServiceNow")
    st.image("assets\service-now-logo.png", use_container_width=True)
    if st.button("🔎 Buscar", key="search_servicenow"):
        st.info("Buscando tickets no ServiceNow...")
        # Aqui entraria a lógica real de integração

# Rodapé de observação
st.markdown("---")
st.caption("*Este é um mock de interface. Integrações reais devem ser configuradas nos parâmetros de autenticação.*")
