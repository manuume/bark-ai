
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

RAW_DATA_PATH = ROOT_DIR / "data" / "raw_data"
VECTOR_STORE_PATH = ROOT_DIR / "data" / "vector_store"
ASSETS_PATH = ROOT_DIR / "src" / "assets" 

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama3-8b-8192"
