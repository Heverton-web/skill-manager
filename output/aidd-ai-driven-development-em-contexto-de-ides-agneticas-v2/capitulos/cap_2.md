# Capítulo 2 — Ecossistema de IDEs Agênticas: Claude Code, Cursor, Windsurf e o MCP

O ecossistema de desenvolvimento agêntico amadureceu rapidamente desde 2024. O que começou como experimentos isolados em CLIs e extensões de editor convergiu para um conjunto de plataformas maduras, cada uma com filosofia própria de interação agente-humano. Compreender esse ecossistema é essencial para escolher a ferramenta certa para cada contexto.

## Claude Code, Cursor, Windsurf: Arquiteturas e Diferenciais

Três plataformas dominam o cenário atual de IDEs agênticas, cada uma com abordagem distinta:

**Claude Code** (Anthropic) é uma CLI agêntica que opera diretamente no terminal, sem interface gráfica. Sua força está na integração profunda com o ecossistema UNIX — pipes, redirecionamento, hooks git e servidores MCP. Ele indexa o repositório inteiro, executa comandos de shell, gerencia branches e permite a criação de sub-agentes que processam tarefas em paralelo. É a escolha ideal para automação em CI/CD, refatorações em escala e integração com ferramentas de linha de comando.

**Cursor** (Anysphere) é uma IDE baseada em fork do VS Code que integra IA diretamente no editor visual. Seu modo *Agent* permite que o modelo planeje e execute tarefas multi-arquivo enquanto o desenvolvedor acompanha em tempo real. O *Composer* coordena edições em múltiplos arquivos simultaneamente. Cursor se destaca pela versatilidade de modelos — suporta Claude, GPT e Gemini intercambiavelmente por tarefa — e pela manutenção da compatibilidade total com extensões do ecossistema VS Code.

**Windsurf** (Codeium) é outra IDE fork do VS Code com foco em contexto contínuo. Seu *Cascade* é um planejador multi-etapas que mantém estado entre sessões (*Flow*), evitando que o agente "esqueça" o contexto ao alternar entre tarefas. Windsurf brilha em monorepos complexos e arquiteturas multi-módulo, onde a capacidade de reter contexto entre execuções é crítica.

![Comparativo de IDEs Agênticas](../imagens/cap_2_diagrama_1.svg)

## Model Context Protocol: O 'USB-C para IA' e seus Servidores

Introduzido pela Anthropic em novembro de 2024, o Model Context Protocol (MCP) resolve um dos gargalos mais persistentes da integração de IA com ferramentas externas: a fragmentação de conectores proprietários.

Antes do MCP, cada IDE precisava implementar conectores específicos para cada fonte de dados — um para bancos SQL, outro para APIs REST, outro para sistemas de arquivos. Cada conector era frágil, específico de plataforma e difícil de manter.

O MCP padroniza essa comunicação em um modelo cliente-servidor: o *MCP Client* (a IDE ou CLI agêntica) se conecta a *MCP Servers* (processos que expõem ferramentas, recursos e prompts). Qualquer desenvolvedor pode criar um servidor MCP para expor qualquer sistema — banco de dados, API, sistema de arquivos, navegador — e imediatamente torná-lo acessível a todas as IDEs compatíveis.

Os modos de transporte incluem stdio (para servidores locais, processos filho) e Streamable HTTP (para servidores remotos). O protocolo define três tipos de primitivas: **Tools** (operações que o agente pode invocar), **Resources** (dados que o agente pode ler) e **Prompts** (templates que o agente pode usar). Essa separação permite controle granular de permissões e segurança.

![Arquitetura MCP](../imagens/cap_2_diagrama_2.svg)

## Extensões Open-Source: Cline, Roo Code e o Ecossistema BYOK

Paralelamente às plataformas comerciais, um ecossistema open-source robusto floresceu. **Cline** (originalmente Claude Dev) é uma extensão para VS Code que transforma o editor padrão em um ambiente agêntico completo — leitura e escrita de arquivos, execução de terminal, navegação web e gerenciamento de arquivos — tudo com aprovação granular do usuário.

**Roo Code** segue filosofia similar, com ênfase em modos de operação (architect, code, debug) e suporte a múltiplos provedores de modelo via Bring Your Own Key (BYOK). Isso permite que times usem a mesma interface com modelos locais (via Ollama), provedores corporativos ou APIs públicas.

O ecossistema BYOK é particularmente relevante para organizações com restrições de dados: elas podem usar a mesma experiência agêntica com modelos hospedados internamente, mantendo compliance sem abrir mão da produtividade.

![Ecossistema AIDD](../imagens/cap_2_diagrama_3.svg)
