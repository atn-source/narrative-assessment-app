import os
from docx import Document
from pypdf import PdfReader
from pathlib import Path

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text(file_path: str) -> str:
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".docx":
        return extract_text_from_docx(file_path)
    elif file_ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Use .docx or .pdf")

def get_file_size_mb(file_path: str) -> float:
    return os.path.getsize(file_path) / (1024 * 1024)
