# SPEC — Livro: AI-Driven Development com OpenCode

## 1. Visão Geral

**Título:** AI-Driven Development: Desenvolvimento de Software com LLMs Gratuitas, OpenCode e Economia Severa de Tokens

**Tema central:** O paradigma de AI-Driven Development utilizando o ecossistema OpenCode como harness, LLMs gratuitas como cérebros, SKILLs e MCPs como operários, e técnicas de economia severa de tokens (CAVEMAN, HEADROOM, RTK, LEAN-CTX) para estender a vida útil das sessões e contornar rate limits diários.

**Público-alvo:** Camadas — iniciantes (fundamentos) e desenvolvedores intermediários/avançados (economia de tokens, FABLE, padrões avançados).

**Formato:** Híbrido (conceitual + prático). Metade do livro explica conceitos, metade mostra implementação.

**Idioma:** PT-BR

**Tamanho:** 18 capítulos, estimativa de 70-90 páginas (~175.000-225.000 caracteres em formato ABNT).

## 2. Requisitos Contratuais

| # | Requisito | Especificação | Validação |
|---|-----------|---------------|-----------|
| R1 | Capítulos | 18 capítulos | Sumário macro |
| R2 | Páginas | 70-90 páginas (~175.000-225.000 caracteres) | Contagem de caracteres |
| R3 | Estrutura/capítulo | 7 seções EITA-V2 | Template EITA |
| R4 | Referências/capítulo | Mínimo 3, formato ABNT | Seção de referências |
| R5 | Artigos científicos | Mínimo 3 papers no dossiê | Seção "Artigos Científicos" |
| R6 | Formatação ABNT | Livro completo | Capa, sumário, referências, numeração |
| R7 | PDF final | 1 arquivo .pdf | Pandoc+Typst |
| R8 | Tom | Transformacional (simples → denso) | Camadas de profundidade |
| R9 | Citações inline | Mínimo 3 [N] por capítulo | Vinculadas às referências |

## 3. Estrutura do Livro (18 capítulos)

### Bloco 1 — Fundamentos (Cap. 1-4)

#### Capítulo 1: O que é AI-Driven Development?
- **Seções EITA:** Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências
- **Conteúdo:**
  - Definição de AI-Driven Development vs. Traditional Development
  - Onde encaixa no ciclo de vida do software
  - O hype vs. a realidade — expectativas gerenciáveis
  - O papel do desenvolvedor humano na era dos agentes
  - Exemplo conceitual: como um agente executa uma tarefa
- **Dicas de busca para pesquisador:** Artigos sobre AI-assisted programming, papers da GitHub sobre Copilot (pesquisador busca referências reais durante Fase 1)

#### Capítulo 2: LLMs Gratuitas como Cérebros
- **Conteúdo:**
  - Panorama de modelos gratuitos (Gemini 2.5, Llama 3.x, Mistral, DeepSeek)
  - Limitações: contexto, alucinação, latência
  - Superpowers: onde LLMs gratuitas superam modelos pagos
  - Como escolher o modelo certo para cada tarefa
  - Configuração no OpenCode
- **Dicas de busca:** Documentação oficial dos modelos, benchmarks (pesquisador busca referências reais)

#### Capítulo 3: OpenCode — O Harness
- **Conteúdo:**
  - Arquitetura: Harness → LLM → Tools
  - Instalação e configuração
  - Diferencial vs. Claude Code, Cursor, Copilot
  - O conceito de "harness" — por que ele importa
  - Primeira sessão: do zero ao "hello world"
- **Dicas de busca:** Docs do OpenCode, repositório GitHub

#### Capítulo 4: Sua Primeira Sessão
- **Conteúdo:**
  - Tutorial passo-a-passo: instalar OpenCode, configurar LLM gratuita
  - Criar um projeto simples (ex.: TODO API)
  - Observar o agente trabalhando
  - Entender o que aconteceu por baixo dos panos
  - Primeiras lições: o que funcionou, o que não funcionou
- **Dicas de busca:** Tutoriais oficiais, guias de início rápido

### Bloco 2 — Ecossistema (Cap. 5-9)

#### Capítulo 5: SKILLs — Os Operários
- **Conteúdo:**
  - O que é uma skill (definição técnica)
  - Anatomia de uma skill: SKILL.md, triggers, checklist
  - Como criar uma skill do zero
  - Registro e descoberta de skills
  - Exemplos: caveman, lean-ctx, headroom
- **Dicas de busca:** Repositório de skills, documentação de formato

#### Capítulo 6: MCPs — Motores de Execução
- **Conteúdo:**
  - Model Context Protocol: o que é e por que existe
  - Arquitetura de um MCP server
  - MCPs úteis para desenvolvimento (filesystem, sqlite, web search)
  - Como configurar MCPs no OpenCode
  - Exemplo prático: criar um MCP simples
- **Dicas de busca:** Spec do MCP, exemplos oficiais

#### Capítulo 7: RULES, HOOKS e SPECS
- **Conteúdo:**
  - CLAUDE.md / AGENTS.md: regras globais
  - Regras locais vs. globais — hierarquia
  - Hooks de pré/pós-execução
  - Specs como contrato de trabalho
  - Como o OpenCode interpreta regras
- **Dicas de busca:** Documentação de configuração do OpenCode

#### Capítulo 8: FABLE — O Método
- **Conteúdo:**
  - FABLE Method: think → act → prove
  - fable-domain: modelagem de domínio
  - fable-judge: verificação adversarial
  - fable-loop: ciclos de execução
  - Quando usar FABLE vs. abordagem direta
- **Dicas de busca:** Skills FABLE do repositório, filosofia FABLE

#### Capítulo 9: Combinando Tudo
- **Conteúdo:**
  - Arquitetura completa: Harness + LLM + Skills + MCPs + Rules
  - Fluxo de trabalho integrado (diagrama)
  - Decisões de design: quando usar cada peça
  - Anti-padrões: o que não fazer
  - Exemplo: projeto completo usando todo o ecossistema
- **Dicas de busca:** Padrões de arquitetura de agentes

### Bloco 3 — Economia Severa (Cap. 10-14)

#### Capítulo 10: O Problema dos Tokens
- **Conteúdo:**
  - O que é um token (definição técnica simplificada)
  - Rate limits: por que existem e como funcionam
  - Custo de contexto: como o tamanho da conversa afeta performance
  - Sessões que acabam — o problema do contexto esgotado
  - Métricas: tokens por sessão, custo estimado
- **Dicas de busca:** Documentação de rate limits dos provedores

#### Capítulo 11: CAVEMAN — Comunicação Telegráfica
- **Conteúdo:**
  - O que é o modo caveman
  - Regras: respostas cirúrgicas, sem fluff, diffs limpos
  - Ativação: triggers e configuração
  - Antes vs. depois: exemplos reais de compressão
  - Quando NÃO usar caveman
- **Dicas de busca:** Skill caveman, exemplos de uso

#### Capítulo 12: HEADROOM e LEAN-CTX
- **Conteúdo:**
  - HEADROOM: compressão de logs e outputs (>7 linhas → 3 topo + 4 fim)
  - LEAN-CTX: grep antes de read, assinaturas antes de corpos
  - Implementação: como configurar no OpenCode
  - Impacto mensurável: economia de tokens por sessão
  - Exemplos práticos de aplicação
- **Dicas de busca:** Skills headroom e lean-ctx

#### Capítulo 13: RTK Memory e Pre-Flight
- **Conteúdo:**
  - RTK SCRATCHPAD: o que é e como funciona
  - Registro de erros de build/tipo/runtime
  - Padrões aprendidos e reutilizados
  - Pre-flight-check: type-check, testes e build antes de commit
  - Auto-correção: como o agente corrige erros anteriores
- **Dicas de busca:** Skills rtk-memory e pre-flight-check

#### Capítulo 14: Estratégias Avançadas
- **Conteúdo:**
  - Subagentes paralelos: quando e como instanciar
  - Handoff: passar contexto entre sessões
  - Sessões longas: técnicas para estender a vida útil
  - Rate limit stretching: estratégias avançadas
  - Worktrees: isolamento de código
- **Dicas de busca:** Skills handoff, worktrees, claude-handoff

### Bloco 4 — Mão na Massa (Cap. 15-18)

#### Capítulo 15: Projeto — CRUD Completo
- **Conteúdo:**
  - Do zero ao deploy: API REST + frontend + testes
  - Usando AI-Driven Development do início ao fim
  - Cada etapa: pesquisa → arquitetura → implementação → testes → deploy
  - Economia de tokens aplicada ao projeto real
- **Dicas de busca:** Guias de desenvolvimento web

#### Capítulo 16: Projeto — Refactoring de Legado
- **Conteúdo:**
  - Tomar código existente e refatorar com agentes
  - Diagnóstico: como o agente entende código legado
  - Estratégia de refactoring: incremental vs. big bang
  - Antes vs. depois: métricas de melhoria
- **Dicas de busca:** Padrões de refactoring, Clean Code

#### Capítulo 17: Troubleshooting
- **Conteúdo:**
  - Problemas comuns e soluções
  - LLMs que alucinam: como detectar e corrigir
  - Tokens excedidos: recuperação
  - Skills quebradas: diagnóstico
  - MCPs que não conectam: debugging
  - Lista de erros frequentes e soluções
- **Dicas de busca:** Issues do GitHub, fóruns

#### Capítulo 18: O Futuro do AI-Driven Development
- **Conteúdo:**
  - Tendências: agentes mais autônomos, multimodal
  - Onde o OpenCode está indo
  - Roadmap pessoal: como evoluir como desenvolvedor AI-Driven
  - Reflexão final: o que mudou na forma de programar
- **Dicas de busca:** Artigos de tendências, roadmap do OpenCode

## 4. Fluxo de Produção

### Comando de disparo
```
/criar-livro AI-Driven Development com OpenCode: LLMs Gratuitas, FABLE e Economia Severa de Tokens
```

### Slug derivado
`ai-driven-development`

### Esteira de produção (autônoma)
1. **Fase 1:** pesquisador → arquiteto → sumário_macro.json
2. **Fase 2:** subagentes-redator-capitulo (paralelo, 18 capítulos)
3. **Fase 3:** compilador-abnt → livro_final.md → Pandoc+Typst → livro_final.pdf

### Validação pós-produção
1. `Select-String "^## 1. Introdução"` em todos os capítulos
2. `Select-String "^## [2-7]\. "` em cada capítulo
3. `(Get-Content livro_final.md | Measure-Object -Character).Characters` > 175.000
4. `(Get-ChildItem capitulos/).Count` >= 18
5. `Select-String "\[\d+\]"` — referências >= 3 por capítulo

## 5. Casos de Borda

| Situação | Comportamento esperado |
|----------|----------------------|
| Tema com caracteres especiais | Slug derivado com normalização automática |
| Pasta output/<slug> já existe | Sufixo `-v2` automático |
| LLM gratuita indisponível | Retry com modelo alternativo ou pausa com mensagem |
| Pandoc/Typst ausente | Markdown expedido, PDF como pendência |
| Capítulo sem referências | compilador-abnt reporta não-conformidade |

## 6. Economia de Tokens Aplicada à Produção

A própria produção do livro obedece às regras de economia que ele ensina:

1. **lean-ctx:** Pesquisador faz grep antes de ler arquivos inteiros
2. **headroom:** Logs de execução comprimidos (3+4)
3. **caveman:** Comunicação entre agentes telegráfica
4. **rtk-memory:** Erros de formatação registrados para evitar repetição
5. **pre-flight-check:** Validação de cada capítulo antes de avançar

## 7. Suporte Multi-IDE

O livro será produzido pela Fábrica Agêntica (Claude Code como referência) mas o conteúdo ensina OpenCode. A portabilidade do CLAUDE.md → AGENTS.md → .cursor/rules etc. já está implementada na fábrica.
