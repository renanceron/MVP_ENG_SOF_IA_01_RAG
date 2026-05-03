from dataclasses import dataclass

import pytest
from langchain.schema import Document

from app import config
from app import rag_pipeline


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
    assert "Contexto de teste" in prompt
    assert "Pergunta de teste" in prompt
