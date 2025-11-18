# Two-Doc Checker

AI-powered invoice verification tool that compares invoices against contracts or purchase orders to detect billing discrepancies and mismatches.

## Features

- Multi-format support (PDF, DOCX, TXT)
- LLM-powered analysis via OpenRouter
- OCR fallback for scanned PDFs (Mistral AI)
- Detects 14+ types of billing errors
- Export results as JSON or CSV
- Simple web interface

## Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API key ([get one here](https://openrouter.ai))

### Installation

1. **Clone and install**
```bash
git clone <your-repo>
cd two-doc-checker
pip install -r requirements.txt
```

2. **Configure API keys**
```bash
# Create .env file
echo "LLM_API_KEY=your_openrouter_key" > .env
echo "MISTRAL_API_KEY=your_mistral_key" >> .env  # Optional for OCR
```

3. **Run the backend**
```bash
uvicorn main:app --reload
```

4. **Open the frontend**
```bash
# Open index.html in your browser, or serve with:
python -m http.server 8080
# Then visit: http://localhost:8080
```

## Usage

### Web Interface
1. Upload an invoice file
2. Upload a contract or purchase order
3. Click "Compare"
4. Review findings and export results

### API Endpoint

```bash
curl -X POST http://localhost:8000/compare \
  -F "invoice=@invoice.pdf" \
  -F "governing=@contract.pdf" \
  -F "force=false"
```

**Response:**
```json
{
  "relatedness": {
    "score": 0.85,
    "label": "related",
    "explain": ["PO number matches", "Vendor names align"]
  },
  "governing_doc_type": "po",
  "findings": [
    {
      "code": "TOTAL_OVER_AUTH",
      "type": "monetary",
      "severity": "high",
      "confidence": 0.9,
      "expected": "$10,000",
      "actual": "$12,000",
      "a_excerpt": "Total: $12,000",
      "b_excerpt": "Not to exceed $10,000",
      "a_location": "page 1",
      "b_location": "section 3.2",
      "suggested_resolution": "Verify authorization for additional $2,000"
    }
  ],
  "metadata": {
    "ocr": "none",
    "truncated": false
  }
}
```

## Discrepancy Types

The system detects:
- **Identity**: Document ID, vendor, or customer mismatches
- **Monetary**: Overcharges, unauthorized fees, missing discounts
- **Date**: Out-of-term invoices, billing frequency violations
- **Policy**: Unauthorized taxes, shipping, or line items
- **Structure**: Currency mismatches, unmet milestones

Full list of codes:
`DOC_ID_MISMATCH`, `VENDOR_MISMATCH`, `CUSTOMER_MISMATCH`, `OUT_OF_TERM`, `TOTAL_OVER_AUTH`, `LINE_NOT_IN_AUTH`, `UNIT_RATE_EXCEEDS`, `QTY_EXCEEDS`, `TAX_NOT_ALLOWED`, `SHIPPING_NOT_ALLOWED`, `DISCOUNT_MISSING`, `CURRENCY_MISMATCH`, `MILESTONE_NOT_MET`, `BILLING_FREQUENCY_VIOLATION`

## Project Structure

```
two-doc-checker/
├── backend/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── main.py            # FastAPI app
│   ├── parse.py           # Text extraction
│   ├── ocr.py             # OCR fallback
│   └── llm.py             # LLM integration
├── frontend/
│   ├── index.html         # Web UI
│   ├── app.js             # Client logic
│   └── styles.css         # Styling
├── requirements.txt
├── .env
└── README.md
```

## Configuration

Edit `.env` file:

```env
# Required
LLM_API_KEY=your_openrouter_api_key

# Optional
MISTRAL_API_KEY=your_mistral_api_key  # For OCR
LLM_MODEL=mistralai/mistral-7b-instruct:free
```

Available models: `mistralai/mistral-7b-instruct:free`, `anthropic/claude-3-haiku`, `openai/gpt-4-turbo`, etc.

## Limits

- Max file size: 10 MB
- Max text per document: 120,000 characters
- Supported formats: PDF, DOCX, TXT

## Troubleshooting

**"Couldn't read document text"**
- Ensure PDF isn't password-protected
- Add Mistral API key for scanned PDFs
- Try re-exporting as a new PDF

**CORS errors in browser**
- Backend runs on `localhost:8000`
- Frontend should be on `localhost:8080` or file://
- Check browser console for details

**Empty LLM responses**
- Verify OpenRouter API key is valid
- Check API credits/quota
- Try a different model

## Development

```bash
# Format code
black backend/

# Run with auto-reload
uvicorn main:app --reload --port 8000
```

## License

MIT

## Contributing


Issues and PRs welcome! eb1b0ffaad8242e483dbdc445215c551d9407edf
