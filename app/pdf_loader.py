import re
from pathlib import Path

from pypdf import PdfReader

from app import config


QUESTION_PATTERN = re.compile(r"(?<!\S)(\d{1,2})\.\s+.{1,220}?\?")


def resolve_chunk_settings(
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> tuple[int, int]:
    resolved_size = chunk_size if chunk_size is not None else config.CHUNK_SIZE
    resolved_overlap = (
        chunk_overlap if chunk_overlap is not None else config.CHUNK_OVERLAP
    )

    if resolved_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if resolved_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if resolved_overlap >= resolved_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    return resolved_size, resolved_overlap


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


def find_question_cursors(text: str) -> list[int]:
    return [match.start() for match in QUESTION_PATTERN.finditer(text)]


def split_text_into_question_answer_blocks(text: str) -> list[str]:
    cursors = find_question_cursors(text)

    if not cursors:
        return []

    blocks = []

    for index, cursor in enumerate(cursors):
        next_cursor = cursors[index + 1] if index + 1 < len(cursors) else len(text)
        block = text[cursor:next_cursor].strip()

        if block:
            blocks.append(block)

    return blocks


def split_blocks_into_chunks(
    blocks: list[str],
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    chunks = []
    current_blocks: list[str] = []
    current_size = 0

    for block in blocks:
        block_size = len(block)

        if block_size > chunk_size:
            if current_blocks:
                chunks.append(" ".join(current_blocks).strip())
                current_blocks = []
                current_size = 0

            chunks.extend(split_text_into_chunks(block, chunk_size, chunk_overlap))
            continue

        next_size = current_size + block_size + (1 if current_blocks else 0)

        if current_blocks and next_size > chunk_size:
            chunks.append(" ".join(current_blocks).strip())
            current_blocks = [block]
            current_size = block_size
            continue

        current_blocks.append(block)
        current_size = next_size

    if current_blocks:
        chunks.append(" ".join(current_blocks).strip())

    return chunks


def split_text_into_chunks(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[str]:
    if not text:
        raise ValueError("Text cannot be empty")

    resolved_size, resolved_overlap = resolve_chunk_settings(chunk_size, chunk_overlap)

    chunks = []
    start = 0

    while start < len(text):
        end = start + resolved_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += resolved_size - resolved_overlap

    return chunks


def split_text_into_semantic_chunks(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[str]:
    if not text:
        raise ValueError("Text cannot be empty")

    resolved_size, resolved_overlap = resolve_chunk_settings(chunk_size, chunk_overlap)

    blocks = split_text_into_question_answer_blocks(text)

    if not blocks:
        return split_text_into_chunks(text, resolved_size, resolved_overlap)

    return split_blocks_into_chunks(blocks, resolved_size, resolved_overlap)


def load_pdf_chunks(pdf_path: str | Path | None = None) -> list[str]:
    text = extract_text_from_pdf(pdf_path or config.PDF_PATH)
    return split_text_into_semantic_chunks(text)
