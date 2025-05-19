import sys, os
from pathlib import Path
import streamlit as st
import logging
import pandas as pd
from plugins.schema import PluginResult

# importa embedding e cluster
from clustering.embedding import embed_texts
from clustering.cluster import cluster_texts

# Ajusta PYTHONPATH para importar plugins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Sidebar já configurada em app.py: lê empresa_cache
empresa = st.session_state.get("empresa_cache", "").strip()
if not empresa:
    st.warning("▶️ Defina a empresa na barra lateral e volte aqui para explorar clusters.")
    st.stop()

st.set_page_config(page_title="🔢 Data Explorer", layout="wide")
st.title(f"🔢 Clusters de Reclamações para: {empresa.upper()}")

# Logger
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("data-explorer")

# --- Helpers ---

def load_records_all(empresa: str) -> pd.DataFrame:
    """
    Carrega todos os PluginResult JSONs para a empresa em DataFrame.
    Campos: source, date, category, description
    """
    rows = []
    for f in Path("data").glob(f"*_{empresa}.json"):
        pr: PluginResult = PluginResult.model_validate_json(f.read_text(encoding="utf-8"))
        for c in pr.complaints:
            rows.append({
                "source": pr.plugin,
                "date": c.date,
                "category": c.category,
                "description": c.description
            })
    return pd.DataFrame(rows)

# Botão de ação
if st.button("🎯 Gerar clusters"):
    df = load_records_all(empresa)
    if df.empty:
        st.error("Nenhum dado disponível para clusterização.")
        st.stop()

    with st.spinner("Gerando embeddings e clusters... 🧠"):
        texts = df["description"].tolist()
        embeddings = embed_texts(texts)
        clusters_map = cluster_texts(embeddings, texts)  # dict[int, List[str]]
        # converte para DataFrame de mapeamento
        mapping = []
        for cid, tlist in clusters_map.items():
            for txt in tlist:
                mapping.append({"description": txt, "cluster": cid})
        map_df = pd.DataFrame(mapping)
        # junta com df original
        df2 = df.merge(map_df, on="description", how="left")

    # gráfico de barras com tamanhos
    cluster_counts = df2["cluster"].value_counts().sort_index()
    st.subheader("📈 Tamanho de cada cluster")
    st.bar_chart(cluster_counts)

    # tabela detalhada
    st.subheader("📝 Reclamações por cluster")
    df2 = df2.sort_values("cluster")[["source", "category", "cluster", "description"]]
    st.dataframe(df2.reset_index(drop=True))
else:
    st.info("Clique em **🎯 Gerar clusters** para iniciar a clusterização.")
