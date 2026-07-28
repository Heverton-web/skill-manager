# Dossiê de Pesquisa — AIDD: AI-Driven Development em Contexto de IDEs Agênticas

## Conceitos-chave

- **AI-Driven Development (AIDD):** Paradigma de engenharia de software onde o desenvolvimento é orientado por agentes de IA autônomos, com o desenvolvedor humano assumindo o papel de arquiteto de intenção e validador — não mais de implementador manual. A ênfase migra da escrita de código (execution bottleneck) para a clareza de especificação (intent bottleneck).
- **Spec-Driven Development (SDD):** Metodologia onde especificações estruturadas (não prompts soltos) funcionam como contratos executáveis que governam o comportamento dos agentes de IA. Seis elementos de uma boa spec: Outcomes, Scope Boundaries, Constraints & Assumptions, Prior Decisions, Task Breakdown, Verification Criteria.
- **Intent-Driven Development:** Foco na qualidade da hipótese e mapeamento de intenção antes de agentes autônomos executarem a construção. Permite que equipes encolham até 70% mantendo a mesma entrega.
- **Model Context Protocol (MCP):** Padrão aberto criado pela Anthropic (o "USB-C for AI") que estabelece uma camada cliente-servidor universal para conectar LLMs a ferramentas, fontes de dados e APIs. Arquitetura JSON-RPC 2.0 com tool calls, resources e prompts.
- **Context Engineering:** Disciplina de preencher a janela de contexto de agentes com a informação certa no momento certo. 6 camadas: System Prompt Architecture, RAG de Código, Tool Selection, Memory Systems, Context Compression, Information Ordering.
- **Coding Agents (Agentes de Programação):** Ferramentas como Claude Code, Cursor, Windsurf/Devin Desktop, Cline, Aider, GitHub Copilot Agent — executam loops autônomos de leitura-edição-teste em bases de código reais.
- **SWE-bench / SWE-bench Pro:** Conjunto de benchmarks que avaliam a capacidade de modelos de IA resolverem issues reais do GitHub. Modelos frontier chegam a 96% no SWE-bench Verified e 80% no SWE-bench Pro em 2026.

## Estado da arte / ferramentas de referência

- **Claude Code (Anthropic):** Agente nativo de terminal, loop multi-etapas, integração com MCP e sub-agentes. Excelente para raciocínio profundo e refatorações complexas em grandes bases.
- **Cursor (Anysphere):** IDE mais adotada para fluxo diário, autocompletar Tab ultrarrápido, Agent Mode/Composer para edições coordenadas multi-arquivo, suporte multi-modelo.
- **Windsurf / Devin Desktop (Cognition):** Agente Cascade/Devin Local, forte compreensão de contexto entre arquivos, suporte nativo a MCP.
- **Cline (Open Source):** Extensão VS Code com modos Plan/Act, BYOM (bring your own model), mercado de MCPs em um clique, 200+ modelos suportados.
- **Aider (Open Source, CLI):** Programador-par em terminal, integração nativa com Git (commits semânticos atômicos), agnóstico de modelos.
- **GitHub Copilot (Agent Mode & Workspace):** Integração profunda com ecossistema GitHub, modo agente assíncrono em nuvem que gera PRs a partir de Issues.
- **MCP Registry / Servers:** Milhares de servidores públicos e corporativos conectando agentes a bancos, APIs, sistemas de arquivos, CI/CD.
- **Frameworks Multi-Agente:** CrewAI, LangGraph, AutoGen, Semantic Kernel, DSPy — orquestração de agentes especializados.
- **Spec Toolkits:** GitHub Spec Kit (CLI), Tessl (spec-as-source), Amazon Kiro & Q Developer.

## Casos de uso corporativos

- **Banking, Seguros, Software/Internet:** Líderes em adoção (44-47% em produção). Refatoração de legados, migração de frameworks, testes automatizados em escala, triagem/correção de bugs rotineiros.
- **Saúde e Setor Público:** Adoção mais lenta (14-18% em produção), barrada por conformidade (HIPAA, FedRAMP) e governança de dados.
- **Métricas:** Aumento de ~100% em PRs por desenvolvedor, mas tempo de revisão cresce até 90%. Ganhos reais de 25-50% em tarefas rotineiras. 7-9 horas/semana economizadas por engenheiro.
- **Perception Gap (METR):** Desenvolvedores acham que estão 20% mais rápidos, mas na realidade levam 19% mais tempo em tarefas complexas em codebases legadas — lacuna de ~40 pontos percentuais.
- **Fracasso de Pilotos:** 88% dos pilotos de agentes de IA falham em chegar à produção. Principais causas: falta de evals automatizadas (64%), saídas não-determinísticas (51%), governança/vazamento de dados (57%).

## Limitações e controvérsias

- **Sobrecarga de Revisão (Review Bottleneck):** Agentes geram código mais rápido do que humanos conseguem revisar — o gargalo muda de lugar.
- **Markdown Overload:** Frameworks SDD podem gerar dezenas de specs em markdown tão difíceis de revisar quanto o código.
- **Não-determinismo dos LLMs:** Mesmo com especificações bem estruturadas, variações na saída dos modelos exigem property-based testing e validação rigorosa.
- **Risco de Dívida Técnica:** Código gerado por IA pode elevar incidência de bugs sutis e vulnerabilidades se mesclado sem revisão rigorosa.
- **Atrito Cultural:** Risco de "atrofia de processos" onde engenheiros aprovam cegamente o que agentes geram sem julgamento crítico.
- **Crise de Precificação:** Agentes consomem 50-100x mais tokens que chat comum. Todas as plataformas migraram para modelos de créditos.
- **Professionalização:** 56% das empresas criaram papéis de AI Agent Owners ou Agentic Ops.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- Anthropic. "Introducing the Model Context Protocol." https://www.anthropic.com/news/model-context-protocol Acesso em: 28 jul. 2026.
- Anthropic. "Claude Code Documentation." https://docs.anthropic.com/en/docs/claude-code/overview Acesso em: 28 jul. 2026.
- Model Context Protocol. "Architecture Overview." https://modelcontextprotocol.io/docs/learn/architecture Acesso em: 28 jul. 2026.
- Model Context Protocol. "Server Concepts & Primitives." https://modelcontextprotocol.io/docs/learn/server-concepts Acesso em: 28 jul. 2026.
- Model Context Protocol. "MCP Specification (November 2025)." https://modelcontextprotocol.io/specification/2025-11-25 Acesso em: 28 jul. 2026.
- MCP Blog. "One Year of MCP & November 2025 Release Details." https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ Acesso em: 28 jul. 2026.
- Cursor. "Official Documentation." https://docs.cursor.com Acesso em: 28 jul. 2026.
- GitHub. "Copilot Documentation." https://docs.github.com/en/copilot Acesso em: 28 jul. 2026.
- Aider. "Documentation." https://aider.chat/docs/ Acesso em: 28 jul. 2026.
- Cline. "Documentation." https://docs.cline.bot Acesso em: 28 jul. 2026.
- Princeton SWE-bench. "SWE-bench Verified & Pro." https://www.swebench.com Acesso em: 28 jul. 2026.
- Thoughtworks. "Technology Radar — AI-Assisted Development." https://www.thoughtworks.com/radar Acesso em: 28 jul. 2026.
- DORA / Google Cloud. "2024 State of DevOps Report." https://dora.dev Acesso em: 28 jul. 2026.
- Gartner. "AI Agent Adoption in Enterprises, 2026." Acesso em: 28 jul. 2026.
- METR. "Measuring AI Agent Capabilities in Real-World Software Engineering Tasks." Acesso em: 28 jul. 2026.
- Faros AI. "Engineering DevOps and AI Impact Report." Acesso em: 28 jul. 2026.
- Amazon AWS. "AI-Driven Development Lifecycle (AI-DLC)." Acesso em: 28 jul. 2026.
- GitHub Spec Kit. "Spec-Driven Development Toolkit." https://github.com/github/spec-kit Acesso em: 28 jul. 2026.
- Fable Method. "Structured Agent Workflow Methodology." Acesso em: 28 jul. 2026.
- O'Reilly Media. "AI-Driven Development: State of the Industry 2026." Acesso em: 28 jul. 2026.
- McKendrick, Joe. "AI Augmentation in Software Engineering: The Spec-Driven Paradigm." Acesso em: 28 jul. 2026.
- Bind AI. "Context Engineering Best Practices for Coding Agents." Acesso em: 28 jul. 2026.
