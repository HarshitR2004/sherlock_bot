import fitz  # PyMuPDF
import re
from tqdm import tqdm  # Progress bar

# Load PDF
pdf_path = "SherlockHolmesComplete.pdf"  # Change this to your file path
doc = fitz.open(pdf_path)

# Extract text from each page with progress bar
text = ""
for page in tqdm(doc, desc="Extracting pages", unit="page"):
    text += page.get_text("text") + "\n"

# Cleaning: Remove extra whitespace, headers, and footers
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'^\s+|\s+$', '', text)  # Strip leading/trailing spaces
    text = re.sub(r'Page \d+', '', text)  # Remove page numbers
    text = re.sub(r'\b(The Adventures of Sherlock Holmes|Arthur Conan Doyle)\b', '', text, flags=re.IGNORECASE)  # Remove headers
    return text

# Apply cleaning with progress tracking
print("\n🔹 Cleaning text...")
cleaned_text = clean_text(text)

# Save the cleaned text to a file
with open("sherlock_holmes_cleaned.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)
