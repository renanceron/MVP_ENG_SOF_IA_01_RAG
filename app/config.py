import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
PDF_PATH = Path("data/faq_capes.pdf")
TOP_K = 3
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
