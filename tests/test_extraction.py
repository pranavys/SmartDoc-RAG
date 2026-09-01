from app.etl.extractor import extract_document
from app.etl.transformer import clean_text, chunk_text


def test_document_extraction_and_transformation():
    file_path = "data/raw/company_policy.pdf"

    raw_text = extract_document(file_path)

    assert raw_text
    assert isinstance(raw_text, str)

    cleaned_text = clean_text(raw_text)

    assert cleaned_text
    assert isinstance(cleaned_text, str)

    chunks = chunk_text(cleaned_text)

    assert chunks
    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk
        assert isinstance(chunk, str)