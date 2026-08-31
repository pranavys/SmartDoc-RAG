from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_docx(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    return "\n".join(paragraphs)


def extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    return "\n".join(pages)


def extract_document(file_path: str) -> str:
    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".docx":
        return extract_docx(file_path)

    if extension == ".pdf":
        return extract_pdf(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Only PDF and DOCX are supported."
    )