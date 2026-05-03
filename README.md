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
- O chat nao possui memoria conversacional; cada pergunta e tratada de forma independente.
- Nao ha autenticacao.
- Nao ha upload de novos documentos pela interface.
- Nao ha suporte a multiplos documentos.
- Nao ha reranking ou busca hibrida.

## Proximas Implementacoes

Possiveis evolucoes, mantendo controle de escopo:

- adicionar memoria conversacional opcional no chat;
- permitir carregamento de multiplos documentos;
- adicionar reranking para melhorar a ordenacao dos trechos recuperados;
- melhorar a exibicao de respostas longas na interface;
- exibir trechos recuperados como fonte da resposta;
- permitir recriacao manual do indice FAISS pela interface;
- documentar melhor o fluxo de atualizacao do PDF local;
- ampliar testes de interface e validacao visual.

## Uso de IA no Desenvolvimento

Este projeto utilizou IA como apoio direto na cadeia de engenharia de software, com o Codex no terminal auxiliando em:

- definicao e validacao do escopo do MVP;
- organizacao da arquitetura;
- implementacao dos modulos Python;
- criacao e revisao dos testes automatizados;
- refatoracao do pipeline RAG;
- validacao de aderencia ao escopo;
- documentacao tecnica;
- versionamento com Conventional Commits.

Dados tecnicos do apoio com IA:

- Ferramenta: Codex CLI
- Versao local validada: `codex-cli 0.128.0`
- Modelo/agente utilizado na sessao: Codex baseado em GPT-5
- Uso principal: apoio a engenharia de software, revisao, testes e documentacao
- Execucao: terminal local do projeto

## Licenca

Este projeto usa a licenca MIT. Veja `LICENSE`.
