import importlib
import sys


class PipelineStub:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def ask(self, question: str) -> str:
        self.questions.append(question)
        return f"answer: {question}"


class FailingPipelineStub:
    def __init__(self) -> None:
        raise RuntimeError("startup failed")


class ErrorPipelineStub:
    def ask(self, question: str) -> str:
        raise RuntimeError("query failed")


def import_main_with_pipeline(monkeypatch, pipeline_class):
    import app.rag_pipeline as rag_pipeline

    monkeypatch.setattr(rag_pipeline, "RAGPipeline", pipeline_class)
    sys.modules.pop("app.main", None)

    return importlib.import_module("app.main")


def test_answer_question_uses_rag_pipeline(monkeypatch) -> None:
    main = import_main_with_pipeline(monkeypatch, PipelineStub)

    assert main.answer_question("Pergunta de teste") == "answer: Pergunta de teste"


def test_answer_question_returns_startup_error(monkeypatch) -> None:
    main = import_main_with_pipeline(monkeypatch, FailingPipelineStub)

    assert main.answer_question("Pergunta") == "Ocorreu um erro ao iniciar o Assistente RAG."


def test_answer_question_returns_query_error(monkeypatch) -> None:
    main = import_main_with_pipeline(monkeypatch, PipelineStub)
    main.pipeline = ErrorPipelineStub()
    main.pipeline_error = None

    assert main.answer_question("Pergunta") == "Ocorreu um erro ao consultar o Assistente RAG."


def test_gradio_interface_has_single_input_and_output(monkeypatch) -> None:
    main = import_main_with_pipeline(monkeypatch, PipelineStub)

    assert len(main.app.input_components) == 1
    assert len(main.app.output_components) == 1
    assert main.app.input_components[0].label == "Pergunta"
    assert main.app.output_components[0].label == "Resposta"


def test_gradio_interface_uses_readable_response_area(monkeypatch) -> None:
    main = import_main_with_pipeline(monkeypatch, PipelineStub)
    question_input = main.app.input_components[0]
    answer_output = main.app.output_components[0]

    assert main.app.title == main.APP_TITLE
    assert main.app.description == main.APP_DESCRIPTION
    assert question_input.placeholder == main.QUESTION_PLACEHOLDER
    assert question_input.lines == 2
    assert answer_output.lines == main.ANSWER_LINES
    assert answer_output.max_lines == main.ANSWER_MAX_LINES
