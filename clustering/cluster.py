from typing import Dict, List
from sklearn.cluster import DBSCAN
import numpy as np


def cluster_texts(
    embeddings: list[list[float]],
    texts: List[str],
    eps: float = 0.3,
    min_samples: int = 5,
) -> Dict[int, List[str]]:
    """
    Agrupa textos em clusters via DBSCAN (distância de cosseno).
    - embeddings: lista de vetores (mesma ordem de `texts`)
    - texts: lista de strings
    - eps: limiar de distância para o DBSCAN
    - min_samples: min. de pontos para formar um cluster

    Retorna um dict mapping cluster_id -> lista de textos.
    rótulo -1 representa "noise" (fora de cluster).
    """
    X = np.array(embeddings)
    db = DBSCAN(metric='cosine', eps=eps, min_samples=min_samples)
    raw_labels = db.fit_predict(X).tolist()
    # remapeia labels originais (ordenados) para novos IDs começando em 1
    unique_raw = sorted(set(raw_labels))
    mapping = {raw: idx + 1 for idx, raw in enumerate(unique_raw)}

    clusters: Dict[int, List[str]] = {}
    for raw_lbl, txt in zip(raw_labels, texts):
        new_lbl = mapping[raw_lbl]
        clusters.setdefault(new_lbl, []).append(txt)
    return clusters