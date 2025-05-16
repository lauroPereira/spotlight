from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

store = None

def store_embeddings(texts, embeddings):
    global store
    from langchain.docstore.document import Document
    docs = [Document(page_content=t) for t in texts]
    store = FAISS.from_documents(docs, OpenAIEmbeddings())
    store.save_local("indexes/faiss_index")

def get_store():
    global store
    if store is None:
        try:
            store = FAISS.load_local("indexes/faiss_index", OpenAIEmbeddings())
        except:
            raise ValueError("Índice FAISS não encontrado. Rode o pipeline antes.")
    return store

def query_similar(query, k=5):
    if store is None:
        raise ValueError("Base vetorial ainda não inicializada.")
    results = store.similarity_search(query, k=k)
    return [r.page_content for r in results]