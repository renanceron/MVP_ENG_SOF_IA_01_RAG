# Arquitetura — Assistente RAG

## 1. Visão Geral

O projeto implementa um assistente RAG simples para consulta a um único documento PDF.

O fluxo principal consiste em:

1. Carregar o PDF local
2. Extrair o texto
3. Dividir o texto em chunks
4. Gerar embeddings
5. Armazenar os vetores em FAISS
6. Receber pergunta do usuário
7. Buscar trechos relevantes
8. Gerar resposta com base no contexto recuperado
9. Exibir resposta na interface Gradio

---

## 2. Diagrama de Arquitetura

```mermaid
flowchart TD
    A[Usuário] --> B[Interface Gradio]
    B --> C[Função de Pergunta]
    C --> D[Retriever RAG]

    E[PDF Local] --> F[PDF Loader]
    F --> G[Text Splitter]
    G --> H[OpenAI Embeddings]
    H --> I[FAISS Vector Store]

    I --> D
    D --> J[Contexto Recuperado]
    J --> K[LLM OpenAI]
    C --> K
    K --> L[Resposta Final]
    L --> B


---

## 3. Componentes
Interface (Gradio)

Recebe a pergunta do usuário e exibe a resposta.

PDF Loader

Carrega o PDF e extrai o texto.

Text Splitter

Divide o texto em chunks menores.

Embeddings (OpenAI)

Transforma texto em vetores.

FAISS

Armazena os vetores e permite busca semântica.

Retriever

Busca os trechos mais relevantes.

LLM (OpenAI)

Gera a resposta com base no contexto.

4. Fluxo de Execução
4.1 Indexação (pré-processamento)

sequenceDiagram
    participant PDF as PDF Local
    participant Loader as PDF Loader
    participant Splitter as Text Splitter
    participant Embeddings as OpenAI Embeddings
    participant FAISS as FAISS

    PDF->>Loader: Carregar documento
    Loader->>Splitter: Extrair texto
    Splitter->>Embeddings: Gerar embeddings
    Embeddings->>FAISS: Armazenar vetores

4.2 Pergunta e Resposta

sequenceDiagram
    participant User as Usuário
    participant UI as Gradio
    participant Retriever as Retriever
    participant FAISS as FAISS
    participant LLM as OpenAI

    User->>UI: Envia pergunta
    UI->>Retriever: Encaminha pergunta
    Retriever->>FAISS: Busca contexto
    FAISS-->>Retriever: Retorna trechos
    Retriever->>LLM: Pergunta + contexto
    LLM-->>UI: Retorna resposta
    UI-->>User: Exibe resposta
    
5. Estrutura de Módulos

app/
├── main.py
├── config.py
├── pdf_loader.py
├── rag_pipeline.py
└── __init__.py

6. Decisões Técnicas
Decisão	Justificativa
FAISS local	Simplicidade e execução offline
Gradio	Interface rápida para MVP
OpenAI Embeddings	Integração direta com LangChain
PDF fixo	Escopo controlado
Sem memória	Evita complexidade
Sem banco relacional	Não necessário para o MVP
7. Limites da Arquitetura

Não contempla:

múltiplos documentos
upload de arquivos
autenticação
histórico de conversa
deploy em nuvem
reranking
busca híbrida