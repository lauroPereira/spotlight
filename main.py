from pipeline.embedding import embed_texts
from pipeline.vectorstore import store_embeddings, query_similar
from pipeline.qa_chain import build_qa_chain, ask_question
from clustering.cluster import cluster_texts
from utils.text_cleaner import clean_texts
import json

if __name__ == "__main__":
    # Carregar dados de exemplo (reclamações genéricas)
    with open("data/sample_complaints.json", "r") as f:
        raw_texts = json.load(f)

    texts = clean_texts(raw_texts)
    embeddings = embed_texts(texts)
    store_embeddings(texts, embeddings)

    # Buscar similaridade semântica
    similar = query_similar("Problema com fatura em débito automático", k=5)
    print("Reclamações similares:")
    for s in similar:
        print("-", s)

    # Agrupar por similaridade
    clusters = cluster_texts(embeddings, texts)
    print("Clusters identificados:")
    for cluster, items in clusters.items():
        print(f"Cluster {cluster}:")
        for item in items:
            print(" •", item)

    # Consulta via LLM
    chain = build_qa_chain()
    resposta = ask_question(chain, "Quais são os principais temas de reclamações?")
    print("Resposta gerada pela IA:", resposta)
