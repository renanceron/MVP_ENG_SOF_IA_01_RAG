# Escopo do MVP — Assistente RAG

## 1. Problema

Usuários precisam consultar rapidamente informações dentro de um documento PDF (FAQ), sem a necessidade de leitura completa do conteúdo.

## 2. Objetivo

Desenvolver um assistente baseado em RAG (Retrieval Augmented Generation) capaz de responder perguntas utilizando exclusivamente o conteúdo de um documento PDF.

---

## 3. Escopo Funcional

### Funcionalidades incluídas

- Carregar um único documento PDF local
- Extrair texto do PDF
- Dividir o conteúdo em chunks
- Gerar embeddings utilizando OpenAI
- Armazenar embeddings em vector store local (FAISS)
- Realizar busca semântica
- Recuperar trechos relevantes
- Gerar respostas baseadas no conteúdo recuperado
- Interface simples com Gradio:
  - campo de entrada (pergunta)
  - campo de saída (resposta)

---

## 4. Fora do Escopo

- Upload de múltiplos documentos
- Memória conversacional
- Autenticação de usuários
- Banco de dados relacional
- Deploy em nuvem
- Integração com APIs externas além da OpenAI
- Otimizações avançadas (reranking, busca híbrida)
- Interfaces complexas

---

## 5. Regras Funcionais

- As respostas devem ser baseadas exclusivamente no conteúdo recuperado do documento
- O sistema não deve gerar respostas fora do contexto
- Caso não haja informação suficiente, o sistema deve informar claramente

---

## 6. Critérios de Aceite

1. O sistema deve responder perguntas com base no conteúdo do PDF
2. As respostas devem ser coerentes e contextualizadas
3. O sistema deve indicar quando não encontrar informação relevante
4. A aplicação deve executar localmente
5. Deve ser possível rodar o projeto seguindo o README
6. Testes automatizados devem executar com sucesso

---

## 7. Casos de Teste

- Pergunta: "Quem pode participar do programa?"
  - Esperado: resposta baseada no documento

- Pergunta: "Quais são os requisitos?"
  - Esperado: resposta baseada no documento

- Pergunta: "Qual a capital da França?"
  - Esperado: mensagem informando ausência de informação no documento

---

## 8. Definição do MVP

Este projeto implementa um assistente RAG simples capaz de responder perguntas com base em um único documento PDF, utilizando busca semântica e geração de respostas com LLM, garantindo que as respostas sejam fundamentadas exclusivamente no conteúdo do documento.