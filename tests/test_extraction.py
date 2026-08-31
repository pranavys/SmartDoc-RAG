from app.etl.extractor import extract_document
from app.etl.transformer import clean_text, chunk_text


file_path = "data/raw/company_policy.pdf"

raw_text = extract_document(file_path)

print("===== RAW TEXT =====")
print(raw_text)

cleaned_text = clean_text(raw_text)

print("\n===== CLEANED TEXT =====")
print(cleaned_text)

chunks = chunk_text(cleaned_text)

print("\n===== CHUNKS =====")

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index} ---")
    print(chunk)