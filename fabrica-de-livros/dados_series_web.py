#!/usr/bin/env python3
"""
Dados das 5 Séries de Livros de Desenvolvimento Web Fullstack (W1-W5)
Cada série tem 10 livros, cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-web.py e compilar-para-pdf.py
"""

SERIES_WEB = {
    "W1": {"nome": "Fundamentos da Web e Arquitetura", "prefixo": "W1"},
    "W2": {"nome": "Frontend: Interfaces Modernas e Escaláveis", "prefixo": "W2"},
    "W3": {"nome": "Backend: Servidores, APIs e Lógica de Negócio", "prefixo": "W3"},
    "W4": {"nome": "Bancos de Dados e Persistência de Dados", "prefixo": "W4"},
    "W5": {"nome": "DevOps, Automação, IA e Carreira Fullstack", "prefixo": "W5"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
SERIES_PARTES = {
    "W1": ["Fundamentos da Web", "Linguagens e Tecnologias", "Arquitetura e Padrões", "Ferramentas e Produtividade"],
    "W2": ["Fundamentos do Frontend Moderno", "Frameworks e Renderização", "Qualidade e Performance", "Escala e Arquitetura Frontend"],
    "W3": ["Fundamentos do Backend", "APIs e Comunicação", "Segurança e Autenticação", "Testes e Ecossistemas"],
    "W4": ["Fundamentos de Dados", "Modelagem e Persistência", "Otimização e Busca", "Operação e Integração de Dados"],
    "W5": ["Fundamentos de DevOps", "Infraestrutura e Deploy", "Automação e Observabilidade", "IA, Arquitetura e Carreira"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_WEB = {
    # ═══════════════ SÉRIE W1 — FUNDAMENTOS DA WEB E ARQUITETURA ═══════════════
    "W1-01-anatomia-da-web": (
        "A Anatomia da Web",
        "A Anatomia da Web: Como o protocolo HTTP, DNS e navegadores funcionam por trás dos panos",
        "Como o protocolo HTTP, DNS e navegadores funcionam por trás dos panos",
        "Quando você digita uma URL e a página carrega, uma cadeia complexa de eventos acontece em milissegundos: DNS, TCP, HTTP, renderização. Este livro disseca cada camada dessa anatomia e mostra como o conhecimento profundo do protocolo transforma a forma como você desenvolve para a web.",
        "A web é uma máquina maravilhosa e invisível. Dominar sua anatomia — do DNS ao HTTP, do navegador ao servidor — permite diagnosticar problemas com precisão, otimizar performance e construir aplicações que respeitam os fundamentos do meio em que vivem.",
        "A anatomia da web começa quando um usuário digita uma URL: o navegador consulta o DNS para transformar o domínio em um endereço IP, estabelece uma conexão TCP, envia uma requisição HTTP e processa a resposta [1]. O HTTP, protocolo da camada de aplicação, define verbos (GET, POST, PUT, DELETE), códigos de status e cabeçalhos que governam a comunicação entre cliente e servidor [2].\n\n**Por que importa?** Cada etapa da anatomia tem latência própria: DNS caching, conexão TCP (handshake), TLS e o próprio download dos recursos. Perfis de performance (Core Web Vitals) são medidos justamente sobre essas etapas.\n\n**O que muda na prática:** Um desenvolvedor que entende o protocolo sabe quando usar HTTP/2, quando cachear via ETag, como o Service Worker intercepta requisições e por que a ordem dos recursos no HTML importa [3]."
    ),
    "W1-02-html5-semantico-a11y": (
        "HTML5 Semântico e Acessibilidade (a11y)",
        "HTML5 Semântico e Acessibilidade (a11y): Construindo a base estrutural correta para aplicações modernas",
        "Construindo a base estrutural correta para aplicações modernas",
        "HTML é a fundação de tudo: uma semântica correta melhora SEO, acessibilidade, testes e manutenção. Este livro ensina a construir a estrutura correta desde a primeira tag — com elementos semânticos, ARIA, landmarks e boas práticas de acessibilidade que beneficiam todos os usuários.",
        "A base estrutural da web não é um detalhe: é uma decisão de arquitetura. HTML5 semântico e acessibilidade andam juntos — o mesmo código que ajuda leitores de tela também melhora SEO, reduz CSS desnecessário e facilita a vida de qualquer desenvolvedor que herde o projeto.",
        "HTML5 introduziu elementos semânticos (header, nav, main, section, article, aside, footer) que descrevem o conteúdo em vez de apenas formatá-lo [1]. A acessibilidade (a11y) usa essa semântica como base: landmarks navegáveis, hierarquia correta de headings, textos alternativos e atributos ARIA quando necessário [2].\n\n**Por que importa?** WCAG 2.1 define critérios de conformidade que aplicações modernas precisam atender. Além da obrigação ética e legal, sites acessíveis têm melhor SEO e melhor experiência para todos.\n\n**O que muda na prática:** Use elementos semânticos em vez de divs genéricos, teste com leitores de tela (NVDA, VoiceOver), garanta navegação por teclado e contraste suficiente. A semântica é a fundação que suporta tudo o que vem depois [3]."
    ),
    "W1-03-css-moderno": (
        "CSS Moderno do Zero ao Avançado",
        "CSS Moderno do Zero ao Avançado: Flexbox, Grid, Variáveis e metodologias de estilização escaláveis",
        "Flexbox, Grid, Variáveis e metodologias de estilização escaláveis",
        "O CSS que aprendemos há dez anos não é mais o CSS que escrevemos hoje: Flexbox e Grid resolvem layouts que exigiam hacks, variáveis trouxeram design tokens, e metodologias organizam a escala. Este livro cobre o CSS moderno do zero ao avançado, com foco em código escalável e manutenível.",
        "CSS moderno é uma linguagem poderosa e expressiva. Dominar Flexbox, Grid, variáveis, custom properties e metodologias (BEM, SMACSS) transforma a estilização em uma atividade previsível, organizada e escalável — em vez de um acúmulo de gambiarras.",
        "Flexbox resolve layouts unidimensionais (linha ou coluna) com alinhamento e distribuição de espaço [1]. CSS Grid, por sua vez, é bidimensional: define linhas e colunas que formam um sistema de grade completo [2]. Variáveis CSS (custom properties) permitem design tokens reutilizáveis e temas dinâmicos em runtime.\n\n**Por que importa?** Juntos, Flexbox, Grid e variáveis eliminaram a necessidade de frameworks de layout e hacks antigos (floats, tabelas). A escalabilidade vem das metodologias: BEM organiza as classes em Bloco-Elemento-Modificador, e design tokens centralizam decisões de design.\n\n**O que muda na prática:** Use Grid para o layout da página e Flexbox para componentes; centralize cores, espaçamentos e tipografia em variáveis; adote uma metodologia de nomenclatura consistente [3]."
    ),
    "W1-04-javascript-essencial": (
        "JavaScript Essencial (ES6+)",
        "JavaScript Essencial (ES6+): Closures, protótipos, assincronicidade (Promises, Async/Await) e manipulação do DOM",
        "Closures, protótipos, assincronicidade (Promises, Async/Await) e manipulação do DOM",
        "JavaScript é a linguagem da web — e a mais mal compreendida. Closures, protótipos, event loop e Promises são conceitos que separam quem copia código de quem domina a linguagem. Este livro cobre o essencial do ES6+ com profundidade técnica real.",
        "JavaScript não é uma linguagem que se aprende por acaso: seus mecanismos internos (closures, protótipos, event loop) explicam os comportamentos mais surpreendentes do dia a dia. Dominá-los é a diferença entre escrever código que funciona por sorte e código que funciona por compreensão.",
        "Closures são funções que lembram o escopo onde foram criadas, permitindo encapsulamento de estado [1]. O sistema de protótipos é o mecanismo de herança da linguagem — cada objeto tem um prototype que delega propriedades. O event loop gerencia a assincronicidade: Promises e async/await organizam operações que não bloqueiam a thread principal [2].\n\n**Por que importa?** Erros clássicos — como usar var no lugar de let, perder o this ou criar memory leaks com closures — são evitados quando os mecanismos são compreendidos. O DOM, por sua vez, é a ponte entre JavaScript e a página.\n\n**O que muda na prática:** Pratique closures com encapsulamento, entenda a diferença entre call stack e task queue, e use async/await para legibilidade com Promise.all para paralelismo [3]."
    ),
    "W1-05-typescript-na-pratica": (
        "TypeScript na Prática",
        "TypeScript na Prática: Tipagem estática, interfaces, generics e como blindar seu código contra erros em tempo de execução",
        "Tipagem estática, interfaces, generics e como blindar seu código contra erros em tempo de execução",
        "TypeScript não é JavaScript com tipos de enfeite: é uma ferramenta de engenharia que move erros de runtime para compile-time. Este livro ensina tipagem estática na prática — interfaces, generics, type narrowing e utilitários — para blindar seu código em escala real.",
        "TypeScript é o padrão de fato do desenvolvimento web moderno. Quando bem usado, o compilador vira um aliado que impede bugs inteiros de classes de erros antes de chegar ao navegador. Dominar a linguagem de tipos é um multiplicador de produtividade.",
        "TypeScript adiciona um sistema de tipos estático ao JavaScript, compilado antes da execução [1]. Interfaces descrevem a forma de objetos, generics permitem funções e tipos parametrizados, e o type narrowing reduz tipos amplos a tipos específicos por análise de fluxo [2].\n\n**Por que importa?** Estatisticamente, uma parcela significativa de bugs em JavaScript é capturável em compile-time: typos, null/undefined, chamadas erradas. O TypeScript elimina essa classe inteira de erros e documenta contratos de código.\n\n**O que muda na prática:** Ative strict mode, modele domínios com discriminated unions, use generics em utilitários e prefira type narrowing com type guards em vez de casts agressivos [3]."
    ),
    "W1-06-arquitetura-client-server": (
        "Arquitetura Client-Server",
        "Arquitetura Client-Server: O fluxo de requisições, respostas, APIs REST e o ciclo de vida de uma aplicação web",
        "O fluxo de requisições, respostas, APIs REST e o ciclo de vida de uma aplicação web",
        "Toda aplicação web é um diálogo entre cliente e servidor: o navegador faz uma requisição, o servidor processa e responde. Este livro mapeia esse ciclo de vida completo — do clique do usuário à resposta renderizada — e as arquiteturas (REST, camadas, monólitos, microsserviços) que o sustentam.",
        "A arquitetura client-server é o esqueleto de tudo que construímos na web. Compreender o fluxo completo de requisições e respostas — incluindo camadas, statelessness e evolução para microsserviços — é o que permite desenhar sistemas que escalam e evoluem.",
        "Na arquitetura client-server, o cliente (navegador, app mobile) inicia a comunicação e o servidor responde [1]. APIs REST organizam esse diálogo em recursos identificados por URLs, acessados por verbos HTTP e representados em JSON [2].\n\n**Por que importa?** O ciclo de vida de uma requisição atravessa camadas: roteamento, middlewares, controllers, services, repositories e o banco de dados. Cada camada adiciona responsabilidade e latência — e cada uma precisa ser compreendida para se projetar bem.\n\n**O que muda na prática:** Projete APIs REST com recursos e status codes corretos, mantenha o servidor stateless (tokens em vez de sessões em memória) e entenda onde o cache se encaixa no fluxo [3]."
    ),
    "W1-07-solid-e-clean-code": (
        "Princípios SOLID e Clean Code",
        "Princípios SOLID e Clean Code: Escrevendo código limpo, manutenível e de fácil expansão no Fullstack",
        "Escrevendo código limpo, manutenível e de fácil expansão no Fullstack",
        "Código que funciona hoje é fácil; código que continua funcionando — e sendo fácil de mudar — daqui a um ano é a verdadeira arte. SOLID e Clean Code são as ferramentas dessa arte. Este livro aplica esses princípios ao ecossistema Fullstack JavaScript/TypeScript.",
        "SOLID e Clean Code não são dogmas: são decisões que reduzem o custo de mudança. Em projetos Fullstack — onde frontend e backend evoluem juntos — a clareza e a separação de responsabilidades determinam a velocidade do time a longo prazo.",
        "SOLID é um acrônimo de cinco princípios: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation e Dependency Inversion [1]. Clean Code, popularizado por Robert Martin, complementa com práticas: nomes expressivos, funções pequenas, sem duplicação e comentários que explicam o porquê, não o quê [2].\n\n**Por que importa?** O custo real de software está na manutenção, não na construção. Cada princípio SOLID ataca uma causa específica de fragilidade — acoplamento, rigidez e quebra inesperada ao estender.\n\n**O que muda na prática:** Extraia responsabilidades em módulos pequenos, programe para interfaces, inverta dependências com injeção e escreva testes que documentam o comportamento esperado [3]."
    ),
    "W1-08-design-patterns-web": (
        "Design Patterns Comuns no Desenvolvimento Web",
        "Design Patterns Comuns no Desenvolvimento Web: Padrões de projeto aplicados ao ecossistema JavaScript/TypeScript",
        "Padrões de projeto aplicados ao ecossistema JavaScript/TypeScript",
        "Padrões de projeto são soluções reutilizáveis para problemas recorrentes — e o JavaScript/TypeScript os expressa de formas próprias. Do Module Pattern ao Observer e ao Repository, este livro mapeia os padrões mais comuns no desenvolvimento web e quando aplicá-los.",
        "Design patterns são vocabulário compartilhado: quando você diz 'esse módulo usa o padrão Observer', todo o time entende a estrutura em segundos. Aplicá-los com discernimento — no momento certo e no contexto JavaScript — reduz acoplamento e acelera o onboarding.",
        "Padrões de projeto foram catalogados no clássico Gang of Four [1], mas o JavaScript os expressa de formas idiossincráticas: Module Pattern via ES modules, Observer via eventos e Reactive programming, Factory via funções que retornam objetos [2]. Padrões arquiteturais como Repository e Service Layer estruturam o backend.\n\n**Por que importa?** Padrões resolvem problemas comuns de forma testada. No ecossistema web, eles aparecem em toda parte: React é baseado em componentes (composição), Redux em Observer/State, e Express em Middleware Chain.\n\n**O que muda na prática:** Estude os padrões que já usa implicitamente (composição, middleware, observer), aprenda a reconhecer o problema antes de aplicar o padrão e evite over-engineering com padrões desnecessários [3]."
    ),
    "W1-09-git-e-github": (
        "Gerenciamento de Versão com Git e GitHub",
        "Gerenciamento de Versão com Git e GitHub: Estratégias de branch (Git Flow), pull requests e colaboração em equipe",
        "Estratégias de branch (Git Flow), pull requests e colaboração em equipe",
        "Git é o sistema nervoso do trabalho em equipe moderno: cada commit, branch e pull request é uma decisão de colaboração. Este livro ensina Git além do 'commit-push-pull' — estratégias de branching, rebase vs merge, pull requests eficazes e fluxos de equipe.",
        "Gerenciamento de versão não é burocracia: é a memória e a cola do projeto. Dominar Git e GitHub — com estratégias claras de branch e code review via pull requests — permite times grandes trabalharem no mesmo código sem colisão e com história legível.",
        "Git é um sistema de controle de versão distribuído: cada clone contém o repositório completo, e commits são snapshots com grafo de histórico [1]. Estratégias de branching organizam esse grafo: Git Flow usa branches de feature, develop e release; trunk-based mantém a main sempre deployável [2].\n\n**Por que importa?** Pull requests no GitHub centralizam revisão, CI e discussão de cada mudança. O conflito não é um fracasso: é uma conversa que o Git ajuda a resolver com precisão.\n\n**O que muda na prática:** Escreva commits semânticos (feat, fix, chore), prefira PRs pequenos e revisáveis, e escolha a estratégia de branch adequada ao ritmo de deploy do time [3]."
    ),
    "W1-10-ambiente-de-desenvolvimento": (
        "Ambiente de Desenvolvimento Ideal",
        "Ambiente de Desenvolvimento Ideal: Configuração de terminais, editores, linters, formatadores e produtividade",
        "Configuração de terminais, editores, linters, formatadores e produtividade",
        "Seu ambiente de desenvolvimento é a sua oficina: terminais, editor, atalhos, linters e formatadores determinam sua velocidade diária. Este livro ensina a configurar o ambiente ideal — do shell ao editor, da automação à integração com IA — para trabalhar com fluidez.",
        "Um ambiente bem configurado é um multiplicador de produtividade silencioso: cada segundo economizado em atalhos, automação e feedback imediato se acumula em dias ao longo de um ano. Configurar o ambiente é um investimento com retorno garantido.",
        "O ambiente de desenvolvimento ideal combina: terminal configurado (shell, aliases, zsh/oh-my-zsh ou PowerShell), editor com atalhos e snippets (VS Code, Neovim), linters (ESLint) e formatadores (Prettier) integrados [1]. O objetivo é feedback imediato: erros aparecem antes do commit [2].\n\n**Por que importa?** A configuração padrão de qualquer ferramenta é apenas o ponto de partida. Quem investe tempo em setup — keybindings, tarefas automatizadas, templates — trabalha mais rápido e com menos fricção.\n\n**O que muda na prática:** Configure format-on-save, um ESLint rigoroso no CI, aliases para comandos frequentes e um dotfiles no GitHub para versionar sua configuração [3]."
    ),

    # ═══════════════ SÉRIE W2 — FRONTEND: INTERFACES MODERNAS E ESCALÁVEIS ═══════════════
    "W2-01-dominando-react": (
        "Dominando o React.js",
        "Dominando o React.js: Componentização, estado, hooks personalizados e fluxo de dados unidirecional",
        "Componentização, estado, hooks personalizados e fluxo de dados unidirecional",
        "React mudou a forma como construímos interfaces: componentes, estado declarativo e fluxo de dados unidirecional. Este livro vai além dos tutoriais — componentização real, hooks personalizados, performance de re-renders e arquitetura de aplicações React maduras.",
        "Dominar React é dominar um modelo mental: UI como função do estado. Componentização, hooks e fluxo unidirecional formam a base que suporta aplicações de qualquer tamanho — e entender o porquê de cada decisão evita os anti-padrões mais comuns.",
        "React é uma biblioteca para construir interfaces declarativas: o desenvolvedor descreve o que a UI deve ser dado um estado, e o React cuida de atualizar o DOM [1]. A componentização divide a interface em unidades reutilizáveis; o estado — local ou global — alimenta o fluxo de dados unidirecional (props descem, eventos sobem) [2].\n\n**Por que importa?** Hooks (useState, useEffect, useMemo) introduziram estado e efeitos em componentes de função, e hooks personalizados encapsulam lógica reutilizável. O fluxo unidirecional torna o comportamento previsível e testável.\n\n**O que muda na prática:** Modele componentes pequenos e focados, extraia hooks para lógica de domínio, memorize computações caras e entenda quando cada re-render acontece [3]."
    ),
    "W2-02-nextjs-renderizacao-hibrida": (
        "Next.js e Renderização Híbrida",
        "Next.js e Renderização Híbrida: SSR, SSG, ISR e Server Actions para aplicações de alta performance",
        "SSR, SSG, ISR e Server Actions para aplicações de alta performance",
        "Next.js consolidou-se como o framework React de produção: renderização no servidor, geração estática, revalidação incremental e ações de servidor. Este livro explica cada estratégia de renderização e quando usá-la para máxima performance e SEO.",
        "A renderização não é uma escolha binária: é um espectro. SSG, SSR, ISR e CSR atendem casos diferentes — e o Next.js permite combiná-los página a página. Dominar esse espectro é o que separa aplicações rápidas de aplicações lentas.",
        "O Next.js oferece várias estratégias de renderização: SSG (Static Site Generation) pré-renderiza no build; SSR (Server-Side Rendering) renderiza por requisição; ISR (Incremental Static Regeneration) revalida páginas estáticas em segundo plano [1]. Server Actions permitem mutações de servidor sem API dedicada [2].\n\n**Por que importa?** O HTML renderizado no servidor chega pronto ao navegador: melhor SEO, melhor primeira pintura e menos JavaScript executado no cliente. A escolha certa por página otimiza os Core Web Vitals.\n\n**O que muda na prática:** Use SSG para conteúdo, ISR para dados semi-dinâmicos, SSR para dados personalizados e Client Components apenas quando a interatividade exige [3]."
    ),
    "W2-03-gerenciamento-de-estado": (
        "Gerenciamento de Estado Global",
        "Gerenciamento de Estado Global: Quando e como usar Context API, Zustand, Redux Toolkit ou TanStack Query",
        "Quando e como usar Context API, Zustand, Redux Toolkit ou TanStack Query",
        "O estado é o coração da aplicação — e o gerenciá-lo mal é a fonte dos bugs mais caros. Context API, Zustand, Redux Toolkit e TanStack Query resolvem problemas diferentes. Este livro define quando e como usar cada ferramenta, com critérios objetivos.",
        "Gerenciamento de estado não é uma competição entre bibliotecas: é uma decisão de arquitetura. Separar estado de servidor (dados da API) de estado de cliente (UI e sessão) — e escolher a ferramenta certa para cada um — reduz drasticamente a complexidade da aplicação.",
        "O estado de servidor (dados vindos da API) merece TanStack Query: cache, revalidação, retries e sincronização automática [1]. O estado de cliente simples pode usar Context API ou estado local; o estado complexo e compartilhado beneficia-se de Zustand ou Redux Toolkit [2].\n\n**Por que importa?** A maioria dos 'problemas de estado' em React são, na verdade, problemas de dados de servidor — que o TanStack Query resolve com API declarativa. Usar a ferramenta errada adiciona complexidade sem ganho.\n\n**O que muda na prática:** Use Query para dados assíncronos, Context para temas e preferências, Zustand para estado de UI compartilhado e Redux apenas quando o domínio justifica [3]."
    ),
    "W2-04-tailwind-css": (
        "Estilização Ágil com Tailwind CSS",
        "Estilização Ágil com Tailwind CSS: Design tokens, componentes reutilizáveis e layouts responsivos avançados",
        "Design tokens, componentes reutilizáveis e layouts responsivos avançados",
        "Tailwind mudou a estilização: utility classes no HTML, tokens de design e zero CSS em cascata perdido. Este livro ensina Tailwind do básico ao avançado — configuração de tokens, responsividade, dark mode, componentes reutilizáveis e integração com frameworks.",
        "Tailwind não é 'CSS inline': é um sistema de design em forma de utilitários. Com tokens centralizados, variantes responsivas e a filosofia mobile-first, ele entrega consistência e velocidade — sem abrir mão de CSS avançado quando necessário.",
        "Tailwind CSS gera utility classes a partir de uma configuração central (tailwind.config): cores, espaçamentos, tipografia e breakpoints viram tokens reutilizáveis [1]. A responsividade é declarativa: sm:, md:, lg: aplicam estilos por breakpoint, e dark: alterna temas [2].\n\n**Por que importa?** A consistência nasce dos tokens: mudar a paleta no config atualiza o app inteiro. A purga de estilos não utilizados (tree-shaking) mantém o CSS final mínimo.\n\n**O que muda na prática:** Centralize o tema em tokens, use @apply para componentes repetidos ou prefira componentes React, e pense mobile-first com as variantes de breakpoint [3]."
    ),
    "W2-05-formularios-e-validacao": (
        "Formulários e Validação Robusta",
        "Formulários e Validação Robusta: Integrando React Hook Form com Zod para validações complexas",
        "Integrando React Hook Form com Zod para validações complexas",
        "Formulários são a interface mais crítica — e a mais negligenciada: re-renders desnecessários, validação espalhada e estados inconsistentes. React Hook Form com Zod oferece a combinação moderna: performance, tipagem e validação em um só lugar. Este livro ensina a dupla na prática.",
        "Um formulário bem construído é uma vitrine de qualidade de engenharia. Com React Hook Form controlando o estado de forma performática e Zod validando com tipos TypeScript, você elimina uma classe inteira de bugs e atrasos de UX.",
        "React Hook Form gerencia o estado de formulários minimizando re-renders, usando refs em vez de estado controlado a cada tecla [1]. Zod define schemas de validação que são também fontes de tipo TypeScript — uma única fonte de verdade para forma e regras [2].\n\n**Por que importa?** A integração resolve: o resolver do Zod valida no submit e em cada campo, com mensagens de erro tipadas e internacionalizáveis. Esquemas compartilhados entre frontend e backend evitam duplicação.\n\n**O que muda na prática:** Defina o schema Zod do domínio, conecte via resolver, use erros tipados no formulário e reutilize o schema no backend para validação dupla [3]."
    ),
    "W2-06-testes-frontend": (
        "Testes Unitários e de Integração no Frontend",
        "Testes Unitários e de Integração no Frontend: Garantindo a estabilidade da interface com Vitest e Testing Library",
        "Garantindo a estabilidade da interface com Vitest e Testing Library",
        "Testar frontend sempre foi tratado como difícil — até que Vitest e Testing Library mudaram as regras do jogo. Testar o que o usuário vê e interage, em vez de detalhes de implementação, tornou os testes de interface rápidos, estáveis e valiosos. Este livro ensina a estratégia completa.",
        "Testes de frontend não são luxo: são a rede de segurança que permite refatorar com confiança. Com Testing Library testando comportamento do usuário e Vitest executando em milissegundos, a interface ganha a mesma proteção que o backend sempre teve.",
        "Vitest é um test runner nativo do ecossistema Vite, rápido e compatível com Jest [1]. Testing Library promove testar a UI como o usuário a enxerga: queries por papel (getByRole), eventos reais e asserções de acessibilidade [2].\n\n**Por que importa?** Testar detalhes de implementação (classes, state interno) gera testes frágeis que quebram sem bug real. Testes baseados em comportamento do usuário sobrevivem a refatorações e documentam a experiência esperada.\n\n**O que muda na prática:** Teste por papel e texto visível, use fireEvent/userEvent para interações, cubra fluxos críticos (login, formulários) e integre a cobertura no CI [3]."
    ),
    "W2-07-performance-web": (
        "Performance Web e Otimização de Core Web Vitals",
        "Performance Web e Otimização de Core Web Vitals: SEO técnico, lazy loading e otimização de assets",
        "SEO técnico, lazy loading e otimização de assets",
        "Velocidade é feature: cada 100ms de atraso custa conversão, e o Google mede a experiência via Core Web Vitals. Este livro ensina a auditar e otimizar performance web — LCP, INP, CLS, lazy loading, code splitting e otimização de assets — de forma sistemática.",
        "Performance não é uma fase do projeto: é uma disciplina contínua, medida e protegida. Dominar os Core Web Vitals e as técnicas de otimização — imagens, fontes, JavaScript, cache — transforma sites lentos em experiências instantâneas.",
        "Os Core Web Vitals são métricas centradas no usuário: LCP (maior conteúdo visível), INP (capacidade de resposta) e CLS (estabilidade visual) [1]. Otimizações clássicas incluem lazy loading de imagens (loading=lazy), code splitting via dynamic import, otimização de assets (AVIF/WebP, minificação) e cache agressivo [2].\n\n**Por que importa?** O INP mede a latência real de interação; o CLS mede saltos de layout. Ambos afetam ranking de busca e, mais importante, a percepção de qualidade do usuário.\n\n**O que muda na prática:** Meça com Lighthouse e Web Vitals, priorize o LCP com pré-carregamento, evite layout shift reservando espaço de mídia e reduza o JavaScript que bloqueia a renderização [3]."
    ),
    "W2-08-pwa-offline-first": (
        "Aplicações Offline-First e PWAs",
        "Aplicações Offline-First e PWAs: Transformando sites em Progressive Web Apps com suporte a cache local",
        "Transformando sites em Progressive Web Apps com suporte a cache local",
        "Aplicações que funcionam sem internet, instaláveis na tela inicial e com performance nativa: as Progressive Web Apps são o elo entre web e mobile. Este livro ensina a estratégia offline-first com Service Workers, cache API, manifest e sincronização em segundo plano.",
        "O offline-first não é um extra: é uma mudança de mentalidade — projetar para a rede como algo que falha, em vez de algo garantido. PWAs entregam confiabilidade, velocidade e instalabilidade com a distribuição simples da web.",
        "Service Workers são scripts que interceptam requisições e implementam estratégias de cache (cache-first, network-first, stale-while-revalidate) [1]. O manifest JSON torna a aplicação instalável, e APIs como Background Sync e Push permitem atualização e notificação offline [2].\n\n**Por que importa?** Uma PWA pode reduzir drasticamente o tempo de carregamento em redes ruins, manter o app utilizável offline e alcançar usuários sem passar pela loja de aplicativos.\n\n**O que muda na prática:** Implemente um Service Worker com precaching do shell da aplicação, estratégia network-first para dados e cache-first para assets, e teste com Lighthouse PWA [3]."
    ),
    "W2-09-animacoes-micro-interacoes": (
        "Animações e Micro-interações",
        "Animações e Micro-interações: Elevando a experiência do usuário com Framer Motion e CSS animations",
        "Elevando a experiência do usuário com Framer Motion e CSS animations",
        "Micro-interações são a assinatura de interfaces memoráveis: um botão que responde ao toque, uma página que transiciona com elegância. Este livro ensina a criar animações de alta qualidade com CSS animations, transitions e Framer Motion — com performance e acessibilidade em mente.",
        "Animações não são decoração: são comunicação. Elas guiam o olhar, dão feedback e criam continuidade entre estados da interface. Feitas com moderação e técnica, transformam a percepção de qualidade do produto.",
        "CSS transitions e animations animam propriedades com custo baixo quando usam transform e opacity (aceleradas por GPU) [1]. Framer Motion, biblioteca React, oferece animações declarativas, gestos, layout animations e variantes com API ergonômica [2].\n\n**Por que importa?** Animar propriedades caras (width, height, box-shadow) causa jank. A acessibilidade exige respeitar prefers-reduced-motion — quem sofre de cinetose precisa de animações reduzidas.\n\n**O que muda na prática:** Prefira transform/opacity, use Framer Motion para entradas e saídas de componentes, defina durações curtas (150-300ms) e respeite prefers-reduced-motion [3]."
    ),
    "W2-10-micro-frontends": (
        "Micro-frontends",
        "Micro-frontends: Escalando aplicações grandes com múltiplos times independentes",
        "Escalando aplicações grandes com múltiplos times independentes",
        "Quando vários times evoluem o mesmo frontend, o monólito se torna um gargalo. Micro-frontends estendem o conceito de microsserviços à interface: times independentes, deploys isolados e integração controlada. Este livro cobre as arquiteturas, os trade-offs e as ferramentas.",
        "Micro-frontends resolvem um problema organizacional: escalar times sem atropelo. Como qualquer arquitetura distribuída, têm custo — integração, duplicação de dependências, experiência fragmentada. Dominar os trade-offs é o que permite decidir quando valem a pena.",
        "Micro-frontends dividem a interface em aplicações independentes, cada uma com seu time, repositório e deploy [1]. Padrões de integração: composição no servidor (SSI, esi), build-time (npm packages) e runtime (module federation, iframes, Web Components) [2].\n\n**Por que importa?** O module federation do Webpack permite compartilhar dependências e montar a aplicação em runtime, sem redeploy do todo. O custo: acordos de contrato, design system unificado e observabilidade distribuída.\n\n**O que muda na prática:** Comece apenas quando o monólito frontend é o gargalo, defina um shell com navegação e design system, e avalie module federation para integração em runtime [3]."
    ),

    # ═══════════════ SÉRIE W3 — BACKEND: SERVIDORES, APIS E LÓGICA DE NEGÓCIO ═══════════════
    "W3-01-nodejs-ecossistema-assincrono": (
        "Node.js e o Ecossistema Assíncrono",
        "Node.js e o Ecossistema Assíncrono: O motor V8, event loop e criação de servidores HTTP nativos",
        "O motor V8, event loop e criação de servidores HTTP nativos",
        "Node.js levou JavaScript ao servidor com uma arquitetura radicalmente diferente: event loop single-thread, I/O assíncrono e o motor V8. Este livro explica como essa máquina funciona por dentro e como construir servidores HTTP nativos e aplicações escaláveis.",
        "Entender o event loop é entender o que o Node faz de melhor — e o que ele não faz. I/O não bloqueante, single thread e o módulo http nativo formam a base de todo o ecossistema: frameworks, streams e clusters dependem desse modelo.",
        "Node.js executa JavaScript no motor V8 do Chrome fora do navegador [1]. Seu modelo de concorrência é o event loop: operações de I/O são delegadas ao sistema e o loop continua processando outras tarefas; callbacks, Promises e async/await retornam quando a operação termina [2].\n\n**Por que importa?** O módulo http nativo permite criar servidores sem framework — e entender esse nível base desmistifica Express e Fastify, que são abstrações sobre ele. O modelo não bloqueante escala bem para I/O intensivo.\n\n**O que muda na prática:** Evite operações síncronas bloqueantes em produção, use streams para arquivos grandes e entenda o papel do worker pool (libuv) para tarefas pesadas [3]."
    ),
    "W3-02-apis-restful-express-fastify": (
        "Desenvolvimento de APIs RESTful com Express.js e Fastify",
        "Desenvolvimento de APIs RESTful com Express.js e Fastify: Rotas, middlewares, tratamento de erros e boas práticas",
        "Rotas, middlewares, tratamento de erros e boas práticas",
        "Express dominou o Node por uma década; Fastify chegou com performance e schema validation. Este livro ensina a construir APIs RESTful sólidas com ambos — rotas, middlewares, tratamento de erros centralizado, validação e boas práticas de produção.",
        "Uma API RESTful é a porta de entrada do seu produto: contratos claros, erros consistentes e validação robusta definem a qualidade percebida por todos os clientes. Dominar o framework é só o começo — a arquitetura de rotas e middlewares é a parte que escala.",
        "Express e Fastify são frameworks HTTP para Node. Express é minimalista e ubíquo, com middlewares como funções no pipeline de requisição [1]. Fastify prioriza performance e validação de schema (JSON Schema) embutida [2].\n\n**Por que importa?** Middlewares permitem cross-cutting concerns (auth, logging, CORS, rate limit) em camadas reutilizáveis. O tratamento de erros centralizado garante respostas consistentes — o que os clientes precisam para reagir corretamente.\n\n**O que muda na prática:** Organize rotas por recurso, use middlewares para validação e autenticação, centralize erros em um handler único e documente com OpenAPI [3]."
    ),
    "W3-03-arquitetura-limpa-backend": (
        "Arquitetura Limpa no Backend",
        "Arquitetura Limpa no Backend: Separação de responsabilidades entre Controllers, Services, Repositories e Domínio",
        "Separação de responsabilidades entre Controllers, Services, Repositories e Domínio",
        "A arquitetura do backend determina o custo de cada nova feature. Separar Controllers, Services, Repositories e o Domínio — com dependências apontando para dentro — torna o sistema testável e evoluível. Este livro aplica arquitetura limpa em Node/TypeScript na prática.",
        "Arquitetura limpa não é uma pilha de pastas bonitas: é uma direção de dependências. Quando o domínio não conhece o framework, o banco ou o HTTP, as regras de negócio sobrevivem a qualquer mudança tecnológica — e os testes rodam sem infraestrutura.",
        "A arquitetura limpa, popularizada por Robert Martin, organiza o código em camadas concêntricas: no centro o domínio (entidades e casos de uso), depois as adapters e, na borda, os frameworks [1]. Controllers recebem requisições HTTP e delegam a Services; Repositories abstraem a persistência [2].\n\n**Por que importa?** A regra de dependência aponta sempre para dentro: o domínio não importa nada externo. Isso permite testar casos de uso com mocks, trocar de banco ou de framework sem tocar na lógica de negócio.\n\n**O que muda na prática:** Modelo entidades e casos de uso independentes de Express/Prisma, injete dependências (repositórios) nos services e mantenha controllers finos [3]."
    ),
    "W3-04-graphql-vs-rest": (
        "GraphQL vs. REST",
        "GraphQL vs. REST: Quando adotar consultas flexíveis e como estruturar schemas e resolvers",
        "Quando adotar consultas flexíveis e como estruturar schemas e resolvers",
        "REST organiza recursos; GraphQL organiza consultas. Cada abordagem tem superpoderes e custos — e a escolha errada cobra caro. Este livro compara as duas arquiteturas com critérios objetivos e ensina a estruturar schemas, resolvers e o N+1 problem.",
        "A guerra REST vs GraphQL não tem vencedor: tem contextos. REST simplifica caching e versionamento; GraphQL elimina over-fetching e under-fetching com consultas declarativas. A maturidade está em escolher a ferramenta para o problema — e saber migrar quando necessário.",
        "REST modela a API como recursos com URLs e verbos, com caching HTTP natural [1]. GraphQL expõe um único endpoint com um schema tipado; o cliente consulta exatamente os campos que precisa, e resolvers atendem cada campo [2].\n\n**Por que importa?** O N+1 problem — um resolver que dispara uma query por item — é a armadilha clássica do GraphQL; DataLoader resolve com batching. A complexidade do schema cresce com o domínio, e ferramentas de introspecção ajudam.\n\n**O que muda na prática:** Use REST para APIs públicas e caching simples; use GraphQL para clientes com necessidades de dados variadas. Modele o schema pelo domínio e implemente DataLoader para evitar N+1 [3]."
    ),
    "W3-05-websockets-tempo-real": (
        "Comunicação em Tempo Real com WebSockets",
        "Comunicação em Tempo Real com WebSockets: Construindo chats, notificações e dashboards ao vivo com Socket.io",
        "Construindo chats, notificações e dashboards ao vivo com Socket.io",
        "O HTTP é pedido-resposta; o tempo real exige uma conexão persistente bidirecional. WebSockets e Socket.io permitem chats, notificações e dashboards ao vivo. Este livro cobre o protocolo, os padrões de arquitetura e a escala de aplicações em tempo real.",
        "Tempo real não é um recurso: é uma mudança de arquitetura. Conexões persistentes, eventos bidirecionais e reconexão resiliente têm regras próprias — e o Socket.io abstrai a complexidade mantendo o controle nas mãos do desenvolvedor.",
        "WebSockets estabelecem uma conexão TCP persistente bidirecional entre cliente e servidor, após um handshake HTTP [1]. Socket.io é uma biblioteca que abstrai WebSockets com fallbacks (long-polling), salas (rooms), eventos nomeados e reconexão automática [2].\n\n**Por que importa?** Escalar tempo real exige atenção: balanceamento de carga com sticky sessions, redis adapter para múltiplas instâncias e horizontal scaling do servidor de sockets.\n\n**O que muda na prática:** Modele o domínio por eventos (message:created, user:joined), use rooms para canais, e configure o adapter Redis quando crescer para mais de uma instância [3]."
    ),
    "W3-06-processamento-assincrono-filas": (
        "Processamento Assíncrono e Filas",
        "Processamento Assíncrono e Filas: Gerenciamento de tarefas em segundo plano com Redis e BullMQ",
        "Gerenciamento de tarefas em segundo plano com Redis e BullMQ",
        "Nem todo trabalho precisa acontecer na requisição: envio de e-mails, processamento de imagens, relatórios e webhooks são tarefas de segundo plano. Filas com Redis e BullMQ dão resiliência e escala a esse trabalho. Este livro cobre o design e a operação de filas em produção.",
        "Filas são o padrão para desacoplar trabalho pesado da resposta ao usuário. Com Redis e BullMQ, você ganha retries, agendamento, prioridade e observabilidade — transformando tarefas frágeis em pipelines resilientes.",
        "Filas de mensagens seguem o padrão produtor-consumidor: um job é publicado, um worker o processa [1]. BullMQ, construído sobre Redis, oferece filas persistentes, retries com backoff, agendamento, prioridade e fluxos (flows) de dependência entre jobs [2].\n\n**Por que importa?** A idempotência é o contrato crítico: reprocessar um job não deve causar efeito duplicado. A observabilidade (filas, jobs concluídos, falhas) é essencial para operar em produção.\n\n**O que muda na prática:** Mova operações lentas para workers, torne os handlers idempotentes, configure retries com backoff exponencial e monitore o tamanho das filas [3]."
    ),
    "W3-07-seguranca-backend": (
        "Segurança no Backend",
        "Segurança no Backend: Proteção contra OWASP Top 10, sanitização de inputs, CORS e Rate Limiting",
        "Proteção contra OWASP Top 10, sanitização de inputs, CORS e Rate Limiting",
        "A segurança de uma aplicação se decide no backend: cada input, cada header e cada endpoint é uma superfície de ataque. Este livro traduz o OWASP Top 10 para o dia a dia do Node — sanitização, SQL injection, XSS, CSRF, CORS e rate limiting — com defesas práticas.",
        "Segurança não é uma feature: é uma propriedade do sistema. Conhecer o OWASP Top 10 e aplicar defesas por camadas — validação de entrada, controle de saída, política CORS e limitação de taxa — reduz drasticamente a superfície de ataque.",
        "O OWASP Top 10 lista as vulnerabilidades mais críticas: Injection (SQL/NoSQL), Broken Access Control, XSS, CSRF e Security Misconfiguration, entre outras [1]. As defesas fundamentais incluem sanitização e validação de inputs, queries parametrizadas, escaping de saída e políticas CORS restritas [2].\n\n**Por que importa?** Rate limiting protege contra brute force e abuso; headers de segurança (CSP, HSTS) endurecem o navegador; e a atualização de dependências elimina vulnerabilidades conhecidas.\n\n**O que muda na prática:** Valide tudo na entrada, parametrize queries, use helmet para headers seguros, configure CORS com lista de origens e adicione rate limit por rota sensível [3]."
    ),
    "W3-08-autenticacao-autorizacao": (
        "Autenticação e Autorização Avançada",
        "Autenticação e Autorização Avançada: JWT, Cookies HttpOnly, OAuth2 e controle de acesso baseado em roles (RBAC)",
        "JWT, Cookies HttpOnly, OAuth2 e controle de acesso baseado em roles (RBAC)",
        "Autenticação responde 'quem é você?'; autorização responde 'o que você pode fazer?'. JWT, cookies HttpOnly, OAuth2 e RBAC são as ferramentas modernas dessas respostas. Este livro cobre o desenho seguro de sessões e controle de acesso em profundidade.",
        "Autenticação e autorização são as linhas de defesa mais sensíveis do produto — e as mais fáceis de errar. Entender as diferenças entre JWT em localStorage vs cookies HttpOnly, os fluxos do OAuth2 e a modelagem de RBAC evita as falhas mais exploradas.",
        "JWT (JSON Web Token) é um token assinado que carrega claims — mas sua segurança depende do armazenamento: cookies HttpOnly com Secure e SameSite são superiores a localStorage, que é acessível a XSS [1]. OAuth2 delega autenticação a provedores (Google, GitHub) com tokens de acesso e refresh [2].\n\n**Por que importa?** RBAC (Role-Based Access Control) modela permissões por roles e capacidades, com middlewares que verificam a autorização por rota. O refresh token rotativo e a revogação completam o ciclo seguro.\n\n**O que muda na prática:** Prefira cookies HttpOnly para sessões, use access tokens de curta duração com refresh tokens, e implemente RBAC com middlewares por recurso [3]."
    ),
    "W3-09-testes-integracao-e2e-backend": (
        "Testes de Integração e E2E no Backend",
        "Testes de Integração e E2E no Backend: Validando rotas e regras de negócio com Supertest e Jest",
        "Validando rotas e regras de negócio com Supertest e Jest",
        "Um backend sem testes de integração é uma caixa preta: você só descobre que quebrou algo quando o cliente reclama. Supertest e Jest permitem validar rotas, banco e regras de negócio de ponta a ponta em segundos. Este livro ensina a estratégia completa.",
        "Testes de integração são a prova de que o sistema funciona como um todo: rotas, banco, middlewares e regras de negócio juntos. Com a pirâmide de testes equilibrada — unitários rápidos e integração focados — o backend evolui com confiança.",
        "Jest é o test runner mais difundido do ecossistema Node [1]. Supertest permite disparar requisições HTTP reais contra a aplicação Express sem subir o servidor, validando status, corpo e headers [2].\n\n**Por que importa?** Testes de integração capturam os bugs que os unitários não veem: contratos de rota, serialização, transações e interações com o banco. Um banco de testes (testcontainers ou SQLite) isola o ambiente.\n\n**O que muda na prática:** Teste cada rota com cenários felizes e de erro, isole o banco por teste, e rode a suíte no CI a cada push [3]."
    ),
    "W3-10-ecossistemas-alternativos": (
        "Ecossistemas Alternativos para o Backend",
        "Ecossistemas Alternativos para o Backend: Explorando Python (FastAPI), Go ou Bun para microsserviços de alta performance",
        "Explorando Python (FastAPI), Go ou Bun para microsserviços de alta performance",
        "Node não é a única opção: FastAPI traz tipagem e OpenAPI automático, Go entrega concorrência nativa e performance brutal, e Bun promete velocidade no ecossistema JavaScript. Este livro compara esses ecossistemas e orienta a escolha por contexto.",
        "A escolha da linguagem de backend é uma decisão estratégica: produtividade, performance, ecossistema e contratação. Comparar Node, Python/FastAPI, Go e Bun com critérios objetivos — em vez de moda — permite escolher a ferramenta certa para cada serviço.",
        "FastAPI (Python) oferece tipagem com Pydantic e documentação OpenAPI automática, com alta produtividade [1]. Go entrega concorrência com goroutines, performance de linguagem compilada e deploys binários simples [2]. Bun é um runtime JavaScript focado em velocidade e ferramentas integradas.\n\n**Por que importa?** Microsserviços podem (e devem) usar linguagens diferentes por serviço: o custo está na operação, não na língua. Critérios: latência exigida, produtividade do time, ecossistema de bibliotecas e facilidade de operação.\n\n**O que muda na prática:** Avalie a complexidade do domínio (Python é expressivo), a latência crítica (Go brilha) e a unificação da stack (Bun/Node). Prototipe cada opção com o mesmo serviço de teste [3]."
    ),

    # ═══════════════ SÉRIE W4 — BANCOS DE DADOS E PERSISTÊNCIA DE DADOS ═══════════════
    "W4-01-modelagem-relacional-sql": (
        "Modelagem Relacional (SQL)",
        "Modelagem Relacional (SQL): Normalização, chaves estrangeiras, índices e otimização de consultas em PostgreSQL ou MySQL",
        "Normalização, chaves estrangeiras, índices e otimização de consultas em PostgreSQL ou MySQL",
        "Antes do ORM, existe o modelo: entidades, relacionamentos, normalização e integridade. Este livro ensina modelagem relacional de verdade — da teoria da normalização às otimizações de consulta com EXPLAIN em PostgreSQL e MySQL.",
        "Um bom modelo relacional é a fundação silenciosa de qualquer sistema que dura. Normalização correta, chaves estrangeiras e índices bem escolhidos previnem dados inconsistentes e consultas lentas — problemas que ORMs sozinhos não resolvem.",
        "A modelagem relacional organiza dados em tabelas com chaves primárias e estrangeiras que garantem integridade [1]. A normalização elimina redundância em formas normais (1NF, 2NF, 3NF), enquanto a desnormalização controlada otimiza leituras [2].\n\n**Por que importa?** Índices aceleram consultas — mas custam escrita e espaço. O EXPLAIN revela como o planner executa a query: onde o índice falta, onde o full scan acontece.\n\n**O que muda na prática:** Modele pelo domínio, normalize até 3NF e desnormalize com consciência, crie índices para as queries reais e valide com EXPLAIN [3]."
    ),
    "W4-02-orms-e-query-builders": (
        "Dominando ORMs e Query Builders",
        "Dominando ORMs e Query Builders: Produtividade e segurança com Prisma, Drizzle ORM ou TypeORM",
        "Produtividade e segurança com Prisma, Drizzle ORM ou TypeORM",
        "ORMs prometem produtividade e segurança — e entregam ambos quando bem usados. Prisma, Drizzle e TypeORM dominam o ecossistema TypeScript. Este livro compara as ferramentas, ensina modelagem com schema, migrations e quando escapar para SQL puro.",
        "ORMs não eliminam o SQL: abstraem-no. O valor está na tipagem de ponta a ponta, nas migrations e na prevenção de SQL injection — mas o custo aparece em queries complexas mal modeladas. A maturidade está em saber quando o ORM ajuda e quando atrapalha.",
        "Prisma oferece schema declarativo, client tipado e migrations automáticas [1]. Drizzle ORM prioriza a proximidade com SQL e performance, com TypeScript-first. TypeORM, o veterano, segue o estilo decorator do TypeScript [2].\n\n**Por que importa?** Queries parametrizadas dos ORMs previnem SQL injection por padrão. Relações (includes), paginação e transações são abstrações que aceleram o desenvolvimento — mas o raw SQL continua disponível para o que precisa de precisão.\n\n**O que muda na prática:** Modele o schema no ORM, use migrations versionadas, tipifique as queries de ponta a ponta e caia para SQL raw quando a query exige (relatórios, agregações complexas) [3]."
    ),
    "W4-03-nosql-mongodb": (
        "Bancos de Dados NoSQL",
        "Bancos de Dados NoSQL: Quando e como utilizar MongoDB para dados flexíveis e não estruturados",
        "Quando e como utilizar MongoDB para dados flexíveis e não estruturados",
        "Nem todos os dados cabem em tabelas: documentos, catálogos e esquemas que evoluem rápido pedem bancos NoSQL. O MongoDB, com documentos JSON-like e escalabilidade horizontal, é o mais popular. Este livro ensina quando usá-lo e como modelar para ele.",
        "NoSQL não é 'sem SQL': é 'não apenas SQL'. O MongoDB brilha em dados flexíveis, protótipos que evoluem e escala horizontal — mas o modelamento em documentos segue regras próprias que, mal aplicadas, geram dados inconsistentes.",
        "MongoDB armazena documentos BSON com esquema flexível [1]. A modelagem é guiada pelos padrões de acesso: embedding para dados lidos juntos e referências para relacionamentos que crescem (1-N, N-N) [2].\n\n**Por que importa?** O esquema flexível acelera a evolução, mas transfere a responsabilidade de consistência para a aplicação. Índices e aggregation pipelines são as ferramentas de performance.\n\n**O que muda na prática:** Modele pelos padrões de leitura, use embedding quando faz sentido e referências quando não, e adote transações multi-documento para operações atômicas críticas [3]."
    ),
    "W4-04-caching-redis": (
        "Caching e Estruturas de Chave-Valor",
        "Caching e Estruturas de Chave-Valor: Otimizando aplicações de alto tráfego com Redis",
        "Otimizando aplicações de alto tráfego com Redis",
        "Quando o banco vira o gargalo de uma aplicação de alto tráfego, o cache entra em cena. O Redis — armazenamento em memória com estruturas de dados ricas — é a ferramenta padrão. Este livro ensina estratégias de caching, invalidação e os padrões de uso do Redis.",
        "Caching é a arte de responder rápido sem consultar a fonte a cada vez. O Redis entrega latência de microsegundos e estruturas de dados (strings, hashes, sets, sorted sets) que resolvem problemas além do cache — filas, sessões, rate limiting e leaderboards.",
        "Redis é um armazenamento em memória de chave-valor com estruturas ricas [1]. Estratégias de cache: cache-aside (a aplicação gerencia o cache), write-through, write-back e TTL para expiração [2].\n\n**Por que importa?** A invalidação é o problema clássico: cache desatualizado entrega dados errados. O cache stampede — muitas requisições simultâneas para a mesma chave expirada — exige locks ou dogpile prevention.\n\n**O que muda na prática:** Cacheie com TTL e invalidação explícita, use hashes para objetos, sorted sets para rankings e o padrão read-through com fallback para o banco [3]."
    ),
    "W4-05-migracoes-de-banco": (
        "Migrações de Banco de Dados",
        "Migrações de Banco de Dados: Versionamento de esquema e estratégias de deploy sem downtime",
        "Versionamento de esquema e estratégias de deploy sem downtime",
        "O esquema do banco evolui junto com o código — e evoluir sem quebrar produção é uma arte. Migrações versionadas e estratégias de deploy sem downtime (expand-migrate-contract) são a diferença entre mudanças suaves e incidentes. Este livro cobre o ciclo completo.",
        "Migrações são o controle de versão do banco: cada mudança de esquema é uma migração revisável, executável e reversível. Combinadas com a estratégia de deploy em fases — expandir, migrar, contrair — permitem evoluir sem downtime.",
        "Migrações versionam o esquema: cada arquivo de migração altera o banco de forma incremental e ordenada [1]. A estratégia sem downtime separa a mudança em fases: expandir o esquema para aceitar o novo estado, fazer o deploy do código, migrar os dados e contrair o esquema antigo [2].\n\n**Por que importa?** Alterações destrutivas (drop de coluna) quebram a versão antiga do código ainda em execução. A estratégia em fases mantém compatibilidade durante o rollout.\n\n**O que muda na prática:** Versione as migrações com o código, teste em staging, aplique expand-contract para mudanças destrutivas e monitore o tempo de execução das migrações [3]."
    ),
    "W4-06-busca-textual": (
        "Busca Textual e Full-Text Search",
        "Busca Textual e Full-Text Search: Implementando buscas avançadas com PostgreSQL ou Elasticsearch",
        "Implementando buscas avançadas com PostgreSQL ou Elasticsearch",
        "Campo de busca é a feature mais usada de qualquer aplicação — e a mais subestimada. Full-text search em PostgreSQL resolve a maioria dos casos; Elasticsearch escala para buscas avançadas com relevância e faceting. Este livro compara e implementa ambas.",
        "Busca boa é busca que entende o usuário: stemming, relevância, tolerância a erros e filtros. Começar com o full-text do PostgreSQL é barato e eficaz; migrar para Elasticsearch quando a relevância e a escala exigem é uma evolução natural.",
        "PostgreSQL oferece full-text search nativo com tsvector/tsquery, stemming em múltiplos idiomas e ranking por relevância [1]. Elasticsearch é um motor de busca distribuído baseado em Lucene, com análise de texto, relevância configurável (BM25) e faceting [2].\n\n**Por que importa?** A busca por LIKE '%termo%' não usa índice e não entende variações. O full-text usa índices GIN e compreende a linguagem; o Elasticsearch adiciona escala horizontal e análises avançadas.\n\n**O que muda na prática:** Comece com tsvector + índice GIN no PostgreSQL; quando a busca exigir relevância fina, faceting e escala, introduza o Elasticsearch com ingestão via fila [3]."
    ),
    "W4-07-seguranca-em-dados": (
        "Segurança e Boas Práticas em Dados",
        "Segurança e Boas Práticas em Dados: Prevenção contra SQL Injection e estratégias de mascaramento de dados sensíveis",
        "Prevenção contra SQL Injection e estratégias de mascaramento de dados sensíveis",
        "Dados são o ativo mais valioso e o alvo mais visado: SQL injection lidera a lista de ataques há décadas. Este livro ensina a defender a camada de dados — queries parametrizadas, mascaramento, criptografia em repouso e mínimo privilégio.",
        "A segurança em dados é uma disciplina de camadas: parametrização contra injeção, criptografia em repouso e em trânsito, mascaramento para ambientes não produtivos e controle de acesso mínimo. Cada camada reduz o dano potencial de qualquer falha.",
        "SQL injection ocorre quando input do usuário é concatenado em queries — a defesa padrão são queries parametrizadas (prepared statements), que separam código de dados [1]. O mascaramento de dados substitui valores sensíveis em ambientes de desenvolvimento e testes [2].\n\n**Por que importa?** A criptografia em repouso (encryption at rest) protege o banco físico; o mascaramento evita que dados reais de clientes circulem fora de produção. O princípio do mínimo privilégio limita o dano de contas comprometidas.\n\n**O que muda na prática:** Use sempre queries parametrizadas ou ORM, criptografe dados sensíveis com chaves gerenciadas, mascare ambientes de teste e revise as permissões de banco periodicamente [3]."
    ),
    "W4-08-backup-e-recuperacao": (
        "Estratégias de Backup e Recuperação",
        "Estratégias de Backup e Recuperação: Garantindo a integridade dos dados em ambientes de produção",
        "Garantindo a integridade dos dados em ambientes de produção",
        "Nenhum sistema está imune a erro humano, falha de hardware ou ransomware. Backup não é opcional: é contrato de sobrevivência. Este livro ensina as estratégias de backup (full, incremental, PITR), os testes de restauração e o desenho de RPO/RTO.",
        "Um backup que nunca foi testado é uma esperança, não uma garantia. Definir RPO (quanto dado você aceita perder) e RTO (quanto tempo para voltar) orienta a estratégia — e o teste regular de restauração valida o processo.",
        "Backups classificam-se em full (cópia completa), incremental (mudanças desde o último) e point-in-time recovery (PITR), que permite restaurar até um momento exato com WAL no PostgreSQL [1]. A regra 3-2-1 recomenda 3 cópias, 2 mídias, 1 off-site [2].\n\n**Por que importa?** O teste de restauração é a única forma de saber se o backup funciona. RPO e RTO definem a estratégia: quanto mais agressivo, maior o custo operacional.\n\n**O que muda na prática:** Automatize os backups, teste restaurações periodicamente, mantenha cópias off-site (cloud, bucket) e documente o runbook de recuperação [3]."
    ),
    "W4-09-banco-de-dados-na-nuvem": (
        "Banco de Dados na Nuvem",
        "Banco de Dados na Nuvem: Gerenciamento de instâncias gerenciadas (Supabase, Neon, AWS RDS)",
        "Gerenciamento de instâncias gerenciadas (Supabase, Neon, AWS RDS)",
        "Bancos gerenciados na nuvem removem a dor de operação: backups, alta disponibilidade e escala viram responsabilidade do provedor. Supabase, Neon e AWS RDS representam esse novo paradigma. Este livro compara as opções e orienta a migração e a operação.",
        "A nuvem transformou o banco de dados em um serviço: provisionar em minutos, escalar sob demanda e delegar backups. Entender as diferenças entre Postgres gerenciado (RDS), serverless (Neon) e a plataforma all-in-one (Supabase) permite escolher com critério.",
        "AWS RDS oferece Postgres/MySQL gerenciados com replicação, backups automatizados e failover [1]. Neon é Postgres serverless com branchs para desenvolvimento e escala automática [2]. Supabase combina Postgres com autenticação, storage e API em uma plataforma.\n\n**Por que importa?** A portabilidade do Postgres permite migrar entre provedores; a escolha depende do time (Supabase é rápido para produtos), da escala (RDS é robusto) e do custo sob demanda (Neon serverless).\n\n**O que muda na prática:** Comece com Postgres gerenciado, use branchs/banco efêmero para desenvolvimento, configure pooling de conexões e monitore custos de serverless [3]."
    ),
    "W4-10-data-pipelines-etl": (
        "Introdução a Data Pipelines e ETL",
        "Introdução a Data Pipelines e ETL: Movimentação e tratamento de dados entre sistemas",
        "Movimentação e tratamento de dados entre sistemas",
        "Dados vivem em vários sistemas — e precisam se mover: do banco transacional para o analytics, de APIs para data warehouses. Este livro introduz os data pipelines e o ETL/ELT: extração, transformação e carga, com ferramentas e boas práticas.",
        "O pipeline de dados é o sistema circulatório da informação. Compreender ETL vs ELT, orquestração e qualidade de dados permite construir fluxos confiáveis que alimentam relatórios, dashboards e modelos de IA.",
        "ETL (Extract, Transform, Load) extrai dados, transforma-os fora do destino e carrega [1]. O ELT inverte a ordem: carrega e transforma no destino (como no BigQuery ou ClickHouse), aproveitando a potência do warehouse [2].\n\n**Por que importa?** A orquestração (Airflow, Prefect) agenda e gerencia dependências; a qualidade de dados — validação, deduplicação, monitoramento — determina a confiança nos resultados.\n\n**O que muda na prática:** Desenhe pipelines idempotentes e observáveis, prefira ELT quando o destino processa bem, e monitore métricas de qualidade a cada execução [3]."
    ),

    # ═══════════════ SÉRIE W5 — DEVOPS, AUTOMAÇÃO, IA E CARREIRA FULLSTACK ═══════════════
    "W5-01-docker-e-conteineres": (
        "Docker e Contêineres do Zero",
        "Docker e Contêineres do Zero: Criando ambientes de desenvolvimento e produção isolados com Dockerfiles e Docker Compose",
        "Criando ambientes de desenvolvimento e produção isolados com Dockerfiles e Docker Compose",
        "Contêineres resolveram o problema mais antigo da engenharia: funciona na minha máquina. Docker empacota aplicação e dependências em unidades isoladas e reproduzíveis. Este livro ensina Docker do zero — Dockerfiles otimizados, Compose e boas práticas de produção.",
        "Docker não é só uma ferramenta: é um contrato de portabilidade entre desenvolvimento e produção. Dominar Dockerfiles multi-stage, imagens enxutas e o Docker Compose elimina a classe mais comum de bugs de ambiente.",
        "Contêineres isolam processos com namespaces e cgroups do Linux, empacotando aplicação e dependências em imagens imutáveis [1]. O Dockerfile define a imagem (multi-stage builds reduzem o tamanho), e o Docker Compose orquestra múltiplos serviços (app, banco, fila) em um arquivo YAML [2].\n\n**Por que importa?** Imagens reproduzíveis eliminam o 'na minha máquina funciona'. Boas práticas: imagens base oficiais, usuário não root, camadas de cache bem ordenadas e healthchecks.\n\n**O que muda na prática:** Construa Dockerfiles multi-stage, defina o compose para desenvolvimento com volumes, e use o mesmo Dockerfile otimizado em produção [3]."
    ),
    "W5-02-ci-cd": (
        "CI/CD (Integração e Entrega Contínua)",
        "CI/CD (Integração e Entrega Contínua): Automatizando testes e deploys com GitHub Actions",
        "Automatizando testes e deploys com GitHub Actions",
        "Integração contínua executa testes a cada push; entrega contínua deploys a cada merge. GitHub Actions tornou a automação nativa do fluxo Git. Este livro ensina a construir pipelines de CI/CD completos — do lint ao deploy em produção.",
        "CI/CD é o cinto de segurança do time: mudanças pequenas, validadas automaticamente e entregues com frequência. Com GitHub Actions, o pipeline vive ao lado do código — triggers, jobs paralelos, caches e secrets integrados.",
        "GitHub Actions automatiza workflows com triggers (push, pull_request, schedule) e jobs que rodam em runners [1]. O pipeline típico: lint e testes no push, build e deploy no merge para main [2].\n\n**Por que importa?** CI detecta regressões em minutos; CD reduz o risco de releases grandes e lentos. Secrets gerenciados, artifacts e environments com proteção completam o ciclo seguro.\n\n**O que muda na prática:** Comece com lint+testes no PR, adicione build e deploy por ambiente, cacheie dependências e proteja a main com status checks obrigatórios [3]."
    ),
    "W5-03-infraestrutura-vps": (
        "Infraestrutura em Servidores VPS",
        "Infraestrutura em Servidores VPS: Configuração de Linux, gerenciamento de processos com PM2 e redes básicas",
        "Configuração de Linux, gerenciamento de processos com PM2 e redes básicas",
        "Antes da nuvem gerenciada, existe a VPS: um servidor Linux seu, com poder e responsabilidade. Este livro ensina a configurar uma VPS do zero — usuários, firewall, PM2 para processos Node e noções de rede — para hospedar aplicações reais.",
        "A VPS é a escola da infraestrutura: quem domina Linux, processos e rede básica entende o que as plataformas gerenciadas automatizam. Configurar um servidor do zero dá controle total e visão completa do ambiente de produção.",
        "Uma VPS é um servidor Linux dedicado, tipicamente acessado via SSH [1]. O setup essencial: usuário não root com sudo, chave SSH, firewall (UFW) e fail2ban. Para aplicações Node, o PM2 gerencia processos: restart automático, logs e clusters [2].\n\n**Por que importa?** PM2 mantém a aplicação viva com auto-restart e clustering; o Nginx na frente faz proxy reverso e SSL. Redes básicas — portas, DNS, registros A — conectam tudo.\n\n**O que muda na prática:** Segure o SSH com chaves, configure o firewall mínimo, gerencie a app com PM2 e aponte o domínio com DNS correto [3]."
    ),
    "W5-04-proxy-reverso": (
        "Proxy Reverso e Gerenciamento de Tráfego",
        "Proxy Reverso e Gerenciamento de Tráfego: Roteamento e certificados SSL automatizados com Nginx, Traefik ou Caddy",
        "Roteamento e certificados SSL automatizados com Nginx, Traefik ou Caddy",
        "Na frente de todo servidor de aplicação existe um proxy reverso: roteia tráfego, termina SSL, equilibra carga e protege. Nginx, Traefik e Caddy representam as abordagens — do clássico ao automático. Este livro ensina o gerenciamento de tráfego na prática.",
        "O proxy reverso é a porta de entrada da aplicação. Terminar TLS, rotear por hostname, servir assets estáticos e balancear múltiplas instâncias são funções que qualquer produção real exige — e que as ferramentas modernas automatizam cada vez mais.",
        "O Nginx é o proxy reverso clássico: configuração declarativa, alta performance e SSL com certbot [1]. Caddy automatiza o TLS por padrão (ACME nativo); Traefik integra-se ao Docker com service discovery automático [2].\n\n**Por que importa?** Roteamento por hostname/path, HTTP/2, compressão, rate limit e balanceamento são camadas de arquitetura. Certificados SSL renovados automaticamente eliminam o erro mais comum de produção.\n\n**O que muda na prática:** Ponha o proxy na frente da aplicação, configure SSL automático, roteie por hostname e sirva estáticos direto do proxy para aliviar a app [3]."
    ),
    "W5-05-monitoramento-observabilidade": (
        "Monitoramento e Observabilidade",
        "Monitoramento e Observabilidade: Logs centralizados, rastreamento de erros (Sentry) e métricas de servidores",
        "Logs centralizados, rastreamento de erros (Sentry) e métricas de servidores",
        "Em produção, o que não é observável é invisível: você só descobre o problema quando o usuário reclama. Observabilidade é a disciplina de métricas, logs e traces que tornam o sistema compreensível. Este livro ensina a instrumentar e operar com visibilidade.",
        "Monitorar é saber que algo está errado; observar é entender por quê. Métricas (quantitativas), logs (eventos) e traces (caminho da requisição) formam os três pilares que permitem diagnosticar incidentes em minutos, não em dias.",
        "Observabilidade assenta em três pilares: métricas (Prometheus, Grafana), logs centralizados (Loki, ELK) e tracing distribuído (OpenTelemetry) [1]. O Sentry captura exceções com stack traces e contexto de usuário em tempo real [2].\n\n**Por que importa?** Alertas bem calibrados detectam problemas antes dos usuários; traces mostram onde a latência morre em sistemas distribuídos; logs centralizados tornam a busca por erros viável.\n\n**O que muda na prática:** Instrumente métricas-chave (latência, erros, saturação), integre o Sentry no app, centralize os logs e defina alertas com ações documentadas [3]."
    ),
    "W5-06-arquitetura-serverless": (
        "Arquitetura Serverless",
        "Arquitetura Serverless: Construindo backends escaláveis baseados em funções na nuvem (AWS Lambda, Vercel)",
        "Construindo backends escaláveis baseados em funções na nuvem (AWS Lambda, Vercel)",
        "Sem servidor para gerenciar: o serverless escala do zero ao infinito sob demanda, cobrando por execução. AWS Lambda e Vercel Functions levam funções à nuvem sem operação. Este livro ensina a arquitetura serverless — funções, cold starts, custo e limitações.",
        "Serverless não é ausência de servidor: é servidor invisível. O provedor gerencia escala, disponibilidade e capacidade — e você paga pelo que executa. A arquitetura muda: funções puras, stateless, integradas por eventos.",
        "Em arquitetura serverless, funções (AWS Lambda, Vercel Functions) rodam em resposta a eventos (HTTP, filas, timers) e escalam automaticamente [1]. O custo é por execução e duração, com free tiers generosos [2].\n\n**Por que importa?** Cold starts adicionam latência às primeiras chamadas; funções stateless exigem armazenamento externo; o vendor lock-in é real. O limite de duração e tamanho define o que pode rodar.\n\n**O que muda na prática:** Mova rotas e webhooks para funções, mantenha-as pequenas e stateless, use filas para trabalhos longos e monitore o custo por função [3]."
    ),
    "W5-07-engenharia-de-ia": (
        "Engenharia de IA no Desenvolvimento",
        "Engenharia de IA no Desenvolvimento: Integrando LLMs, APIs da OpenAI/Anthropic e bancos de dados vetoriais em aplicações Fullstack",
        "Integrando LLMs, APIs da OpenAI/Anthropic e bancos de dados vetoriais em aplicações Fullstack",
        "A IA virou uma camada do Fullstack: chamadas a LLMs, embeddings, RAG e interfaces de chat integram-se às aplicações. Este livro ensina a engenharia de IA no desenvolvimento — integração com APIs, prompt engineering, bancos vetoriais e o desenho de features com IA.",
        "Integrar IA não é chamar uma API e torcer: é projetar — contexto, custo, latência, fallbacks e segurança. Com LLMs, embeddings e RAG bem estruturados, o Fullstack entrega features que eram impossíveis há poucos anos.",
        "LLMs (OpenAI, Anthropic, modelos open source) são acessados por APIs com prompt e contexto [1]. RAG (Retrieval-Augmented Generation) combina busca em banco vetorial (Pinecone, pgvector) com geração: o modelo responde com base no conhecimento recuperado [2].\n\n**Por que importa?** O custo e a latência dos tokens exigem desenho cuidadoso; a segurança (prompt injection) e a evolução dos modelos pedem abstração (provedor plugável).\n\n**O que muda na prática:** Abstraia o provedor de LLM, use embeddings + pgvector para RAG, meça custo/latência por request e aplique guardrails de conteúdo [3]."
    ),
    "W5-08-no-code-low-code": (
        "Desenvolvimento No-Code e Low-Code Integrado",
        "Desenvolvimento No-Code e Low-Code Integrado: Conectando plataformas como N8N e Supabase para automações rápidas",
        "Conectando plataformas como N8N e Supabase para automações rápidas",
        "Nem todo software precisa ser codificado do zero: n8n automatiza fluxos visualmente, e Supabase fornece banco, auth e API prontos. O low-code/no-code, integrado ao Fullstack, acelera produtos e operações internas. Este livro ensina a combinar as duas forças.",
        "Low-code não substitui o desenvolvedor: potencializa-o. Automatizar operações com n8n e prototipar produtos com Supabase libera o time para o que exige código real — e o desenvolvedor Fullstack é quem integra essas plataformas com engenharia.",
        "n8n é uma ferramenta de automação visual com centenas de integrações (webhooks, bancos, APIs) [1]. Supabase combina Postgres, autenticação, storage e API REST/GraphQL automática — um backend completo sem escrevê-lo [2].\n\n**Por que importa?** Para operações internas (notificações, integrações, sincronizações), o n8n entrega em horas o que demandaria dias. Para produtos, o Supabase acelera o time-to-market mantendo o Postgres padrão.\n\n**O que muda na prática:** Automatize fluxos operacionais com n8n, use Supabase para auth + banco em MVPs, e escreva código apenas onde a plataforma não escala [3]."
    ),
    "W5-09-gestao-de-projetos-microsservicos": (
        "Gestão de Projetos e Arquitetura de Microsserviços",
        "Gestão de Projetos e Arquitetura de Microsserviços: Do monolito escalável à transição para microsserviços",
        "Do monolito escalável à transição para microsserviços",
        "Microsserviços são a resposta a um problema de organização — não um fim em si. O monolito modular bem arquitetado ainda é a melhor escolha na maioria dos casos. Este livro ensina gestão de projetos e a transição criteriosa para microsserviços, sem dogmatismo.",
        "A maturidade está em começar simples e evoluir com critério: monolito modular primeiro, divisão por fronteiras de domínio quando o time e a escala exigirem. Arquitetura é uma decisão de negócio, não uma medalha tecnológica.",
        "Microsserviços dividem o sistema em serviços independentes por domínio, com comunicação via APIs e dados próprios [1]. A transição começa com um monolito modular, define fronteiras (bounded contexts) e extrai serviços um a um [2].\n\n**Por que importa?** O custo distribuído é real: operação, consistência de dados e debugging entre serviços. Gestão de projetos — fluxo, priorização e autonomia de times — é o que torna a arquitetura sustentável.\n\n**O que muda na prática:** Comece monolito modular, identifique os bounded contexts, extraia um serviço por vez e estabeleça contratos de API e observabilidade antes da migração [3]."
    ),
    "W5-10-guia-carreira-fullstack": (
        "O Guia da Carreira Fullstack",
        "O Guia da Carreira Fullstack: Portfólio, entrevistas técnicas, arquitetura de sistemas e posicionamento profissional no mercado global",
        "Portfólio, entrevistas técnicas, arquitetura de sistemas e posicionamento profissional no mercado global",
        "A carreira Fullstack é mais do que saber frontend e backend: é portfólio que prova, entrevistas que desbloqueiam e posicionamento que diferencia. Este livro é o guia completo — do primeiro projeto ao emprego remoto global, com método e estratégia.",
        "Construir uma carreira Fullstack é um projeto de produto: você é o produto, seu portfólio é a vitrine e as entrevistas são o funil. Com método — projetos reais, preparação técnica e posicionamento — o caminho se torna previsível e acelerado.",
        "A carreira Fullstack combina habilidade técnica com estratégia: portfólio com projetos completos (front, back, banco, deploy), proficiência em entrevistas (algoritmos, system design, trivias) e posicionamento no mercado [1]. O mercado remoto global amplia as oportunidades, mas exige comunicação e disciplina [2].\n\n**Por que importa?** Entrevistas técnicas avaliam fundamentos (estruturas de dados, arquitetura) além da stack. O portfólio com código real e deploy publicado vale mais que certificados. O posicionamento (nicho, marca pessoal) atrai as oportunidades.\n\n**O que muda na prática:** Publique projetos completos e documentados, estude fundamentos e system design, e posicione-se com um nicho claro e presença em comunidades [3]."
    ),
}

# Auto-gerar lista completa de slugs
SLUGS_WEB = list(LIVROS_WEB.keys())
