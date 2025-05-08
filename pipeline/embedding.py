from langchain_openai import OpenAIEmbeddings
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

def embed_texts(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não definido no .env")
    
    embedder = OpenAIEmbeddings(openai_api_key=api_key)
    return embedder.embed_documents(texts)