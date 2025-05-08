from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from pipeline.vectorstore import get_store
from dotenv import load_dotenv
import os

load_dotenv()

def build_qa_chain():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY não definido no .env")
    
    retriever = get_store().as_retriever()
        
    if retriever is None:
        raise ValueError("Base vetorial não foi inicializada para o QA chain.")
    
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return chain

def ask_question(chain, question):
    return chain.run(question)