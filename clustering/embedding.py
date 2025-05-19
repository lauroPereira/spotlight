from sentence_transformers import SentenceTransformer

# mantém o modelo carregado em cache
_model = None

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Gera embeddings para uma lista de textos usando SentenceTransformer.
    Retorna uma lista de vetores.
    """
    global _model
    if _model is None:
        # modelo leve e eficiente
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    # encode retorna numpy.ndarray
    embs = _model.encode(texts, show_progress_bar=False)
    # converte para lista de listas para compatibilidade
    return embs.tolist()