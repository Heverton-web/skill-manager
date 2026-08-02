---
name: headroom
description: Compressão reversível de logs, JSONs e payloads de ferramentas > 7 linhas.
---

# headroom — Proxy e Compressão de Logs/Payloads

## Diretrizes de Uso
1. **Compressão Automática:** Sempre que a ferramenta emitir logs ou saídas JSON com mais de 7 linhas, o `headroom` comprime mantendo as primeiras 3 linhas e as últimas 4 linhas.
2. **Reversibilidade:** Use `headroom_retrieve` se precisar inspecionar a saída completa original.
3. **Execução:** O proxy roda via CLI: `headroom proxy --port 8787` ou encapsulado via `headroom wrap <comando>`.
