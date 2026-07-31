#!/usr/bin/env python3
"""
Dados das 5 Séries de Livros da Stack Fullstack (FE, BE, BD, AP, DV)
Cada série tem 10 livros, cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-stack.py e compilar-para-pdf.py
"""

SERIES_STACK = {
    "FE": {"nome": "Frontend", "prefixo": "FE"},
    "BE": {"nome": "Backend", "prefixo": "BE"},
    "BD": {"nome": "Banco de Dados", "prefixo": "BD"},
    "AP": {"nome": "APIs", "prefixo": "AP"},
    "DV": {"nome": "DevOps", "prefixo": "DV"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
SERIES_PARTES = {
    "FE": ["Fundamentos do Frontend", "Linguagens e Frameworks", "Estado, Dados e Formulários", "Qualidade e Performance"],
    "BE": ["Fundamentos do Backend", "APIs e Comunicação", "Segurança e Autenticação", "Escala e Arquitetura"],
    "BD": ["Fundamentos de Dados", "Modelagem e Persistência", "Otimização e Busca", "Operação e Segurança"],
    "AP": ["Fundamentos de APIs", "Design e Documentação", "Segurança e Resiliência", "Operação e Gestão"],
    "DV": ["Fundamentos de DevOps", "Contêineres e Automação", "Infraestrutura e Rede", "Observabilidade e Deploy"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_STACK = {
    # ═══════════════ SÉRIE FE — FRONTEND ═══════════════
    "FE-01-html5-semantico-a11y": (
        "HTML5 Semântico e Acessibilidade (a11y)",
        "HTML5 Semântico e Acessibilidade (a11y): Estruturação correta de documentos e conformidade com padrões globais de inclusão digital",
        "Estruturação correta de documentos e conformidade com padrões globais de inclusão digital",
        "Uma página bem estruturada é a fundação de tudo: semântica correta, landmarks de acessibilidade e conformidade com padrões globais como WCAG beneficiam todos os usuários — e o SEO junto. Este livro ensina a construir documentos HTML5 corretos e acessíveis desde a primeira tag.",
        "Semântica e acessibilidade não são requisitos opcionais: são a base da inclusão digital. Um documento HTML5 bem estruturado, com landmarks, hierarquia correta e ARIA quando necessário, funciona para todos — pessoas, leitores de tela, motores de busca e máquinas.",
        "HTML5 introduziu elementos semânticos (header, nav, main, section, article, aside, footer) que descrevem a estrutura do documento em vez de apenas formatá-lo [1]. A acessibilidade (a11y) apoia-se nessa semântica: landmarks navegáveis, hierarquia correta de headings, textos alternativos e atributos ARIA apenas quando necessário [2].\n\n**Por que importa?** As diretrizes WCAG definem critérios de conformidade que aplicações modernas precisam atender — obrigação ética e, em muitos países, legal. Sites acessíveis também têm melhor SEO e melhor experiência para todos.\n\n**O que muda na prática:** Use elementos semânticos em vez de divs genéricos, garanta navegação por teclado, contraste suficiente e teste com leitores de tela (NVDA, VoiceOver) — a semântica correta é o alicerce de tudo o que vem depois [3]."
    ),
    "FE-02-css-moderno-arquiteturas": (
        "CSS Moderno e Arquiteturas de Estilização",
        "CSS Moderno e Arquiteturas de Estilização: Metodologias (BEM), Flexbox, CSS Grid, Custom Properties e pré-processadores",
        "Metodologias (BEM), Flexbox, CSS Grid, Custom Properties e pré-processadores",
        "O CSS moderno é uma linguagem de arquitetura: Flexbox e Grid resolvem layouts complexos, Custom Properties centralizam design tokens e metodologias como BEM organizam a escala. Este livro cobre o CSS do zero ao avançado com foco em estilização escalável e manutenível.",
        "Estilização escalável não é acúmulo de regras: é arquitetura. Flexbox e Grid resolvem o layout, Custom Properties tornam o tema centralizado, e metodologias como BEM mantêm o código previsível à medida que o projeto cresce.",
        "Flexbox resolve layouts unidimensionais com alinhamento e distribuição de espaço [1]. CSS Grid é bidimensional: define linhas e colunas que formam um sistema de grade completo [2]. Custom Properties (variáveis CSS) centralizam design tokens e permitem temas dinâmicos em runtime.\n\n**Por que importa?** A escalabilidade vem das metodologias: BEM organiza as classes em Bloco-Elemento-Modificador, e os pré-processadores (Sass, LESS) adicionam aninhamento e funções que o CSS puro ainda não tem.\n\n**O que muda na prática:** Use Grid para o layout da página, Flexbox para componentes, tokens em variáveis e uma metodologia de nomenclatura consistente — a arquitetura de estilos suporta o crescimento do projeto [3]."
    ),
    "FE-03-javascript-essencial-assincrono": (
        "JavaScript Essencial e Programação Assíncrona",
        "JavaScript Essencial e Programação Assíncrona: Manipulação avançada do DOM, escopos, closures, Promises e async/await",
        "Manipulação avançada do DOM, escopos, closures, Promises e async/await",
        "JavaScript é a linguagem da web — e a mais mal compreendida. Escopos, closures, event loop, Promises e async/await explicam os comportamentos mais surpreendentes do dia a dia. Este livro cobre o essencial do ES6+ com profundidade técnica real, do DOM à programação assíncrona avançada.",
        "JavaScript não se aprende por acaso: seus mecanismos internos — escopos, closures, protótipos e o event loop — governam o comportamento de qualquer aplicação. Dominá-los é a diferença entre código que funciona por sorte e código que funciona por compreensão.",
        "Closures são funções que lembram o escopo onde foram criadas, permitindo encapsulamento de estado [1]. O event loop gerencia a assincronicidade: Promises e async/await organizam operações que não bloqueiam a thread principal, e a manipulação avançada do DOM usa event delegation e mutation observers [2].\n\n**Por que importa?** Erros clássicos — var no lugar de let, this perdido e memory leaks por closures — são evitados quando os mecanismos são compreendidos. O DOM é a ponte entre o JavaScript e a página.\n\n**O que muda na prática:** Pratique closures para encapsulamento, use async/await com Promise.all para paralelismo e delegue eventos no DOM para performance e simplicidade [3]."
    ),
    "FE-04-typescript-frontend": (
        "Ecossistema TypeScript no Frontend",
        "Ecossistema TypeScript no Frontend: Tipagem estática, interfaces, generics e segurança de tipos em aplicações web",
        "Tipagem estática, interfaces, generics e segurança de tipos em aplicações web",
        "TypeScript é o padrão de fato do frontend moderno: tipagem estática que move erros de runtime para compile-time, interfaces que documentam contratos e generics que generalizam com segurança. Este livro ensina a aplicar o ecossistema TypeScript em aplicações web reais.",
        "TypeScript não é JavaScript com tipos de enfeite: é uma ferramenta de engenharia. Com strict mode, interfaces e generics bem aplicados, o compilador vira um aliado que impede classes inteiras de bugs antes de chegar ao navegador.",
        "TypeScript adiciona um sistema de tipos estático ao JavaScript, compilado antes da execução [1]. Interfaces descrevem a forma de objetos, generics permitem funções e tipos parametrizados, e o type narrowing reduz tipos amplos a específicos por análise de fluxo [2].\n\n**Por que importa?** Uma parcela significativa dos bugs de frontend é capturável em compile-time: typos, null/undefined e chamadas erradas. O TypeScript documenta contratos de código e melhora o autocomplete em todo o ecossistema.\n\n**O que muda na prática:** Ative strict mode, modele domínios com discriminated unions, use generics em utilitários e prefira type guards em vez de casts agressivos [3]."
    ),
    "FE-05-dominando-react": (
        "Dominando o React.js",
        "Dominando o React.js: Componentização avançada, ciclo de vida, gerenciamento de estado local e custom hooks",
        "Componentização avançada, ciclo de vida, gerenciamento de estado local e custom hooks",
        "React é mais que componentes: é um modelo mental de UI como função do estado. Este livro vai além dos tutoriais — componentização avançada, ciclo de vida, estado local, custom hooks e a arquitetura de aplicações React maduras.",
        "Dominar React é dominar um modelo mental: a UI é uma função do estado. Componentização, hooks e fluxo unidirecional formam a base que suporta aplicações de qualquer tamanho — e entender o porquê de cada decisão evita os anti-padrões mais comuns.",
        "React é uma biblioteca para interfaces declarativas: o desenvolvedor descreve o que a UI deve ser dado um estado, e o React atualiza o DOM [1]. O ciclo de vida moderno é governado por hooks: useEffect para efeitos, useMemo/useCallback para performance e custom hooks para encapsular lógica reutilizável [2].\n\n**Por que importa?** A componentização divide a interface em unidades reutilizáveis; o estado local alimenta o fluxo de dados unidirecional. Custom hooks extraem lógica de domínio que pode ser testada isoladamente.\n\n**O que muda na prática:** Modele componentes pequenos e focados, extraia hooks para lógica reutilizável, entenda quando cada re-render acontece e use memoização apenas onde há ganho real [3]."
    ),
    "FE-06-nextjs-renderizacao-hibrida": (
        "Next.js e Renderização Híbrida",
        "Next.js e Renderização Híbrida: Estratégias de SSR, SSG, ISR e Server Actions para alta performance e SEO",
        "Estratégias de SSR, SSG, ISR e Server Actions para alta performance e SEO",
        "A renderização não é uma escolha binária: é um espectro. Next.js permite combinar SSR, SSG, ISR e Server Actions página a página — a estratégia certa para cada caso de uso. Este livro explica cada modo de renderização e quando usá-lo para alta performance e SEO.",
        "A escolha de renderização define a performance percebida: SSG entrega estático no edge, ISR revalida em segundo plano, SSR personaliza por requisição e Server Actions movem mutações para o servidor. Dominar esse espectro é o que separa apps rápidos de apps lentos.",
        "O Next.js oferece várias estratégias de renderização: SSG (Static Site Generation) pré-renderiza no build; SSR (Server-Side Rendering) renderiza por requisição; ISR (Incremental Static Regeneration) revalida páginas estáticas em segundo plano [1]. Server Actions permitem mutações de servidor sem API dedicada [2].\n\n**Por que importa?** O HTML renderizado no servidor chega pronto ao navegador: melhor SEO, melhor primeira pintura e menos JavaScript no cliente. A escolha certa por página otimiza os Core Web Vitals.\n\n**O que muda na prática:** Use SSG para conteúdo, ISR para dados semi-dinâmicos, SSR para dados personalizados e Client Components apenas quando a interatividade exige [3]."
    ),
    "FE-07-estado-global-servidor": (
        "Gerenciamento de Estado Global e Servidor",
        "Gerenciamento de Estado Global e Servidor: Otimização de dados assíncronos com TanStack Query, Zustand e Context API",
        "Otimização de dados assíncronos com TanStack Query, Zustand e Context API",
        "O estado é o coração da aplicação — e gerenciá-lo mal é a fonte dos bugs mais caros. TanStack Query resolve o estado de servidor, Zustand o estado de UI compartilhado e Context API os temas e preferências. Este livro define quando e como usar cada ferramenta.",
        "Gerenciamento de estado não é competição entre bibliotecas: é decisão de arquitetura. Separar estado de servidor (dados da API) de estado de cliente (UI e sessão) — e escolher a ferramenta certa para cada um — reduz drasticamente a complexidade.",
        "O estado de servidor merece TanStack Query: cache, revalidação, retries e sincronização automática [1]. O estado de cliente simples usa Context API; o estado complexo e compartilhado beneficia-se de Zustand, leve e sem boilerplate [2].\n\n**Por que importa?** A maioria dos 'problemas de estado' em React é, na verdade, problema de dados de servidor — que o TanStack Query resolve com API declarativa. Usar a ferramenta errada adiciona complexidade sem ganho.\n\n**O que muda na prática:** Use Query para dados assíncronos, Context para temas e preferências, Zustand para estado de UI compartilhado e evite reimplementar o que o TanStack Query já resolve [3]."
    ),
    "FE-08-formularios-validacao": (
        "Formulários Complexos e Validação de Dados",
        "Formulários Complexos e Validação de Dados: Integração de alta performance entre React Hook Form e esquemas Zod",
        "Integração de alta performance entre React Hook Form e esquemas Zod",
        "Formulários são a interface mais crítica — e a mais negligenciada: re-renders desnecessários, validação espalhada e estados inconsistentes. React Hook Form com Zod oferece a combinação moderna: performance, tipagem e validação em um só lugar. Este livro cobre formulários complexos na prática.",
        "Um formulário bem construído é vitrine de qualidade de engenharia. Com React Hook Form controlando o estado de forma performática e Zod validando com tipos TypeScript, você elimina uma classe inteira de bugs e atrasos de UX.",
        "React Hook Form gerencia o estado de formulários minimizando re-renders, usando refs em vez de estado controlado a cada tecla [1]. Zod define schemas de validação que são também fontes de tipo TypeScript — uma única fonte de verdade para forma e regras [2].\n\n**Por que importa?** A integração resolve: o resolver do Zod valida no submit e em cada campo, com mensagens de erro tipadas e internacionalizáveis. Formulários complexos — dinâmicos, com dependência entre campos — ficam previsíveis.\n\n**O que muda na prática:** Defina o schema Zod do domínio, conecte via resolver, use erros tipados no formulário e reutilize o schema no backend para validação dupla [3]."
    ),
    "FE-09-testes-automatizados-interfaces": (
        "Testes Automatizados para Interfaces",
        "Testes Automatizados para Interfaces: Garantia de regressão e estabilidade com Vitest, Testing Library e Cypress",
        "Garantia de regressão e estabilidade com Vitest, Testing Library e Cypress",
        "Testar frontend era tratado como difícil — até Vitest e Testing Library mudarem as regras. Testar o que o usuário vê e interage, em vez de detalhes de implementação, tornou os testes de interface rápidos, estáveis e valiosos. Este livro cobre a estratégia completa de testes de interface.",
        "Testes de interface são a rede de segurança que permite refatorar com confiança. Com Testing Library testando comportamento do usuário, Vitest executando em milissegundos e Cypress cobrindo fluxos E2E, a interface ganha a mesma proteção que o backend sempre teve.",
        "Vitest é um test runner nativo do ecossistema Vite, rápido e compatível com Jest [1]. Testing Library promove testar a UI como o usuário a enxerga: queries por papel (getByRole), eventos reais e asserções de acessibilidade [2].\n\n**Por que importa?** Testar detalhes de implementação (classes, estado interno) gera testes frágeis que quebram sem bug real. Testes baseados em comportamento sobrevivem a refatorações e documentam a experiência esperada.\n\n**O que muda na prática:** Teste por papel e texto visível, use userEvent para interações, cubra fluxos críticos (login, formulários) e integre a cobertura no CI [3]."
    ),
    "FE-10-performance-web-core-vitals": (
        "Performance Web e Core Web Vitals",
        "Performance Web e Core Web Vitals: Técnicas avançadas de otimização de ativos, lazy loading e métricas de velocidade de carregamento",
        "Técnicas avançadas de otimização de ativos, lazy loading e métricas de velocidade de carregamento",
        "Velocidade é feature: cada 100ms de atraso custa conversão, e o Google mede a experiência via Core Web Vitals. Este livro ensina a auditar e otimizar performance web de forma sistemática — LCP, INP, CLS, lazy loading, code splitting e otimização de assets.",
        "Performance não é fase do projeto: é disciplina contínua, medida e protegida. Dominar os Core Web Vitals e as técnicas de otimização — imagens, fontes, JavaScript e cache — transforma sites lentos em experiências instantâneas.",
        "Os Core Web Vitals são métricas centradas no usuário: LCP (maior conteúdo visível), INP (capacidade de resposta) e CLS (estabilidade visual) [1]. Otimizações clássicas incluem lazy loading (loading=lazy), code splitting via dynamic import e otimização de assets (AVIF/WebP, minificação) [2].\n\n**Por que importa?** O INP mede a latência real de interação; o CLS mede saltos de layout. Ambos afetam ranking de busca e, mais importante, a percepção de qualidade do usuário.\n\n**O que muda na prática:** Meça com Lighthouse e Web Vitals, priorize o LCP com pré-carregamento, evite layout shift reservando espaço de mídia e reduza o JavaScript que bloqueia a renderização [3]."
    ),

    # ═══════════════ SÉRIE BE — BACKEND ═══════════════
    "BE-01-nodejs-event-loop": (
        "Fundamentos do Node.js e Event Loop",
        "Fundamentos do Node.js e Event Loop: Arquitetura assíncrona orientada a eventos do motor V8 e streams de dados",
        "Arquitetura assíncrona orientada a eventos do motor V8 e streams de dados",
        "Node.js levou JavaScript ao servidor com uma arquitetura radical: event loop single-thread, I/O assíncrono e o motor V8. Este livro explica como essa máquina funciona por dentro — e como streams de dados e o modelo orientado a eventos sustentam aplicações escaláveis.",
        "Entender o event loop é entender o que o Node faz de melhor — e o que ele não faz. I/O não bloqueante, single thread, streams e o modelo orientado a eventos formam a base de todo o ecossistema backend.",
        "Node.js executa JavaScript no motor V8 do Chrome fora do navegador [1]. Seu modelo de concorrência é o event loop: operações de I/O são delegadas ao sistema e o loop continua processando outras tarefas; callbacks, Promises e async/await retornam quando a operação termina [2].\n\n**Por que importa?** Streams processam dados em pedaços, sem carregar arquivos inteiros na memória — essencial para uploads, logs e grandes arquivos. O modelo orientado a eventos escala bem para I/O intensivo.\n\n**O que muda na prática:** Evite operações síncronas bloqueantes em produção, use streams para arquivos grandes e entenda o papel do worker pool (libuv) para tarefas pesadas [3]."
    ),
    "BE-02-servidores-express-fastify": (
        "Desenvolvimento de Servidores com Express.js e Fastify",
        "Desenvolvimento de Servidores com Express.js e Fastify: Criação de rotas, middlewares modulares e tratamento robusto de erros",
        "Criação de rotas, middlewares modulares e tratamento robusto de erros",
        "Express dominou o Node por uma década; Fastify chegou com performance e schema validation. Este livro ensina a construir servidores sólidos com ambos — rotas, middlewares modulares, tratamento de erros centralizado e boas práticas de produção.",
        "Um servidor bem estruturado é a porta de entrada do produto: contratos claros, middlewares modulares e erros consistentes definem a qualidade percebida por todos os clientes. A arquitetura de rotas e middlewares é a parte que escala.",
        "Express e Fastify são frameworks HTTP para Node. Express é minimalista e ubíquo, com middlewares como funções no pipeline de requisição [1]. Fastify prioriza performance e validação de schema (JSON Schema) embutida [2].\n\n**Por que importa?** Middlewares permitem cross-cutting concerns (auth, logging, CORS, rate limit) em camadas reutilizáveis. O tratamento de erros centralizado garante respostas consistentes — o que os clientes precisam para reagir corretamente.\n\n**O que muda na prática:** Organize rotas por recurso, use middlewares para validação e autenticação, centralize erros em um handler único e documente com OpenAPI [3]."
    ),
    "BE-03-clean-architecture-ddd": (
        "Clean Architecture e Domain-Driven Design (DDD)",
        "Clean Architecture e Domain-Driven Design (DDD): Separação estrita de camadas entre Domínio, Aplicação e Infraestrutura",
        "Separação estrita de camadas entre Domínio, Aplicação e Infraestrutura",
        "Clean Architecture e DDD se complementam: o primeiro organiza as camadas com dependências apontando para dentro; o segundo modela o domínio com a linguagem do negócio. Este livro aplica a combinação em Node/TypeScript na prática — domínio rico, aplicação enxuta e infraestrutura plugável.",
        "A arquitetura do backend determina o custo de cada nova feature. Quando o domínio não conhece o framework, o banco ou o HTTP, as regras de negócio sobrevivem a qualquer mudança tecnológica — e os testes rodam sem infraestrutura.",
        "A Clean Architecture organiza o código em camadas concêntricas: no centro o domínio (entidades e casos de uso), depois a aplicação e, na borda, a infraestrutura [1]. O DDD contribui com bounded contexts, entidades, value objects e a linguagem ubíqua do negócio [2].\n\n**Por que importa?** A regra de dependência aponta para dentro: o domínio não importa nada externo. Isso permite testar casos de uso com mocks, trocar de banco ou de framework sem tocar na lógica de negócio.\n\n**O que muda na prática:** Modele o domínio com a linguagem do negócio, separe casos de uso da infraestrutura, injete dependências e mantenha controllers finos [3]."
    ),
    "BE-04-solid-design-patterns": (
        "Princípios SOLID e Design Patterns no Backend",
        "Princípios SOLID e Design Patterns no Backend: Aplicação prática de padrões de projeto e código limpo em ambientes corporativos",
        "Aplicação prática de padrões de projeto e código limpo em ambientes corporativos",
        "SOLID e Design Patterns não são dogmas: são decisões que reduzem o custo de mudança. Em ambientes corporativos — onde o backend evolui com múltiplos times — a clareza e a separação de responsabilidades determinam a velocidade a longo prazo. Este livro aplica os princípios na prática.",
        "O custo real de software está na manutenção, não na construção. Cada princípio SOLID ataca uma causa específica de fragilidade — acoplamento, rigidez e quebra inesperada ao estender — e os padrões de projeto dão vocabulário compartilhado ao time.",
        "SOLID é um acrônimo de cinco princípios: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation e Dependency Inversion [1]. Padrões de projeto como Repository, Factory, Strategy e Observer resolvem problemas recorrentes com soluções testadas [2].\n\n**Por que importa?** Em ambientes corporativos, o código é lido muitas vezes mais do que escrito. Padrões e princípios reduzem a fricção do onboarding e o custo de cada mudança — desde que aplicados com discernimento, sem over-engineering.\n\n**O que muda na prática:** Extraia responsabilidades em módulos pequenos, programe para interfaces, inverta dependências com injeção e aplique padrões apenas quando o problema exigir [3]."
    ),
    "BE-05-websockets-tempo-real": (
        "Comunicação em Tempo Real com WebSockets",
        "Comunicação em Tempo Real com WebSockets: Arquitetura de eventos bidirecionais de baixa latência para chats e dashboards",
        "Arquitetura de eventos bidirecionais de baixa latência para chats e dashboards",
        "O HTTP é pedido-resposta; o tempo real exige conexão persistente bidirecional. WebSockets e Socket.io permitem chats, notificações e dashboards ao vivo. Este livro cobre o protocolo, os padrões de arquitetura e a escala de aplicações em tempo real.",
        "Tempo real não é um recurso: é uma mudança de arquitetura. Conexões persistentes, eventos bidirecionais e reconexão resiliente têm regras próprias — e o Socket.io abstrai a complexidade mantendo o controle nas mãos do desenvolvedor.",
        "WebSockets estabelecem uma conexão TCP persistente bidirecional entre cliente e servidor, após um handshake HTTP [1]. Socket.io abstrai WebSockets com fallbacks (long-polling), salas (rooms), eventos nomeados e reconexão automática [2].\n\n**Por que importa?** Escalar tempo real exige atenção: balanceamento de carga com sticky sessions, redis adapter para múltiplas instâncias e horizontal scaling do servidor de sockets.\n\n**O que muda na prática:** Modele o domínio por eventos (message:created, user:joined), use rooms para canais e configure o adapter Redis quando crescer para mais de uma instância [3]."
    ),
    "BE-06-filas-mensagens": (
        "Processamento Assíncrono e Filas de Mensagens",
        "Processamento Assíncrono e Filas de Mensagens: Gerenciamento de tarefas em segundo plano com Redis e BullMQ",
        "Gerenciamento de tarefas em segundo plano com Redis e BullMQ",
        "Nem todo trabalho precisa acontecer na requisição: envio de e-mails, processamento de imagens e relatórios são tarefas de segundo plano. Filas com Redis e BullMQ dão resiliência e escala a esse trabalho. Este livro cobre o design e a operação de filas em produção.",
        "Filas são o padrão para desacoplar trabalho pesado da resposta ao usuário. Com Redis e BullMQ, você ganha retries, agendamento, prioridade e observabilidade — transformando tarefas frágeis em pipelines resilientes.",
        "Filas de mensagens seguem o padrão produtor-consumidor: um job é publicado, um worker o processa [1]. BullMQ, construído sobre Redis, oferece filas persistentes, retries com backoff, agendamento, prioridade e fluxos de dependência entre jobs [2].\n\n**Por que importa?** A idempotência é o contrato crítico: reprocessar um job não deve causar efeito duplicado. A observabilidade (filas, jobs concluídos, falhas) é essencial para operar em produção.\n\n**O que muda na prática:** Mova operações lentas para workers, torne os handlers idempotentes, configure retries com backoff exponencial e monitore o tamanho das filas [3]."
    ),
    "BE-07-seguranca-owasp": (
        "Segurança Avançada e OWASP Top 10",
        "Segurança Avançada e OWASP Top 10: Mitigação de vulnerabilidades, sanitização de inputs, CORS e rate limiting",
        "Mitigação de vulnerabilidades, sanitização de inputs, CORS e rate limiting",
        "A segurança de uma aplicação se decide no backend: cada input, cada header e cada endpoint é uma superfície de ataque. Este livro traduz o OWASP Top 10 para o dia a dia do Node — sanitização, SQL injection, XSS, CSRF, CORS e rate limiting — com defesas práticas.",
        "Segurança não é feature: é propriedade do sistema. Conhecer o OWASP Top 10 e aplicar defesas por camadas — validação de entrada, controle de saída, política CORS e limitação de taxa — reduz drasticamente a superfície de ataque.",
        "O OWASP Top 10 lista as vulnerabilidades mais críticas: Injection, Broken Access Control, XSS, CSRF e Security Misconfiguration, entre outras [1]. As defesas fundamentais incluem sanitização e validação de inputs, queries parametrizadas, escaping de saída e políticas CORS restritas [2].\n\n**Por que importa?** Rate limiting protege contra brute force e abuso; headers de segurança (CSP, HSTS) endurecem o navegador; e a atualização de dependências elimina vulnerabilidades conhecidas.\n\n**O que muda na prática:** Valide tudo na entrada, parametrize queries, use helmet para headers seguros, configure CORS com lista de origens e adicione rate limit por rota sensível [3]."
    ),
    "BE-08-autenticacao-autorizacao": (
        "Autenticação e Autorização Seguras",
        "Autenticação e Autorização Seguras: Implementação de fluxos com JWT, Cookies HttpOnly, OAuth2 e controle de acesso RBAC",
        "Implementação de fluxos com JWT, Cookies HttpOnly, OAuth2 e controle de acesso RBAC",
        "Autenticação responde 'quem é você?'; autorização responde 'o que você pode fazer?'. JWT, cookies HttpOnly, OAuth2 e RBAC são as ferramentas modernas dessas respostas. Este livro cobre o desenho seguro de sessões e controle de acesso em profundidade.",
        "Autenticação e autorização são as linhas de defesa mais sensíveis do produto — e as mais fáceis de errar. Entender as diferenças entre JWT em localStorage vs cookies HttpOnly, os fluxos do OAuth2 e a modelagem de RBAC evita as falhas mais exploradas.",
        "JWT (JSON Web Token) é um token assinado que carrega claims — mas sua segurança depende do armazenamento: cookies HttpOnly com Secure e SameSite são superiores a localStorage, acessível a XSS [1]. OAuth2 delega autenticação a provedores (Google, GitHub) com tokens de acesso e refresh [2].\n\n**Por que importa?** RBAC (Role-Based Access Control) modela permissões por roles e capacidades, com middlewares que verificam a autorização por rota. O refresh token rotativo e a revogação completam o ciclo seguro.\n\n**O que muda na prática:** Prefira cookies HttpOnly para sessões, use access tokens de curta duração com refresh tokens e implemente RBAC com middlewares por recurso [3]."
    ),
    "BE-09-testes-integracao-contrato": (
        "Testes de Integração e Contrato",
        "Testes de Integração e Contrato: Validação de endpoints e regras de negócio com Supertest, Jest e arquiteturas mockadas",
        "Validação de endpoints e regras de negócio com Supertest, Jest e arquiteturas mockadas",
        "Um backend sem testes de integração é uma caixa preta: você só descobre que quebrou algo quando o cliente reclama. Supertest e Jest validam rotas, banco e regras de negócio em segundos — com arquiteturas mockadas para isolar o que interessa. Este livro ensina a estratégia completa.",
        "Testes de integração provam que o sistema funciona como um todo: rotas, banco, middlewares e regras de negócio juntos. Com a pirâmide de testes equilibrada — unitários rápidos, integração focada e contrato estável — o backend evolui com confiança.",
        "Jest é o test runner mais difundido do ecossistema Node [1]. Supertest dispara requisições HTTP reais contra a aplicação sem subir o servidor, validando status, corpo e headers [2]. Mocks de dependências (banco, serviços externos) isolam a unidade testada.\n\n**Por que importa?** Testes de integração capturam os bugs que os unitários não veem: contratos de rota, serialização, transações e interações com o banco. Um banco de testes (testcontainers ou SQLite) isola o ambiente.\n\n**O que muda na prática:** Teste cada rota com cenários felizes e de erro, isole o banco por teste e rode a suíte no CI a cada push [3]."
    ),
    "BE-10-microsservicos-escalaveis": (
        "Desenvolvimento de Microsserviços Escaláveis",
        "Desenvolvimento de Microsserviços Escaláveis: Comunicação entre serviços via gRPC, filas e gateways de API",
        "Comunicação entre serviços via gRPC, filas e gateways de API",
        "Microsserviços resolvem um problema organizacional: escalar times sem atropelo. A comunicação entre serviços — gRPC para chamadas síncronas, filas para assíncronas e gateways de API na borda — é o esqueleto dessa arquitetura. Este livro cobre o desenvolvimento de microsserviços escaláveis na prática.",
        "A maturidade está em começar simples e evoluir com critério: monolito modular primeiro, divisão por fronteiras de domínio quando o time e a escala exigirem. A comunicação entre serviços e a observabilidade são o que sustentam a arquitetura distribuída.",
        "Microsserviços dividem o sistema em serviços independentes por domínio [1]. A comunicação síncrona usa gRPC (HTTP/2, protobuf, baixa latência) ou REST; a assíncrona usa filas (RabbitMQ, Kafka, BullMQ); e o gateway de API concentra roteamento e autenticação de borda [2].\n\n**Por que importa?** O custo distribuído é real: operação, consistência de dados e debugging entre serviços. Contratos de API, tolerância a falhas e observabilidade distribuída são pré-requisitos de escala.\n\n**O que muda na prática:** Comece com fronteiras claras de domínio, defina contratos de comunicação e implemente retries, circuit breakers e tracing distribuído antes de escalar [3]."
    ),

    # ═══════════════ SÉRIE BD — BANCO DE DADOS ═══════════════
    "BD-01-modelagem-relacional-sql": (
        "Modelagem de Dados Relacionais (SQL)",
        "Modelagem de Dados Relacionais (SQL): Técnicas de normalização, chaves estrangeiras, restrições e integridade referencial",
        "Técnicas de normalização, chaves estrangeiras, restrições e integridade referencial",
        "Antes do ORM, existe o modelo: entidades, relacionamentos, normalização e integridade. Este livro ensina modelagem relacional de verdade — da teoria da normalização às restrições e chaves estrangeiras que garantem consistência em PostgreSQL e MySQL.",
        "Um bom modelo relacional é a fundação silenciosa de qualquer sistema que dura. Normalização correta, chaves estrangeiras e restrições previnem dados inconsistentes — problemas que ORMs sozinhos não resolvem.",
        "A modelagem relacional organiza dados em tabelas com chaves primárias e estrangeiras que garantem integridade [1]. A normalização elimina redundância em formas normais (1NF, 2NF, 3NF), enquanto a desnormalização controlada otimiza leituras [2].\n\n**Por que importa?** Restrições (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) são a última linha de defesa da consistência: elas impedem que dados inválidos entrem no banco, independentemente de quem escreve o código.\n\n**O que muda na prática:** Modele pelo domínio, normalize até 3NF e desnormalize com consciência, use chaves estrangeiras para integridade referencial e valide com EXPLAIN [3]."
    ),
    "BD-02-otimizacao-consultas-indices": (
        "Otimização de Consultas e Índices",
        "Otimização de Consultas e Índices: Estratégias de indexação (B-Tree, Hash), planos de execução e tunning em PostgreSQL ou MySQL",
        "Estratégias de indexação (B-Tree, Hash), planos de execução e tunning em PostgreSQL ou MySQL",
        "Consultas lentas derrubam sistemas — e a maioria dos gargalos está em índices ausentes ou mal planejados. Este livro ensina estratégias de indexação (B-Tree, Hash, GIN), leitura de planos de execução e tunning de consultas em PostgreSQL e MySQL.",
        "A otimização de consultas é a disciplina que mantém o banco rápido à medida que os dados crescem. Índices bem escolhidos aceleram leituras, o EXPLAIN revela o que o planner decide e o tunning ajusta configurações que fazem a diferença em escala.",
        "Índices B-Tree aceleram igualdade e faixa; índices Hash, igualdade exata; e índices GIN/GiST, buscas textuais e vetoriais [1]. O plano de execução (EXPLAIN ANALYZE) mostra onde a query gasta tempo: full scans, joins ineficientes e condições não sargable [2].\n\n**Por que importa?** Cada índice custa escrita e espaço — criar índice demais é tão ruim quanto de menos. O tunning de configuração (work_mem, shared_buffers, connection pool) complementa as decisões de modelagem.\n\n**O que muda na prática:** Use EXPLAIN ANALYZE antes de otimizar, crie índices para as queries reais, evite funções em colunas indexadas e revise a configuração com métricas [3]."
    ),
    "BD-03-orms-query-builders": (
        "Dominando ORMs e Query Builders",
        "Dominando ORMs e Query Builders: Mapeamento objeto-relacional seguro e eficiente com Prisma, Drizzle ORM ou TypeORM",
        "Mapeamento objeto-relacional seguro e eficiente com Prisma, Drizzle ORM ou TypeORM",
        "ORMs prometem produtividade e segurança — e entregam ambos quando bem usados. Prisma, Drizzle e TypeORM dominam o ecossistema TypeScript. Este livro compara as ferramentas, ensina modelagem com schema, migrations e quando escapar para SQL puro.",
        "ORMs não eliminam o SQL: abstraem-no. O valor está na tipagem de ponta a ponta, nas migrations e na prevenção de SQL injection — mas o custo aparece em queries complexas mal modeladas. A maturidade está em saber quando o ORM ajuda e quando atrapalha.",
        "Prisma oferece schema declarativo, client tipado e migrations automáticas [1]. Drizzle ORM prioriza a proximidade com SQL e performance, com TypeScript-first. TypeORM, o veterano, segue o estilo decorator do TypeScript [2].\n\n**Por que importa?** Queries parametrizadas dos ORMs previnem SQL injection por padrão. Relações (includes), paginação e transações são abstrações que aceleram o desenvolvimento — mas o raw SQL continua disponível para o que precisa de precisão.\n\n**O que muda na prática:** Modele o schema no ORM, use migrations versionadas, tipifique as queries de ponta a ponta e caia para SQL raw quando a query exige (relatórios, agregações complexas) [3]."
    ),
    "BD-04-nosql-mongodb": (
        "Bancos de Dados NoSQL e Modelagem Flexível",
        "Bancos de Dados NoSQL e Modelagem Flexível: Quando e como utilizar MongoDB para documentos estruturados e sem esquema fixo",
        "Quando e como utilizar MongoDB para documentos estruturados e sem esquema fixo",
        "Nem todos os dados cabem em tabelas: documentos, catálogos e esquemas que evoluem rápido pedem bancos NoSQL. O MongoDB, com documentos JSON-like e escalabilidade horizontal, é o mais popular. Este livro ensina quando usá-lo e como modelar para ele.",
        "NoSQL não é 'sem SQL': é 'não apenas SQL'. O MongoDB brilha em dados flexíveis, protótipos que evoluem e escala horizontal — mas o modelamento em documentos segue regras próprias que, mal aplicadas, geram dados inconsistentes.",
        "MongoDB armazena documentos BSON com esquema flexível [1]. A modelagem é guiada pelos padrões de acesso: embedding para dados lidos juntos e referências para relacionamentos que crescem (1-N, N-N) [2].\n\n**Por que importa?** O esquema flexível acelera a evolução, mas transfere a responsabilidade de consistência para a aplicação. Índices e aggregation pipelines são as ferramentas de performance.\n\n**O que muda na prática:** Modele pelos padrões de leitura, use embedding quando faz sentido e referências quando não, e adote transações multi-documento para operações atômicas críticas [3]."
    ),
    "BD-05-chave-valor-redis": (
        "Estruturas de Chave-Valor e Caching com Redis",
        "Estruturas de Chave-Valor e Caching com Redis: Armazenamento em memória para sessões, contadores e aceleração de consultas",
        "Armazenamento em memória para sessões, contadores e aceleração de consultas",
        "Quando o banco vira o gargalo de uma aplicação de alto tráfego, o cache entra em cena. O Redis — armazenamento em memória com estruturas de dados ricas — é a ferramenta padrão para sessões, contadores e aceleração de consultas. Este livro ensina estratégias de caching e padrões de uso.",
        "Caching é a arte de responder rápido sem consultar a fonte a cada vez. O Redis entrega latência de microsegundos e estruturas de dados (strings, hashes, sets, sorted sets) que resolvem problemas além do cache — sessões, rate limiting e leaderboards.",
        "Redis é um armazenamento em memória de chave-valor com estruturas ricas [1]. Estratégias de cache: cache-aside (a aplicação gerencia o cache), write-through, write-back e TTL para expiração [2].\n\n**Por que importa?** A invalidação é o problema clássico: cache desatualizado entrega dados errados. O cache stampede — muitas requisições simultâneas para a mesma chave expirada — exige locks ou dogpile prevention.\n\n**O que muda na prática:** Cacheie com TTL e invalidação explícita, use hashes para objetos, sorted sets para rankings e o padrão read-through com fallback para o banco [3]."
    ),
    "BD-06-busca-textual-fulltext": (
        "Busca Textual e Full-Text Search",
        "Busca Textual e Full-Text Search: Implementação de mecanismos de busca avançados em bancos relacionais e motores dedicados",
        "Implementação de mecanismos de busca avançados em bancos relacionais e motores dedicados",
        "Campo de busca é a feature mais usada de qualquer aplicação — e a mais subestimada. Full-text search em PostgreSQL resolve a maioria dos casos; Elasticsearch escala para buscas avançadas com relevância e faceting. Este livro compara e implementa ambas.",
        "Busca boa é busca que entende o usuário: stemming, relevância, tolerância a erros e filtros. Começar com o full-text do PostgreSQL é barato e eficaz; migrar para Elasticsearch quando a relevância e a escala exigem é uma evolução natural.",
        "PostgreSQL oferece full-text search nativo com tsvector/tsquery, stemming em múltiplos idiomas e ranking por relevância [1]. Elasticsearch é um motor de busca distribuído baseado em Lucene, com análise de texto, relevância configurável (BM25) e faceting [2].\n\n**Por que importa?** A busca por LIKE '%termo%' não usa índice e não entende variações. O full-text usa índices GIN e compreende a linguagem; o Elasticsearch adiciona escala horizontal e análises avançadas.\n\n**O que muda na prática:** Comece com tsvector + índice GIN no PostgreSQL; quando a busca exigir relevância fina, faceting e escala, introduza o Elasticsearch com ingestão via fila [3]."
    ),
    "BD-07-migracoes-versionamento": (
        "Migrações e Versionamento de Esquema",
        "Migrações e Versionamento de Esquema: Gestão segura de alterações estruturais em bases de dados de produção sem downtime",
        "Gestão segura de alterações estruturais em bases de dados de produção sem downtime",
        "O esquema do banco evolui junto com o código — e evoluir sem quebrar produção é uma arte. Migrações versionadas e estratégias de deploy sem downtime (expand-migrate-contract) são a diferença entre mudanças suaves e incidentes. Este livro cobre o ciclo completo.",
        "Migrações são o controle de versão do banco: cada mudança de esquema é uma migração revisável, executável e reversível. Combinadas com a estratégia de deploy em fases — expandir, migrar, contrair — permitem evoluir sem downtime.",
        "Migrações versionam o esquema: cada arquivo de migração altera o banco de forma incremental e ordenada [1]. A estratégia sem downtime separa a mudança em fases: expandir o esquema para aceitar o novo estado, fazer o deploy do código, migrar os dados e contrair o esquema antigo [2].\n\n**Por que importa?** Alterações destrutivas (drop de coluna) quebram a versão antiga do código ainda em execução. A estratégia em fases mantém compatibilidade durante o rollout.\n\n**O que muda na prática:** Versione as migrações com o código, teste em staging, aplique expand-contract para mudanças destrutivas e monitore o tempo de execução das migrações [3]."
    ),
    "BD-08-seguranca-mascaramento": (
        "Segurança e Mascaramento de Dados Sensíveis",
        "Segurança e Mascaramento de Dados Sensíveis: Conformidade com LGPD/GDPR, criptografia em repouso e prevenção a SQL Injection",
        "Conformidade com LGPD/GDPR, criptografia em repouso e prevenção a SQL Injection",
        "Dados são o ativo mais valioso e o alvo mais visado: SQL injection lidera a lista de ataques há décadas, e LGPD/GDPR impõem obrigações legais. Este livro ensina a defender a camada de dados — parametrização, criptografia em repouso, mascaramento e mínimo privilégio.",
        "A segurança em dados é uma disciplina de camadas: parametrização contra injeção, criptografia em repouso e em trânsito, mascaramento para ambientes não produtivos e controle de acesso mínimo. Cada camada reduz o dano potencial de qualquer falha.",
        "SQL injection ocorre quando input do usuário é concatenado em queries — a defesa padrão são queries parametrizadas (prepared statements) [1]. A LGPD e o GDPR exigem minimização, base legal e proteção de dados pessoais, incluindo criptografia em repouso e em trânsito [2].\n\n**Por que importa?** O mascaramento substitui valores sensíveis em ambientes de desenvolvimento e testes, evitando que dados reais de clientes circulem fora de produção. O princípio do mínimo privilégio limita o dano de contas comprometidas.\n\n**O que muda na prática:** Use sempre queries parametrizadas ou ORM, criptografe dados sensíveis com chaves gerenciadas, mascare ambientes de teste e revise as permissões de banco periodicamente [3]."
    ),
    "BD-09-backup-alta-disponibilidade": (
        "Estratégias de Backup, Restore e Alta Disponibilidade",
        "Estratégias de Backup, Restore e Alta Disponibilidade: Replicação de dados, failover automático e planos de recuperação de desastres",
        "Replicação de dados, failover automático e planos de recuperação de desastres",
        "Nenhum sistema está imune a erro humano, falha de hardware ou ransomware. Backup não é opcional: é contrato de sobrevivência. Este livro ensina as estratégias de backup (full, incremental, PITR), replicação, failover automático e os planos de recuperação de desastres.",
        "Um backup que nunca foi testado é uma esperança, não uma garantia. Definir RPO (quanto dado você aceita perder) e RTO (quanto tempo para voltar) orienta a estratégia — e a replicação com failover automático reduz o RTO a minutos.",
        "Backups classificam-se em full, incremental e point-in-time recovery (PITR), que permite restaurar até um momento exato com WAL no PostgreSQL [1]. A replicação (streaming, síncrona ou assíncrona) mantém réplicas prontas para failover automático [2].\n\n**Por que importa?** A regra 3-2-1 recomenda 3 cópias, 2 mídias, 1 off-site. O teste de restauração é a única forma de saber se o backup funciona; o plano de recuperação de desastres documenta o passo a passo.\n\n**O que muda na prática:** Automatize os backups, teste restaurações periodicamente, configure replicação com failover e mantenha o runbook de recuperação atualizado [3]."
    ),
    "BD-10-bancos-vetoriais-ia": (
        "Bancos de Dados Vetoriais para IA",
        "Bancos de Dados Vetoriais para IA: Armazenamento e indexação de embeddings vetoriais com extensões como pgvector",
        "Armazenamento e indexação de embeddings vetoriais com extensões como pgvector",
        "A busca semântica é a base do RAG e das aplicações de IA: converter texto em vetores e recuperar por similaridade. pgvector estende o PostgreSQL com indexação vetorial nativa — sem infraestrutura extra. Este livro ensina a armazenar e indexar embeddings para aplicações de IA.",
        "O banco vetorial é a memória de longo prazo da aplicação de IA. pgvector combina a simplicidade do Postgres com busca de similaridade (HNSW, IVFFlat), permitindo que o RAG e os agentes recuperem conhecimento relevante com SQL padrão.",
        "Bancos vetoriais armazenam embeddings (vetores numéricos de texto) e recuperam vizinhos por similaridade de cosseno ou distância [1]. pgvector estende o PostgreSQL com tipos vetoriais e índices (HNSW, IVFFlat), evitando infraestrutura adicional [2].\n\n**Por que importa?** A busca semântica supera a busca por palavras-chave: sinônimos e paráfrases retornam resultados. O índice vetorial (HNSW) determina a velocidade e a precisão do recall — essencial para RAG em produção.\n\n**O que muda na prática:** Gere embeddings com o modelo do seu provider, armazene no pgvector com índice HNSW e combine busca vetorial com filtros SQL (metadados) para precisão [3]."
    ),

    # ═══════════════ SÉRIE AP — APIS ═══════════════
    "AP-01-arquitetura-restful": (
        "Arquitetura RESTful de Alto Padrão",
        "Arquitetura RESTful de Alto Padrão: Boas práticas de design de endpoints, verbos HTTP, códigos de status e versionamento",
        "Boas práticas de design de endpoints, verbos HTTP, códigos de status e versionamento",
        "Uma API RESTful bem projetada é um contrato que clientes confiam: recursos claros, verbos corretos, status codes significativos e versionamento que não quebra consumidores. Este livro define o padrão de design de APIs REST de alto nível.",
        "O design de API é uma decisão de produto: um contrato consistente reduz custo de integração, erros e retrabalho. Recursos, verbos HTTP, códigos de status e versionamento formam o vocabulário que todos os clientes compartilham.",
        "REST organiza a API em recursos identificados por URLs, acessados por verbos HTTP (GET, POST, PUT, PATCH, DELETE) e representados em JSON [1]. Códigos de status significativos (200, 201, 400, 404, 422, 500) comunicam o resultado de cada operação [2].\n\n**Por que importa?** A consistência reduz erros de integração; o versionamento (URL ou header) permite evoluir sem quebrar consumidores existentes. Idempotência e paginação são boas práticas que definem o padrão.\n\n**O que muda na prática:** Modele recursos pelo domínio, use verbos e status corretos, versione desde o início e documente com OpenAPI [3]."
    ),
    "AP-02-documentacao-openapi": (
        "Documentação Automatizada com OpenAPI e Swagger",
        "Documentação Automatizada com OpenAPI e Swagger: Especificação clara e interativa de contratos de API para equipes de desenvolvimento",
        "Especificação clara e interativa de contratos de API para equipes de desenvolvimento",
        "Documentação de API não é um PDF que envelhece: é um contrato vivo gerado a partir do código. OpenAPI descreve o contrato, e o Swagger UI o torna interativo. Este livro ensina a documentação automatizada que mantém o contrato sincronizado com a implementação.",
        "A documentação viva reduz custo de integração e erros: quando o contrato é gerado do código, ele nunca desatualiza. OpenAPI descreve rotas, schemas e autenticação, e o Swagger UI permite testar a API direto do navegador.",
        "OpenAPI (anteriormente Swagger) é uma especificação JSON/YAML que descreve a API: rotas, parâmetros, schemas de resposta e autenticação [1]. O Swagger UI renderiza essa especificação como uma interface interativa de testes [2].\n\n**Por que importa?** A geração a partir do código (OpenAPI generators, decorators) mantém a documentação sincronizada. A especificação vira contrato para clientes, testes e code generation.\n\n**O que muda na prática:** Gere a especificação OpenAPI do código, exponha o Swagger UI em staging, use o contrato para tipar clientes e validar contratos de integração [3]."
    ),
    "AP-03-graphql": (
        "GraphQL: Consultas Flexíveis e Schemas",
        "GraphQL: Consultas Flexíveis e Schemas: Criação de tipos, resolvers, mutations e prevenção de over-fetching ou under-fetching",
        "Criação de tipos, resolvers, mutations e prevenção de over-fetching ou under-fetching",
        "GraphQL dá ao cliente o poder de consultar exatamente o que precisa — eliminando over-fetching e under-fetching. Tipos, resolvers e mutations formam o contrato, e o N+1 problem é a armadilha clássica. Este livro ensina a criar schemas GraphQL de produção.",
        "GraphQL modela a API como um grafo tipado: o cliente consulta campos exatos, e resolvers atendem cada campo. A flexibilidade exige disciplina — schema por domínio, DataLoader para N+1 e controle de profundidade para evitar abusos.",
        "GraphQL expõe um único endpoint com um schema tipado; o cliente consulta exatamente os campos que precisa, e resolvers atendem cada campo [1]. Mutations executam mudanças de estado com o mesmo contrato tipado [2].\n\n**Por que importa?** O N+1 problem — um resolver que dispara uma query por item — é a armadilha clássica; o DataLoader resolve com batching. Controles de profundidade e complexidade protegem o servidor de consultas abusivas.\n\n**O que muda na prática:** Modele o schema pelo domínio, use DataLoader para evitar N+1, limite profundidade de consulta e monitore a performance de resolvers [3]."
    ),
    "AP-04-webhooks-eventos": (
        "Webhooks e Arquitetura orientada a Eventos",
        "Webhooks e Arquitetura orientada a Eventos: Emissão e consumo de webhooks seguros com assinaturas criptográficas e reentregas",
        "Emissão e consumo de webhooks seguros com assinaturas criptográficas e reentregas",
        "Webhooks são o padrão de notificação entre sistemas: o provedor avisa o consumidor quando algo acontece. A robustez vem das assinaturas criptográficas (verificação), da reentrega com retry e da idempotência no consumo. Este livro cobre a arquitetura orientada a eventos com webhooks.",
        "A arquitetura orientada a eventos desacopla sistemas: o provedor emite, o consumidor reage. A confiabilidade depende da segurança (assinatura), da entrega (retries) e do processamento idempotente.",
        "Webhooks são chamadas HTTP que o provedor faz ao consumidor quando um evento ocorre [1]. A verificação usa assinaturas criptográficas (HMAC) no header; a confiabilidade, reentregas com retry e expiração; o consumo exige idempotência (processar o mesmo evento duas vezes sem efeito duplicado) [2].\n\n**Por que importa?** Webhooks são fire-and-forget: o consumidor pode estar fora do ar, a rede pode falhar. Assinatura impede eventos falsificados; retry com backoff e dead-letter queue garantem que nenhum evento se perca.\n\n**O que muda na prática:** Assine os payloads com HMAC, implemente retry com backoff e expiração, e torne o processamento idempotente com IDs de evento [3]."
    ),
    "AP-05-seguranca-rate-limiting": (
        "Segurança, Throttling e Rate Limiting",
        "Segurança, Throttling e Rate Limiting: Proteção de APIs contra ataques de negação de serviço e abuso de requisições",
        "Proteção de APIs contra ataques de negação de serviço e abuso de requisições",
        "APIs públicas atraem uso legítimo — e abuso. Rate limiting, throttling e autenticação de borda protegem contra negação de serviço e excesso de requisições. Este livro ensina a proteger APIs em profundidade, com estratégias por rota, usuário e IP.",
        "Proteção de API é uma disciplina de camadas: autenticação na borda, rate limiting por chave e IP, throttling de recursos e limites de payload. Cada camada reduz a superfície de abuso sem sacrificar a experiência legítima.",
        "Rate limiting limita o número de requisições por janela de tempo, por cliente ou IP [1]. Throttling regula o consumo de recursos (conexões, workers), e o Redis é a ferramenta padrão para contadores distribuídos (sliding window, token bucket) [2].\n\n**Por que importa?** Sem rate limit, uma chave vazada ou um script abusivo derruba a API. As respostas 429 com Retry-After orientam clientes legítimos; a estratégia por camada (gateway, API, banco) protege o sistema inteiro.\n\n**O que muda na prática:** Implemente rate limit por chave e IP com Redis, devolva 429 com Retry-After e proteja rotas sensíveis com limites mais rígidos [3]."
    ),
    "AP-06-consumo-apis-terceiros": (
        "Consumo de APIs de Terceiros e Resiliência",
        "Consumo de APIs de Terceiros e Resiliência: Implementação de padrões Circuit Breaker, Retries e Fallbacks com Axios ou Fetch",
        "Implementação de padrões Circuit Breaker, Retries e Fallbacks com Axios ou Fetch",
        "Integrar APIs de terceiros é inevitável — e falhas delas são inevitáveis também. Retries com backoff, circuit breakers e fallbacks são os padrões que mantêm sua aplicação de pé quando o fornecedor cai. Este livro ensina o consumo resiliente de APIs externas.",
        "A resiliência a falhas de terceiros é o que separa sistemas robustos de sistemas frágeis: retry com backoff para falhas transitórias, circuit breaker para falhas prolongadas e fallback para degradação graciosa.",
        "Retries com backoff exponencial tratam falhas transitórias (timeouts, 429, 5xx) [1]. O Circuit Breaker interrompe chamadas a um serviço falho por um período, evitando cascata; o Fallback entrega uma resposta degradada quando o serviço não responde [2].\n\n**Por que importa?** Sem esses padrões, a falha de um terceiro propaga-se para sua API: retries cegos sobrecarregam o serviço falho, e a ausência de fallback derruba a experiência do usuário.\n\n**O que muda na prática:** Implemente retry com jitter e backoff, use um circuit breaker (opossum, e.g.) por serviço externo e defina fallbacks com dados em cache ou respostas parciais [3]."
    ),
    "AP-07-testes-contrato-pact": (
        "Testes de Contrato de API",
        "Testes de Contrato de API: Garantia de compatibilidade entre provedores e consumidores usando Pact",
        "Garantia de compatibilidade entre provedores e consumidores usando Pact",
        "Testes de integração entre equipes falham nos detalhes: um campo renomeado, um status mudado, um formato alterado. Testes de contrato com Pact verificam que o provedor e o consumidor concordam sobre a API — sem infraestrutura de integração cara. Este livro ensina a implementação.",
        "O teste de contrato é a balança entre o testar tudo (caro) e o não testar nada (arriscado): o consumidor define o contrato que espera, e o provedor valida que o cumpre. Pact automatiza essa verificação nos dois lados.",
        "Pact é uma ferramenta de teste de contrato: o consumidor gera um contrato (pact file) com as interações esperadas, e o provedor valida que suas respostas atendem ao contrato [1]. O ciclo roda no CI: consumidor publica, provedor verifica [2].\n\n**Por que importa?** Integrações quebram por contratos desalinhados — e o teste de contrato detecta a quebra antes do deploy, sem depender de ambientes de integração compartilhados.\n\n**O que muda na prática:** Defina os pacts a partir dos testes do consumidor, valide no provedor no CI e mantenha um broker para gerenciar a compatibilidade entre versões [3]."
    ),
    "AP-08-sse-tempo-real": (
        "APIs em Tempo Real com Server-Sent Events (SSE)",
        "APIs em Tempo Real com Server-Sent Events (SSE): Transmissão unidirecional eficiente de dados via HTTP para atualizações ao vivo",
        "Transmissão unidirecional eficiente de dados via HTTP para atualizações ao vivo",
        "Atualizações ao vivo nem sempre exigem WebSockets: quando o fluxo é unidirecional (do servidor para o cliente), Server-Sent Events entregam com simplicidade e reconexão automática sobre HTTP puro. Este livro ensina a implementar SSE para notificações, feeds e streaming.",
        "SSE é o canal simples e robusto para atualizações unidirecionais: um único endpoint HTTP que mantém a conexão aberta e envia eventos. A reconexão automática e os event IDs fazem dele a escolha certa para muitos cenários de tempo real.",
        "Server-Sent Events (SSE) é um protocolo HTTP de streaming unidirecional: o servidor mantém a conexão aberta e empurra eventos de texto (event:, data:, id:) [1]. O cliente (EventSource API) reconecta automaticamente e retoma com Last-Event-ID [2].\n\n**Por que importa?** SSE usa HTTP comum (funciona em proxies, tem cache e TLS nativo) e é mais simples que WebSockets quando a comunicação é só do servidor para o cliente — notificações, feeds e streaming de LLM.\n\n**O que muda na prática:** Prefira SSE para atualizações unidirecionais, use event IDs para retomada, e mantenha a conexão saudável com heartbeats [3]."
    ),
    "AP-09-api-gateways": (
        "Microgateways e API Gateways",
        "Microgateways e API Gateways: Roteamento centralizado, autenticação de borda e balanceamento de carga com Traefik ou Nginx",
        "Roteamento centralizado, autenticação de borda e balanceamento de carga com Traefik ou Nginx",
        "O gateway de API é a porta de entrada do sistema: roteamento centralizado, autenticação de borda, balanceamento de carga e rate limiting em um só lugar. Traefik e Nginx representam as abordagens — do automático ao declarativo. Este livro ensina a arquitetura de gateways.",
        "O API gateway concentra na borda o que seria duplicado em cada serviço: autenticação, roteamento, limitação e observação. A escolha entre Traefik (integração com containers) e Nginx (configuração madura) depende do seu ecossistema.",
        "O API gateway roteia requisições para os serviços corretos, autentica na borda, aplica rate limiting e balanceia carga entre instâncias [1]. Traefik integra-se nativamente ao Docker com service discovery; Nginx oferece configuração declarativa madura e alta performance [2].\n\n**Por que importa?** A autenticação de borda centraliza a política de segurança; o roteamento desacopla os clientes da topologia interna; e o balanceamento distribui carga e escala os serviços.\n\n**O que muda na prática:** Roteie por hostname/path no gateway, concentre auth e rate limit na borda, e use sticky sessions ou balanceamento por hash quando necessário [3]."
    ),
    "AP-10-monetizacao-ciclo-de-vida": (
        "Monetização e Gestão de Ciclo de Vida de APIs",
        "Monetização e Gestão de Ciclo de Vida de APIs: Portais de desenvolvedores, chaves de acesso (API Keys) e métricas de consumo",
        "Portais de desenvolvedores, chaves de acesso (API Keys) e métricas de consumo",
        "Uma API pode ser um produto: com portais de desenvolvedores, chaves de acesso, planos de uso e métricas de consumo. Este livro ensina a monetizar e gerir o ciclo de vida de APIs — do onboarding do desenvolvedor à medição de receita.",
        "Gestão de ciclo de vida de API transforma um endpoint em um produto gerenciado: onboarding, chaves, planos, quotas e métricas. A monetização converte o valor entregue em receita — e as métricas de consumo orientam as decisões.",
        "O ciclo de vida de uma API inclui: design, publicação, onboarding de desenvolvedores (portal), emissão de chaves (API Keys), planos de uso (quotas, limites) e métricas de consumo [1]. A monetização define modelos: gratuita com limites, por uso, por assinatura ou por tier [2].\n\n**Por que importa?** Sem gestão, a API é um custo; com portais e métricas, vira um canal. As chaves com planos permitem cobrar e proteger; as métricas mostram quem usa, como usa e quanto vale.\n\n**O que muda na prática:** Publique a documentação no portal, emita chaves com planos de quota, meça consumo por chave e evolua os modelos de monetização com dados [3]."
    ),

    # ═══════════════ SÉRIE DV — DEVOPS ═══════════════
    "DV-01-docker-conteineres": (
        "Docker e Contêineres do Zero ao Avançado",
        "Docker e Contêineres do Zero ao Avançado: Criação de Dockerfiles otimizados, multi-stage builds e gerenciamento de volumes",
        "Criação de Dockerfiles otimizados, multi-stage builds e gerenciamento de volumes",
        "Contêineres resolveram o problema mais antigo da engenharia: funciona na minha máquina. Docker empacota aplicação e dependências em unidades isoladas e reproduzíveis. Este livro cobre Docker do zero ao avançado — Dockerfiles otimizados, multi-stage builds e volumes.",
        "Docker não é só uma ferramenta: é um contrato de portabilidade entre desenvolvimento e produção. Dominar Dockerfiles multi-stage, imagens enxutas e o gerenciamento de volumes elimina a classe mais comum de bugs de ambiente.",
        "Contêineres isolam processos com namespaces e cgroups do Linux, empacotando aplicação e dependências em imagens imutáveis [1]. O Dockerfile define a imagem, e os multi-stage builds reduzem drasticamente o tamanho separando o build do runtime [2].\n\n**Por que importa?** Imagens reproduzíveis eliminam o 'na minha máquina funciona'. Volumes persistir dados entre execuções; redes definem a comunicação entre contêineres. Boas práticas: imagens base oficiais, usuário não root e camadas de cache bem ordenadas.\n\n**O que muda na prática:** Construa Dockerfiles multi-stage, defina volumes para dados persistentes e use o mesmo Dockerfile otimizado em produção [3]."
    ),
    "DV-02-docker-compose": (
        "Orquestração com Docker Compose",
        "Orquestração com Docker Compose: Configuração de ambientes multi-contêineres interligados para desenvolvimento e homologação",
        "Configuração de ambientes multi-contêineres interligados para desenvolvimento e homologação",
        "Aplicações modernas têm múltiplos serviços: app, banco, fila e cache. O Docker Compose orquestra esses contêineres interligados com um único arquivo YAML — para desenvolvimento, homologação e até produção. Este livro ensina a configurar ambientes multi-contêineres.",
        "O Compose transforma a descrição do ambiente em código versionável: cada serviço, rede e volume declarado em um arquivo. Ambientes de desenvolvimento e homologação fiéis ao de produção eliminam as surpresas do 'na minha máquina funciona'.",
        "O Docker Compose define serviços, redes e volumes em um arquivo YAML, orquestrando a criação e a interligação de contêineres [1]. Serviços comunicam-se por nomes de serviço em redes internas, com portas expostas apenas quando necessário [2].\n\n**Por que importa?** Um compose bem configurado reproduz o ambiente de produção localmente: mesma imagem, mesma rede, mesmas variáveis. Healthchecks, dependências (depends_on) e perfis permitem cenários variados.\n\n**O que muda na prática:** Defina serviços com healthchecks, separe variáveis em .env, use volumes nomeados para dados e perfis para cenários diferentes [3]."
    ),
    "DV-03-linux-para-desenvolvedores": (
        "Fundamentos de Linux para Desenvolvedores",
        "Fundamentos de Linux para Desenvolvedores: Gerenciamento de processos, permissões de arquivos, redes e manipulação de shell",
        "Gerenciamento de processos, permissões de arquivos, redes e manipulação de shell",
        "Linux é o sistema operacional da web: servidores, contêineres e CI rodam nele. Este livro ensina os fundamentos essenciais para desenvolvedores — processos, permissões, redes e shell — para operar e depurar qualquer ambiente.",
        "Dominar o Linux é dominar o ambiente onde seu código roda: processos que você precisa gerenciar, permissões que protegem o sistema e comandos de shell que aceleram a operação. É a base do DevOps e da operação em produção.",
        "Linux gerencia processos com sinais, prioridades e tools (ps, top, kill) [1]. As permissões de arquivos (rwx, chmod, chown, ACLs) definem quem acessa o quê; o shell (bash) permite pipelines, redirecionamentos e automação [2].\n\n**Por que importa?** Em servidores VPS e contêineres, a interface é o terminal: entender processos e permissões é pré-requisito para hardening e depuração. O shell é a ferramenta de automação mais universal da computação.\n\n**O que muda na prática:** Pratique gerenciamento de processos (ps, kill, systemd), revise permissões (princípio do mínimo privilégio) e monte pipelines de shell para tarefas repetitivas [3]."
    ),
    "DV-04-ci-cd-github-actions": (
        "CI/CD com GitHub Actions",
        "CI/CD com GitHub Actions: Automação de pipelines para execução de testes, verificações de linting e deploys contínuos",
        "Automação de pipelines para execução de testes, verificações de linting e deploys contínuos",
        "Integração contínua executa testes a cada push; entrega contínua deploys a cada merge. GitHub Actions tornou a automação nativa do fluxo Git. Este livro ensina a construir pipelines de CI/CD completos — do lint ao deploy em produção.",
        "CI/CD é o cinto de segurança do time: mudanças pequenas, validadas automaticamente e entregues com frequência. Com GitHub Actions, o pipeline vive ao lado do código — triggers, jobs paralelos, caches e secrets integrados.",
        "GitHub Actions automatiza workflows com triggers (push, pull_request, schedule) e jobs que rodam em runners [1]. O pipeline típico: lint e testes no push, build e deploy no merge para main [2].\n\n**Por que importa?** CI detecta regressões em minutos; CD reduz o risco de releases grandes e lentos. Secrets gerenciados, artifacts e environments com proteção completam o ciclo seguro.\n\n**O que muda na prática:** Comece com lint+testes no PR, adicione build e deploy por ambiente, cacheie dependências e proteja a main com status checks obrigatórios [3]."
    ),
    "DV-05-infraestrutura-vps": (
        "Infraestrutura e Administração de Servidores VPS",
        "Infraestrutura e Administração de Servidores VPS: Provisionamento seguro, hardening de servidores e configuração de redes locais",
        "Provisionamento seguro, hardening de servidores e configuração de redes locais",
        "Antes da nuvem gerenciada, existe a VPS: um servidor Linux seu, com poder e responsabilidade. Este livro ensina a infraestrutura e a administração de VPS do zero — provisionamento, hardening de segurança e configuração de redes — para hospedar aplicações reais.",
        "A VPS é a escola da infraestrutura: quem domina provisionamento, hardening e redes entende o que as plataformas gerenciadas automatizam. Configurar um servidor do zero dá controle total e visão completa do ambiente de produção.",
        "O provisionamento de uma VPS envolve: acesso SSH com chaves, usuário não root com sudo e firewall mínimo (UFW) [1]. O hardening inclui desabilitar login por senha, atualizar o sistema e configurar fail2ban [2].\n\n**Por que importa?** Uma VPS exposta à internet é alvo constante de bots. O hardening básico — chaves SSH, firewall e atualizações — bloqueia a maioria dos ataques automatizados. As redes locais conectam os serviços com segmentação correta.\n\n**O que muda na prática:** Provisione com chaves SSH, aplique hardening (sem senha, firewall, atualizações) e configure as redes com portas mínimas abertas [3]."
    ),
    "DV-06-proxy-reverso-ssl": (
        "Proxy Reverso e Certificados SSL",
        "Proxy Reverso e Certificados SSL: Gerenciamento de tráfego, roteamento de domínios e automação de HTTPS com Caddy ou Nginx",
        "Gerenciamento de tráfego, roteamento de domínios e automação de HTTPS com Caddy ou Nginx",
        "Na frente de todo servidor de aplicação existe um proxy reverso: roteia tráfego, termina SSL, equilibra carga e protege. Nginx e Caddy representam as abordagens — do clássico ao automático. Este livro ensina o gerenciamento de tráfego e a automação de HTTPS na prática.",
        "O proxy reverso é a porta de entrada da aplicação. Terminar TLS, rotear por hostname, servir assets estáticos e balancear múltiplas instâncias são funções que qualquer produção real exige — e que as ferramentas modernas automatizam cada vez mais.",
        "O Nginx é o proxy reverso clássico: configuração declarativa, alta performance e SSL com certbot [1]. Caddy automatiza o TLS por padrão (ACME nativo); Traefik integra-se ao Docker com service discovery automático [2].\n\n**Por que importa?** Roteamento por hostname/path, HTTP/2, compressão, rate limit e balanceamento são camadas de arquitetura. Certificados SSL renovados automaticamente eliminam o erro mais comum de produção.\n\n**O que muda na prática:** Ponha o proxy na frente da aplicação, configure SSL automático, roteie por hostname e sirva estáticos direto do proxy para aliviar a app [3]."
    ),
    "DV-07-processos-monitoramento": (
        "Gerenciamento de Processos e Monitoramento",
        "Gerenciamento de Processos e Monitoramento: Manutenção de uptime com PM2, systemd e rastreamento de logs centralizados",
        "Manutenção de uptime com PM2, systemd e rastreamento de logs centralizados",
        "A aplicação está em produção — e se o processo cair às 3h da manhã? Gerenciamento de processos (PM2, systemd) mantém o uptime com auto-restart, e os logs centralizados permitem diagnosticar o que aconteceu. Este livro ensina a operação de processos e logs.",
        "Uptime não é acaso: é gerenciamento de processos. PM2 e systemd reiniciam a aplicação automaticamente, monitoram a saúde e gerem logs; a centralização de logs torna a busca por erros viável em qualquer escala.",
        "O PM2 gerencia processos Node: auto-restart, clustering, logs e monitoramento [1]. O systemd é o gerenciador nativo do Linux, com unit files que definem serviços, restarts e dependências [2].\n\n**Por que importa?** Um processo que cai e não reinicia é um incidente silencioso. Com PM2/systemd, o restart é automático; com logs centralizados (Loki, ELK), o diagnóstico leva minutos em vez de horas.\n\n**O que muda na prática:** Gerencie a aplicação com PM2 ou systemd, configure max_memory_restart e auto-restart, e centralize os logs com rotação e retenção definidas [3]."
    ),
    "DV-08-observabilidade-erros": (
        "Observabilidade e Gestão de Erros",
        "Observabilidade e Gestão de Erros: Configuração de ferramentas de monitoramento de performance e rastreamento de falhas (Sentry)",
        "Configuração de ferramentas de monitoramento de performance e rastreamento de falhas (Sentry)",
        "Em produção, o que não é observável é invisível: você só descobre o problema quando o usuário reclama. Observabilidade é a disciplina de métricas, logs e traces — e o Sentry captura erros com contexto de usuário em tempo real. Este livro ensina a instrumentar e operar com visibilidade.",
        "Monitorar é saber que algo está errado; observar é entender por quê. Métricas (quantitativas), logs (eventos) e traces (caminho da requisição) formam os três pilares — e o Sentry agrega o rastreamento de erros com contexto rico.",
        "Observabilidade assenta em três pilares: métricas (Prometheus, Grafana), logs centralizados (Loki, ELK) e tracing distribuído (OpenTelemetry) [1]. O Sentry captura exceções com stack traces e contexto de usuário em tempo real [2].\n\n**Por que importa?** Alertas bem calibrados detectam problemas antes dos usuários; traces mostram onde a latência morre em sistemas distribuídos; o Sentry correlaciona erros com releases e usuários afetados.\n\n**O que muda na prática:** Instrumente métricas-chave (latência, erros, saturação), integre o Sentry no app, centralize os logs e defina alertas com ações documentadas [3]."
    ),
    "DV-09-iac-infraestrutura-como-codigo": (
        "Introdução à Infraestrutura como Código (IaC)",
        "Introdução à Infraestrutura como Código (IaC): Provisionamento automatizado e repetível de recursos computacionais",
        "Provisionamento automatizado e repetível de recursos computacionais",
        "Infraestrutura como Código trata recursos como software: versionado, revisado e testado. Terraform, Ansible e CloudFormation automatizam o provisionamento repetível de servidores, redes e serviços. Este livro introduz o IaC na prática, com os padrões essenciais.",
        "IaC transforma a infraestrutura em um produto de engenharia: o mesmo código provisiona ambientes idênticos, com revisão e histórico. A repetibilidade elimina a configuração manual que gera diferenças entre ambientes.",
        "O Terraform declara o estado desejado da infraestrutura e o aplica de forma idempotente, com planos de execução e estado versionável [1]. O Ansible configura servidores com playbooks declarativos; o CloudFormation modela recursos AWS em templates [2].\n\n**Por que importa?** Ambientes provisionados por código são reproduzíveis e audíveis: desenvolvimento, homologação e produção idênticos. O estado (state) é o ativo crítico do Terraform — precisa ser versionado e protegido.\n\n**O que muda na prática:** Declare a infraestrutura em módulos reutilizáveis, revise via pull request e aplique em ambientes na ordem: dev → staging → prod [3]."
    ),
    "DV-10-deploy-sem-downtime": (
        "Estratégias de Deploy sem Downtime",
        "Estratégias de Deploy sem Downtime: Implementação de manobras de atualização contínua em ambientes de produção",
        "Implementação de manobras de atualização contínua em ambientes de produção",
        "Deploy não deve ser um evento de risco: com as manobras certas — rolling, blue-green e canary — a nova versão entra em produção sem interromper o serviço. Este livro ensina as estratégias de deploy sem downtime e quando usar cada uma.",
        "O deploy contínuo reduz o risco: mudanças pequenas, reversíveis e observáveis. Rolling atualiza gradualmente, blue-green troca o ambiente inteiro e canary expõe a versão nova a uma fração do tráfego. A escolha depende da arquitetura.",
        "O rolling update substitui instâncias gradualmente, mantendo a disponibilidade durante a transição [1]. O blue-green mantém dois ambientes (azul antigo, verde novo) e troca o tráfego de uma vez, com rollback imediato. O canary direciona uma pequena fatia do tráfego à versão nova e observa antes de expandir [2].\n\n**Por que importa?** A reversibilidade é o coração do deploy sem downtime: se a versão nova falha, voltar é uma ação simples. Migrações de banco compatíveis (expand-contract) são pré-requisito para as três manobras.\n\n**O que muda na prática:** Adote rolling como padrão, blue-green para releases críticos e canary para mudanças de alto risco, com monitoramento entre cada etapa [3]."
    ),
}

# Auto-gerar lista completa de slugs
SLUGS_STACK = list(LIVROS_STACK.keys())
