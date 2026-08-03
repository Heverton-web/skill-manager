# SPEC — SDLC AI-first (Software Development Life Cycle)

## 1. Visão Geral

**Título:** SDLC AI-first — Ciclo de Vida de Desenvolvimento de Software orientado a Agentes

**Tema central:** Reestruturar o ciclo de vida de desenvolvimento de software (SDLC) para um paradigma onde o agente de IA é o executor e o humano é o orquestrador + árbitro de qualidade. O artefato-mestre deixa de ser o documento/backlog e passa a ser a **spec executável + testes**, e a verificação deixa de ser fase final para ser **adversarial e contínua**.

**Contexto no repo:** Este esboço integra o ecossistema já existente — FABLE, skills (fable-judge, fable-loop, verification-before-completion, to-tickets, wayfinder, tdd, dispatching-parallel-agents, using-git-worktrees, self-learning), economia severa de tokens (CAVEMAN, HEADROOM, RTK, LEAN-CTX) e a Fábrica Agêntica de Livros como caso real de maturidade L3-L4.

**Formato:** Esboço conceitual + operacional (fases, papéis, maturidade, anti-padrões).

**Idioma:** PT-BR

## 2. Premissa Central

> SDLC tradicional otimiza **fases manuais**; SDLC AI-first otimiza **o contrato entre humano, agente e verificação**. O humano deixa de ser o executor e vira o **orquestrador + árbitro de qualidade** (spec-driven, verify-driven, feedback-driven).

### 2.1 Diferença estrutural vs. SDLC clássico (Waterfall/Ágil)

| Dimensão | SDLC clássico | SDLC AI-first |
|----------|---------------|---------------|
| Artefato-mestre | Documento/backlog | **Spec executável + testes** |
| Papel do humano | Executa fases | Define intenção, revisa diffs, julga |
| Verificação | Fase final | **Adversarial e contínua** |
| Custo dominante | Horas-homem | **Tokens + contexto** |
| Aprendizado | Post-mortem | **Loop por iteração** (skills/RTK memory) |

## 3. As 8 Fases do Ciclo

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ 1. Intenção│→│ 2. Spec  │→│ 3. Design│→│ 4. Build │
│ (humano)  │  │ (contrato)│  │ (domínio) │  │ (agentes)│
└──────────┘  └──────────┘  └──────────┘  └────┬─────┘
                                              │
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───▼─────┐
│ 8. Evoluir│←│ 7. Operar│←│ 6. Entregar│←│ 5. Verificar│
│ (loop)   │  │ (monitor)│  │ (release)│  │ (adversarial)│
└──────────┘  └──────────┘  └──────────┘  └─────────┘
```

### Fase 1 — Intenção (humano, ~1x)

- **Input:** problema de negócio, dor, pedido vago.
- **Output:** 1 parágrafo de intenção + definição de "done" (DoD).
- **Regras:** nada de implementar antes da spec. O agente pode *provocar* (grill-me), mas não *decidir*.
- **Ferramentas no ecossistema:** `brainstorming`, `grill-me`, `to-questionnaire`.

### Fase 2 — Spec (contrato)

- **Input:** intenção.
- **Output:** spec curta: escopo, restrições, requisitos (R1..Rn), casos de borda, critérios de aceite.
- **Verificação embutida:** a spec vira issue/tickets com **bloqueios explícitos** (`to-tickets`, `wayfinder`).
- **Regra de ouro:** se não dá pra escrever o teste de aceite na spec, a spec está incompleta.

### Fase 3 — Design (modelagem de domínio)

- **Input:** spec aprovada.
- **Output:** vocabulário ubíguo, contratos de módulos, decisões de arquitetura (ADRs).
- **Ferramentas:** `ubiquitous-language`, `domain-modeling`, `codebase-design`, `archify` (diagramas).
- **Regra:** design em camadas — interface primeiro (deep modules), nunca implementação antes da fronteira.

### Fase 4 — Build (execução agêntica)

- **Input:** spec + design + worktree isolado (`using-git-worktrees`).
- **Output:** código + testes.
- **Regra de ouro:** **test-first** (`tdd`, `test-driven-development`); o agente escreve o teste vermelho antes do código.
- **Execução em paralelo:** `dispatching-parallel-agents` para tarefas independentes; sequencial para dependentes.
- **Economia de tokens:** LeanCTX (grep antes de read), subagentes caveman para busca/edição, Headroom em logs.

### Fase 5 — Verificar (o coração do AI-first)

- **Input:** diff + testes verdes.
- **Camadas de verificação:**
  1. **Máquina:** typecheck, lint, testes (pré-flight).
  2. **Adversarial:** revisor subagente que tenta *refutar* (receiving-code-review, `fable-judge`, code-reviewer).
  3. **Humano:** leitura do diff, decisão de merge.
- **Evidência antes de afirmação:** `verification-before-completion` — nunca "está pronto" sem output do comando.
- **Regra:** quem escreveu não valida sozinho — o reviewer é sempre outro agente/pessoa.

### Fase 6 — Entregar (release)

- **Input:** merge aprovado.
- **Output:** build limpo, tag, changelog, deploy (canário/gradual).
- **Regra:** release = artefato reproduzível; se o ambiente bloqueia, cuspir comandos prontos (como o fallback Pandoc/Typst da fábrica).

### Fase 7 — Operar (monitorar)

- **Input:** release em produção.
- **Output:** métricas, logs, alertas; o agente observa o *próprio* comportamento (opencode-monitor já existe no repo).
- **Regra:** todo erro de produção vira **insumo de aprendizado**, não só incidente.

### Fase 8 — Evoluir (loop de aprendizado)

- **Input:** observações + erros + feedback.
- **Output:** skills novas/atualizadas (`self-learning`), RTK memory (erros recorrentes), specs revisadas.
- **Regra:** o SDLC melhora a cada iteração — o *ciclo de vida do próprio ciclo de vida* é o diferencial AI-first.

## 4. Papel Humano por Fase (Matriz RACI simplificada)

| Fase | Humano (Responsible) | Agente (Responsible) | Humano (Accountable) |
|------|----------------------|----------------------|----------------------|
| Intenção | Define problema | Provoca/refina | Sim |
| Spec | Aprova | Redige | Sim |
| Design | Decide fronteiras | Propõe opções | Sim |
| Build | Revisa diffs | Escreve código | Não |
| Verificar | Julga merge | Testa/refuta | Sim |
| Entregar | Autoriza | Executa | Sim |
| Operar | Responde incidentes | Monitora | Sim |
| Evoluir | Prioriza | Captura/skills | Sim |

## 5. Níveis de Maturidade

1. **L1 — Copiloto:** humano escreve, IA autocompleta. (SDLC clássico + ferramenta)
2. **L2 — Agente supervisionado:** IA escreve funções/módulos, humano revisa tudo. (hoje, maioria)
3. **L3 — Spec-driven:** IA executa da spec ao teste; humano só aprova contratos. (**alvo deste esboço**)
4. **L4 — Verificação adversarial:** agentes se verificam entre si; humano arbitra conflitos.
5. **L5 — Autônomo com supervisão por exceção:** IA opera o ciclo inteiro; humano só intervém em exceções.

## 6. Anti-padrões a evitar

- **Prompt-and-pray:** pedir código sem spec → desperdício de tokens e retrabalho.
- **Specs como decoração:** spec que não vira teste de aceite.
- **Verificação do próprio agente:** quem escreveu não revisa sozinho.
- **Ignorar o custo do contexto:** sessão morre no meio do build → economize desde a Fase 1.
- **Sem worktree/isolamento:** agente bagunçando o working dir principal.

## 7. Encaixe no Repo

- **Este esboço** → vira um artefato (spec/plano) em `docs/superpowers/`.
- O **livro AI-Driven Development** pode ganhar um capítulo sobre isso (fecha com a estrutura de 18 capítulos que já existe — provavelmente no Bloco 2/4).
- A **fábrica de livros** já *é* um exemplo de L3-L4: spec → sumário → redação paralela → auditoria determinística (`auditar-obra.py`) → revisor adversarial.

## 8. Casos de Borda

| Situação | Comportamento esperado |
|----------|----------------------|
| Pedido vago sem intenção clara | Fase 1 bloqueia: agente provoca (grill-me), não implementa |
| Spec sem teste de aceite | Fase 2 incompleta: não avança para Design |
| Agente não consegue verificar sozinho | Fase 5 exige reviewer externo (outro agente/humano) |
| Contexto/tokens esgotados | Fallback: handoff/worktrees; economia desde Fase 1 |
| Release bloqueado por ambiente | Cuspir comandos prontos (padrão fallback Pandoc/Typst) |
| Erro recorrente em produção | Vira skill/RTK memory na Fase 8 (loop de aprendizado) |

## 9. Economia de Tokens Aplicada

1. **lean-ctx:** grep antes de read (Fases 3-4)
2. **headroom:** logs de execução comprimidos (3+4)
3. **caveman:** comunicação entre agentes telegráfica
4. **rtk-memory:** erros de build/tipo/runtime registrados
5. **pre-flight-check:** validação antes de avançar de fase
6. **worktrees:** isolamento de código sem custo de contexto extra
