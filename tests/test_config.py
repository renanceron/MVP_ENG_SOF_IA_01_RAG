from pathlib import Path

from app import config


def test_config_uses_expected_models_and_parameters() -> None:
    assert config.MODEL_NAME == "gpt-4o-mini"
    assert config.EMBEDDING_MODEL == "text-embedding-3-small"
    assert config.TOP_K == 5
    assert config.CHUNK_SIZE == 700
    assert config.CHUNK_OVERLAP == 180
    assert config.TEMPERATURE == 0.2


def test_config_paths_are_local_project_paths() -> None:
    assert config.PDF_PATH == Path("data/faq_capes.pdf")
    assert config.FAISS_INDEX_DIR == Path("faiss_index")
    assert not config.PDF_PATH.is_absolute()
    assert not config.FAISS_INDEX_DIR.is_absolute()


def test_openai_api_key_is_loaded_from_environment_only() -> None:
    config_source = Path("app/config.py").read_text(encoding="utf-8")

    assert 'os.getenv("OPENAI_API_KEY")' in config_source
    assert "sk-" not in config_source
