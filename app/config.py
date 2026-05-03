import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
PDF_PATH = Path("data/faq_capes.pdf")
FAISS_INDEX_DIR = Path("faiss_index")
TOP_K = 5
CHUNK_SIZE = 700
CHUNK_OVERLAP = 180
TEMPERATURE = 0.2
