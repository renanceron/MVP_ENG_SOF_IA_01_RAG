from dataclasses import dataclass
from pathlib import Path
import shutil

import pytest
from langchain.schema import Document
from openai import OpenAIError

from app import config
from app import rag_pipeline
from app.pdf_loader import load_pdf_chunks


QUESTIONS = [
    "Qual o primeiro passo para fazer a inscricao no PEC-PG?",
    "E obrigatorio ter mestrado para se candidatar ao doutorado no PEC-PG?",
    "Qual e o valor da bolsa de doutorado do PEC-PG?",
    "Quais sao os requisitos para um candidato estrangeiro que ja mora no Brasil participar do PEC-PG?",
    "Qual e a capital da Franca?",
]


@dataclass
class ResponseStub:
    content: str


class LLMStub:
    def __init__(self, response: str = "Resposta baseada no contexto.") -> None:
        self.response = response
        self.prompts: list[str] = []

    def invoke(self, prompt: str) -> ResponseStub:
        self.prompts.append(prompt)
        return ResponseStub(self.response)


class VectorStoreStub:
    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents
        self.questions: list[str] = []
        self.top_k_values: list[int] = []

    def similarity_search(self, question: str, k: int) -> list[Document]:
        self.questions.append(question)
        self.top_k_values.append(k)
        return self.documents


def create_pipeline(documents: list[Document]) -> rag_pipeline.RAGPipeline:
    pipeline = rag_pipeline.RAGPipeline.__new__(rag_pipeline.RAGPipeline)
    pipeline.llm = LLMStub()
    pipeline.vector_store = VectorStoreStub(documents)
    return pipeline


def test_rag_pipeline_class_exposes_ask_method() -> None:
    assert hasattr(rag_pipeline.RAGPipeline, "ask")
    assert callable(rag_pipeline.RAGPipeline.ask)


def test_ask_returns_message_for_empty_question() -> None:
    pipeline = create_pipeline([])

    assert pipeline.ask("") == "Informe uma pergunta valida."
    assert pipeline.ask("   ") == "Informe uma pergunta valida."


def test_ask_returns_message_when_context_is_missing() -> None:
    pipeline = create_pipeline([])

    assert pipeline.ask("Qual e a capital da Franca?") == rag_pipeline.NO_CONTEXT_MESSAGE


@pytest.mark.parametrize("question", QUESTIONS)
def test_ask_uses_retrieved_context_for_expected_questions(question: str) -> None:
    documents = [Document(page_content="Contexto recuperado do documento PEC-PG.")]
    pipeline = create_pipeline(documents)

    answer = pipeline.ask(question)

    assert answer == "Resposta baseada no contexto."
    assert pipeline.vector_store.questions == [question]
    assert pipeline.vector_store.top_k_values == [config.TOP_K]
    assert "Contexto recuperado do documento PEC-PG." in pipeline.llm.prompts[0]
    assert question in pipeline.llm.prompts[0]


def test_build_prompt_instructs_model_to_use_only_context() -> None:
    pipeline = create_pipeline([])

    prompt = pipeline._build_prompt("Pergunta de teste", "Contexto de teste")

    assert "exclusivamente o contexto" in prompt
    assert "trecho relacionado ao tema da pergunta" in prompt
    assert "Contexto de teste" in prompt
    assert "Pergunta de teste" in prompt


def test_build_save_load_and_retrieve_faiss_vector_store_with_real_embeddings() -> None:
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY.startswith("insira_"):
        pytest.skip("OPENAI_API_KEY is required to run the real embeddings integration test")

    chunks = load_pdf_chunks(config.PDF_PATH)
    index_dir = Path(".tmp_pytest") / "faiss_index"

    if index_dir.exists():
        shutil.rmtree(index_dir)

    try:
        try:
            vector_store = rag_pipeline.build_vector_store(chunks, index_dir=index_dir)
        except OpenAIError as exc:
            pytest.skip(f"OpenAI embeddings API unavailable: {exc}")

        assert index_dir.exists()
        assert (index_dir / "index.faiss").exists()
        assert (index_dir / "index.pkl").exists()

        try:
            retrieved_documents = vector_store.similarity_search(
                "Qual e o valor da bolsa de doutorado do PEC-PG?",
                k=config.TOP_K,
            )
        except OpenAIError as exc:
            pytest.skip(f"OpenAI embeddings API unavailable: {exc}")

        assert retrieved_documents
        assert any("R$ 2.200,00" in document.page_content for document in retrieved_documents)

        loaded_vector_store = rag_pipeline.load_vector_store(index_dir=index_dir)
        assert loaded_vector_store is not None

        try:
            loaded_documents = loaded_vector_store.similarity_search(
                "Qual o primeiro passo para fazer a inscricao no PEC-PG?",
                k=config.TOP_K,
            )
        except OpenAIError as exc:
            pytest.skip(f"OpenAI embeddings API unavailable: {exc}")

        assert loaded_documents
        assert any("online" in document.page_content for document in loaded_documents)
    finally:
        if index_dir.exists():
            shutil.rmtree(index_dir)


def test_real_rag_pipeline_answers_expected_questions() -> None:
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY.startswith("insira_"):
        pytest.skip("OPENAI_API_KEY is required to run the real RAG integration test")

    print("\nEtapa 1 - Inicializar RAGPipeline")

    try:
        pipeline = rag_pipeline.RAGPipeline()
    except OpenAIError as exc:
        pytest.skip(f"OpenAI API unavailable while initializing RAGPipeline: {exc}")

    print(f"Etapa 2 - PDF configurado: {config.PDF_PATH}")
    print(f"Etapa 3 - Modelo LLM: {config.MODEL_NAME}")
    print(f"Etapa 4 - Modelo de embeddings: {config.EMBEDDING_MODEL}")
    print(f"Etapa 5 - TOP_K: {config.TOP_K}")
    print("Etapa 6 - Executar perguntas no pipeline real")

    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nPergunta {index}: {question}")

        answer = pipeline.ask(question)

        print(f"Resposta {index}: {answer}")

        assert answer
        assert answer != "Ocorreu um erro ao executar o pipeline RAG."
