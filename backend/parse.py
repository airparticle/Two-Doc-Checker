import io
from pypdf import PdfReader
from docx import Document


def extract_text_from_bytes(filename: str, b: bytes) -> str:
    name = filename.lower()
    
    try:
        if name.endswith(".txt"):
            return b.decode("utf-8", errors="ignore")
        
        if name.endswith(".docx"):
            doc = Document(io.BytesIO(b))
            return "\n".join(p.text for p in doc.paragraphs)
        
        if name.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(b))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception:
        pass
    
    return ""
