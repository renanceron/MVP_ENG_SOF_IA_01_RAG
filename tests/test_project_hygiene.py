from pathlib import Path


REQUIRED_REQUIREMENTS = {
    "python-dotenv",
    "gradio",
    "langchain",
    "langchain-community",
    "langchain-openai",
    "pypdf",
    "faiss-cpu",
    "pytest",
}


def test_requirements_are_pinned_and_limited_to_mvp() -> None:
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
    packages = {
        line.split("==", maxsplit=1)[0]
        for line in requirements
        if line and not line.startswith("#")
    }

    assert packages == REQUIRED_REQUIREMENTS
    assert all(
        "==" in line
        for line in requirements
        if line and not line.startswith("#")
    )


def test_gitignore_protects_sensitive_and_generated_files() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert ".env" in gitignore
    assert "!.env.example" in gitignore
    assert "faiss_index/" in gitignore
    assert "*.faiss" in gitignore
    assert "*.pkl" in gitignore
    assert ".pytest_cache/" in gitignore
    assert ".venv/" in gitignore


def test_env_example_contains_only_placeholder_key() -> None:
    env_example = Path(".env.example").read_text(encoding="utf-8")

    assert "OPENAI_API_KEY=insira_sua_chave_openai_aqui" in env_example
    assert "sk-" not in env_example


def test_required_documentation_files_exist_and_have_content() -> None:
    docs = [
        Path("README.md"),
        Path("docs/context.md"),
        Path("docs/mvp_scope.md"),
        Path("docs/architecture.md"),
        Path("docs/prompts.md"),
        Path("docs/backlog.md"),
        Path("docs/release.md"),
        Path("docs/workflow.md"),
        Path("docs/ai_usage.md"),
        Path("LICENSE"),
    ]

    for doc in docs:
        assert doc.exists()
        assert doc.stat().st_size > 0
