import fitz  
import re
from tqdm import tqdm  

# Load PDF
pdf_path = "setup\SherlockHolmesComplete.pdf" 
doc = fitz.open(pdf_path)


text = ""
for page in tqdm(doc, desc="Extracting pages", unit="page"):
    text += page.get_text("text") + "\n"

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'^\s+|\s+$', '', text)  # Strip leading/trailing spaces
    text = re.sub(r'Page \d+', '', text)  # Remove page numbers
    text = re.sub(r'\b(The Adventures of Sherlock Holmes|Arthur Conan Doyle)\b', '', text, flags=re.IGNORECASE)  # Remove headers
    return text

cleaned_text = clean_text(text)

with open("sherlock_holmes_cleaned.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)
