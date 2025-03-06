import json
import re
import nltk
from tqdm import tqdm
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Load cleaned text file
with open("sherlock_holmes_cleaned.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split text into sentences
sentences = sent_tokenize(text)

# Initialize chunks
chunk_size = 500  # Approx. word limit per chunk
chunks = []
current_chunk = []
word_count = 0

# Define patterns to detect dialogues, deductions, and narration
dialogue_pattern = r'“[^”]+”'  # Matches text inside quotes
deduction_keywords = ["evidence suggests", "it is elementary", "therefore", "we can deduce", "the suspect"]
narration_keywords = ["he walked", "she ran", "the room was", "the streets were"]

# Process each sentence and categorize
for sentence in tqdm(sentences, desc="Processing text"):
    words = sentence.split()
    word_count += len(words)
    current_chunk.append(sentence)

    # If chunk size limit is reached, classify and store it
    if word_count >= chunk_size:
        chunk_text = " ".join(current_chunk)
        
        # Classify chunk type
        if re.search(dialogue_pattern, chunk_text):
            chunk_type = "dialogue"
        elif any(keyword in chunk_text.lower() for keyword in deduction_keywords):
            chunk_type = "deduction"
        else:
            chunk_type = "narration"

        # Save chunk as structured data
        chunks.append({
            "type": chunk_type,
            "text": chunk_text
        })

        # Reset chunk
        current_chunk = []
        word_count = 0

# Save structured chunks to JSON
with open("sherlock_holmes_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)
