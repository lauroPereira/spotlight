import sys, os
# Evita file watcher do Streamlit tentar acessar torch._classes
import torch
from pathlib import Path
import streamlit as st

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

import logging
import pandas as pd
from collections import Counter
from plugins.schema import PluginResult

# Ajusta PYTHONPATH para importar plugins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_icon="🔦", page_title="Spotlight – Análise de sentimentos", layout="wide")
st.title(f"Analise de sentimentos das reclamações de {st.session_state.get('empresa_cache','N/D').upper()}")

# Configura a barra lateral com o nome da empresa
st.session_state.setdefault("empresa_cache", "")
with st.sidebar:
    st.sidebar.title("🔦 Spotlight")
    st.sidebar.markdown(
        "Coleta e agrupa reclamações e processos de empresas. "
        "Escolha uma empresa na barra lateral para começar."
    )
    st.header("⚙️ Parâmetros")
    empresa = st.text_input(
        "🏢 Empresa", 
        value=st.session_state["empresa_cache"], 
        key="empresa_sidebar",
        disabled=True
        
    )
     # 👉 Bullet sempre visível informando a empresa selecionada
    if st.session_state["empresa_cache"]:
        st.markdown(f"- **Empresa selecionada:** {st.session_state['empresa_cache']}")
        
    st.button("🚀 Definir Empresa", disabled=True)
        
# configura logger para plugins
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT)
logger = logging.getLogger("mood-explorer")

# --- Helpers ---

def load_records(empresa: str) -> pd.DataFrame:
    """
    Carrega reclamações/processos JSON para a empresa e retorna DataFrame.
    Campos: source, date, category, description
    """
    data_dir = Path("data")
    rows = []
    for f in data_dir.glob(f"*_{empresa}.json"):
        pr: PluginResult = PluginResult.model_validate_json(f.read_text(encoding="utf-8"))
        for c in pr.complaints:
            rows.append({
                "source": pr.plugin,
                "date": c.date,
                "category": c.category,
                "description": c.description
            })
    return pd.DataFrame(rows)

@st.cache_resource(show_spinner=False)
def load_sentiment_model():
    """
    Carrega pipeline de sentiment-analysis multilingue (inclui PT).
    Modelo: nlptown/bert-base-multilingual-uncased-sentiment
    """
    # Hugging Face pipeline para análise de sentimento em PT
    from transformers import pipeline
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

@st.cache_data(show_spinner=False)
def analyze_sentiment(_sentiment_model, text: str) -> str:
    """Classifica texto em Positive/Neutral/Negative via Hugging Face."""
    # Limita texto para o modelo (>=512 tokens pode quebrar)
    truncated = text[:512]
    out = _sentiment_model(truncated)[0]
    # rótulos: '1 star', ..., '5 stars'
    label = out.get("label", "3 stars")
    try:
        stars = int(label.split()[0])
    except:
        stars = 3
    if stars <= 2:
        return "Negative"
    elif stars == 3:
        return "Neutral"
    else:
        return "Positive"

        
# Carrega dados
empresa = st.session_state.get("empresa_cache", "").strip()
if not empresa:
    st.warning("▶️ Defina a empresa na sidebar para analisar sentimentos.")
    st.stop()

df = load_records(empresa)
if df.empty:
    st.error("Nenhum dado encontrado para análise de sentimentos.")
    st.stop()

# Botão de ação
_sentiment_model = load_sentiment_model()
if st.button("🔍 Identificar Sentimentos"):
    with st.spinner("Classificando sentimentos... 🧠"):
        df["sentiment"] = df["description"].apply(lambda txt: analyze_sentiment(_sentiment_model, txt))
        st.session_state["mood_df"] = df

# Verifica ausência de categoria
if "mood_df" in st.session_state:
    dff = st.session_state["mood_df"]
    null_cat = dff[dff["category"].isna() | (dff["category"] == "")]
    if not null_cat.empty:
        st.warning(f"Existem {len(null_cat)} reclamações sem categoria definida.")

    # Escolher origem(s)
    sources = sorted(dff["source"].unique())
    sel = st.multiselect("Origens para exibir:", sources, default=sources)
    filt = dff[dff["source"].isin(sel)]

    # Visão geral por categoria
    st.header("📊 Panorama Geral por Categoria")
    pivot = dff.pivot_table(
        index=["category","source"],
        columns="sentiment",
        values="description",
        aggfunc="count",
        fill_value=0,
    )
    st.dataframe(pivot)
    
    st.markdown("---")
    
    # Agrupa por source e category
    for src in sel:
        st.subheader(f"📑 Origem: {src}")
        grp = filt[filt["source"] == src]
        table = (grp.groupby(["category", "sentiment"]).size().reset_index(name="count"))
        # calcula percentuais por categoria
        pct = table.copy()
        table["pct"] = 100 * table["count"] / table.groupby("category")["count"].transform("sum")
        st.dataframe(pct)

else:
    st.info("Clique em **🔍 Identificar Sentimentos** para começar.")
