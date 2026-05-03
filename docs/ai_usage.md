# Uso de IA no Processo de Engenharia

## Objetivo

Registrar como IA foi usada no desenvolvimento do Assistente RAG.

## Etapas com Apoio de IA

| Etapa | Evidencia |
|---|---|
| Requisitos | `docs/context.md`, `docs/mvp_scope.md` |
| Arquitetura | `docs/architecture.md` |
| Codificacao | `app/pdf_loader.py`, `app/rag_pipeline.py`, `app/main.py` |
| Testes | `tests/test_pdf_loader.py`, `tests/test_rag_pipeline.py` |
| Revisao | Validacoes completas contra o MVP |
| Refatoracao | Chunking semantico, parametros centralizados, prompt ajustado |
| Documentacao | README e docs do projeto |
| Versionamento | Commits no padrao Conventional Commits |

## Decisoes Tecnicas

- Usar `gpt-4o-mini` como LLM padrao.
- Usar `text-embedding-3-small` para embeddings.
- Usar FAISS local para manter simplicidade.
- Usar chunking semantico por perguntas e respostas para preservar contexto.
- Manter `.env` apenas para credenciais.

## Cuidados

- Nao versionar `.env`.
- Nao expor chave OpenAI.
- Nao adicionar funcionalidades fora do MVP.
- Manter o PDF local como unica fonte de conhecimento.
