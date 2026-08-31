from app.etl.pipeline import ingest_document


file_path = "data/raw/employee_handbook.docx"

ingest_document(file_path)

print("Document ingestion completed successfully!")