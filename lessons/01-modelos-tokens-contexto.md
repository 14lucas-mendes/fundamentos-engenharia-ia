# Lição 01 — Modelos, tokens, contexto e reasoning

- **Lesson ID:** `lesson_m01_modelos_tokens_contexto`
- **Item do currículo:** M01 · `topic_modelos_tokens_contexto`
- **Ponto fraco relacionado:** fronteira modelo vs. sistema (`weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885`)
- **Status:** in_progress

## Objetivo observável

Ao final, você consegue explicar **sem consultar**, e demonstrar com código, por que um assistente "esquece" numa conversa longa,
usando cinco ideias: **chamada stateless**, **histórico reenviado pela aplicação**, **janela de contexto finita (em tokens)**,
**degradação com contexto longo (context rot)** e **compactação**.

## Pré-requisitos

- Saber o que é uma requisição a uma API (enviar dados → receber resposta).
- Para a prática: Python 3 e uma chave de API (Anthropic ou OpenAI) em variável de ambiente. Alternativa sem custo: Ollama local.

## Fontes verificadas

- `source_anthropic_context_eng` — Anthropic, *Effective context engineering for AI agents*.
- `source_huyen_ai_eng` — Chip Huyen, *AI Engineering* (cap. sobre foundation models e prompt engineering).
- `source_from_scratch` — `ai-engineering-from-scratch`, Fase 0 (primeira chamada real à API).

## Explicação curta

1. **Token.** O modelo não lê palavras: lê *tokens* (pedaços de palavras). Tudo é medido em tokens — o limite de contexto, o custo e
   a velocidade. Português costuma gastar mais tokens por palavra que inglês.
2. **Uma chamada = uma função pura.** A API do modelo é *stateless*: cada requisição recebe uma lista de mensagens e devolve uma
   resposta. Entre uma chamada e outra o modelo **não guarda nada**.
3. **Quem "lembra" é a aplicação.** O chat parece ter memória porque o app (ChatGPT, Claude Code, seu backend) **reenvia o histórico
   inteiro** a cada mensagem. A "memória" da conversa é uma lista mantida pelo **código**, não pelo modelo.
4. **Janela de contexto.** Essa lista (system prompt + histórico + resultados de tools + a resposta que está sendo gerada) tem um
   limite em tokens. Quando chega perto dele, a aplicação precisa **cortar** ou **resumir** — e o que for cortado deixa de existir
   para o modelo.
5. **Context rot.** Mesmo *dentro* do limite, a precisão para recuperar uma informação cai à medida que o contexto cresce. O modelo
   **relê tudo** a cada chamada — o problema não é "não revisitar", é que a atenção se dilui entre muitos tokens.
6. **Compactação e sessões novas.** Resumir o histórico (ex.: `/compact` no Claude Code) ou começar uma sessão nova com um resumo
   são decisões **da aplicação** para manter o contexto pequeno e relevante. Instruções que precisam valer sempre vão para um lugar
   que é reinjetado em toda chamada (system prompt, `CLAUDE.md`), não para a mensagem nº 3 de uma conversa de 200.
7. **Reasoning.** Modelos com "thinking" geram tokens de raciocínio antes da resposta. Eles também ocupam orçamento de tokens
   (e custo) — raciocinar mais não é de graça.

## Exemplo concreto

```text
Chamada 1 → messages = [system, user1]
Chamada 2 → messages = [system, user1, assistant1, user2]
Chamada 3 → messages = [system, user1, assistant1, user2, assistant2, user3]
...
Chamada 80 → a lista passou do limite → o app resume ou descarta user1..user30
             → a instrução que você deu em user2 sumiu (ou virou uma linha de resumo)
```

Consequência prática: o custo de **cada** chamada cresce com a conversa, porque todos os tokens anteriores são reenviados.

## Prática guiada (projeto `projects/m01-contexto/`)

1. Script que chama a API com uma lista `messages` que **você** mantém em Python.
2. A cada turno, imprimir quantos tokens de entrada foram usados (o campo `usage` da resposta).
3. Experimento: na 1ª mensagem, dê uma instrução ("responda sempre em maiúsculas"). Depois, **remova** essa mensagem da lista e
   observe o comportamento. Quem esqueceu: o modelo ou o seu código?

## Tarefa autônoma (evidência)

- **Feynman:** explicar, sem consultar este arquivo, por que o assistente esquece instruções numa conversa longa e o que fazer —
  usando as cinco ideias do objetivo.
- **Aplicação:** o script da prática rodando, com a saída dos tokens por turno e o resultado do experimento.
- **Transferência:** um cenário novo, apresentado na sessão (não está neste arquivo).

## Erros esperados

- "O modelo não revisita o início" → na verdade ele relê tudo; o que acontece é corte/resumo pela aplicação ou context rot.
- "O modelo tem memória da conversa" → quem mantém o histórico é o código.
- Achar que uma janela maior resolve tudo → context rot e custo continuam.

## Critério de evidência

| Evidência | Conta quando |
|---|---|
| feynman | Explicação autônoma cobre as 5 ideias sem contradição relevante. |
| application | Script roda; saída mostra tokens crescendo e o efeito de remover a instrução. |
| application + transfer | Resolve corretamente o cenário novo sem ajuda além do enunciado. |

## Atualização de estado

Registrar cada evidência em `state.json` com `kind` = `feynman` / `application`, `autonomous`, `transfer` e o nível de ajuda usado.
Mastery 60 após feynman + application autônomos; 80 com a transferência. A lição só fecha com os três.
