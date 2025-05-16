import sys, os
# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import importlib, pkgutil, logging
from pathlib import Path
from collections import Counter
from plugins.schema import PluginResult
from plugins.base import IngestPlugin

# configura logger para plugins
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("front-end")

# --- Helpers ---
def load_plugins() -> dict[str, IngestPlugin]:
    plugins = {}
    for _, name, _ in pkgutil.iter_modules(["plugins"]):
        if name.startswith("ingest_"):
            module = importlib.import_module(f"plugins.{name}")
            for obj in vars(module).values():
                if isinstance(obj, type) and issubclass(obj, IngestPlugin) and obj is not IngestPlugin:
                    plugins[name] = obj()
    return plugins


def path_for(plugin_key: str, empresa: str) -> Path:
    return Path("data") / f"{plugin_key}_{empresa}.json"


def load_result(plugin_key: str, empresa: str):
    file = path_for(plugin_key, empresa)
    if not file.exists():
        return None
    try:
        result = PluginResult.model_validate_json(file.read_text(encoding="utf-8"))
        return result
    except Exception:
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Spotlight – Reclamações", layout="wide")

# Initialize detail selection state
if "detail_selected" not in st.session_state:
    st.session_state["detail_selected"] = None

# Empresa input e botão Investigar
empresa = st.text_input("🏢 Nome da empresa", key="empresa_input")

if st.button("🔦 Investigar", key="investigar_empresa"):
    st.session_state.detail_selected = None
    st.rerun()

if not empresa:
    st.info("Preencha o nome da empresa para iniciar.")
    st.stop()
else:
    st.markdown(f"**Investigando as reclamações/processos da empresa:** **{empresa.strip().upper()}**")

plugins = load_plugins()
if not plugins:
    st.error("Nenhum plugin encontrado.")
    st.stop()

# Prepare session state flags
for key in plugins:
    if f"loading_{key}" not in st.session_state:
        st.session_state[f"loading_{key}"] = False

# Render cards
cols = st.columns(min(len(plugins), 3), gap="large")
for idx, (key, plugin) in enumerate(plugins.items()):
    label = key.replace("ingest_", "").upper()
    col = cols[idx % len(cols)]
    with col:
        card = st.container()
        with card:
            # Card title
            st.markdown(f"<h3>{label}</h3>", unsafe_allow_html=True)
            result = load_result(key, empresa)
            # Metrics section
            if result:
                st.markdown(f"**Total de reclamações analisadas:** {result.total_raw}")
                st.markdown(f"**Reclamações para a empresa:** {len(result.complaints)}")
                brand_counts = Counter(c.raw_brand for c in result.complaints)
                st.markdown("**Reclamações por marca:**")
                for b, q in brand_counts.most_common(): st.markdown(f"- {b}: {q}")
            else:
                st.markdown("*Nenhum dado disponível.*")

            # Buttons side by side
            b1, b2 = st.columns([1,1])
            with b1:
                update_btn = st.button("🔄 Atualizar", key=f"btn_{key}")
            with b2:
                detail_btn = st.button("ℹ️ Detalhes", key=f"info_{key}")

            # Messages container
            msg = st.empty()

            # Handle update
            if update_btn:
                st.session_state[f"loading_{key}"] = True
            if st.session_state[f"loading_{key}"]:
                with st.spinner(f"Atualizando {label}..."):
                    try:
                        pr = plugin.fetch(empresa)
                        path = path_for(key, empresa)
                        path.parent.mkdir(exist_ok=True)
                        path.write_text(pr.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
                        st.session_state[f"loading_{key}"] = False
                        msg.success(f"{len(pr.complaints)} reclamações coletadas de {label}.")
                        # Force rerender metrics
                        st.rerun()
                    except Exception as e:
                        st.session_state[f"loading_{key}"] = False
                        msg.warning(f"Falha em {label}: {e}")

            # Handle detail toggle
            if detail_btn:
                st.session_state.detail_selected = None if st.session_state.detail_selected == key else key

# Detail section
if st.session_state.detail_selected:
    sel = st.session_state.detail_selected
    label = sel.replace("ingest_", "").upper()
    st.markdown("---")
    st.subheader(f"Detalhamento de {label}")
    res = load_result(sel, empresa)
    if res:
        cat_counts = Counter(c.category for c in res.complaints)
        for cat, q in cat_counts.most_common(): st.markdown(f"- {cat}: {q}")
    else:
        st.markdown("*Nenhum dado detalhado disponível.*")
