# SPEC — Comando `/criar-livro`: Produção Autônoma e Paralela de Livro Técnico

Este documento especifica o processo ponta a ponta disparado pelo comando
`/criar-livro <tema>` (definido em `.claude/commands/criar-livro.md`), que é o ponto de
entrada único da Fábrica Agêntica de Livros: o operador informa o tema central da obra
e o comando conduz a produção inteira — pesquisa, arquitetura, redação paralela capítulo a
capítulo, arte final comercial e compilação em Markdown e PDF — respeitando as diretrizes
definidas em `CLAUDE.md`.

## 1. Sintaxe e disparo

```
/criar-livro <tema central da obra>
```

Exemplo:

```
/criar-livro Observabilidade em Sistemas Distribuídos com OpenTelemetry
```

- `$ARGUMENTS` é o texto livre após o nome do comando; é usado como tema de pesquisa
  (Fase 1) e como base do título de trabalho da obra.
- Se `$ARGUMENTS` vier vazio, o comando solicita o tema ao operador na pergunta inicial. **Após essa definição do tema, não haverá nenhuma outra interação com o operador.**
- **Fora do Claude Code:** peça diretamente ao agente "siga o processo de `.claude/commands/criar-livro.md` para o tema X".

## 2. Natureza do processo: esteira 100% autônoma e paralela

Por causa da **REGRA 3 (Autonomia Total Agêntica)**, este comando executa em modo **lote autônomo**. Após a definição do tema inicial, a esteira não realiza nenhuma pausa para aprovação manual no chat. O Orquestrador Mestre gerencia a execução e instancia **Subagentes de Execução Paralela** para otimizar o tempo de redação e ilustração técnica dos capítulos.

## 3. Máquina de estados de alto nível

```
[tema informado]
       │
       ▼
┌─────────────────────┐
│ Passo 0 — Preparação │  slug da obra, registro inicial em db_state
└─────────┬────────────┘
          ▼
┌──────────────────────────────┐
│ Passo 1 — Fase 1 (P&D)        │  pesquisador / subagente-pesquisador → arquiteto → sumario_macro.json
└─────────┬──────────────────────┘
          ▼
   ╔══════════════════════════════════════════════════════════════╗
   ║ Passo 2 — Fase 2 (Manufatura Paralela por Capítulos)         ║
   ║  [subagente-redator-capitulo] (em paralelo por capítulo)      ║
   ║   (estrategista → redator-eita → auto-validação)             ║
   ║                             │                                ║
   ║                             ▼                                ║
   ║  [subagente-ilustrador] geram diagramas conceituais          ║
   ╚══════════════════════════════════════════════════════════════╝
          │ (todos os capítulos concluídos e diagramados)
          ▼
┌───────────────────────────────────────┐
│ Passo 2.5 — Fase 3.5 (Arte Final)     │  subagente-arte-final gera capa.svg e contracapa.svg
└─────────┬─────────────────────────────┘  após analisar a obra completa concluída
          ▼
┌───────────────────────────────────────┐
│ Passo 3 — Fase 4 (Acabamento & ABNT)  │  compilador-abnt: merge + ABNT → livro_final.md
│                                         │  Nó 10: pdf_gen (CloudConvert) → livro_final.pdf
└─────────┬───────────────────────────────┘
          ▼
┌──────────────────────┐
│ Passo 4 — Relatório    │  caminhos finais + estatísticas autônomas
└──────────────────────┘
```

## 4. Especificação detalhada por etapa

### Passo 0 — Preparação
| | |
|---|---|
| Entrada | `$ARGUMENTS` (tema) |
| Ação | Deriva `slug` em kebab-case do tema; verifica se `output/<slug>/` já existe |
| Caso de borda | Se a pasta já existir com conteúdo, gera automaticamente um sufixo (ex.: `<slug>-v2`) para garantir execução autônoma sem sobrescrever dados anteriores |
| Efeito colateral | Grava linha inicial em `data/estado_fabrica.db` via MCP `db_state`: `fase_atual="fase_1_pesquisa"`, `estado_execucao="iniciado_via_comando"` |

### Passo 1 — Fase 1 (P&D e Inteligência)
| | |
|---|---|
| Agente | `pesquisador` / `subagente-pesquisador` depois `arquiteto` |
| Entrada | Tema (`$ARGUMENTS`) |
| Saída | `output/<slug>/pesquisa/dossie_<slug-do-tema>.md`, `output/<slug>/sumario_macro.json` |
| Autonomia | O Orquestrador prossegue diretamente para a produção assim que o `sumario_macro.json` for gerado, sem pausar para confirmação manual |

### Passo 2 — Fase 2 (Manufatura Tática Paralela) & Fase 3 (Ilustração de Capítulos + Design por Parte + Skills de Design)
| | |
|---|---|
| Agentes/Subagentes | `subagente-redator-capitulo` (processamento paralelo) → `subagente-ilustrador` (capítulos) + **`subagente-design-por-parte`** 🆕 (Partes, em paralelo) |
| Entrada | Coordenadas `{parte, capitulo}` para capítulos; `{slug, parte_atual}` para Partes |
| Saída por capítulo | `cap_<n>_draft.json`, `cap_<n>.md`, `cap_<n>_estado.json`, `cap_<n>_diagrama_<m>.svg` (MCP image_gen), `cap_<n>_diagrama_<m>_animado.svg` (skill `svg-animations`), `cap_<n>_landing.html` (skill `huashu-design`, primeiro capítulo de cada Parte) |
| Saída por Parte | `selo_parte_<n>.html` + `.svg` (skill `reversa-selo-generativo`), `parte_<n>_conceitos_animados.svg` (skill `svg-animations`), `parte_<n>_landing.html` (skill `huashu-design`) |
| **Auto-Validação** | Cada subagente aplica verificação técnica e validação pedagógica EITA antes de transicionar o estado para `concluido_autonomo` |
| Restrição de Arte | Nesta fase são gerados **diagramas conceituais + animados + landing pages + selos generativos por Parte**. **Capa e Contracapa NÃO são geradas nesta fase** |
| Skills auxiliares (Fase 3) | `reversa-selo-generativo` — selo generativo seeded p5.js para cada Parte; `svg-animations` — diagramas SVG animados SMIL/CSS para capítulos e Partes; `huashu-design` — landing pages premium com design direction advisor mode |

### Passo 2.5 — Fase 3.5 (Arte Final da Obra Completa — com Skills de Design)
| | |
|---|---|
| Subagente | `subagente-arte-final` |
| Pré-condição | 100% dos capítulos do sumario_macro concluídos e ilustrados com diagramas |
| Saída | `output/<slug>/imagens/capa.svg` (MCP image_gen), `output/<slug>/imagens/contracapa.svg` (MCP image_gen), `output/<slug>/imagens/selo_parte_<n>.html` (skill `reversa-selo-generativo`), `output/<slug>/imagens/capa_conceito.html` (skill `huashu-design`), `output/<slug>/imagens/ecossistema_animado.svg` (skill `svg-animations`) |
| Regra de Negócio | A Capa, Contracapa, selos e diagramas finais são gerados apenas quando o conteúdo completo do livro já estiver terminado, garantindo sinopse fiel e alinhamento visual com a obra finalizada |
| Skills auxiliares (Fase 3.5) | `huashu-design` — landing page conceito da capa com 3 variações visuais; `svg-animations` — diagrama SVG animado do ecossistema completo da obra; `reversa-image-prompt-json` — prompt estruturado para capa/contracapa de alta qualidade; `archify` — diagramas interativos de arquitetura/workflow/sequência; `dashi-ppt` — deck de apresentação do livro completo |

### Passo 3 — Fase 4 (Acabamento & ABNT) + exportação em PDF
| | |
|---|---|
| Agente | `compilador-abnt` (Nós 5–10) |
| Pré-condição | Capa, Contracapa e todos os capítulos finalizados |
| Saída | `output/<slug>/livro_final.md` (Nó 9) e `output/<slug>/livro_final.pdf` (Nó 10, via MCP `pdf_gen`/CloudConvert) |
| Caso de borda | Se `CLOUDCONVERT_API_KEY` não estiver configurada, o Nó 10 não bloqueia o Nó 9: o Markdown é expedido normalmente e a pendência do PDF é reportada |

### Passo 4 — Relatório final
Mensagem objetiva (REGRA 2) informando: caminho de `livro_final.md`, status de `livro_final.pdf`, total de capítulos produzidos e resumo de subagentes executados.

## 5. Contratos de dados usados no processo

- `templates/payload_estado.json` — payload genérico de estado inter-agentes.
- `output/<slug>/sumario_macro.json` — schema do `arquiteto` (coordenadas de partes e capítulos).
- `output/<slug>/capitulos/cap_<n>_draft.json` — draft pedagógico do capítulo (3 pilares EITA).
- `output/<slug>/capitulos/cap_<n>_estado.json` — espelha `payload_estado.json` (`estado_execucao: "concluido_autonomo"`).
- Tabela `estado_esteira` em `data/estado_fabrica.db`.

## 6. Casos de erro e de borda cobertos

| Situação | Comportamento esperado |
|---|---|
| Tema vazio | Solicita o tema na pergunta inicial e inicia a esteira autônoma |
| Obra com o mesmo slug já existe | Deriva automaticamente `<slug>-v2` mantendo o fluxo 100% autônomo |
| Falha na validação do capítulo | Subagente reaplica a correção internamente (REGRA 4) até atingir conformidade EITA |
| `CLOUDCONVERT_API_KEY` ausente | Markdown expedido normalmente; pendência registrada objetivamente |

## 7. Economia Severa de Tokens & Diretrizes Operacionais

Toda a esteira autônoma do comando `/criar-livro` opera sob as regras estritas:
1. **lean-ctx**: `grep_search` antes de `view_file`.
2. **headroom**: compressão de logs/outputs.
3. **caveman**: comunicação telegráfica sem prolixidade.
4. **rtk-memory**: registros de exceção/erros persistidos diretamente no `RTK SCRATCHPAD`.
5. **pre-flight-check**: validações executadas obrigatoriamente.
