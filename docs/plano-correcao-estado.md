# Plano de correção do estado do tutor

Escrito em 2026-10-07, a partir de uma revisão feita na formação Python. A correção deve ser feita **numa sessão aberta neste projeto**, lendo este documento primeiro. Até lá, nada aqui foi alterado.

## Por que corrigir

O `validate_study` da skill `ai-tutor` reprova este estudo com **186 erros**. A skill em uso é o clone de [`14lucas-mendes/ai-tutor-skill`](https://github.com/14lucas-mendes/ai-tutor-skill), commit `bd567cd` ou mais novo, em `C:\Users\lucka\.config\mimocode\skills\ai-tutor`. O estado foi gravado com nomes de campo diferentes dos que o contrato exige. Um erro é de conteúdo: o diagnóstico de entrada foi gravado como evidência e virou domínio.

Para conferir o diagnóstico, rode a partir da raiz da skill:

```
python -m scripts.validate_study "E:\Lucas\Documents\Faculdade AI\Fundamentos da Engenharia de IA"
```

## O que está errado

| Grupo | Erros | Tipo |
|---|---|---|
| 19 fontes em `sources.json` com nomes de campo antigos | ~170 | mecânico |
| A execução `diagnostic_entrada_001` fora do formato do contrato | 9 | mecânico com julgamento |
| 10 respostas do diagnóstico gravadas em `evidences` (`kind: "diagnostic"`) e somadas ao domínio | — (o validador não pega) | **decisão** |
| Referências de evidência do tipo `conversation` (14 evidências) | 1 | mecânico |
| O ponto fraco `weak_01ebbe5b…` com `evidence_ids` e `status: "open"` | 3 | mecânico com decisão |
| O projeto `project_m01_contexto` sem `name` | 2 | mecânico |

### 1. Fontes (`sources.json`)

As 19 fontes usam nomes antigos. Basta renomear, sem mudar nenhum valor:

| Hoje | Contrato |
|---|---|
| `author` | `author_or_institution` |
| `published_or_updated` | `publication_date` |
| `type` | `source_type` |
| `why_authoritative` | `authority_reason` |
| (ausente) | `lesson_ids`: `["lesson_m01_modelos_tokens_contexto"]` para as fontes usadas na M01; `[]` para as demais |

O campo extra `access` pode ficar.

### 2. A execução do diagnóstico (`state.diagnostics[0]`)

Hoje as observações têm só `topic_id`, `evidence_id`, `recorded_at` e `note`, e o `summary` é uma lista de frases. O contrato (`references/diagnostic-contract.md`) pede, em cada observação:
- `observation_id`, com o prefixo `diagnostic_observation_`;
- `prompt` e `response`;
- `estimate`: `not_observed`, `unknown`, `weak`, `partial` ou `likely_known`;
- `confidence`: `low`, `medium` ou `high`;
- `direction`: `probe_up`, `probe_down` ou `probe_across`;
- `prerequisite_gap`, booleano;
- `reason` e `recorded_at`.

O `summary` pede itens `{topic_id, estimate, confidence, observation_ids}`.

Para montar cada observação:
- **`prompt`:** vem do `context` da evidência correspondente.
- **`response` e `reason`:** vêm do `error` e da `note`. Se o `session-log.md` tiver a resposta literal, use-a.
- **`estimate`:** `partial` para os que hoje estão em 20 e `likely_known` para os em 40 (MCP, subagentes, formatos). `topic_avaliacao_ia`, com resultado `incorrect`, fica `weak`.
- **`confidence`:** `low` (uma sondagem por tópico).

### 3. A decisão principal: diagnóstico não é evidência

O contrato é explícito: observações de diagnóstico "never populate `evidences`, attach to `evidence_ids`, or raise `mastery`". Hoje, 10 tópicos têm domínio 20 ou 40 vindo só dessas respostas:

| Tópico | Domínio hoje | Origem |
|---|---|---|
| `topic_mcp_integracoes`, `topic_agentes_subagentes`, `topic_formatos_ferramentas` | 40 | só diagnóstico |
| `topic_prompts_interface`, `topic_arquitetura_aplicacao`, `topic_tools_function_calling`, `topic_assistentes_workflows`, `topic_seguranca_harness` | 20 | só diagnóstico |
| `topic_avaliacao_ia` | 0 | diagnóstico incorreto |
| `topic_modelos_tokens_contexto` | 20 | 1 diagnóstico + 4 evidências reais da M01 |

**Recomendado: mover para o diagnóstico e recalcular o domínio.**
1. Tirar as 10 evidências `kind: "diagnostic"` de `evidences` e dos `evidence_ids` dos tópicos. O conteúdo delas não se perde, porque vira as observações do item 2.
2. Gravar a estimativa em `topics[].diagnostic` (`{estimate, confidence, diagnostic_id}`). Esse campo é informativo e ajuda a ordenar o currículo.
3. Os nove tópicos que só tinham diagnóstico voltam a `mastery: 0`, `status: "not_started"`.
4. Reavaliar `topic_modelos_tokens_contexto` pela matriz usando só as 4 evidências da M01:
   - Feynman parcial com degrau 3: teto 40;
   - duas aplicações autônomas parciais;
   - uma aplicação correta com degrau 4: teto 40.

   Pela matriz, 20 ou 40. O 60 exige Feynman **e** aplicação autônomos corretos, que ainda não existem.

O domínio cai no papel, mas o conhecimento não muda. O diagnóstico continua dizendo "começar além daqui" em MCP, subagentes e formatos, e essa informação fica no lugar certo.

**Alternativa (não recomendada): manter como está.** Seria preciso mudar o contrato da skill para todos os estudos. Isso também deixaria o domínio medir sondagens curtas, e não o que foi demonstrado.

### 4. Referências do tipo `conversation`

As 14 evidências usam `reference: {"type": "conversation", "id": "lesson_m01/retrieval_1"}`. O validador só aceita `lesson`, `session` ou `project`. Troque para `{"type": "session", "id": <session_id da evidência>, "location": <id antigo>}`. Assim a referência aponta para a sessão real e o rótulo antigo é preservado. Depois do item 3, sobram só as 4 evidências da M01.

### 5. O ponto fraco `weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885`

São três ajustes:
- renomear `evidence_ids` para `supporting_evidence_ids`;
- trocar `status: "open"` por `"active"`;
- decidir o que fazer com o apoio. As três evidências que o sustentam são diagnósticas e saem no item 3.

Opções para o apoio:
- **Recomendado:** manter o ponto fraco com `supporting_evidence_ids: []` e uma nota citando as observações do diagnóstico que o originaram. A fronteira entre modelo e sistema é uma lacuna real, observada três vezes, e vale acompanhar.
- Alternativa: arquivar (`status: "archived"`) e reabrir quando aparecer em evidência de aula.

### 6. Projeto sem nome

`project_m01_contexto` precisa de `name`, tirado do `curriculum.md` ou do `README` da pasta `projects/m01-contexto`.

## Como fazer, na sessão deste projeto

1. Ler este documento, o `SKILL.md` da skill e os contratos `architecture`, `state`, `learning`, `diagnostic` e `learner-profile`.
2. Decidir os itens 3 e 5. Os outros itens são mecânicos.
3. Fazer backup de `.ai-tutor/` numa pasta `.ai-tutor/migrations/2026-10-xx-correcao/` (ou confiar no git, que está limpo no commit `ee788bc`).
4. Escrever um script de migração único e idempotente em `.ai-tutor/migrations/`, como o estudo Python fez em 2026-09-12, que aplique os itens 1 a 6 e grave cada arquivo com `scripts.state_io.atomic_update_json` e `expected_revision`.
5. Rodar `validate_study` até dar `STUDY VALIDATION: PASS`.
6. Registrar no `session-log.md` o que mudou, o commit da skill em uso e a decisão sobre o domínio.
7. Atualizar o `curriculum.md`, se ele citar os domínios antigos.
8. Commitar no repositório `14lucas-mendes/fundamentos-engenharia-ia`.

Depois disso, retomar a sessão interrompida `session_634d4ad2…`, que o `next_focus` indica: a previsão do experimento `conversa.py` na M01.

## O que não mudar

- As 4 evidências reais da M01: só a referência muda (item 4).
- O texto das respostas e dos erros, que passa para o diagnóstico sem reescrita.
- O `learner-profile.json`, que está vazio e válido.

## Para a skill (opcional, no repositório da skill)

O validador aceita `kind: "diagnostic"` em `evidences` sem reclamar, e foi assim que o problema do item 3 passou despercebido. Vale um PR em `ai-tutor-skill` que rejeite esse `kind` em `evidences` e aponte para `state.diagnostics`.
