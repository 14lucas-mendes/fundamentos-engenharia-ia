"""M01 — primeira chamada à API (material de estudo, fornecido pelo tutor).

Uma chamada = uma requisição stateless: tudo o que o modelo "sabe" nesta
resposta está na lista `messages` abaixo. Nada mais.
"""
import os

from openai import OpenAI

MODELO = os.environ.get("OPENAI_MODEL", "gpt-5-mini")

client = OpenAI()  # lê a chave de OPENAI_API_KEY; nunca escreva a chave no código

messages = [
    {"role": "system", "content": "Você é um assistente conciso. Responda em português."},
    {"role": "user", "content": "Em uma frase: o que é um token num LLM?"},
]

resposta = client.chat.completions.create(model=MODELO, messages=messages)

print("Resposta:", resposta.choices[0].message.content)
print()
print("Tokens de entrada (prompt):  ", resposta.usage.prompt_tokens)
print("Tokens de saída (completion):", resposta.usage.completion_tokens)
print("Total:                       ", resposta.usage.total_tokens)
