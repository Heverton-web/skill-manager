---
name: rtk
description: Redundancy Reduction Toolkit — Truncagem e minificação de comandos CLI.
---

# rtk — Proxy de Comandos CLI

## Diretrizes de Uso
1. **Filtro de Terminal:** Intercepta a saída de comandos ruidosos (`git status`, `npm test`, `pytest`, `eslint`).
2. **Eliminação de Boilerplate:** Remove avisos de depreciação repetitivos e linhas em branco.
3. **Saída Telegráfica:** Retorna apenas o código de erro, exceção ou contagem de testes falhos/passados.
