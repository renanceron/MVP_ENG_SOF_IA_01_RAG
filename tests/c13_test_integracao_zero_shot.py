"""Integração offline: PDF e FAISS reais; somente embeddings são substituídos."""

import math
import re
from pathlib import Path

import pytest
from langchain_core.embeddings import Embeddings
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from app import config, pdf_loader, rag_pipeline


class LocalEmbeddings(Embeddings):
    """Vetores lexicais determinísticos para verificar o transporte dos textos."""

    vocabulary = ("bolsa", "inscricao", "visto")

    def embed_query(self, text: str) -> list[float]:
        words = re.findall(r"\w+", text.lower())
        vector = [float(words.count(word)) for word in self.vocabulary] + [1.0]
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]


def write_pdf(path: Path, pages: list[list[str]]) -> Path:
    """Cria PDFs de texto com pypdf, sem dependências adicionais."""
    writer = PdfWriter()
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    for lines in pages:
        page = writer.add_blank_page(width=612, height=792)
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})
        })
        commands = ["BT /F1 12 Tf 40 750 Td 16 TL"]
        for line in lines:
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(f"({escaped}) Tj T*")
        commands.append("ET")
        stream = DecodedStreamObject()
        stream.set_data("\n".join(commands).encode("ascii"))
        page[NameObject("/Contents")] = writer._add_object(stream)
    with path.open("wb") as output:
        writer.write(output)
    return path


@pytest.fixture
def local_embeddings(monkeypatch):
    embeddings = LocalEmbeddings()
    monkeypatch.setattr(rag_pipeline, "create_embeddings", lambda: embeddings)
    return embeddings


@pytest.fixture
def faq(tmp_path, monkeypatch, local_embeddings):
    blocks = [
        "1. Qual a bolsa? A bolsa mensal vale 2200 reais.",
        "2. Como fazer inscricao? A inscricao ocorre online.",
        "3. Qual o visto? O visto deve estar regular.",
    ]
    path = write_pdf(tmp_path / "faq.pdf", [
        ["FAQ", "1. Qual a bolsa?", "A bolsa mensal vale 2200 reais."],
        [blocks[1], blocks[2]],
    ])
    monkeypatch.setattr(config, "PDF_PATH", path)
    monkeypatch.setattr(config, "CHUNK_SIZE", 65)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 10)
    return path, blocks


def test_pdf_multipagina_preserva_perguntas_respostas_e_fonte_no_faiss(faq, tmp_path):
    path, blocks = faq
    chunks = pdf_loader.load_pdf_chunks()
    assert chunks == blocks
    store = rag_pipeline.build_vector_store(chunks, tmp_path / "index")
    assert store.index.ntotal == len(blocks)
    for question, expected in zip(("bolsa", "inscricao", "visto"), blocks):
        documents = store.similarity_search(question, k=1)
        assert len(documents) == 1
        assert documents[0].page_content == expected
        assert documents[0].metadata == {"source": str(path)}


def test_pdf_sem_perguntas_usa_janelas_com_overlap_e_indexa_todas(
    tmp_path, monkeypatch, local_embeddings
):
    text = "abcdefghijklmnopqrstuvwxyz"
    path = write_pdf(tmp_path / "prosa.pdf", [[text]])
    monkeypatch.setattr(config, "PDF_PATH", path)
    monkeypatch.setattr(config, "CHUNK_SIZE", 10)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 2)
    chunks = pdf_loader.load_pdf_chunks(path)
    expected = ["abcdefghij", "ijklmnopqr", "qrstuvwxyz", "yz"]
    assert chunks == expected
    store = rag_pipeline.build_vector_store(chunks, tmp_path / "index")
    documents = store.similarity_search("texto", k=10)
    assert store.index.ntotal == 4
    assert sorted(doc.page_content for doc in documents) == sorted(expected)


def test_bloco_de_pergunta_longo_e_dividido_e_recuperado_integralmente(
    tmp_path, monkeypatch, local_embeddings
):
    text = "1. Qual a bolsa? " + "bolsa mensal de 2200 reais. " * 6
    path = write_pdf(tmp_path / "longo.pdf", [[text]])
    monkeypatch.setattr(config, "PDF_PATH", path)
    monkeypatch.setattr(config, "CHUNK_SIZE", 60)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 10)
    normalized = text.strip()
    expected = [normalized[start:start + 60].strip()
                for start in range(0, len(normalized), 50)]
    chunks = pdf_loader.load_pdf_chunks(path)
    assert chunks == expected
    assert len(chunks) > 1
    store = rag_pipeline.build_vector_store(chunks, tmp_path / "index")
    documents = store.similarity_search("bolsa", k=len(chunks) + 1)
    assert sorted(doc.page_content for doc in documents) == sorted(expected)


def test_indice_persistido_recupera_textos_e_metadados_sem_pdf(faq, tmp_path):
    path, blocks = faq
    index_dir = tmp_path / "index"
    assert rag_pipeline.load_vector_store(index_dir) is None
    store = rag_pipeline.build_vector_store(pdf_loader.load_pdf_chunks(), index_dir)
    before = store.similarity_search("inscricao", k=3)
    assert (index_dir / "index.faiss").is_file()
    assert (index_dir / "index.pkl").is_file()
    path.unlink()  # Apenas o PDF criado pela fixture no diretório temporário.
    loaded = rag_pipeline.load_vector_store(index_dir)
    assert loaded is not None
    after = loaded.similarity_search("inscricao", k=3)
    assert [(doc.page_content, doc.metadata) for doc in after] == [
        (doc.page_content, doc.metadata) for doc in before
    ]
    assert after[0].page_content == blocks[1]


@pytest.mark.parametrize("top_k", [1, 2, 5])
def test_contexto_do_pipeline_respeita_top_k_com_faiss_real(
    faq, tmp_path, monkeypatch, top_k
):
    _, blocks = faq
    store = rag_pipeline.build_vector_store(
        pdf_loader.load_pdf_chunks(), tmp_path / "index"
    )
    # O escopo termina na recuperação: evita inicializar o cliente LLM.
    pipeline = rag_pipeline.RAGPipeline.__new__(rag_pipeline.RAGPipeline)
    pipeline.vector_store = store
    monkeypatch.setattr(config, "TOP_K", top_k)
    context = pipeline._retrieve_context("visto")
    parts = context.split("\n\n")
    assert len(parts) == min(top_k, len(blocks))
    assert parts[0] == blocks[2]
    assert len(set(parts)) == len(parts)
    assert all(part in blocks for part in parts)
