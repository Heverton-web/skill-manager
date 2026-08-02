# SPEC — Comando `/criar-livro`: Produção Autônoma e Paralela de Livro Técnico

Este documento especifica o processo ponta a ponta disparado pelo comando
`/criar-livro <tema>` (definido em `.claude/commands/criar-livro.md`), que é o ponto de
entrada único da Fábrica Agêntica de Livros: o operador informa o tema central da obra
e o comando conduz a produção inteira — pesquisa, arquitetura, redação paralela capítulo a
capítulo e compilação em Markdown e PDF — respeitando as diretrizes
definidas em `CLAUDE.md`.

## 1. REQUISITOS CONTRATUAIS OBRIGATÓRIOS

Toda obra produzida pela Fábrica Agêntica de Livros DEVE atender:

| # | Requisito | Mínimo | Validação |
|---|-----------|--------|-----------|
| R1 | Capítulos por obra | 16 capítulos | Verificado no sumário macro |
| R2 | Páginas estimadas | 70 páginas (~175.000-210.000 caracteres em formato ABNT) | Verificado na compilação |
| R3 | Estrutura por capítulo | 7 seções: Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências | Template EITA-V2 |
| R4 | Referências por capítulo | Mínimo 3 referências no formato ABNT | Seção de referências de cada capítulo |
| R5 | Artigos científicos no dossiê | Mínimo 3 papers | Seção "Artigos Científicos" do dossiê |
| R6 | Formatação ABNT | Livro completo | Capa, sumário, referências, numeração |
| R7 | PDF final | 1 arquivo .pdf | Pandoc → `.typ` → Typst (obrigatório) |
| R8 | Linguagem | Simples para iniciantes, transformacional para PhDs | Tom em camadas |
| R9 | Sem horizontal rules | Nenhum `---` dentro dos capítulos | `auditar-obra.py` |
| R10 | Citações inline [N] | Mínimo 3 por capítulo | Vinculadas às referências |
| R11 | Diagrama por capítulo | 1+ bloco ```mermaid válido na seção Ilustra | `auditar-obra.py` + `renderizar-diagramas.py --validar` |
| R12 | Código validado | 1+ bloco de código na seção Técnica, aprovado no CI de sintaxe | `validar-codigo.py` |
| R13 | Sem truncamento | Nenhum TODO/placeholder/capítulo cortado | `auditar-obra.py` |
| R14 | Rastreabilidade | Todo `[N]` do corpo existe na seção 7 | `auditar-obra.py` |

**Violação de qualquer requisito = obra NÃO CONFORME.** A skill `revisor-tecnico`
(Fase 2.5) corrige as não conformidades detectáveis; o `compilador-abnt` reporta o que
restar antes da entrega.

**Verificação em um comando:**
```bash
python scripts/auditar-obra.py <slug> --estrito && python scripts/validar-codigo.py <slug> --estrito
```

## 2. Sintaxe e disparo

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

## 3. Natureza do processo: esteira 100% autônoma e paralela

Por causa da **REGRA 3 (Autonomia Total Agêntica)**, este comando executa em modo **lote autônomo**. Após a definição do tema inicial, a esteira não realiza nenhuma pausa para aprovação manual no chat. O Orquestrador Mestre gerencia a execução e instancia **Subagentes de Execução Paralela** para otimizar o tempo de redação e validação dos capítulos.

## 4. Máquina de estados de alto nível

```
[tema informado]
       │
       ▼
┌─────────────────────┐
│ Passo 0 — Preparação │  slug da obra, registro inicial em db_state
└─────────┬────────────┘
          ▼
┌──────────────────────────────┐
│ Passo 1 — Fase 1 (P&D)        │  pesquisador / subagente-pesquisador → indexar-dossie.py
│                               │  → arquiteto → sumario_macro.json
└─────────┬──────────────────────┘
          ▼
   ╔══════════════════════════════════════════════════════════════╗
   ║ Passo 2 — Fase 2 (Manufatura Paralela EM LOTES de 4)         ║
   ║  pool-capitulos.py --plano/--proximo-lote                     ║
   ║  [subagente-redator-capitulo] x4 por lote                     ║
   ║   (estrategista → redator-eita → mermaid → CI de código       ║
   ║    → auto-validação → --registrar sucesso/falha)              ║
   ║  retentativa com backoff exponencial (máx. 3 por capítulo)    ║
   ╚══════════════════════════════════════════════════════════════╝
          │
          ▼
   ╔══════════════════════════════════════════════════════════════╗
   ║ Passo 3 — Fase 2.5 (Peer Review Autônomo)                    ║
   ║  auditar-obra.py + validar-codigo.py + validação de diagramas ║
   ║  → revisor-tecnico / [subagente-revisor-tecnico] em lotes     ║
   ║  → revisao/parecer_revisao.md                                 ║
   ╚══════════════════════════════════════════════════════════════╝
          │
          ▼
┌───────────────────────────────────────┐
│ Passo 4 — Fase 3 (Acabamento & ABNT)  │  compilador-abnt: merge + ABNT → livro_final.md
│                                         │  Nó 9.5: mermaid → PNG | Nó 9.6: capa + CIP
│                                         │  Nó 10: Pandoc → .typ → Typst → livro_final.pdf
└─────────┬───────────────────────────────┘
          ▼
┌──────────────────────┐
│ Passo 5 — Relatório    │  caminhos finais + checklist R1-R14
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
| Saída | `output/<slug>/pesquisa/dossie_<slug-do-tema>.md`, `output/<slug>/pesquisa/indice_dossie.json`, `output/<slug>/sumario_macro.json` |
| Passo intermediário | `python scripts/indexar-dossie.py <slug> --indexar` (índice RAG do dossiê) |
| Autonomia | O Orquestrador prossegue diretamente para a produção assim que o `sumario_macro.json` for gerado, sem pausar para confirmação manual |

### Passo 2 — Fase 2 (Manufatura Tática Paralela em Lotes)
| | |
|---|---|
| Agentes/Subagentes | `subagente-redator-capitulo` (paralelo, **lotes de 4**) |
| Orquestração | `scripts/pool-capitulos.py <slug> --plano --lote 4` → despacha lote → aguarda o lote inteiro → `--proximo-lote` |
| Entrada | Coordenadas `{parte, capitulo}` + blocos do dossiê obtidos por RAG |
| Saída por capítulo | `cap_<n>_draft.json`, `cap_<n>.md`, `cap_<n>_estado.json` |
| **Auto-Validação** | Cada subagente roda `validar-codigo.py --capitulo <n>` e `renderizar-diagramas.py --capitulos --validar`, corrige (REGRA 4) e registra o desfecho no pool |
| **Resiliência** | Falha de subagente é retentada com backoff exponencial (15s → 30s → 60s, máx. 3 tentativas). Capítulo `esgotado` vira não conformidade reportada, sem travar a esteira |
| Estado do pool | `output/<slug>/capitulos/_pool_estado.json` |

### Passo 3 — Fase 2.5 (Revisão Técnica Autônoma / Peer Review)
| | |
|---|---|
| Agente | skill `revisor-tecnico` + `subagente-revisor-tecnico` (lotes de 4) |
| Pré-condição | Nenhum capítulo pendente no pool |
| Evidência | `revisao/relatorio_auditoria.json`, `validacao/relatorio_codigo.json`, `validacao/relatorio_diagramas.json` |
| Escopo da correção | Seções EITA faltantes, referências insuficientes, `---`, citações órfãs, diagrama inválido, código com erro de sintaxe, truncamento, **sobreposição de conteúdo entre capítulos** (Jaccard ≥ 0,45 em shingles de 6 palavras) e **grafia inconsistente de termos** |
| Saída | `output/<slug>/revisao/parecer_revisao.md` |
| Limite | Máximo de 3 rodadas de reauditoria; o que sobrar é reportado como ressalva |

### Passo 4 — Fase 3 (Acabamento & ABNT) + exportação em PDF
| | |
|---|---|
| Agente | `compilador-abnt` (Nós 5–10) |
| Pré-condição | Parecer da Fase 2.5 gravado |
| Nó 9.5 | `scripts/renderizar-diagramas.py <slug>` → `imagens/diagramas/*.png` + `_livro_render.md` |
| Nó 9.6 | `scripts/metadados_livro.py <slug>` → paleta, ficha catalográfica (CIP), sinopse |
| Nó 10 | `python compilar-para-pdf.py <slug> --paginas-exatas` (Pandoc → `.typ` → `typst compile --root`) |
| Saída | `output/<slug>/livro_final.md` (Nó 9) e `output/<slug>/livro_final.pdf` (Nó 10) |
| Caso de borda | Se Pandoc ou Typst não estiverem disponíveis, o Nó 10 reporta erro mas não bloqueia o Nó 9: o Markdown é expedido normalmente e a pendência do PDF é reportada |
| Caso de borda | Se o mermaid-cli não estiver instalado, os diagramas permanecem como blocos de código no PDF e a pendência é reportada — a compilação não falha |

### Passo 5 — Relatório final
Mensagem objetiva (REGRA 2) informando: caminho de `livro_final.md`, status de `livro_final.pdf`, total de capítulos, páginas do PDF, diagramas renderizados, taxa de aprovação do CI de código, veredito da auditoria e checklist R1-R14.

## 5. Contratos de dados usados no processo

Livro vive em `output/livros/<slug>/` (V4.1: raízes separadas por tipo de obra no
topo de `output/` — ver seção 1.5 do `CLAUDE.md`). `config_obra.json` (quando a
obra nasceu via `/esbocar`) fica na raiz da obra, sem subpasta `esboco/`. Nos
caminhos abaixo, `<slug>` já denota `livros/<slug>`.

- `templates/payload_estado.json` — payload genérico de estado inter-agentes.
- `output/<slug>/sumario_macro.json` — schema do `arquiteto` (coordenadas de partes e capítulos).
- `output/<slug>/capitulos/cap_<n>_draft.json` — draft pedagógico do capítulo (3 pilares EITA).
- `output/<slug>/capitulos/cap_<n>_estado.json` — espelha `payload_estado.json` (`estado_execucao: "concluido_autonomo"`).
- `output/<slug>/capitulos/_pool_estado.json` — tentativas e estado por capítulo no pool de concorrência.
- `output/<slug>/pesquisa/indice_dossie.json` — índice RAG (blocos + IDF) do dossiê.
- `output/<slug>/revisao/relatorio_auditoria.json` — requisitos automatizáveis (R1-R4, R9-R14), sobreposição, terminologia.
- `output/<slug>/validacao/relatorio_codigo.json` — status de sintaxe por bloco de código.
- `output/<slug>/validacao/relatorio_diagramas.json` — diagramas renderizados, em cache e com falha.
- Tabela `estado_esteira` em `data/estado_fabrica.db`.

## 6. Casos de erro e de borda cobertos

| Situação | Comportamento esperado |
|---|---|
| Tema vazio | Solicita o tema na pergunta inicial e inicia a esteira autônoma |
| Obra com o mesmo slug já existe | Deriva automaticamente `<slug>-v2` mantendo o fluxo 100% autônomo |
| Falha na validação do capítulo | Subagente reaplica a correção internamente (REGRA 4) até atingir conformidade EITA |
| Pandoc/Typst ausente | Markdown expedido normalmente; pendência do PDF registrada objetivamente |
| Subagente de capítulo falha ou trava | Pool registra a falha e retenta com backoff exponencial (máx. 3); depois marca `esgotado` e a esteira segue |
| Rate-limit da API (TPM/RPM) | Lotes de 4 + backoff exponencial reduzem a pressão; o lote seguinte só sai quando o anterior fecha |
| mermaid-cli ausente ou diagrama inválido | Bloco permanece como código no PDF; falha registrada em `relatorio_diagramas.json` |
| Código de capítulo com erro de sintaxe | `validar-codigo.py` reprova; `revisor-tecnico` corrige e revalida |
| Sobreposição de conteúdo entre capítulos | `revisor-tecnico` reescreve o trecho do capítulo posterior como referência cruzada |
| Slug novo fora do catálogo de `compilar-para-pdf.py` | O script aceita qualquer slug que exista em `output/` |

## 7. Economia Severa de Tokens & Diretrizes Operacionais

Toda a esteira autônoma do comando `/criar-livro` opera sob as regras estritas:
1. **lean-ctx**: `grep_search` antes de `view_file`.
2. **headroom**: compressão de logs/outputs.
3. **caveman**: comunicação telegráfica sem prolixidade.
4. **rtk-memory**: registros de exceção/erros persistidos diretamente no `RTK SCRATCHPAD`.
5. **pre-flight-check**: validações executadas obrigatoriamente.
