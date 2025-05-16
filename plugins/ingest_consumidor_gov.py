import requests
import pandas as pd
import io
import logging
from typing import List
from plugins.base import IngestPlugin
from plugins.schema import PluginResult, Complaint
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ConsumidorGovPlugin(IngestPlugin):
    URL = (
        "https://dados.mj.gov.br/dataset/"
        "0182f1bf-e73d-42b1-ae8c-fa94d9ce9451/resource/"
        "8f22bdc1-3044-46ee-9dd1-4ace84da28e4/"
        "download/basecompleta2025-04.csv"
    )

    def fetch(self, company: str) -> PluginResult:
        logger.info("🔄 Iniciando download do CSV do Consumidor.gov.br")
        try:
            resp = requests.get(self.URL, timeout=60, headers={"User-Agent": "Spotlight/1.0"})
            resp.raise_for_status()
            content = resp.content.decode('utf-8-sig')
            logger.info("✅ Download concluído (tamanho %d bytes)", len(resp.content))
        except Exception as e:
            logger.error("❌ Erro HTTP ao baixar CSV: %s", e, exc_info=True)
            raise RuntimeError(f"Erro HTTP ao baixar dados do Consumidor.gov.br: {e}")

        complaints: List[Complaint] = []
        total_raw = 0
        try:
            df = pd.read_csv(io.StringIO(content), sep=';', dtype=str)
            df.columns = df.columns.str.strip()
            total_raw = len(df)
            logger.info("📥 CSV lido com %d linhas", total_raw)

            # filtra pelo "Nome Fantasia"
            mask = df['Nome Fantasia'].str.contains(company, case=False, na=False)
            filtered = df[mask]
            logger.info("🔎 %d linhas correspondentes à empresa '%s'", len(filtered), company)

            for _, row in filtered.iterrows():
                date_str = row.get('Data Abertura', '').strip()
                # converte DD/MM/YYYY para datetime
                try:
                    date = datetime.strptime(date_str, "%d/%m/%Y")
                except Exception:
                    logger.warning("Formato de data inválido '%s', usando now()", date_str)
                    date = datetime.utcnow()
                    
                c = Complaint(
                    date=date,
                    category=row.get('Assunto', ''),
                    description=row.get('Problema', ''),
                    razao_social=row.get('Nome Fantasia', '')
                )
                complaints.append(c)
        except Exception as e:
            logger.error("❌ Falha ao processar CSV do Consumidor.gov.br: %s", e, exc_info=True)
            raise RuntimeError(f"Erro ao processar CSV do Consumidor.gov.br: {e}")

        result = PluginResult(
            plugin='CONSUMIDOR_GOV',
            company=company,
            total_raw=total_raw,
            complaints=complaints
        )
        logger.info(
            "🏁 Consumidor.gov.br: total_raw=%d, complaints=%d",
            result.total_raw,
            len(result.complaints)
        )
        return result

