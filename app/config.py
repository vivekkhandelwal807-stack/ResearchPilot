import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

os.environ.pop("GEMINI_API_KEY", None)
os.environ.pop("GOOGLE_API_KEY", None)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "chroma_db"
TOP_K_RESULTS = 4