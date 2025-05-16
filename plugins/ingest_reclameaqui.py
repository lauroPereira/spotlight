import requests
from bs4 import BeautifulSoup
from typing import List
from plugins.base import IngestPlugin

class ReclameAquiPlugin(IngestPlugin):
    BASE = "https://www.reclameaqui.com.br/empresa/{slug}/"

    def fetch(self, empresa: str) -> List[str]:
        slug = empresa.lower().replace(" ", "-")
        page = 1
        textos = []
        while True:
            url = self.BASE.format(slug=slug) + f"pagina/{page}/"
            try:
                r = requests.get(url, timeout=20, headers={"User-Agent":"Mozilla/5.0"})
                r.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Erro HTTP no ReclameAQUI (pág. {page}): {e}")
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.select(".complaint-card__text")
            if not cards:
                break
            textos += [c.get_text(strip=True) for c in cards]
            page += 1
        return textos
