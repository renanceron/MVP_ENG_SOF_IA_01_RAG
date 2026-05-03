import gradio as gr

from app.rag_pipeline import RAGPipeline


APP_TITLE = "Assistente RAG"
APP_DESCRIPTION = "Consulte o conteudo do PDF local configurado no projeto."
QUESTION_PLACEHOLDER = "Digite sua pergunta sobre o documento..."
ANSWER_LINES = 12
ANSWER_MAX_LINES = 20

pipeline: RAGPipeline | None = None
pipeline_error: str | None = None


try:
    pipeline = RAGPipeline()
except Exception:
    pipeline_error = "Ocorreu um erro ao iniciar o Assistente RAG."


def answer_question(question: str) -> str:
    if pipeline_error:
        return pipeline_error

    if pipeline is None:
        return "Assistente RAG indisponivel."

    try:
        return pipeline.ask(question)
    except Exception:
        return "Ocorreu um erro ao consultar o Assistente RAG."


app = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(
        label="Pergunta",
        placeholder=QUESTION_PLACEHOLDER,
        lines=2,
    ),
    outputs=gr.Textbox(
        label="Resposta",
        lines=ANSWER_LINES,
        max_lines=ANSWER_MAX_LINES,
    ),
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    submit_btn="Perguntar",
    clear_btn="Limpar",
)


if __name__ == "__main__":
    app.launch()
