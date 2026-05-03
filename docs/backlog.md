# Backlog - Assistente RAG

## Etapa 1 - Preparacao e Setup

- [x] Validar escopo do MVP em `docs/context.md`
- [x] Validar arquitetura em `docs/architecture.md`
- [x] Definir estrutura inicial de diretorios
- [x] Criar estrutura do projeto
- [x] Configurar arquivo `.env.example`
- [x] Validar dependencias em `requirements.txt`
- [x] Garantir `.env` fora do Git
- [ ] Configurar ambiente virtual local
- [ ] Definir `OPENAI_API_KEY` no `.env` local

## Etapa 2 - Ingestao de Dados (PDF)

- [x] Criar modulo `pdf_loader.py`
- [x] Definir caminho do PDF local
- [x] Implementar leitura de PDF
- [x] Implementar extracao de texto
- [x] Validar PDF inexistente
- [x] Validar PDF sem texto extraivel
- [x] Implementar chunking semantico
- [x] Configurar tamanho dos chunks
- [x] Configurar overlap dos chunks
- [x] Retornar chunks prontos para indexacao

## Etapa 3 - Indexacao e Vetorizacao

- [x] Configurar OpenAI Embeddings
- [x] Gerar embeddings dos chunks
- [x] Criar vector store com FAISS
- [x] Persistir indice FAISS localmente
- [x] Implementar carregamento do indice local
- [x] Tratar ausencia do indice salvo
- [x] Evitar recriar embeddings quando o indice existe
- [x] Validar busca semantica no indice

## Etapa 4 - Pipeline RAG

- [x] Criar modulo `rag_pipeline.py`
- [x] Implementar classe `RAGPipeline`
- [x] Configurar carregamento do vector store
- [x] Implementar recuperacao de contexto com `TOP_K`
- [x] Implementar prompt com contexto recuperado
- [x] Integrar com LLM OpenAI
- [x] Implementar metodo `ask(question)`
- [x] Garantir respostas baseadas no contexto recuperado
- [x] Tratar pergunta vazia
- [x] Tratar ausencia de contexto suficiente

## Etapa 5 - Interface

- [x] Criar interface com Gradio
- [x] Criar campo de entrada para pergunta
- [x] Criar campo de saida para resposta
- [x] Integrar interface com `RAGPipeline`
- [x] Configurar execucao local da interface
- [x] Testar fluxo completo via pipeline

## Etapa 6 - Testes

- [x] Configurar testes com pytest
- [x] Criar testes para carregamento do PDF
- [x] Criar testes para extracao de texto
- [x] Criar testes para chunking
- [x] Criar testes para recuperacao de contexto
- [x] Criar testes para resposta sem contexto suficiente
- [x] Criar testes para inicializacao do pipeline
- [x] Criar teste de integracao real com OpenAI quando houver chave
- [x] Executar suite de testes localmente

## Etapa 7 - Documentacao

- [x] Atualizar `README.md`
- [x] Documentar configuracao do ambiente
- [x] Documentar configuracao do `.env`
- [x] Documentar execucao da aplicacao
- [x] Documentar execucao dos testes
- [x] Validar `docs/architecture.md`
- [x] Validar `docs/mvp_scope.md`
- [x] Validar `docs/context.md`
- [x] Validar `docs/prompts.md`
- [x] Criar `docs/release.md`
- [x] Criar `docs/ai_usage.md`
- [x] Atualizar `docs/workflow.md`

## Etapa 8 - Revisao e Refatoracao

- [x] Revisar codigo com foco em Clean Code
- [x] Melhorar nomes e estrutura
- [x] Remover duplicacoes desnecessarias
- [x] Garantir separacao de responsabilidades
- [x] Validar aderencia ao escopo do MVP
- [x] Validar tratamento de erros essenciais
- [x] Executar testes apos refatoracao
- [x] Remover arquivos temporarios ou sensiveis do versionamento

## Etapa 9 - Versionamento e Release

- [x] Revisar status do Git
- [x] Garantir ausencia de credenciais sensiveis
- [x] Criar commits estruturados
- [x] Garantir historico consistente
- [x] Revisar branch `main`
- [x] Executar testes finais
- [x] Validar aplicacao localmente por testes de pipeline
- [ ] Criar tag `v1.0.0`
- [ ] Publicar release `v1.0.0`
