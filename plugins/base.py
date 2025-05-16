from abc import ABC, abstractmethod
from typing import List

class IngestPlugin(ABC):
    @abstractmethod
    def fetch(self, empresa: str) -> List[str]:
        """
        Deve retornar uma lista de textos de reclamações
        para a empresa passada.
        """
        pass
