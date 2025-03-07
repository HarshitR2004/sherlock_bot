import json
import chromadb
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

with open("sherlock_holmes_chunks.json", "r", encoding="utf-8") as f:
    sherlock_data = json.load(f)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="sherlock_chromadb")

collection = chroma_client.get_or_create_collection(name="sherlock_holmes")

for i, chunk in enumerate(tqdm(sherlock_data, desc="Processing & Storing Chunks")):
    text = chunk["text"]
    embedding = embedding_model.encode(text).tolist() 

    collection.add(
        ids=[f"chunk_{i}"],  
        embeddings=[embedding],  
        metadatas=[{"type": chunk["type"], "text": text}]  
    )
