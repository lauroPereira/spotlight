import pandas as pd
import logging
from typing import List
from plugins.base import IngestPlugin
from plugins.schema import PluginResult, Complaint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ProconPlugin(IngestPlugin):
    URL = (
        "http://dados.mj.gov.br/dataset/"
        "8ff7032a-d6db-452b-89f1-d860eb6965ff/resource/"
        "e0c5eaea-ace1-457d-a945-9645644d2783/"
        "download/cnrf2023dadosabertos.xlsx"
    )

    def fetch(self, company: str) -> PluginResult:
        logger.info("🔄 Iniciando download do Excel do PROCON")
        try:
            df = pd.read_excel(self.URL, dtype=str)
            df.columns = df.columns.str.strip()
            total_raw = len(df)
            logger.info("📥 Excel lido com %d linhas", total_raw)
        except Exception as e:
            logger.error("❌ Falha ao baixar/ler PROCON: %s", e, exc_info=True)
            raise RuntimeError(f"Erro ao ler dados do PROCON: {e}")

        complaints: List[Complaint] = []
        try:
            # filtro pelas colunas de razão social
            mask = (
                df['strRazaoSocial'].str.contains(company, case=False, na=False)
                | df['strNomeFantasia'].str.contains(company, case=False, na=False)
                | df['RazaoSocialRFB'].str.contains(company, case=False, na=False)
                | df['NomeFantasiaRFB'].str.contains(company, case=False, na=False)
            )
            filtered = df[mask]
            logger.info("🔎 %d linhas correspondentes à empresa '%s'", len(filtered), company)

            for _, row in filtered.iterrows():
                c = Complaint(
                    date=row.get('DataAbertura', ''),
                    category=row.get('DescricaoAssunto', ''),
                    description=row.get('DescricaoProblema', ''),
                    razao_social=row.get('strRazaoSocial', '')
                )
                complaints.append(c)
        except Exception as e:
            logger.error("❌ Falha ao processar dados do PROCON: %s", e, exc_info=True)
            raise RuntimeError(f"Erro ao processar dados do PROCON: {e}")

        result = PluginResult(
            plugin='PROCON',
            company=company,
            total_raw=total_raw,
            complaints=complaints
        )
        logger.info(
            "🏁 PROCON: total_raw=%d, complaints=%d",
            result.total_raw,
            len(result.complaints)
        )
        return result
