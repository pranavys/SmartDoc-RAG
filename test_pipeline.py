from app.etl.pipeline import process_document


file_path = "data/raw/employee_handbook.docx"

chunks = process_document(file_path)

print("===== ETL PIPELINE RESULT =====")
print(f"Number of chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index} ---")
    print(chunk)