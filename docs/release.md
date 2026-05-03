# Release v1.0.0 - Assistente RAG

## Status

Release candidata: `v1.0.0`

## Escopo Entregue

- Carregamento de um unico PDF local.
- Extracao de texto com `pypdf`.
- Chunking semantico por pergunta e resposta.
- Embeddings com OpenAI.
- Indice FAISS local com persistencia.
- Recuperacao semantica.
- Resposta com `gpt-4o-mini`.
- Interface simples com Gradio.
- Testes automatizados com Pytest.
- Documentacao de setup e uso.

## Fora do Escopo

- Multiplos documentos.
- Upload.
- Memoria conversacional.
- Autenticacao.
- Banco relacional.
- Deploy em nuvem.
- Reranking.
- Busca hibrida.

## Validacoes

Comando recomendado:

```powershell
python -m pytest tests/test_pdf_loader.py tests/test_rag_pipeline.py -q
```

Resultado esperado:

```text
26 passed
```

## Artefatos Locais

O diretorio `faiss_index/` e gerado localmente e nao deve ser versionado.

## Criterios para Criar Tag

- Testes passando.
- README completo.
- Sem credenciais versionadas.
- Branch `main` limpa.
- `LICENSE` preenchido.
- `docs/release.md` atualizado.

## Comandos

```powershell
git status --short
git tag -a v1.0.0 -m "release: v1.0.0"
git push origin main
git push origin v1.0.0
```
