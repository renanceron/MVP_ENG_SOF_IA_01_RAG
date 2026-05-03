# Contexto do Projeto - Assistente RAG

## 1. Visao Geral

Este projeto e um Mini Projeto do Curso 4 com foco em demonstrar o uso de IA em toda a cadeia da engenharia de software.

O objetivo e construir um Assistente RAG capaz de responder perguntas com base em um unico documento PDF local.

## 2. Escopo do MVP

### Funcionalidades incluidas

- Carregar um unico documento PDF local.
- Extrair texto do PDF.
- Dividir texto em chunks semanticos.
- Gerar embeddings com OpenAI.
- Armazenar embeddings em FAISS local.
- Realizar busca semantica.
- Recuperar trechos relevantes.
- Gerar respostas com base no contexto recuperado.
- Disponibilizar interface simples com Gradio.

### Fora do escopo

- Upload de multiplos documentos.
- Memoria conversacional.
- Autenticacao de usuarios.
- Banco de dados relacional.
- Deploy em nuvem.
- Integracoes externas alem da OpenAI.
- Reranking.
- Busca hibrida.
- Interface complexa.

### Regras funcionais

- As respostas devem ser baseadas exclusivamente no conteudo recuperado do documento.
- O sistema nao deve gerar informacoes fora do contexto.
- Caso nao haja informacao suficiente, o sistema deve informar claramente.
- O documento PDF deve ser tratado como a unica fonte de conhecimento.

## 3. Stack Tecnologica

- Python
- LangChain
- OpenAI
- OpenAI Embeddings
- FAISS
- Gradio
- Pytest
- Git
- GitHub
- VSCode
- Codex no terminal

## 4. Modelos

- LLM padrao: `gpt-4o-mini`
- Modelo de embeddings: `text-embedding-3-small`

## 5. Arquitetura Resumida

1. PDF Loader realiza a leitura do documento.
2. Text Splitter divide o conteudo em chunks semanticos.
3. OpenAI Embeddings gera vetores.
4. FAISS armazena vetores localmente.
5. Retriever busca os trechos mais relevantes.
6. LLM gera resposta com base no contexto recuperado.
7. Gradio exibe pergunta e resposta ao usuario.

## 6. Objetivo da IA

A IA apoia:

- definicao de requisitos;
- arquitetura;
- codificacao;
- testes;
- revisao;
- refatoracao;
- documentacao;
- versionamento.

## 7. Diretrizes

- Codigo em ingles.
- Documentacao em portugues.
- Clean Code.
- SOLID quando fizer sentido.
- Priorizar simplicidade.
- Evitar overengineering.
- Manter escopo estritamente limitado ao MVP.

## 8. Sequencia de Execucao

1. Definicao do escopo.
2. Arquitetura.
3. Estrutura de diretorios.
4. Implementacao por modulos.
5. Testes.
6. Revisao e refatoracao.
7. Documentacao.
8. Versionamento.
9. Release ou tag final.

## 9. Criterios de Aceite

- Aplicacao responde perguntas com base no PDF.
- Respostas sao coerentes com o contexto recuperado.
- Sistema indica ausencia de informacao quando necessario.
- Aplicacao executa localmente.
- README esta completo.
- `requirements.txt` esta definido.
- Testes automatizados existem.
- Testes executam com sucesso.
- Projeto esta versionado no GitHub.
- Branch `main` esta limpa.
- Release ou tag `v1.0.0` criada.
- Nao ha credenciais sensiveis no repositorio.
