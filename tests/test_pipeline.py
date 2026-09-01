from app.etl.pipeline import process_document


def test_process_document_returns_chunks():
    file_path = "data/raw/employee_handbook.docx"

    chunks = process_document(file_path)

    assert chunks
    assert isinstance(chunks, list)

    for chunk in chunks:
        assert chunk
        assert isinstance(chunk, str)