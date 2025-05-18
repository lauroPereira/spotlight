import streamlit as st

# Configurações gerais
st.set_page_config(
    page_title="Spotlight", 
    page_icon="🔦",
    layout="wide"
)

# Página inicial
st.title("🔦 Spotlight")
st.markdown(
    "Bem-vindo ao Spotlight! Use o menu lateral para navegar entre as páginas de Ingestão e Exploração de dados."
)

st.sidebar.title("Navegação")
st.sidebar.markdown("- **Spotlight**: Coleta e agrupa reclamações e processos- **Explorar**: Faça perguntas sobre os dados carregados")

# OBS: As páginas estarão disponíveis em streamlit_app/pages/
