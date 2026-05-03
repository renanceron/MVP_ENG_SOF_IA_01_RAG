import logging
from pathlib import Path

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app import config
from app.pdf_loader import load_pdf_chunks


NO_CONTEXT_MESSAGE = "Nao encontrei informacao suficiente no documento para responder."
FAISS_INDEX_DIR = config.FAISS_INDEX_DIR
logger = logging.getLogger(__name__)


def validate_openai_api_key() -> None:
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY.startswith("insira_"):
        raise RuntimeError("OPENAI_API_KEY is not configured")


def create_embeddings() -> OpenAIEmbeddings:
    validate_openai_api_key()
    return OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        api_key=config.OPENAI_API_KEY,
    )


def build_vector_store(chunks: list[str], index_dir: Path = FAISS_INDEX_DIR) -> FAISS:
    if not chunks:
        raise ValueError("No chunks available for indexing")

    documents = [
        Document(page_content=chunk, metadata={"source": str(config.PDF_PATH)})
        for chunk in chunks
        if chunk.strip()
    ]

    if not documents:
        raise ValueError("No valid chunks available for indexing")

    embeddings = create_embeddings()
    logger.info("Creating FAISS index with %s documents", len(documents))
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(str(index_dir))
    logger.info("FAISS index saved at %s", index_dir)

    return vector_store


def load_vector_store(index_dir: Path = FAISS_INDEX_DIR) -> FAISS | None:
    if not index_dir.exists():
        logger.info("FAISS index not found at %s", index_dir)
        return None

    try:
        vector_store = FAISS.load_local(
            str(index_dir),
            create_embeddings(),
            allow_dangerous_deserialization=True,
        )
        logger.info("FAISS index loaded from %s", index_dir)
        return vector_store
    except Exception:
        logger.warning("Failed to load FAISS index from %s", index_dir)
        return None


class RAGPipeline:
    def __init__(self) -> None:
        validate_openai_api_key()
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=config.TEMPERATURE,
        )
        self.vector_store = self._get_or_create_vector_store()

    def ask(self, question: str) -> str:
        if not question or not question.strip():
            return "Informe uma pergunta valida."

        try:
            context = self._retrieve_context(question.strip())

            if not context:
                return NO_CONTEXT_MESSAGE

            prompt = self._build_prompt(question.strip(), context)
            response = self.llm.invoke(prompt)

            return response.content.strip()
        except Exception:
            return "Ocorreu um erro ao executar o pipeline RAG."

    def _get_or_create_vector_store(self) -> FAISS:
        vector_store = load_vector_store()

        if vector_store is not None:
            return vector_store

        chunks = load_pdf_chunks(config.PDF_PATH)
        return build_vector_store(chunks)

    def _retrieve_context(self, question: str) -> str:
        documents = self.vector_store.similarity_search(question, k=config.TOP_K)
        chunks = [document.page_content for document in documents if document.page_content]

        return "\n\n".join(chunks).strip()

    def _build_prompt(self, question: str, context: str) -> str:
        return (
            "Voce e um assistente RAG que responde usando exclusivamente o contexto abaixo.\n"
            "Se existir no contexto um trecho relacionado ao tema da pergunta, responda com "
            "base nesse trecho, mesmo que a formulacao nao seja identica.\n"
            "Quando a resposta depender de condicao, informe a condicao de forma objetiva.\n"
            "Se o contexto realmente nao trouxer informacao relacionada, responda exatamente: "
            f"{NO_CONTEXT_MESSAGE}\n\n"
            f"Contexto:\n{context}\n\n"
            f"Pergunta:\n{question}\n\n"
            "Resposta:"
        )
