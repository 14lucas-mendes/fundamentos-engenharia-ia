# Currículo — Fundamentos da Engenharia de IA

<!-- Itens são adicionados pelo workflow de currículo com IDs estáveis. -->

**Versão:** 1 · **Criado em:** 2026-09-30 · **Base:** diagnóstico `diagnostic_entrada_001` + fontes em `.ai-tutor/sources.json`
**Nota (2026-10-07):** o rótulo `diagnóstico:` em cada módulo é a estimativa de ponto de partida (parcial, provável domínio ou lacuna), não o domínio. O domínio vem só das evidências de aula.
**Ritmo:** ~3 h/semana (fins de semana) · **Estimativa:** ~22–26 semanas (≈ 6 meses)

## Princípio organizador

O diagnóstico mostrou um padrão transversal: a fronteira entre **o que o modelo faz** e **o que o sistema ao redor faz/garante**
(ponto fraco `weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885`). Toda a Fase 1 é construída para resolvê-lo; as fases seguintes o reaplicam
(tools, memória, segurança) até virar reflexo.

Modelo mental do curso: **o modelo recebe tokens e devolve tokens. Todo o resto — memória, ferramentas, permissões, validação,
encaminhamento — é software ao redor (o harness).**

## Regra de conclusão de cada item

Um item só fecha com **mastery ≥ 80**: uma explicação Feynman autônoma + uma aplicação autônoma + uma aplicação em **contexto novo**
(transferência), com IDs de evidência registrados. Ler a aula, rodar o código do repositório ou consumir mídia **não** conta como evidência.

Regra de prática (adaptada do relatório dos repositórios): resumir com suas palavras → digitar o código → rodar → **trocar o stub/`ToyLLM`
por chamada real à API** → explicar e modificar sem adivinhar.

## Sincronização com a formação de Python (`python_automacoes-tutor`)

Adicionado em 2026-10-03 a pedido do aluno. A formação de Python é a fonte da verdade do nível de Python; esta formação **lê** esse
nível e ajusta quanto código o aluno escreve. Ela não altera o roadmap da outra (que deixa IA/agentes/MCP fora do núcleo).

| Esta formação | Habilidade Python exigida para o aluno **escrever** | Na formação de Python | Até lá |
|---|---|---|---|
| M01 contexto | listas, dicionários, `while`, `input` | Python core — 80 ✅ | aluno prevê, roda e modifica |
| M02 arquitetura (backend, env var) | HTTP, cliente de API | Ciclo 6 — HTTP e APIs REST | código do tutor + previsão/modificação |
| M03 prompt-contrato (JSON Schema) | JSON, validação, exceções | Ciclo 4 — Arquivos, CSV e JSON (atual, 60) | aluno escreve a validação do JSON |
| M04 tools | funções + HTTP | Ciclos 6–7 | código do tutor; aluno escreve a função-tool |
| M05 memória | JSON em arquivo; depois SQL | Ciclos 4–5 | aluno escreve salvar/carregar em JSON |
| M11 avaliação | pytest | já validado (Git/testes — 80); aprofunda no Ciclo 12 | aluno escreve os testes de eval |

Regras:
- **Conceito ≠ autoria.** Evidência de IA vem de explicar, prever, modificar e transferir; escrever Python é bônus até o ciclo correspondente.
- **A cada avanço na formação de Python**, reler o domínio dela no início da sessão daqui e subir o nível de autoria.
- Código que o aluno escrever aqui pode virar exercício lá (e vice-versa), sem contar duas vezes a mesma evidência.

---

## Fase 1 — O sistema por baixo do chat (semanas 1–7)

### [ ] M01 · Modelos, tokens, contexto e reasoning — `topic_modelos_tokens_contexto` (diagnóstico: parcial)
- **Capacidade observável:** explicar por que um assistente "esquece" numa conversa longa usando: chamada *stateless*, histórico reenviado,
  janela de contexto finita, *context rot*, compactação.
- **Prática:** script que conversa com a API montando o histórico manualmente; medir tokens por turno; reproduzir o "esquecimento".
  (`from-scratch` Fase 0 — primeira chamada real.)
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_anthropic_context_eng`, `source_huyen_ai_eng`.

### [ ] M02 · Arquitetura de aplicações com IA — `topic_arquitetura_aplicacao` (diagnóstico: parcial · ponto fraco ativo)
- **Capacidade observável:** desenhar o caminho navegador → backend → provedor → resposta; dizer onde a chave mora e por quê;
  classificar cada responsabilidade como *do modelo* ou *do código*.
- **Prática / projeto P1:** mini backend "Resumir documento" (chave só no servidor, em variável de ambiente).
- **Evidências exigidas:** feynman · application (P1) · application+transfer.
- **Fontes:** `source_claude_tool_use`, `source_huyen_ai_eng`.

### [ ] M03 · Prompts como interface de engenharia — `topic_prompts_interface` (diagnóstico: parcial)
- **Capacidade observável:** escrever um prompt como **contrato de saída** consumido por código: formato fixo/JSON Schema, valores
  permitidos, caso "nenhuma das categorias", validação e fallback no código.
- **Prática / projeto P2:** classificador de tickets (`cobranca|bug|duvida|cancelamento|outro`) com structured output + validação.
  (`from-scratch` Fase 11 — prompting.)
- **Evidências exigidas:** feynman · application (P2) · application+transfer.
- **Fontes:** `source_openai_structured`, `source_anthropic_context_eng`.

## Fase 2 — O sistema ganha capacidades (semanas 8–14)

### [ ] M04 · Tools e function calling — `topic_tools_function_calling` (diagnóstico: parcial)
- **Capacidade observável:** explicar e implementar o ciclo `tool_use → sua aplicação executa → tool_result`; distinguir client tools
  e server tools; projetar uma tool boa para agentes.
- **Prática:** `from-scratch` Fase 11 (function calling) + Fase 14 aula 01 (agent loop) trocando `ToyLLM` pela API real; tool de clima.
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_claude_tool_use`, `source_anthropic_tools`.

### [ ] M05 · Memória, contexto e estado (inclui recuperação/RAG) — `topic_memoria_estado` (diagnóstico: lacuna)
- **Capacidade observável:** implementar memória entre sessões (armazenamento externo → injetado no contexto), comparar histórico
  completo, resumo/compactação, memória como tool e recuperação (RAG) — e dizer quando usar cada um.
- **Prática / projeto P3:** chatbot da loja que lembra nome e reclamação da semana anterior. (`from-scratch` Fase 14 — memória.)
  Opcional: consertar `agentic_rag` do `ai-engineering-hub` (fixar versões, corrigir manifesto, escrever um teste).
- **Evidências exigidas:** feynman · application (P3) · application+transfer.
- **Fontes:** `source_anthropic_context_eng`, `source_claude_memory`, `source_huyen_ai_eng`.

### [ ] M06 · MCP, skills, plugins e integrações — `topic_mcp_integracoes` (diagnóstico: provável domínio)
- **Capacidade observável:** explicar host / client / server e primitivas (tools, resources, prompts); diferenciar MCP de skill
  (progressive disclosure) e de plugin; construir e conectar um servidor MCP simples.
- **Prática:** servidor MCP mínimo (ex.: consulta a tickets) usado por um host como Claude Code. (`from-scratch` Fase 13.)
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_mcp_spec`, `source_anthropic_skills`, `source_programe_trilha`.

## Fase 3 — Escolhendo o formato da solução (semanas 15–20)

### [ ] M07 · Assistentes, automações e workflows — `topic_assistentes_workflows` (diagnóstico: parcial)
- **Capacidade observável:** escolher entre workflow e agente pelo critério *o caminho é conhecido de antemão?*; aplicar padrões
  (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); posicionar aprovação humana.
- **Prática:** workflow das notas fiscais com dados simulados.
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_anthropic_effective_agents`, `source_openai_agents_guide`.

### [ ] M08 · Agentes e subagentes — `topic_agentes_subagentes` (diagnóstico: provável domínio)
- **Capacidade observável:** implementar um agent loop com condição de parada; decidir quando dividir em subagentes (contexto isolado
  × custo ~15× tokens × coordenação).
- **Prática:** `from-scratch` Fase 14 aulas 01–12 + aulas selecionadas da Fase 16 (multi-agent).
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_anthropic_multiagent`, `source_anthropic_effective_agents`, `source_claude_code_sandboxing`.

### [ ] M09 · IDEs, CLIs, super apps, assistentes pessoais e modelos locais — `topic_formatos_ferramentas` (diagnóstico: provável domínio)
- **Capacidade observável:** recomendar o formato a partir de requisitos (privacidade, custo, qualidade, contexto, manutenção) e
  explicitar o trade-off aceito.
- **Prática:** rodar um modelo local (Ollama) e comparar com um modelo na nuvem no mesmo resumo (qualidade, tempo, limite de contexto).
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** documentação oficial das ferramentas (a registrar na aula), `source_claude_code_sandboxing`.

## Fase 4 — Confiabilidade (semanas 21–26)

### [ ] M10 · Segurança: harness, permissões, credenciais e prompt injection — `topic_seguranca_harness` (diagnóstico: parcial)
- **Capacidade observável:** identificar a *lethal trifecta*; propor defesas **no sistema** (menor privilégio, confirmação humana para
  efeitos colaterais, allowlist, sandbox, tratar conteúdo externo como dado) em vez de só no prompt; proteger credenciais.
- **Prática:** agente de e-mail simulado — atacar com injeção indireta e bloquear sem depender do modelo obedecer.
  (`from-scratch` Fase 14 aulas 26–30.)
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_owasp_llm` (LLM01, LLM05, LLM06), `source_willison_trifecta`, `source_claude_code_sandboxing`, `source_openai_agents_guide`.

### [ ] M11 · Avaliação de soluções com IA — `topic_avaliacao_ia` (diagnóstico: lacuna)
- **Capacidade observável:** montar conjunto de casos com resposta esperada, fazer error analysis, comparar versões no mesmo conjunto,
  detectar regressão e lidar com não determinismo.
- **Prática:** eval do classificador P2 (≥ 30 casos) comparando duas versões do prompt.
- **Evidências exigidas:** feynman · application · application+transfer.
- **Fontes:** `source_hamel_evals`, `source_anthropic_evals`, `source_huyen_ai_eng`.

### [ ] Capstone — integração
Um assistente pequeno que use M02–M05 + M10 + M11 (backend, prompt-contrato, tool, memória, guardrails no harness e eval).
Pode partir de um capstone da Fase 19 do `from-scratch`, desde que use API real.

---

## Alinhamento com referências externas (verificado em 2026-09-30)

- **programe.ai (Rafael Quintanilha):** o 1º curso da trilha tem o mesmo nome e cobre modelos, tokens, prompts, tools, MCPs, skills,
  agentes, harness e segurança — coincide com M01–M10. Os cursos seguintes da trilha (Programação Agêntica; Harness Engineering) são
  continuação natural **depois** deste. A página não informa carga horária nem projetos.
- **Mudança de vocabulário na indústria:** a Anthropic trata *context engineering* como evolução de *prompt engineering* → coberto em M01/M03/M05.
- **MCP:** a especificação mais recente listada é **2026-07-28**, descrita como stateless — confirmar na aula M06 lendo a spec.
- **Segurança:** OWASP Top 10 LLM 2025 coloca Prompt Injection (LLM01) e Excessive Agency (LLM06) no centro → M10.
- **Avaliação:** Anthropic e Hamel Husain/Shreya Shankar tratam evals e error analysis como prática central → M11.
- **Lacunas assumidas:** fine-tuning, infraestrutura de produção (Fase 17 do `from-scratch`) e programação agêntica ficam fora deste curso.
