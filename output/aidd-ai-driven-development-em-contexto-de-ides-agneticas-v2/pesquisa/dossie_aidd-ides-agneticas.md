# Dossiê de Pesquisa — AIDD: AI-Driven Development em Contexto de IDEs Agênticas

## Conceitos-chave

- **AI-Driven Development (AIDD)**: Paradigma de engenharia de software onde a IA é reposicionada de ferramenta passiva para agente ativo no ciclo de vida de desenvolvimento. O desenvolvedor transita de escritor de código linha a linha para arquiteto de sistemas, engenheiro de especificações e orquestrador de agentes.
- **Specification-Driven Development (SDD)**: Abordagem onde especificações em linguagem natural (Markdown, CLAUDE.md) funcionam como entradas executáveis que agentes de IA interpretam, planejam, executam e testam autonomamente.
- **Contexto Repositório-Amplo**: Capacidade do agente de indexar e compreender a árvore de diretórios inteira, dependências, padrões arquiteturais e convenções do projeto.
- **Ciclos de Auto-Correção**: O agente executa build/testes, captura falhas, analisa causa raiz, aplica patch corretivo e reexecuta até sucesso — sem intervenção humana.

## Estado da arte / ferramentas de referência

- **Claude Code** (Anthropic): CLI agêntica com sub-agentes paralelos, hooks de ciclo de vida, suporte nativo MCP. Padrão de referência para automação ponta a ponta.
- **Cursor** (Anysphere): IDE fork do VS Code com Agent Mode, Composer para edições multi-arquivo, suporte a múltiplos modelos de IA.
- **Windsurf** (Codeium): IDE agêntica com Cascade (planejador multi-etapas), Flow Context contínuo entre sessões, excelente para monorepos.
- **GitHub Copilot / VS Code Agents**: Integração nativa de agentes no ecossistema VS Code com Cline, Roo Code e extensões open-source.
- **Cline**: Extensão open-source VS Code que transforma o editor em ambiente autônomo baseado em agentes com leitura/escrita de arquivos e execução de terminal.
- **Model Context Protocol (MCP)**: Padrão aberto (Anthropic, nov/2024) que padroniza comunicação entre IAs e ferramentas externas — "USB-C para IA".

## Fluxos de trabalho com agentes

1. **Spec-to-Code**: Especificação → plano de execução → código autônomo
2. **Sub-agentes paralelos**: Delegação simultânea de tarefas (schema DB + testes + docs)
3. **Self-Correction Loop**: Build → erro → análise → patch → re-teste
4. **Revisão Humana de Diff**: Desenvolvedor como revisor sênior do diff gerado

## Limitações e controvérsias

- **Alucinação de contexto**: Em codebases grandes, agentes podem violar padrões não escritos da equipe
- **Custos de API elevados**: Execuções autônomas prolongadas com modelos de fronteira
- **Gargalos de segurança**: Permissão irrestrita de terminal sem sandboxing adequado
- **Fadiga de revisão**: Carga cognitiva deslocada de escrever para auditar código gerado em massa

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- Anthropic. "Introducing the Model Context Protocol" — https://www.anthropic.com/news/model-context-protocol
- Model Context Protocol Documentation — https://modelcontextprotocol.io/docs/getting-started/intro
- Codecademy. "Agentic IDE Comparison: Cursor vs Windsurf vs Antigravity" — https://www.codecademy.com/article/agentic-ide-comparison-cursor-vs-windsurf-vs-antigravity
- AWS DevOps Blog. "AI-Driven Development Life Cycle (AI-DLC)" — https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/
- "The Manifesto for AI-Driven Development" — https://www.ai-driven-development.org/
- Denis Kisina. "From Code Completion to Autonomous Development" — https://deniskisina.dev/posts/agentic-coding-revolution/
- Panaversity. "Nine Pillars of AIDD" — https://agentfactory.panaversity.org/docs/General-Agents-Foundations/agent-factory-paradigm/nine-pillars-of-aidd
- DataCamp. "The Best Agentic IDEs" — https://www.datacamp.com/blog/best-agentic-ide
