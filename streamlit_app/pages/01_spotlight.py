import sys, os
# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

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
    for _, name, _ in pkgutil.iter_modules(["../plugins"]):
        if name.startswith("ingest_"):
            module = importlib.import_module(f"plugins.{name}")
            for obj in vars(module).values():
                if isinstance(obj, type) and issubclass(obj, IngestPlugin) and obj is not IngestPlugin:
                    plugins[name] = obj()
    return plugins


def path_for(plugin_key: str, empresa: str) -> Path:
    return Path("../data") / f"{plugin_key}_{empresa}.json"


def load_result(plugin_key: str, empresa: str):
    file = path_for(plugin_key, empresa)
    if not file.exists():
        return None
    try:
        return PluginResult.model_validate_json(file.read_text(encoding="utf-8"))
    except Exception:
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Spotlight – Reclamações", layout="wide")

# Initialize detail selection state
st.session_state.setdefault("detail_selected", None)

# Empresa input e botão Investigar
empresa = st.text_input("🏢 Nome da empresa", key="empresa_input")
if st.button("🔦 Investigar", key="investigar_empresa"):
    st.session_state["detail_selected"] = None
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
    st.session_state.setdefault(f"loading_{key}", False)

# Render cards
cols = st.columns(min(len(plugins), 3), gap="large")
for idx, (key, plugin) in enumerate(plugins.items()):
    label = key.replace("ingest_", "").upper()
    col = cols[idx % len(cols)]
    with col:
        st.markdown(f"### {label}")
        
        # Load existing data
        result = load_result(key, empresa)
        # Placeholder for metrics
        metrics_area = st.empty()
        
        # Initial render of metrics
        if result:
            metrics_area.markdown(
                f"**Total de reclamações analisadas:** {result.total_raw}\n\n"
                f"Reclamações para a empresa: {len(result.complaints)}"
            )
            st.markdown("**Reclamações por marca:**")
            for brand, qty in Counter(c.raw_brand for c in result.complaints).most_common():
                st.markdown(f"- {brand}: {qty}")
        else:
            metrics_area.markdown("*Nenhum dado disponível.*")

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
                    # Update metrics inline after fetch
                    metrics_area.markdown(
                        f"**Total de reclamações analisadas:** {pr.total_raw}\n\n"
                        f"Reclamações para a empresa: {len(pr.complaints)}"
                    )
                except Exception as e:
                    st.session_state[f"loading_{key}"] = False
                    msg.warning(f"Falha em {label}: {e}")

        # Handle detail toggle
        if detail_btn:
            st.session_state["detail_selected"] = None if st.session_state["detail_selected"] == key else key

# Detail section
if st.session_state["detail_selected"]:
    sel = st.session_state["detail_selected"]
    label = sel.replace("ingest_", "").upper()
    st.markdown("---")
    st.subheader(f"Detalhamento de {label}")
    res = load_result(sel, empresa)
    if res:
        for cat, qty in Counter(c.category for c in res.complaints).most_common():
            st.markdown(f"- {cat}: {qty}")
    else:
        st.markdown("*Nenhum dado detalhado disponível.*")
