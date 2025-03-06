import json
import chromadb
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Load the structured Sherlock Holmes dataset
with open("sherlock_holmes_chunks.json", "r", encoding="utf-8") as f:
    sherlock_data = json.load(f)

# Initialize the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="sherlock_chromadb")

# Create a new collection in ChromaDB
collection = chroma_client.get_or_create_collection(name="sherlock_holmes")

# Process and store chunks in ChromaDB
for i, chunk in enumerate(tqdm(sherlock_data, desc="Processing & Storing Chunks")):
    text = chunk["text"]
    embedding = embedding_model.encode(text).tolist()  # Convert to list for ChromaDB storage

    # Add to ChromaDB
    collection.add(
        ids=[f"chunk_{i}"],  # Unique ID for each chunk
        embeddings=[embedding],  # Store embedding
        metadatas=[{"type": chunk["type"], "text": text}]  # Store original text as metadata
    )
