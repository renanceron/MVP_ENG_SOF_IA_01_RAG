import gradio as gr

from app.rag_pipeline import RAGPipeline


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
    inputs=gr.Textbox(label="Pergunta"),
    outputs=gr.Textbox(label="Resposta"),
    title="Assistente RAG",
)


if __name__ == "__main__":
    app.launch()
