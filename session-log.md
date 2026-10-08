# Registro de sessões

<!-- Sessões são projetadas de .ai-tutor/state.json e mantêm o session_id. -->

## session_0c9c87a6-2beb-42e0-ba3b-0fce29ea95fb

- Status: completed (2026-10-01T01:23:29Z → 2026-10-01T01:45:28Z)
- Objetivo: Concluir o diagnóstico de entrada (diagnostic_entrada_001), uma pergunta por tópico.
- Domínio após diagnóstico:
  - Modelos, tokens, contexto e reasoning: 20
  - Prompts como interface de engenharia: 20
  - Arquitetura de aplicações com IA: da requisição ao comportamento: 20
  - Memória, contexto e estado: 0
  - Tools e function calling: 20
  - MCP, skills, plugins e integrações: 40
  - Assistentes, automações e workflows: 20
  - Agentes e subagentes: 40
  - IDEs, CLIs, super apps, assistentes pessoais e modelos locais: 40
  - Segurança: harness, permissões, credenciais e prompt injection: 20
  - Avaliação de soluções com IA: 0
- Resumo:
  - Mais forte: MCP/integrações (40), subagentes (40), modelos locais vs nuvem (40).
  - Base parcial (20): contexto, prompts, arquitetura, tools, workflows, segurança.
  - Sem base (0): memória entre sessões, avaliação/evals.
  - Padrão transversal: fronteira modelo vs. sistema (weak point conceitual).
  - Ordem sugerida: chamada stateless + camadas da aplicação → prompts como contrato → tools → memória → workflows/agentes → segurança no harness → avaliação.
- Ponto fraco aberto: weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885 — Fronteira modelo vs. sistema: atribui ao modelo ações que o código/harness executa ou garante (encaminhar ticket, chamar a API de clima, impedir ação maliciosa).
- Evidências: evidence_21c721e6-8fe7-4dfc-a4b4-9c36228f3576, evidence_395bc1af-dd2a-4ebb-88d1-0b9196a18e20, evidence_f141966b-d798-4a30-9f62-e2a02a5e6523, evidence_23320156-607a-4fa6-9175-03a9de3a5212, evidence_3110bc5d-57a2-44ca-97a4-25712b99ffbf, evidence_f46bdc28-2004-4450-9a2e-850d98fabdf4, evidence_a85c8f46-ac57-4044-84ea-6d26e28af04f, evidence_3a5d8d2d-16be-4a1b-a936-da8c2bab4095, evidence_4a24846b-6faa-41ff-ae70-99c5def008a5, evidence_f33ff488-e22e-4b4c-87a3-cbff4cc5aa66
- Próximo passo: Montar currículo

## session_634d4ad2-32da-42f7-84f6-4e3ecfbea2f3

- Status: interrupted (retomável) — 2026-10-03T17:24:03Z → 2026-10-03T18:20:23Z
- Objetivo: M01: explicar e demonstrar por que o assistente 'esquece' (stateless, histórico reenviado, janela, context rot, compactação).
- Lição: lesson_m01_modelos_tokens_contexto (in_progress)
- Feito: pré-requisito (nunca chamou API via código); 5 ideias construídas por perguntas (stateless, reenvio pelo harness, janela/custo linear-quadrático, context rot, reasoning tokens); primeira chamada à API OpenAI rodada pelo aluno (37/176/213 tokens).
- Ajuste: aluno declarou nível iniciante em Python → evidência via previsão/modificação; sincronização com python_automacoes-tutor no currículo.
- Domínio do tópico: 20 (sem mudança; evidências guiadas/parciais)
- Evidências: evidence_2a59ab7c-8128-45a5-814e-0e4e148fc926, evidence_a493c7ca-06c2-4858-90fc-1cde139fe2ea, evidence_e813682a-d4cf-4633-b712-319800c122a1, evidence_8c5f8420-98a9-433c-b307-80093ac3aab1
- Checkpoint: Pausa a pedido do aluno. conversa.py pronto (não rodado). Pendente: PREVISÃO (a) prompt_tokens turnos 1→3, (b) nome e 🚀 após /esquecer, (c) prompt_tokens turno 5 vs 3.
- Próximo passo: Retomar pedindo a previsão; depois rodar, comparar, modificação de 1 linha (instrução no system → transferência), Feynman das 5 ideias.

## Correção de estado — 2026-10-07 (não é sessão de estudo)

- Motivo: o `validate_study` reprovava o estudo com 186 erros. Plano em `docs/plano-correcao-estado.md`.
- Skill em uso: `14lucas-mendes/ai-tutor-skill`, commit `bd567cd`.
- Script: `.ai-tutor/migrations/2026-10-07-correcao-estado.py` (idempotente; estado anterior no commit `ee788bc`). Resultado: `STUDY VALIDATION: PASS`.
- Decisão sobre o domínio: o diagnóstico não é evidência. As 10 respostas de `diagnostic_entrada_001` saíram de `evidences` e viraram observações do diagnóstico. A de Avaliação (Q11), que faltava, foi reconstruída a partir da evidência.
  - Os domínios 20 e 40 da seção "Domínio após diagnóstico" acima ficam como histórico. Hoje, todos os tópicos estão em 0, exceto Modelos, tokens, contexto e reasoning.
  - Estimativa de ponto de partida (confiança baixa, uma sondagem por tópico):
    - provável domínio: MCP, subagentes, formatos;
    - parcial: contexto, prompts, arquitetura, tools, workflows, segurança;
    - lacuna: memória, avaliação.
  - Modelos, tokens, contexto e reasoning: fica em 20, com as 4 evidências da M01. Pela matriz, cabe 20 ou 40, e a reavaliação fica para quando a M01 fechar. O 60 exige Feynman e aplicação autônomos corretos.
- Ponto fraco `weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885`: continua ativo, sem evidências de apoio. A origem está nas observações q2, q5 e q10 do diagnóstico.
- Outros ajustes:
  - fontes com os nomes de campo do contrato. A OWASP tinha só o ano, que foi para `publication_year`;
  - referências de evidência apontando para a sessão;
  - nome do projeto M01.
- Próximo passo: retomar `session_634d4ad2-32da-42f7-84f6-4e3ecfbea2f3`, na previsão do experimento `conversa.py`.
