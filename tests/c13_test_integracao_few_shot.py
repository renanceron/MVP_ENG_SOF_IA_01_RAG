"""Few-shot integration: real PDF processing and FAISS, local embeddings only."""
import hashlib
import re
from pathlib import Path

import pytest
from langchain_core.embeddings import Embeddings
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from app import config, pdf_loader, rag_pipeline


class LocalEmbeddings(Embeddings):
    """Deterministic normalized token vectors for controlled retrieval fixtures."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        vector = [0.0] * 256
        for token in re.findall(r"\w+", text.lower()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            vector[int.from_bytes(digest[:4], "big") % len(vector)] += 1.0
        norm = sum(value * value for value in vector) ** 0.5
        return [value / norm for value in vector] if norm else vector


@pytest.fixture(autouse=True)
def local_embeddings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rag_pipeline, "create_embeddings", LocalEmbeddings)


def write_pdf(path: Path, pages: list[str]) -> Path:
    """Generate real PDF text with the already installed pypdf."""
    writer = PdfWriter()
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    for text in pages:
        page = writer.add_blank_page(width=612, height=792)
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})
        })
        escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = DecodedStreamObject()
        stream.set_data(f"BT /F1 12 Tf 40 740 Td ({escaped}) Tj ET".encode("ascii"))
        page[NameObject("/Contents")] = stream
    with path.open("wb") as output:
        writer.write(output)
    return path


def build_from_pdf(path: Path, index_dir: Path):
    chunks = pdf_loader.load_pdf_chunks(path)
    return chunks, rag_pipeline.build_vector_store(chunks, index_dir=index_dir)


def test_valid_pdf_normalizes_pages_and_recovers_known_content(tmp_path, monkeypatch):
    path = write_pdf(tmp_path / "known.pdf", [
        "  A bolsa   mensal vale 2200 reais.  ",
        " O pagamento ocorre em conta bancaria. ",
    ])
    monkeypatch.setattr(config, "PDF_PATH", path)
    chunks, store = build_from_pdf(path, tmp_path / "index")
    expected = "A bolsa mensal vale 2200 reais. O pagamento ocorre em conta bancaria."
    assert chunks == [expected]
    documents = store.similarity_search("bolsa mensal", k=5)
    assert [document.page_content for document in documents] == [expected]
    assert documents[0].metadata == {"source": str(path)}
    assert store.index.ntotal == 1


def test_faq_blocks_remain_complete_and_relevant_answer_is_ranked_first(tmp_path, monkeypatch):
    blocks = [
        "1. Qual a bolsa? A bolsa mensal vale 2200 reais.",
        "2. Como inscrever? Inscrever pelo portal online.",
        "3. Qual o prazo? O prazo termina em dezembro.",
    ]
    path = write_pdf(tmp_path / "faq.pdf", ["FAQ " + " ".join(blocks)])
    monkeypatch.setattr(config, "CHUNK_SIZE", 60)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 10)
    chunks, store = build_from_pdf(path, tmp_path / "index")
    assert chunks == blocks
    assert store.index.ntotal == len(blocks)
    documents = store.similarity_search("inscrever portal online", k=1)
    assert [document.page_content for document in documents] == [blocks[1]]
    assert {doc.page_content for doc in store.similarity_search("bolsa", k=10)} == set(blocks)


@pytest.mark.parametrize("prefix", ["", "1. Codigo? "], ids=["plain-text", "oversized-faq"])
def test_character_chunks_preserve_overlap_through_real_index(prefix, tmp_path, monkeypatch):
    text = prefix + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    path = write_pdf(tmp_path / "long.pdf", [text])
    monkeypatch.setattr(config, "CHUNK_SIZE", 26)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 6)
    chunks, store = build_from_pdf(path, tmp_path / "index")
    expected = [text[start:start + 26].strip() for start in range(0, len(text), 20)]
    assert len(chunks) > 1
    assert chunks == expected
    assert all(len(chunk) <= 26 for chunk in chunks)
    assert chunks[0][-6:] == chunks[1][:6]
    assert store.index.ntotal == len(expected)
    retrieved = store.similarity_search(chunks[-1], k=1)
    assert retrieved[0].page_content == chunks[-1]
    assert {doc.page_content for doc in store.similarity_search(text, k=len(chunks))} == set(expected)


def test_saved_index_restores_content_metadata_and_ranking_without_pdf(tmp_path, monkeypatch):
    path = write_pdf(tmp_path / "persist.pdf", [
        "1. Qual a bolsa? Bolsa mensal de 2200 reais. "
        "2. Como inscrever? Portal online para inscrever.",
    ])
    monkeypatch.setattr(config, "PDF_PATH", path)
    monkeypatch.setattr(config, "CHUNK_SIZE", 55)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 5)
    index_dir = tmp_path / "index"
    chunks, store = build_from_pdf(path, index_dir)
    query = "portal online inscrever"
    before = store.similarity_search(query, k=2)
    assert (index_dir / "index.faiss").is_file()
    assert (index_dir / "index.pkl").is_file()
    path.unlink()  # Only the temporary PDF created by this test.
    loaded = rag_pipeline.load_vector_store(index_dir=index_dir)
    assert loaded is not None
    after = loaded.similarity_search(query, k=2)
    assert [(d.page_content, d.metadata) for d in after] == [
        (d.page_content, d.metadata) for d in before
    ]
    assert after[0].page_content == chunks[1]
    assert loaded.index.ntotal == len(chunks)


def test_pipeline_retrieves_top_k_context_from_pdf_index(tmp_path, monkeypatch):
    blocks = [
        "1. Bolsa? Bolsa mensal de 2200 reais.",
        "2. Portal? Inscricao pelo portal online.",
        "3. Prazo? Prazo termina em dezembro.",
    ]
    path = write_pdf(tmp_path / "context.pdf", [" ".join(blocks)])
    monkeypatch.setattr(config, "CHUNK_SIZE", 45)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 5)
    _, store = build_from_pdf(path, tmp_path / "index")
    # Retrieval only needs vector_store; bypass LLM construction entirely.
    pipeline = rag_pipeline.RAGPipeline.__new__(rag_pipeline.RAGPipeline)
    pipeline.vector_store = store
    monkeypatch.setattr(config, "TOP_K", 1)
    assert pipeline._retrieve_context("inscricao portal online") == blocks[1]
    monkeypatch.setattr(config, "TOP_K", 3)
    context = pipeline._retrieve_context("inscricao portal online")
    assert context.split("\n\n")[0] == blocks[1]
    assert set(context.split("\n\n")) == set(blocks)


@pytest.mark.parametrize(
    ("kind", "exception", "message"),
    [
        ("missing", FileNotFoundError, "PDF file not found"),
        ("directory", FileNotFoundError, "PDF path is not a file"),
        ("corrupt", RuntimeError, "Failed to read PDF"),
        ("blank", ValueError, "PDF has no extractable text"),
    ],
)
def test_invalid_pdf_stops_loading_processing_and_index_creation(kind, exception, message, tmp_path):
    path = tmp_path / "input.pdf"
    if kind == "directory":
        path.mkdir()
    elif kind == "corrupt":
        path.write_bytes(b"This is not a PDF")
    elif kind == "blank":
        write_pdf(path, [""])
    index_dir = tmp_path / "index"
    with pytest.raises(exception, match=message) as caught:
        build_from_pdf(path, index_dir)
    assert not index_dir.exists()
    if kind == "corrupt":
        assert caught.value.__cause__ is not None
