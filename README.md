# Assistente RAG - Mini Projeto Curso 4

Assistente RAG em Python para responder perguntas com base em um unico PDF local.

O projeto demonstra o uso de IA ao longo da cadeia de engenharia de software: requisitos, arquitetura, implementacao, testes, revisao, refatoracao, documentacao, versionamento e preparacao de release.

## Objetivo

Construir um MVP de Assistente RAG capaz de:

- carregar um PDF local;
- extrair texto;
- gerar chunks semanticos;
- criar embeddings com OpenAI;
- armazenar e recuperar vetores com FAISS local;
- responder perguntas usando um LLM;
- expor uma interface simples com Gradio.

## Escopo do MVP

Incluido:

- um unico documento PDF local em `data/faq_capes.pdf`;
- leitura e extracao de texto com `pypdf`;
- chunking semantico orientado por perguntas e respostas;
- embeddings com `text-embedding-3-small`;
- FAISS local;
- recuperacao semantica;
- respostas com `gpt-4o-mini`;
- interface simples com Gradio;
- testes automatizados com Pytest.

Fora do escopo:

- upload de multiplos documentos;
- memoria conversacional;
- autenticacao;
- banco relacional;
- deploy em nuvem;
- reranking;
- busca hibrida;
- interface complexa.

## Tecnologias

- Python
- LangChain
- OpenAI
- OpenAI Embeddings
- FAISS
- Gradio
- pypdf
- pytest
- python-dotenv

## Modelos

- LLM: `gpt-4o-mini`
- Embeddings: `text-embedding-3-small`

## Estrutura

```text
app/
  config.py
  pdf_loader.py
  rag_pipeline.py
  main.py
data/
  faq_capes.pdf
docs/
tests/
requirements.txt
.env.example
```

## Configuracao

Crie um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Crie o arquivo `.env`:

```powershell
Copy-Item .env.example .env
```

Edite `.env` e informe sua chave:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
```

O arquivo `.env` nao deve ser versionado.

## Executar Aplicacao

Use:

```powershell
python -m app.main
```

A interface Gradio sera iniciada localmente.

## Executar Testes

Testes unitarios e de integracao:

```powershell
python -m pytest tests/test_pdf_loader.py tests/test_rag_pipeline.py -q
```

Com logs detalhados:

```powershell
python -m pytest tests/test_pdf_loader.py tests/test_rag_pipeline.py -s -vv
```

Os testes reais de embeddings e LLM exigem `OPENAI_API_KEY` valida.

## Fonte de Dados

O PDF utilizado no MVP e:

```text
data/faq_capes.pdf
```

Ele e tratado como unica fonte de conhecimento da aplicacao.

## Parametros Principais

Definidos em `app/config.py`:

```python
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
PDF_PATH = Path("data/faq_capes.pdf")
FAISS_INDEX_DIR = Path("faiss_index")
TOP_K = 5
CHUNK_SIZE = 700
CHUNK_OVERLAP = 180
TEMPERATURE = 0.2
```

## Limitacoes

- O MVP usa apenas um PDF local.
- O indice FAISS e local e recriavel.
- A qualidade das respostas depende do contexto recuperado.
- Nao ha memoria conversacional.
- Nao ha autenticacao.

## Licenca

Este projeto usa a licenca MIT. Veja `LICENSE`.
