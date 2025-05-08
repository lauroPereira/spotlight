from sklearn.cluster import KMeans
import numpy as np

def cluster_texts(embeddings, original_texts, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    clusters = {}
    for label, text in zip(labels, original_texts):
        clusters.setdefault(label, []).append(text)
    return clusters