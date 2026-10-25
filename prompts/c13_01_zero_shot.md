Atue como engenheiro de software sênior, especializado em testes de integração com Python e pytest.

CONTEXTO
Este repositório contém uma aplicação RAG já implementada, com carregamento e processamento de documentos PDF, geração de embeddings, indexação e recuperação de documentos com FAISS.

OBJETIVO
Analise o código e os testes existentes e gere novos testes de integração para verificar a comunicação entre os componentes de carregamento do PDF, processamento dos textos, indexação FAISS e recuperação de documentos.

CRITÉRIOS
- Utilize pytest e as dependências já disponíveis no projeto.
- Priorize testes funcionais de integração, verificando entradas, saídas e comportamentos observáveis entre os componentes.
- Considere os comportamentos definidos na implementação e na documentação existente.
- Evite testes redundantes e testes que exercitem somente funções isoladas.
- Não invente requisitos nem comportamentos não implementados.
- Não utilize chamadas reais à API OpenAI. Quando necessário, substitua apenas a dependência externa de embeddings por uma implementação local e determinística, preservando a integração real com o FAISS.
- Utilize arquivos ou diretórios temporários para não modificar dados e índices existentes.

RESTRIÇÕES
1. Crie os testes exclusivamente em tests/c13_test_integracao_zero_shot.py.
2. Não modifique o código da aplicação, os testes existentes ou as dependências.
3. Não implemente novas funcionalidades.
4. Execute os testes gerados uma única vez, utilizando o Python do ambiente virtual .venv.
5. Preserve os testes produzidos na primeira geração, mesmo que apresentem falhas. Não realize correções automáticas.
6. Não realize commits ou operações de Git.

REGISTRO DO EXPERIMENTO
- Salve uma cópia integral deste prompt em prompts/c13_01_zero_shot.md.
- Ao finalizar, informe:
  a) Quantidade de testes gerados;
  b) Quantidade de testes aprovados, reprovados e ignorados;
  c) Cenários de integração contemplados;
  d) Erros ou limitações identificados.

Se houver impedimentos técnicos, informe-os sem modificar o escopo do experimento.
