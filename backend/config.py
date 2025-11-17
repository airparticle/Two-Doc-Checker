import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free")

# Limits
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_CHARS = 120_000
LLM_TIMEOUT = 30
RETRY_ON_INVALID_JSON = 1
