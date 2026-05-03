import pytest
from pathlib import Path

from app import pdf_loader


FIXTURE_PDF_PATH = "tests/fixtures/sample.pdf"
DATA_PDF_PATH = "data/faq_capes.pdf"


def test_validate_pdf_path_returns_file_path() -> None:
    assert pdf_loader.validate_pdf_path(FIXTURE_PDF_PATH).as_posix() == FIXTURE_PDF_PATH


def test_validate_pdf_path_rejects_missing_file() -> None:
    with pytest.raises(FileNotFoundError, match="PDF file not found"):
        pdf_loader.validate_pdf_path("tests/fixtures/missing.pdf")


def test_validate_pdf_path_rejects_directory() -> None:
    with pytest.raises(FileNotFoundError, match="PDF path is not a file"):
        pdf_loader.validate_pdf_path("tests/fixtures")


def test_normalize_text_collapses_whitespace() -> None:
    text = " First line\n\nSecond\tline   with spaces "

    assert pdf_loader.normalize_text(text) == "First line Second line with spaces"


def test_split_text_into_chunks_uses_overlap() -> None:
    chunks = pdf_loader.split_text_into_chunks(
        "abcdefghijklmnopqrstuvwxyz",
        chunk_size=10,
        chunk_overlap=2,
    )

    assert chunks == ["abcdefghij", "ijklmnopqr", "qrstuvwxyz", "yz"]


@pytest.mark.parametrize(
    ("text", "chunk_size", "chunk_overlap", "expected_message"),
    [
        ("", 10, 2, "Text cannot be empty"),
        ("content", 0, 0, "chunk_size must be greater than zero"),
        ("content", 10, -1, "chunk_overlap cannot be negative"),
        ("content", 10, 10, "chunk_overlap must be smaller than chunk_size"),
    ],
)
def test_split_text_into_chunks_validates_inputs(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    expected_message: str,
) -> None:
    with pytest.raises(ValueError, match=expected_message):
        pdf_loader.split_text_into_chunks(text, chunk_size, chunk_overlap)


def test_extract_text_from_pdf_reads_and_normalizes_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class PageStub:
        def __init__(self, text: str | None) -> None:
            self.text = text

        def extract_text(self) -> str | None:
            return self.text

    class ReaderStub:
        def __init__(self, path: str) -> None:
            assert Path(path) == Path(FIXTURE_PDF_PATH)
            self.pages = [PageStub(" First page\n"), PageStub(None), PageStub("Second page ")]

    monkeypatch.setattr(pdf_loader, "PdfReader", ReaderStub)

    assert pdf_loader.extract_text_from_pdf(FIXTURE_PDF_PATH) == "First page Second page"


def test_extract_text_from_pdf_rejects_pdf_without_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ReaderStub:
        def __init__(self, path: str) -> None:
            self.pages = []

    monkeypatch.setattr(pdf_loader, "PdfReader", ReaderStub)

    with pytest.raises(ValueError, match="PDF has no extractable text"):
        pdf_loader.extract_text_from_pdf(FIXTURE_PDF_PATH)


def test_load_pdf_chunks_from_project_pdf() -> None:
    chunks = pdf_loader.load_pdf_chunks(DATA_PDF_PATH)

    assert len(chunks) >= 3
    assert all(chunk.strip() for chunk in chunks[:3])
    assert all(len(chunk) <= pdf_loader.CHUNK_SIZE for chunk in chunks[:3])
