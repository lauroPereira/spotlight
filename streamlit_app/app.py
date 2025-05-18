import streamlit as st

st.set_page_config(page_title="Spotlight", page_icon="🔦", layout="wide")

# garante que exista
st.session_state.setdefault("empresa_cache", "")

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

    st.markdown("---")
    st.title("🚧 Navegação")
    st.sidebar.markdown(
    "- 🔎 **Discover**: Agrupar reclamações e processos da empresa\n"
    "- 💖 **Mood Explorer**: Analisar sentimento das reclamações\n"
    "- 📊 **Data Explorer**: Visualizar e exportar seus dados\n"
    "- 🤖 **Chat**: Conversar com o agente sobre os dados\n"
    "- 🛠️ **HelpDesk**: Gerenciar atendimento interno ao cliente (CRM, suporte, etc)\n"
)

st.title("🔦 Spotlight – Bem-vindo")
st.write("Escolha uma empresa na barra lateral para começar.")
