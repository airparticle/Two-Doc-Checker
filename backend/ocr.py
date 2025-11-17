import requests


def ocr_pdf_with_mistral(pdf_bytes: bytes, api_key: str) -> str:
    if not api_key or not pdf_bytes:
        return ""
    
    url = "https://api.mistral.ai/v1/chat/completions"  # Updated endpoint
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": ("document.pdf", pdf_bytes, "application/pdf")},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json().get("text", "")
    except Exception:
        return ""
