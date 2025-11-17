from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import MAX_BYTES, MAX_CHARS, MISTRAL_API_KEY
from .parse import extract_text_from_bytes
from .ocr import ocr_pdf_with_mistral
from .llm import safe_llm_json, RELATEDNESS_SYS, DISCREPANCIES_SYS, relatedness_prompt, discrepancies_prompt

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _cap(s: str) -> tuple[str, bool]:
    """Truncate text to MAX_CHARS if needed."""
    if len(s) <= MAX_CHARS:
        return s, False
    return s[:MAX_CHARS] + "\n\n[TRUNCATED DUE TO LENGTH]\n", True


def _is_pdf(name: str) -> bool:
    """Check if filename is PDF."""
    return name.lower().endswith(".pdf")


@app.post("/compare")
async def compare(
    invoice: UploadFile = File(...),
    governing: UploadFile = File(...),
    force: bool = Form(False)
):
    # Read and validate file sizes
    inv_bytes = await invoice.read()
    gov_bytes = await governing.read()
    if len(inv_bytes) > MAX_BYTES or len(gov_bytes) > MAX_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 10 MB)")
    
    # Extract text
    inv_text = extract_text_from_bytes(invoice.filename, inv_bytes)
    gov_text = extract_text_from_bytes(governing.filename, gov_bytes)
    
    # OCR fallback for empty PDFs
    ocr_used = "none"
    if _is_pdf(invoice.filename) and not inv_text.strip():
        ocr_text = ocr_pdf_with_mistral(inv_bytes, MISTRAL_API_KEY)
        if ocr_text.strip():
            inv_text = ocr_text
            ocr_used = "mistral"
    
    if _is_pdf(governing.filename) and not gov_text.strip():
        ocr_text = ocr_pdf_with_mistral(gov_bytes, MISTRAL_API_KEY)
        if ocr_text.strip():
            gov_text = ocr_text
            ocr_used = "mistral"
    
    # Validate we have text
    if not inv_text.strip() or not gov_text.strip():
        raise HTTPException(status_code=400, detail="Couldn't read document text. Try a different file.")
    
    # Truncate if needed
    inv_text, inv_trunc = _cap(inv_text)
    gov_text, gov_trunc = _cap(gov_text)
    
    # Run relatedness check
    rel = safe_llm_json(RELATEDNESS_SYS, relatedness_prompt(inv_text, gov_text))
    if isinstance(rel, list):  # Normalize unexpected format
        rel = {"score": 0.0, "label": "unrelated", "explain": ["Unexpected format"]}
    
    # Run discrepancies if related or forced
    findings = []
    if rel.get("label") == "related" or force:
        findings = safe_llm_json(DISCREPANCIES_SYS, discrepancies_prompt(inv_text, gov_text))
        if isinstance(findings, dict):  # Normalize
            findings = findings.get("findings", [])
    
    # Infer governing doc type
    gov_type = "po" if "purchase order" in gov_text.lower() else "contract"
    
    return {
        "relatedness": rel,
        "governing_doc_type": gov_type,
        "findings": findings,
        "metadata": {
            "ocr": ocr_used,
            "truncated": inv_trunc or gov_trunc
        }
    }
