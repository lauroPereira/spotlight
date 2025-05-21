import requests, zipfile, tempfile, pandas as pd, logging
from typing import List
from plugins.base import IngestPlugin
from plugins.schema import PluginResult, Complaint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CVMPlugin(IngestPlugin):
    URL = (
      "https://dados.cvm.gov.br/"
      "dados/PROCESSO/SANCIONADOR/DADOS/processo_sancionador.zip"
    )
    CSV_MAIN   = "processo_sancionador.csv"
    CSV_ACC    = "processo_sancionador_acusado.csv"

    def fetch(self, company: str) -> PluginResult:
        logger.info("🔄 Download do ZIP CVM")
        resp = requests.get(self.URL, stream=True, timeout=120,
                            headers={"User-Agent":"Spotlight/1.0"})
        resp.raise_for_status()

        # leitura dos CSVs em memória
        with tempfile.TemporaryFile() as tmp:
            for chunk in resp.iter_content(8192):
                tmp.write(chunk)
            tmp.seek(0)
            with zipfile.ZipFile(tmp) as z:
                # 1) DataFrame principal
                with z.open(self.CSV_MAIN) as f_main:
                    df_proc = pd.read_csv(
                        f_main, sep=";", encoding="latin1", dtype=str,
                        on_bad_lines="warn"
                    )
                # 2) DataFrame de acusados
                with z.open(self.CSV_ACC) as f_acc:
                    df_acc = pd.read_csv(
                        f_acc, sep=";", encoding="latin1", dtype=str,
                        on_bad_lines="warn"
                    )

        # 3) Normalize colunas
        df_proc.columns = [c.replace("\ufeff","").strip() for c in df_proc.columns]
        df_acc.columns  = [c.replace("\ufeff","").strip() for c in df_acc.columns]

        # 4) Merge pelos NUPs
        df = df_proc.merge(df_acc, on="NUP", how="left", suffixes=("","_acusado"))
        total_raw = len(df_proc)

        # 5) Detectar nomes de coluna dinamicamente
        date_col  = next((c for c in df.columns if c.lower().startswith("data_abertura")), None)
        obj_col   = next((c for c in df.columns if c.lower() == "objeto"), None)
        acc_col   = next((c for c in df.columns if c.lower().startswith("nome_acusado")), None)
        ementa_col= next((c for c in df.columns if c.lower() == "ementa"), None)

        if not all([date_col, ementa_col]) or not (acc_col or obj_col):
            raise RuntimeError(
                f"Colunas faltando: date={date_col}, ementa={ementa_col}, "
                f"acusado={acc_col}, objeto={obj_col}"
            )

        # 6) Filtrar por acusado OU objeto
        # força string e substitui NaN por "" para não gerar float
        serie_acc = df.get(acc_col, pd.Series()).fillna("").astype(str)
        serie_obj = df.get(obj_col,  pd.Series()).fillna("").astype(str)
        mask = (
            serie_acc.str.contains(company, case=False, na=False)
            | serie_obj.str.contains(company, case=False, na=False)
        )
        matched = df[mask]
        logger.info("🔎 %d processos encontrados para '%s'", len(matched), company)

        # 7) Construir lista de Complaint
        complaints: List[Complaint] = []
        for _, row in matched.iterrows():
            raw_name = row.get(acc_col) or row.get(obj_col) or ""
            name     = str(raw_name).strip()
            complaints.append(
                Complaint(
                    date        = str(row[date_col]).strip(),
                    category    = str(row.get(obj_col, "") or "").strip(),
                    description = str(row.get(ementa_col, "") or "").strip(),
                    razao_social= name
                )
            )
        logger.info("🏁 linhas brutas: %d; reclamações extraídas: %d",
                    total_raw, len(complaints))

        return PluginResult(
            plugin="CVM",
            company=company,
            total_raw=total_raw,
            complaints=complaints,
        )
