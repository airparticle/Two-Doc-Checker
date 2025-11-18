# Two-Doc Checker

AI-powered invoice verification tool that compares invoices against contracts or purchase orders to detect billing discrepancies and mismatches.

## Features

- Multi-format support (PDF, DOCX, TXT)
- LLM-powered analysis via OpenRouter
- OCR fallback for scanned PDFs (Mistral AI)
- Detects 14+ types of billing errors
- Export results as JSON or CSV
- Simple web interface

## Prerequisites

Before installing, make sure you have:
- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** ([Download here](https://git-scm.com/downloads))
- **OpenRouter API key** (free - [get one here](https://openrouter.ai))

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/airparticle/Two-Doc-Checker.git
cd Two-Doc-Checker
```

### Step 2: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get errors**, try upgrading pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure API Keys

Create a `.env` file in the project root:

**Windows:**
```bash
copy NUL .env
notepad .env
```

**Mac/Linux:**
```bash
touch .env
nano .env
```

Add these lines to `.env`:
```env
LLM_API_KEY=your_openrouter_api_key_here
MISTRAL_API_KEY=your_mistral_key_here
```

**Required:**
- `LLM_API_KEY` - Get from [openrouter.ai](https://openrouter.ai) (free tier available)

**Optional:**
- `MISTRAL_API_KEY` - Only needed for OCR of scanned PDFs ([mistral.ai](https://mistral.ai))

Save and close the file.

### Step 5: Start the Backend

```bash
cd backend
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal open!

### Step 6: Open the Frontend

Open a **new terminal** and run:

**Option A - Simple (double-click):**
- Just open `frontend/index.html` in your browser

**Option B - Local server (recommended):**
```bash
cd frontend
python -m http.server 8080
```

Then visit: [http://localhost:8080](http://localhost:8080)

## Quick Test

1. Go to http://localhost:8080
2. Upload any two documents
3. Click "Compare"
4. You should see results!

## Troubleshooting

### "Python not found"
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installing

### "pip not found"
```bash
python -m ensurepip --upgrade
```

### "uvicorn not found"
Make sure your virtual environment is activated (you should see `(venv)` in terminal):
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### "Module not found" errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### CORS errors in browser
- Backend must be running on `http://localhost:8000`
- Frontend should be on `http://localhost:8080` or opened directly
- Check that both terminals are running

### "Empty response from model"
- Verify your OpenRouter API key is correct in `.env`
- Check you have API credits at [openrouter.ai](https://openrouter.ai)
- Try a different model by editing `.env`:
  ```env
  LLM_MODEL=openai/gpt-3.5-turbo
  ```

### "Couldn't read document text"
- Ensure PDFs aren't password-protected
- Try re-exporting the document as a new PDF
- For scanned PDFs, add a Mistral API key for OCR

## Usage

### Web Interface
1. Upload an invoice file (PDF, DOCX, or TXT)
2. Upload a contract or purchase order
3. Click "Compare"
4. Review findings and export results

### API Usage

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
  "findings": [...]
}
```

## Discrepancy Types

The system detects:
- **Identity**: `DOC_ID_MISMATCH`, `VENDOR_MISMATCH`, `CUSTOMER_MISMATCH`
- **Monetary**: `TOTAL_OVER_AUTH`, `UNIT_RATE_EXCEEDS`, `QTY_EXCEEDS`, `DISCOUNT_MISSING`
- **Date**: `OUT_OF_TERM`, `BILLING_FREQUENCY_VIOLATION`
- **Policy**: `TAX_NOT_ALLOWED`, `SHIPPING_NOT_ALLOWED`, `LINE_NOT_IN_AUTH`
- **Structure**: `CURRENCY_MISMATCH`, `MILESTONE_NOT_MET`

## Project Structure

```
Two-Doc-Checker/
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
├── .env                   # Your API keys (not in git)
├── .gitignore
└── README.md
```

## Configuration Options

Edit `.env` to customize:

```env
# Required
LLM_API_KEY=your_key

# Optional
MISTRAL_API_KEY=your_key
LLM_MODEL=mistralai/mistral-7b-instruct:free
```

**Available Models:**
- `mistralai/mistral-7b-instruct:free` (free)
- `anthropic/claude-3-haiku` (fast, cheap)
- `openai/gpt-3.5-turbo` (reliable)
- `openai/gpt-4-turbo` (best quality)

See all models at [openrouter.ai/models](https://openrouter.ai/models)

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
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run with auto-reload
cd backend
uvicorn main:app --reload

# Format code (optional)
pip install black
black backend/
```

## License

MIT

## Contributing

Issues and PRs welcome!

## Support

Having issues? 
1. Check the Troubleshooting section above
2. Open an issue on GitHub
3. Make sure both backend and frontend are running