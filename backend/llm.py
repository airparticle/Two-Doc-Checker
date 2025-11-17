import json
from typing import Union
from .config import LLM_API_KEY, LLM_MODEL, LLM_TIMEOUT, RETRY_ON_INVALID_JSON
import openai


# Initialize client once
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=LLM_API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Two-Doc Checker",
    }
)


def call_llm_json(system_prompt: str, user_prompt: str) -> Union[dict, list]:
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            timeout=LLM_TIMEOUT,
            max_tokens=4000,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        if not content or not content.strip():
            raise ValueError("Empty response from model")
        
        # Clean markdown fences
        content = content.strip()
        if content.startswith("```"):
            content = content.removeprefix("```json").removeprefix("```")
            content = content.removesuffix("```").strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"LLM error: {e}")
        raise


def safe_llm_json(system_prompt: str, user_prompt: str):
    last_err = None
    for _ in range(RETRY_ON_INVALID_JSON + 1):
        try:
            return call_llm_json(system_prompt, user_prompt)
        except Exception as e:
            last_err = e
    raise last_err


# System prompts
RELATEDNESS_SYS = """You are a verifier for business documents. Decide whether an INVOICE matches a governing CONTRACT or PURCHASE ORDER.
Use ONLY the provided full texts. Output a JSON object with:
- score (0..1),
- label: "related" (>=0.6), "possibly_related" (0.4-0.59), or "unrelated" (<0.4),
- explain: an array of short reasons (e.g., "PO number matches", "vendor names align", "period overlaps").
Return ONLY valid JSON."""

DISCREPANCIES_SYS = """Compare a full INVOICE against its governing CONTRACT or PURCHASE ORDER and output ONLY material billing discrepancies as a JSON array.
Allowed codes:
DOC_ID_MISMATCH, VENDOR_MISMATCH, CUSTOMER_MISMATCH, OUT_OF_TERM, TOTAL_OVER_AUTH,
LINE_NOT_IN_AUTH, UNIT_RATE_EXCEEDS, QTY_EXCEEDS, TAX_NOT_ALLOWED, SHIPPING_NOT_ALLOWED,
DISCOUNT_MISSING, CURRENCY_MISMATCH, MILESTONE_NOT_MET, BILLING_FREQUENCY_VIOLATION.
Each finding object must have:
- code, type ("monetary"|"identity"|"date"|"policy"|"structure"), severity ("high"|"medium"|"low"), confidence (0..1),
- expected, actual,
- a_excerpt (<=160 chars), b_excerpt (<=160 chars),
- a_location, b_location,
- suggested_resolution.
If no issues, return [].
Return ONLY a JSON array."""


def relatedness_prompt(inv_text: str, gov_text: str) -> str:
    return f"""INVOICE (full text):
<<<
{inv_text}
>>>
GOVERNING DOC (full text: contract or PO):
<<<
{gov_text}
>>>"""


def discrepancies_prompt(inv_text: str, gov_text: str) -> str:
    return f"""INVOICE (full text):
<<<
{inv_text}
>>>
GOVERNING DOC (full text: contract or PO):
<<<
{gov_text}
>>>"""
