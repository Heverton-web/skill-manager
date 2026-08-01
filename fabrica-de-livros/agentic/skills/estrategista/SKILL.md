---
name: estrategista
description: Fase 2 (Nós 1-2) da Fábrica Agêntica de Livros — decompõe o tema de um capítulo aprovado no sumário macro em três pilares lógicos de ensino, travando a execução para evitar desvios conceituais. Use no início da manufatura de cada capítulo, antes do Skill_Redator_EITA.
---

# Skill_Estrategista

Você é o operário de prototipagem tática da Fábrica Agêntica de Livros
(Fase 2, Nó 1 — Injeção de Requisitos, e Nó 2 — Prototipagem).

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- Trave-se exclusivamente às coordenadas (`parte`/`capitulo`) recebidas de
  `output/<livro>/sumario_macro.json` — não invente capítulos fora do sumário.

## Objetivo
Decompor o tema do capítulo nos pilares lógicos de ensino que servirão de esqueleto
para a redação EITA, evitando dispersão conceitual.

## Regra Transformacional (entre linhas)
Cada pilar deve ser projetado para levar o leitor de um estado de "não sei" a "domino
isso". Isso NÃO é dito explicitamente — é implementado através da escolha do que
ensinar, na ordem em que ensinar, e da profundidade de cada pilar.

**Progressão por pilar:**
- Pilar 1 (Fundamento): o que o leitor precisa entender ANTES de qualquer coisa.
  Sem ele, nada mais faz sentido.
- Pilar 2 (Núcleo): o conceito-chave que o leitor dominará. É o coração do capítulo.
- Pilar 3 (Avançado/Conexão): o que separa um amador de um profissional.
  Este pilar deve fazer o leitor pensar "agora estou vendo o que os especialistas veem".

## Procedimento
1. Carregue as coordenadas do capítulo (`parte`, `capitulo`) e seu `objetivo` e
   `pilares_previstos` em `sumario_macro.json`.
2. Refine os 3 pilares lógicos previstos em pilares definitivos, cada um com:
   - Nome do pilar (conceito nuclear a ensinar).
   - Escopo (o que entra e o que fica de fora, explicitamente).
   - Ponto de ancoragem cognitiva esperado (`ancora_visual`): especifique aqui o
     **diagrama Mermaid** que o `redator-eita` deverá desenhar na seção Ilustra —
     tipo (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`...) e o que
     o diagrama precisa mostrar. Exemplo: `"flowchart LR do caminho de uma requisição
     do cliente até o cache semântico, com o ponto de decisão de invalidação"`.
   - `entrega_tecnica`: qual artefato de código a seção Técnica deve trazer para este
     pilar (linguagem + o que o código faz). É o insumo do CI de código (R12).
3. Monte o draft estratégico do capítulo seguindo o payload de estado
   (`templates/payload_estado.json`), preenchendo `payload_estrategico.pilares`:

```json
{
  "fase_atual": "fase_2_manufatura",
  "coordenadas": { "parte": "I", "capitulo": "1" },
  "estado_execucao": "draft_pronto_para_redacao",
  "payload_estrategico": {
    "pilares": [
      {
        "nome": "string",
        "escopo": "string",
        "ancora_visual": "string (tipo de diagrama Mermaid + o que ele mostra)",
        "entrega_tecnica": "string (linguagem + artefato de código a produzir)",
        "evolucao_leitor": "string (de X para Y — o que o leitor ganha ao dominar este pilar)"
      },
      {
        "nome": "string",
        "escopo": "string",
        "ancora_visual": "string (tipo de diagrama Mermaid + o que ele mostra)",
        "entrega_tecnica": "string (linguagem + artefato de código a produzir)",
        "evolucao_leitor": "string"
      },
      {
        "nome": "string",
        "escopo": "string",
        "ancora_visual": "string",
        "evolucao_leitor": "string"
      }
    ]
  }
}
```

4. Grave o draft em `output/<livro>/capitulos/cap_<capitulo>_draft.json`.

5. Entregue o draft ao `Skill_Redator_EITA`. Não escreva prosa final aqui — apenas a
   arquitetura tática do capítulo.
