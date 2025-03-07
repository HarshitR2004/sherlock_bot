import json
import chromadb
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Load Sherlock Holmes text data
with open("backend\setup\sherlock_holmes_chunks.json", "r", encoding="utf-8") as f:
    sherlock_data = json.load(f)

# Initialize Sentence Transformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB Persistent Client
chroma_client = chromadb.PersistentClient(path="sherlock_chromadb")
collection = chroma_client.get_or_create_collection(name="sherlock_holmes")

# Ensure data is correctly structured before processing
if not isinstance(sherlock_data, list):
    raise ValueError("Invalid JSON format: Expected a list of dictionaries.")

# Store embeddings in ChromaDB
for i, chunk in enumerate(tqdm(sherlock_data, desc="Processing & Storing Chunks")):
    if "text" not in chunk or "type" not in chunk:
        continue  # Skip invalid data entries
    
    text = chunk["text"]
    embedding = embedding_model.encode(text).tolist() 

    collection.add(
        ids=[f"chunk_{i}"],  
        embeddings=[embedding],  
        metadatas=[{"type": chunk["type"], "text": text}]
    )


print(f"Total documents stored: {collection.count()}")
