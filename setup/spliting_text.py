import json
import re
import nltk
from tqdm import tqdm
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

with open("setup\sherlock_holmes_cleaned.txt", "r", encoding="utf-8") as f:
    text = f.read()

sentences = sent_tokenize(text)

chunk_size = 500  # word limit per chunk
chunks = []
current_chunk = []
word_count = 0

dialogue_pattern = r'“[^”]+”'  
deduction_keywords = ["evidence suggests", "it is elementary", "therefore", "we can deduce", "the suspect"]
narration_keywords = ["he walked", "she ran", "the room was", "the streets were"]

for sentence in tqdm(sentences, desc="Processing text"):
    words = sentence.split()
    word_count += len(words)
    current_chunk.append(sentence)

    if word_count >= chunk_size:
        chunk_text = " ".join(current_chunk)
        
        # Classify chunk type
        if re.search(dialogue_pattern, chunk_text):
            chunk_type = "dialogue"
        elif any(keyword in chunk_text.lower() for keyword in deduction_keywords):
            chunk_type = "deduction"
        else:
            chunk_type = "narration"

        chunks.append({
            "type": chunk_type,
            "text": chunk_text
        })

        current_chunk = []
        word_count = 0

with open("sherlock_holmes_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)
