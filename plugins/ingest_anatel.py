# plugins/ingest_anatel.py
import requests, zipfile, tempfile, pandas as pd, logging
from typing import List
from plugins.base import IngestPlugin
from plugins.schema import PluginResult, Complaint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AnatelPlugin(IngestPlugin):
    URL = (
        "https://www.anatel.gov.br/dadosabertos/"
        "paineis_de_dados/consumidor/consumidor_reclamacoes.zip"
    )
    CSV_NAME = "reclamacoes.csv"

    def fetch(self, company: str) -> PluginResult:
        logger.info("🔄 Iniciando download do ZIP da Anatel")
        try:
            resp = requests.get(self.URL, stream=True, timeout=300,
                                headers={"User-Agent": "Spotlight/1.0"})
            resp.raise_for_status()
            size = resp.headers.get("Content-Length", "desconhecido")
            logger.info("✅ Download concluído (%s bytes)", size)
        except Exception as e:
            logger.error("❌ Erro HTTP ao baixar ZIP: %s", e, exc_info=True)
            raise RuntimeError(f"Erro HTTP ao baixar ZIP da Anatel: {e}")

        complaints: List[Complaint] = []
        total_raw = 0

        try:
            with tempfile.TemporaryFile() as tmp:
                for chunk in resp.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp.seek(0)

                with zipfile.ZipFile(tmp) as z:
                    logger.info("📦 Extraindo %s", self.CSV_NAME)
                    with z.open(self.CSV_NAME) as csvfile:
                        reader = pd.read_csv(
                            csvfile,
                            sep=";",
                            encoding="utf-8-sig",
                            dtype=str,
                            chunksize=100_000,
                        )

                        for idx, chunk_df in enumerate(reader, start=1):
                            # Normalize column names: remove BOM + whitespace
                            clean_cols = [c.replace("\ufeff", "").replace("ï»¿", "").strip()
                                           for c in chunk_df.columns]
                            chunk_df.columns = clean_cols

                            total_raw += len(chunk_df)

                            # Dynamic column detection
                            date_col = next((c for c in clean_cols if c.lower().startswith("data")), None)
                            brand_col = next((c for c in clean_cols if c.lower() == "marca"), None)
                            prob_col = next((c for c in clean_cols if c.lower().startswith("problema")), None)

                            if not all([date_col, brand_col, prob_col]):
                                raise RuntimeError(
                                    f"Colunas não encontradas no chunk {idx}: "
                                    f"date={date_col}, brand={brand_col}, prob={prob_col}"
                                )

                            logger.info(
                                "🔎 chunk %d processado: %d linhas brutas; tentando filtro em '%s'",
                                idx, len(chunk_df), brand_col
                            )

                            # Filter complaints by brand
                            mask = chunk_df[brand_col].str.contains(company, case=False, na=False)
                            filtered = chunk_df[mask]

                            logger.info(
                                "   → %d correspondências encontradas em '%s'",
                                len(filtered), brand_col
                            )

                            # Build Complaint objects
                            for _, row in filtered.iterrows():
                                c = Complaint(
                                    date=row[date_col],
                                    category=row[prob_col],
                                    description=row.get("Assunto", ""),
                                    razao_social=row[brand_col]
                                )
                                complaints.append(c)

        except Exception as e:
            logger.error("❌ Falha ao processar ZIP da Anatel: %s", e, exc_info=True)
            raise RuntimeError(f"Erro ao processar ZIP da Anatel: {e}")

        logger.info(
            "🏁 Total de linhas brutas processadas: %d; reclamações extraídas: %d",
            total_raw, len(complaints)
        )

        return PluginResult(
            plugin="ANATEL",
            company=company,
            total_raw=total_raw,
            complaints=complaints,
        )
