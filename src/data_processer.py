
import os
import torch
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import RAW_DATA_PATH, VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME

def build_vector_store():
    loader = DirectoryLoader(RAW_DATA_PATH, glob="**/*.txt", show_progress=True)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={'device': device})
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(VECTOR_STORE_PATH)
if __name__ == "__main__":
    build_vector_store()
