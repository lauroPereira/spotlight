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
    "- 😠 **Mood Explorer**: Analisar sentimento das reclamações\n"
    "- 📊 **Data Explorer**: Visualizar e exportar seus dados\n"
    "- 🤖 **Chat**: Conversar com o agente sobre os dados\n"
    "- 🛠️ **HelpDesk**: Gerenciar atendimento interno ao cliente (CRM, suporte, etc)\n"
)

st.title("🔦 Spotlight – Seja muito bem-vindo!")
st.markdown("O 🔦 **Spotlight** está aqui para ajudar você a entender o que realmente importa nas reclamações e processos de clientes. Siga estes passos para tirar o máximo proveito:\n")
st.markdown("1. **Escolha sua empresa**  \nNo menu à esquerda, digite o nome da empresa que deseja investigar e clique em **“🚀 Definir Empresa”**. Este passo garante que todas as páginas do app vão trabalhar com essa mesma empresa, sem confusão.\n")
st.markdown("2. **🔎 Discover**  \nAqui você coleta e agrupa todas as reclamações e processos públicos sobre a empresa em questão. Clique em **“🔄 Atualizar”** em cada card para buscar os dados mais recentes — os totais e agrupamentos aparecerão imediatamente!\n")
st.markdown("3. **💖 Mood Explorer**  \nQuer saber como os clientes estão se sentindo? Vá para a aba **Mood Explorer** para rodar uma análise de sentimento e descobrir quais tópicos geram mais frustração (ou elogios!).\n")
st.markdown("4. **📊 Data Explorer**  \nPrecisa de relatórios ou planilhas? Na aba **Data Explorer** você visualiza tabelas interativas, filtra por categorias e pode exportar CSV para compartilhar com o time.\n")
st.markdown("5. **🤖 Chat**  \nTem uma pergunta específica? Use o **Chat** para conversar de forma natural com nosso agente de IA. É só digitar sua dúvida e descobrir insights instantâneos a partir dos dados carregados.\n")
st.markdown("6. **🛠️ HelpDesk**  \nSe o seu time de suporte utiliza CRM ou outro sistema interno, acesse **HelpDesk** para registrar e acompanhar o atendimento ao cliente de forma integrada.\n")
st.markdown("---\n")
st.markdown("**Dica de ouro:**  \n Defina a empresa **uma única vez** na sidebar e navegue entre as páginas sem precisar digitar de novo. Seu trabalho flui de forma contínua, do garimpo de dados até a operação do dia a dia.  \n Pronto para brilhar a lanterna no universo das reclamações? Vamos nessa! 🚀")
