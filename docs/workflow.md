# Workflow de Engenharia - Assistente RAG

## Fluxo

1. Definir escopo do MVP.
2. Validar arquitetura.
3. Criar estrutura de diretorios.
4. Implementar modulos isolados.
5. Criar testes automatizados.
6. Revisar e refatorar.
7. Atualizar documentacao.
8. Versionar com Conventional Commits.
9. Preparar release.

## Execucao Recomendada

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest tests/test_pdf_loader.py tests/test_rag_pipeline.py -q
python -m app.main
```

## Padrao de Commits

- `feat:` nova funcionalidade do MVP
- `fix:` correcao
- `test:` testes
- `docs:` documentacao
- `refactor:` refatoracao sem mudanca de comportamento
- `chore:` tarefas auxiliares

## Criterio de Pronto

- Testes passando.
- README atualizado.
- Sem credenciais no Git.
- Branch `main` limpa.
- Tag `v1.0.0` criada.
