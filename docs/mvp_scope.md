# Escopo do MVP - Assistente RAG

## Problema

Usuarios precisam consultar rapidamente informacoes de um documento PDF sem ler o conteudo completo.

## Objetivo

Criar um Assistente RAG capaz de responder perguntas usando exclusivamente o conteudo recuperado de um unico PDF local.

## Funcionalidades Incluidas

- Carregar um unico PDF local.
- Extrair texto do PDF.
- Dividir texto em chunks semanticos.
- Gerar embeddings com OpenAI.
- Armazenar embeddings em FAISS local.
- Realizar busca semantica.
- Recuperar trechos relevantes.
- Gerar respostas com LLM com base no contexto recuperado.
- Expor interface simples com Gradio.

## Fora do Escopo

- Upload de multiplos documentos.
- Memoria conversacional.
- Autenticacao.
- Banco de dados relacional.
- Deploy em nuvem.
- Integracoes externas alem da OpenAI.
- Reranking.
- Busca hibrida.
- Interface complexa.

## Regras Funcionais

- O PDF local e a unica fonte de conhecimento.
- Respostas devem usar exclusivamente o contexto recuperado.
- Quando nao houver informacao suficiente, o sistema deve informar claramente.
- O sistema nao deve inventar informacoes fora do documento.

## Criterios de Aceite

- Aplicacao responde perguntas com base no PDF.
- Respostas sao coerentes com o contexto recuperado.
- Sistema indica ausencia de informacao quando necessario.
- Aplicacao executa localmente.
- README contem setup, uso e testes.
- Testes automatizados existem e executam com sucesso.
- Nao ha credenciais sensiveis versionadas.
