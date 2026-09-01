from pathlib import Path

from app.etl.pipeline import ingest_document
from app.db.database import SessionLocal
from app.db.models import Document


def test_ingest_document_creates_document():
    file_path = "data/raw/employee_handbook.docx"

    ingest_document(file_path)

    db = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.filename == Path(file_path).name)
            .order_by(Document.id.desc())
            .first()
        )

        assert document is not None
        assert document.filename == "employee_handbook.docx"

    finally:
        db.close()