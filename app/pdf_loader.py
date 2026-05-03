from pathlib import Path

from pypdf import PdfReader

from app import config


def validate_pdf_path(pdf_path: str | Path) -> Path:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.is_file():
        raise FileNotFoundError(f"PDF path is not a file: {path}")

    return path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    path = validate_pdf_path(pdf_path)

    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF: {path}") from exc

    text = normalize_text(text)

    if not text:
        raise ValueError(f"PDF has no extractable text: {path}")

    return text


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def split_text_into_chunks(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[str]:
    chunk_size = chunk_size if chunk_size is not None else config.CHUNK_SIZE
    chunk_overlap = chunk_overlap if chunk_overlap is not None else config.CHUNK_OVERLAP

    if not text:
        raise ValueError("Text cannot be empty")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def load_pdf_chunks(pdf_path: str | Path | None = None) -> list[str]:
    text = extract_text_from_pdf(pdf_path or config.PDF_PATH)
    return split_text_into_chunks(text)
