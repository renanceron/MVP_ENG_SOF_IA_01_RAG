# Prompts Reutilizaveis - Assistente RAG

## Prompt Base

```text
Contexto:
Use docs/context.md como contexto principal do projeto.

Objetivo:
Executar a tarefa solicitada mantendo aderencia ao MVP do Assistente RAG.

Estilo:
- Codigo em ingles
- Documentacao em portugues
- Simplicidade
- Clean Code
- Sem funcionalidades fora do escopo

Resposta:
Gerar resultado pronto para uso e informar validacoes realizadas.
```

## Arquitetura

```text
Use docs/context.md como contexto principal.

Tarefa:
Revisar ou atualizar a arquitetura do Assistente RAG.

Regras:
- Manter um unico PDF local
- Usar OpenAI Embeddings
- Usar FAISS local
- Usar Gradio simples
- Nao incluir upload, memoria, autenticacao ou deploy
```

## PDF Loader

```text
Use docs/context.md como contexto principal.

Tarefa:
Implementar ou revisar app/pdf_loader.py.

Regras:
- Usar pypdf
- Extrair texto
- Gerar chunks semanticos
- Nao usar LangChain, OpenAI, FAISS ou Gradio neste arquivo
```

## Pipeline RAG

```text
Use docs/context.md como contexto principal.

Tarefa:
Implementar ou revisar app/rag_pipeline.py.

Regras:
- Usar LangChain
- Usar OpenAIEmbeddings
- Usar FAISS local
- Usar ChatOpenAI
- Expor ask(question: str) -> str
- Nao implementar memoria conversacional
```

## Interface

```text
Use docs/context.md como contexto principal.

Tarefa:
Criar ou revisar app/main.py.

Regras:
- Usar Gradio
- Um campo de pergunta
- Um campo de resposta
- Sem upload
- Sem autenticacao
- Sem historico
```

## Testes

```text
Use docs/context.md como contexto principal.

Tarefa:
Criar ou revisar testes com pytest.

Regras:
- Testar PDF inexistente
- Testar PDF vazio
- Testar chunking
- Testar pergunta vazia
- Testar ausencia de contexto
- Evitar chamadas reais a OpenAI em testes unitarios
- Permitir teste de integracao real quando OPENAI_API_KEY existir
```

## Revisao

```text
Use docs/context.md como contexto principal.

Tarefa:
Validar o projeto contra MVP, arquitetura, testes, documentacao, seguranca e release.

Regras:
- Nao alterar arquivos
- Marcar OK, PARCIAL ou PENDENTE
- Nao sugerir expansao fora do MVP
```

## Commit

```text
Use docs/context.md como contexto principal.

Tarefa:
Sugerir mensagem de commit.

Formato:
- feat:
- fix:
- docs:
- refactor:
- test:
- chore:
```
