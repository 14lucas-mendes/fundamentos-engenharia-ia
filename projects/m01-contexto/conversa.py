"""M01 — conversa.py: um harness mínimo (material de estudo, fornecido pelo tutor).

O que observar:
- O modelo NÃO guarda nada entre chamadas. Quem guarda é a lista `historico`.
- A cada turno, a lista INTEIRA é enviada de novo para a API.
- O comando /esquecer apaga uma mensagem da lista — e, para o modelo,
  ela passa a nunca ter existido.

Comandos:  sair  → encerra
           /esquecer → remove a primeira mensagem do usuário do histórico
"""
import os
import sys

from openai import OpenAI

sys.stdout.reconfigure(encoding="utf-8")  # acentos e emojis no console do Windows

MODELO = os.environ.get("OPENAI_MODEL", "gpt-5-mini")
client = OpenAI()  # lê OPENAI_API_KEY do ambiente

# A "memória" da conversa. Ela vive AQUI, no seu programa — não no modelo.
historico = [
    {"role": "system", "content": "Você é um assistente conciso. Responda em português."},
]


def esquecer_primeira_mensagem_do_usuario(mensagens):
    """Remove a primeira mensagem com role 'user'. Devolve True se removeu."""
    for indice, mensagem in enumerate(mensagens):
        if mensagem["role"] == "user":
            del mensagens[indice]
            return True
    return False


def mostrar_painel(uso, mensagens):
    """Mostra quanto esta chamada custou em tokens e o tamanho do histórico."""
    raciocinio = 0
    if uso.completion_tokens_details is not None:
        raciocinio = uso.completion_tokens_details.reasoning_tokens or 0

    print("-" * 50)
    print(f"Entrada (prompt_tokens):        {uso.prompt_tokens}")
    print(f"Saída (completion_tokens):      {uso.completion_tokens}")
    print(f"  dos quais raciocínio oculto:  {raciocinio}")
    print(f"Mensagens no histórico:         {len(mensagens)}")
    print("-" * 50)


while True:
    texto = input("\nVocê: ").strip()

    if texto.lower() == "sair":
        break

    if texto == "/esquecer":
        if esquecer_primeira_mensagem_do_usuario(historico):
            print(f"[harness] Primeira mensagem do usuário removida. "
                  f"Histórico agora tem {len(historico)} mensagens. (Nada foi enviado à API.)")
        else:
            print("[harness] Não há mensagem do usuário para remover.")
        continue

    # 1. O harness adiciona a sua mensagem à lista
    historico.append({"role": "user", "content": texto})

    # 2. O harness envia a lista INTEIRA (é aqui que o modelo "vê" a conversa)
    resposta = client.chat.completions.create(model=MODELO, messages=historico)
    conteudo = resposta.choices[0].message.content

    # 3. O harness guarda a resposta na lista, para a próxima chamada
    historico.append({"role": "assistant", "content": conteudo})

    print(f"\nModelo: {conteudo}")
    mostrar_painel(resposta.usage, historico)
