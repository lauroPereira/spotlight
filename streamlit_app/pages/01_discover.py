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
logger = logging.getLogger("discovery-page")
st.set_page_config(page_title="Spotlight", page_icon="🔎", layout="wide")

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
        return PluginResult.model_validate_json(file.read_text(encoding="utf-8"))
    except Exception:
        return None

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
    st.title(f"🔎 Encontre reclamações de **{empresa.upper()}**")


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