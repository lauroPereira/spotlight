import streamlit as st
import json
import os
import sys
import subprocess

# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.embedding import embed_texts
from pipeline.vectorstore import store_embeddings
from clustering.cluster import cluster_texts
from utils.text_cleaner import clean_texts

st.set_page_config(page_title="Spotlight", layout="wide")


st.title("🔦 Spotlight - Agrupador de Reclamações com IA")

st.markdown("""
Digite o nome da empresa abaixo e selecione a(s) origem(ns) desejada(s) para coletar reclamações automaticamente. Após isso, execute o Spotlight para visualizar os clusters de reclamações.
""")

empresa = st.text_input("🏢 Nome da empresa a ser analisada:")

st.subheader("📥 Fontes de dados")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("streamlit_app/consumidor_logo.png", width=250)
    if st.button("Consumidor.gov.br", icon="📊"):
        if empresa.strip():
            try:
                resultado = subprocess.run(
                    ["python", "plugins/consumidor_gov.py", empresa],
                    capture_output=True,
                    text=True
                )
                if resultado.returncode == 0:
                    st.success(f"Dados coletados de consumidor.gov.br para '{empresa}'")
                else:
                    st.error(f"Erro ao coletar dados: {resultado.stderr}")
            except Exception as e:
                st.error(f"Falha ao executar o script de ingestão: {e}")
        else:
            st.warning("Digite o nome da empresa antes de coletar dados.")

with col2:
    if st.button("Banco Central (Bacen)"):
        st.info(f"[Simulação] Dados coletados do Bacen para '{empresa}'")

with col3:
    if st.button("Procon/RS"):
        st.info(f"[Simulação] Dados coletados do Procon/RS para '{empresa}'")

# Botão para processar todos os dados coletados
st.markdown("---")
if st.button("🚀 Rodar Spotlight"):
    try:
        base_dir = os.path.join("data")
        all_texts = []
        for fname in os.listdir(base_dir):
            if fname.endswith(".json"):
                with open(os.path.join(base_dir, fname), encoding="utf-8") as f:
                    all_texts.extend(json.load(f))

        texts = clean_texts(all_texts)
        st.success(f"{len(texts)} reclamações carregadas de múltiplas origens.")

        with st.spinner("Gerando embeddings e agrupando..."):
            embeddings = embed_texts(texts)
            store_embeddings(texts, embeddings)
            clusters = cluster_texts(embeddings, texts)

        st.success("Clusterização concluída!")

        for cluster_id, items in clusters.items():
            with st.expander(f"🔹 Cluster {cluster_id} - {len(items)} itens"):
                for item in items:
                    st.markdown(f"- {item}")

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")