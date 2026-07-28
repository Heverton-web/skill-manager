# Dossiê de Pesquisa — Arquitetura de Servidores MCP como Motor de Ferramentas para Agentes de IA

## Conceitos-chave
- Model Context Protocol (MCP): protocolo aberto que define um vocabulário comum
  (JSON-RPC 2.0), primitivas padrão (Tools, Resources, Prompts) e uma estrutura
  cliente-servidor consistente para conectar aplicações LLM a ferramentas e fontes de
  dados externas. Introduzido pela Anthropic em novembro de 2024.
- Transporte stdio: o servidor roda como subprocesso local e troca mensagens via
  entrada/saída padrão — ideal para ferramentas locais, sem overhead de rede.
- Transporte Streamable HTTP: endpoint único que suporta POST e GET, com streaming
  opcional via Server-Sent Events para mensagens servidor→cliente.
- Descoberta e invocação de ferramentas: `tools/list` (descoberta automática) e
  `tools/call` (invocação), com entradas e saídas tipadas.
- Especificação 2026-07-28 (release candidate): torna o MCP *stateless* na camada de
  protocolo, adiciona extensões como UIs renderizadas pelo servidor (MCP Apps) e
  trabalho de longa duração (extensão Tasks), e alinha autorização a OAuth/OpenID
  Connect.
- Governança: em dezembro de 2025 a Anthropic doou o protocolo à Agentic AI Foundation
  (AAIF), um fundo dirigido dentro da Linux Foundation, cofundado por Anthropic, Block
  e OpenAI.

## Estado da arte / ferramentas de referência
- SDKs oficiais com mais de 97 milhões de downloads mensais e mais de 10.000 servidores
  públicos ativos registrados até a atualização de ecossistema de 9 de dezembro de 2025
  da Anthropic.
- MCP é transport-agnostic: funciona sobre HTTP, WebSocket, stdin/stdout ou IPC, o que
  permite arquiteturas híbridas (servidores locais de baixa latência + servidores
  remotos multi-tenant).
- Arquitetura de referência para sistemas multi-agente: cada agente atua como cliente
  MCP conectado a um ou mais servidores especializados (motor de busca, banco de dados,
  geração de imagem, sistema de arquivos), permitindo composição modular de
  capacidades sem acoplamento direto entre agente e implementação da ferramenta.

## Casos de uso corporativos
- Adoção em 28% das empresas Fortune 500 em menos de 18 meses desde o lançamento,
  segundo levantamento de adoção enterprise de 2026.
- Caso documentado de implantação em produção por 18 meses conectando agentes
  autônomos a 14 sistemas corporativos distribuídos em 270 datacenters globais.
- Padrões arquiteturais para orquestração de ferramentas empresariais: uso de MCP como
  camada de integração entre agentes de IA e sistemas de produção em escala,
  cobrindo gestão de conhecimento, desenvolvimento de software, automação de fluxo de
  trabalho, analytics e suporte ao cliente.

## Limitações e controvérsias
- Injeção de prompt e envenenamento de contexto: MCP introduz um vetor de risco em que
  conteúdo malicioso pode direcionar um agente a uso inseguro de ferramentas, incluindo
  acesso não intencional a dados ou exfiltração.
- Permissões excessivamente amplas: servidores MCP tendem a solicitar escopos amplos
  (ex.: acesso total ao Gmail em vez de apenas leitura), criando risco de agregação de
  dados entre serviços que nunca foram desenhados para isso.
- Problema do "confused deputy": servidores MCP podem executar ações com privilégios
  elevados em vez de em nome do usuário solicitante, violando o princípio do menor
  privilégio.
- Postura de segurança ainda imatura: ao contrário de middlewares consolidados, o MCP
  mistura fluxos de raciocínio e controle em um contexto semântico compartilhado, o que
  favorece a coordenação fluida entre LLMs e ferramentas externas, mas borra fronteiras
  tradicionais de confiança — em muitas implementações, contexto, metadados e
  instruções executáveis coexistem sem isolamento forte.
- Falta de diretrizes uniformes: ausência de responsabilidade centralizada amplia os
  riscos, já que muitos fornecedores delegam o endurecimento de segurança a
  integradores ou usuários finais.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)
- Model Context Protocol. *Specification 2026-07-28*. Disponível em:
  https://modelcontextprotocol.io/specification/2026-07-28. Acesso em: 28 jul. 2026.
- Model Context Protocol Blog. *The 2026-07-28 MCP Specification Release Candidate*.
  Disponível em: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/.
  Acesso em: 28 jul. 2026.
- Model Context Protocol. *Architecture overview*. Disponível em:
  https://modelcontextprotocol.io/docs/learn/architecture. Acesso em: 28 jul. 2026.
- Speakeasy. *What are MCP transports?*. Disponível em:
  https://www.speakeasy.com/mcp/core-concepts/transports. Acesso em: 28 jul. 2026.
- Anthropic. *Introducing the Model Context Protocol*. Disponível em:
  https://www.anthropic.com/news/model-context-protocol. Acesso em: 28 jul. 2026.
- Digital Applied. *MCP Adoption Statistics 2026: Model Context Protocol*. Disponível
  em: https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol.
  Acesso em: 28 jul. 2026.
- International Journal of Computational and Experimental Science and Engineering.
  *The Model Context Protocol and Enterprise Tool Orchestration: Architectural Patterns
  for Connecting AI Agents to Production Systems at Scale*. Disponível em:
  https://ijcesen.com/index.php/ijcesen/article/view/5402. Acesso em: 28 jul. 2026.
- Pillar Security. *The Security Risks of Model Context Protocol (MCP)*. Disponível em:
  https://www.pillar.security/blog/the-security-risks-of-model-context-protocol-mcp.
  Acesso em: 28 jul. 2026.
- Microsoft Community Hub. *Plug, Play, and Prey: The security risks of the Model
  Context Protocol*. Disponível em:
  https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/plug-play-and-prey-the-security-risks-of-the-model-context-protocol/4410829.
  Acesso em: 28 jul. 2026.
- arXiv. *Systematization of Knowledge: Security and Safety in the Model Context
  Protocol Ecosystem*. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em:
  28 jul. 2026.
