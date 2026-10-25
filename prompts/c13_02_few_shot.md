Atue como engenheiro de software sênior, especializado em testes de integração com Python e pytest.

CONTEXTO
Este repositório contém uma aplicação RAG já implementada, com carregamento e processamento de documentos PDF, geração de embeddings, indexação e recuperação de documentos com FAISS.

OBJETIVO
Analise o código e os testes originais do projeto e gere novos testes de integração para verificar a comunicação entre os componentes de carregamento do PDF, processamento dos textos, indexação FAISS e recuperação de documentos.

Utilize a técnica few-shot. Considere os exemplos abaixo como referências para estruturar os casos de teste. Eles são ilustrativos e devem ser adaptados aos contratos e comportamentos efetivamente implementados.

EXEMPLO 1: Integração com dados válidos
Entrada: PDF temporário contendo informações conhecidas.
Ação: Carregar o PDF, processar os textos, gerar embeddings determinísticos, criar o índice FAISS e recuperar documentos.
Resultado esperado: O conteúdo recuperado deve corresponder aos dados previamente inseridos, respeitando os contratos dos componentes.

EXEMPLO 2: Integração com situação limite
Entrada: Documento com conteúdo que exige divisão em múltiplos fragmentos.
Ação: Processar o documento, indexar os fragmentos e realizar a recuperação.
Resultado esperado: Os fragmentos devem ser gerados e recuperados conforme as regras de processamento e os parâmetros existentes.

EXEMPLO 3: Integração com condição de erro
Entrada: Recurso de entrada inválido ou indisponível.
Ação: Executar o fluxo de carregamento e processamento.
Resultado esperado: O sistema deve apresentar o comportamento de erro previsto na implementação, sem assumir regras inexistentes.

CRITÉRIOS
- Utilize pytest e as dependências já disponíveis no projeto.
- Priorize testes funcionais de integração, verificando entradas, saídas e comportamentos observáveis entre os componentes.
- Considere os comportamentos definidos na implementação e na documentação existente.
- Utilize os exemplos como orientação, mas explore também outros cenários pertinentes.
- Evite testes redundantes e testes que exercitem somente funções isoladas.
- Não invente requisitos nem comportamentos não implementados.
- Não utilize chamadas reais à API OpenAI. Quando necessário, substitua apenas a dependência externa de embeddings por uma implementação local e determinística, preservando a integração real com o FAISS.
- Utilize arquivos ou diretórios temporários para não modificar dados e índices existentes.

RESTRIÇÕES
1. Crie os testes exclusivamente em tests/c13_test_integracao_few_shot.py.
2. Não consulte nem reutilize os testes ou prompts do experimento zero-shot, disponíveis em tests/c13_test_integracao_zero_shot.py e prompts/c13_01_zero_shot.md.
3. Não modifique o código da aplicação, os testes existentes ou as dependências.
4. Não implemente novas funcionalidades.
5. Execute os testes gerados uma única vez, utilizando o Python do ambiente virtual .venv.
6. Preserve os testes produzidos na primeira geração, mesmo que apresentem falhas. Não realize correções automáticas.
7. Não realize commits ou operações de Git.

REGISTRO DO EXPERIMENTO
- Salve uma cópia integral deste prompt em prompts/c13_02_few_shot.md.
- Ao finalizar, informe:
  a) Quantidade de testes gerados;
  b) Quantidade de testes aprovados, reprovados e ignorados;
  c) Cenários de integração contemplados;
  d) Erros ou limitações identificados.

Se houver impedimentos técnicos, informe-os sem modificar o escopo do experimento.
