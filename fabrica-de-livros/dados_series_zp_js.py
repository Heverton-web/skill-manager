#!/usr/bin/env python3
"""
Dados da Serie ZP1 — JavaScript: Do Zero ao Profissional (20 livros)
Jornada progressiva: Livro 1 = absoluto zero, Livro 20 = pronto para o mercado.
Cada livro tem 4 Partes e 16 Capitulos (EITA-V2).
Usado por gerar-livros-zp.py e compilar-para-pdf.py
"""

LIVROS_ZP_JS = {
    # ═══════════ NIVEL 0-1: ZERO ABSOLUTO E FUNDAMENTOS ═══════════
    "ZP1-01-logica-de-programacao-com-javascript": (
        "Lógica de Programação com JavaScript",
        "Lógica de Programação com JavaScript: Do Zero Absoluto ao Primeiro Programa",
        "Do zero absoluto: variáveis, tipos, condicionais, laços e o primeiro programa",
        "Você nunca programou? Este é o livro certo. A lógica de programação é a base de tudo: variáveis, tipos de dados, condicionais, laços e funções. Usando o JavaScript como ferramenta, este livro leva quem nunca escreveu uma linha de código até o primeiro programa funcional — sem pular nenhum degrau.",
        "A lógica de programação não é sobre uma linguagem: é sobre pensar em sequência, decisão e repetição. Quem domina esses três pilares consegue programar em qualquer linguagem. Você acabou de construir a fundação sobre a qual toda a sua carreira em JavaScript será erguida.",
        "Programar é traduzir um raciocínio em instruções que uma máquina executa. Toda a programação se apoia em três estruturas básicas: sequência (instruções em ordem), decisão (condicionais como if/else) e repetição (laços como for e while) [1]. No JavaScript, os valores ficam em variáveis (let, const) e possuem tipos: número, string, booleano, array e objeto [2].\n\n**Por que importa?** Dominar a lógica antes da sintaxe evita o erro mais comum de iniciantes: decorar comandos sem entender o raciocínio. Toda aplicação complexa é apenas uma combinação bem organizada dessas três estruturas básicas.\n\n**O que muda na prática:** Comece escrevendo algoritmos em português (pseudocódigo) antes do código. Depois, traduza cada passo para JavaScript. Esse hábito transforma o aprendizado de memorização em compreensão real [3]."
    ),
    "ZP1-02-fundamentos-da-linguagem-javascript": (
        "Fundamentos da Linguagem JavaScript",
        "Fundamentos da Linguagem JavaScript: Sintaxe, Tipos, Operadores e Conversões",
        "Sintaxe, tipos, operadores, coerção e as regras que regem a linguagem",
        "JavaScript é a linguagem da web — e a mais mal compreendida. Este livro destrincha os fundamentos: sintaxe, tipos primitivos, operadores, coerção de tipos e as regras de escopo. Sem esses alicerces, qualquer código mais complexo será um campo minado de bugs invisíveis.",
        "Os fundamentos são a diferença entre quem copia código e quem domina a linguagem. Compreender tipos, operadores e coerção — os comportamentos estranhos que o JavaScript exibe — é o que permite prever resultados em vez de se surpreender com eles.",
        "O JavaScript tem tipos primitivos (string, number, boolean, null, undefined, symbol, bigint) e tipos de referência (objetos, arrays, funções) [1]. A coerção de tipos — conversão automática entre tipos — é fonte clássica de bugs: '1' + 1 resulta em '11', enquanto '1' - 1 resulta em 0 [2]. Operadores de comparação estrita (===) evitam as armadilhas da igualdade frouxa (==).\n\n**Por que importa?** O JavaScript executa no navegador e no servidor (Node.js), mas suas regras de coerção e escopo são as mesmas em qualquer lugar. Conhecê-las evita os bugs mais comuns da linguagem.\n\n**O que muda na prática:** Use sempre comparação estrita (===), prefira const e let (nunca var), e teste conversões no console antes de confiar nelas em produção [3]."
    ),
    "ZP1-03-controle-de-fluxo-e-estruturas-de-dados": (
        "Controle de Fluxo e Estruturas de Dados em JavaScript",
        "Controle de Fluxo e Estruturas de Dados em JavaScript: Condicionais, Laços, Arrays e Objetos",
        "Condicionais, laços, arrays, objetos e como escolher a estrutura certa",
        "Código real é feito de decisões e repetições sobre dados. Este livro aprofunda o controle de fluxo (if, switch, ternário) e as estruturas de dados fundamentais do JavaScript: arrays, objetos, Map e Set. Aprender a escolher a estrutura certa para cada problema é o que separa código funcional de código elegante.",
        "A estrutura de dados certa transforma um algoritmo complexo em uma solução simples. Arrays para sequências, objetos para entidades, Map para associações com chave dinâmica e Set para unicidade — cada estrutura existe para resolver um tipo de problema. Este capítulo encerra o domínio sobre elas.",
        "Arrays armazenam sequências ordenadas e oferecem métodos poderosos: map, filter, reduce, forEach [1]. Objetos modelam entidades com chave-valor e são a base do JSON, formato universal de troca de dados. Map e Set, introduzidos no ES6, resolvem limitações dos objetos (chaves não-string) e garantem unicidade [2].\n\n**Por que importa?** A escolha da estrutura de dados define a legibilidade e a performance do código. Um Map para buscar por chave é O(1), enquanto uma busca linear em array é O(n) — a diferença é invisível em listas pequenas e brutal em escala.\n\n**O que muda na prática:** Antes de escrever o laço, pergunte: qual método de array resolve isso? filter para selecionar, map para transformar, reduce para acumular. Menos laços manuais, menos bugs [3]."
    ),
    "ZP1-04-funcoes-escopo-e-closures": (
        "Funções, Escopo e Closures em JavaScript",
        "Funções, Escopo e Closures: O Coração da Programação Funcional do JavaScript",
        "Declarações, arrow functions, escopo, hoisting e o mecanismo das closures",
        "Funções são o coração do JavaScript: são valores, podem ser passadas, retornadas e combinadas. Este livro explora funções em profundidade — declarações, arrow functions, escopo, hoisting e o mecanismo das closures — o conceito que explica os comportamentos mais surpreendentes da linguagem.",
        "Dominar funções é dominar a linguagem. Closures — funções que lembram o escopo onde nasceram — são a base de padrões como módulos, fábricas e funções de alta ordem. Quem entende closures deixa de se surpreender com o JavaScript e passa a usá-lo com intenção.",
        "Funções em JavaScript são cidadãos de primeira classe: podem ser atribuídas a variáveis, passadas como argumento e retornadas por outras funções [1]. Closures ocorrem quando uma função interna acessa variáveis do escopo externo mesmo após a função externa terminar — a função 'lembra' do ambiente onde foi criada [2]. Hoisting move declarações para o topo do escopo, explicando comportamentos aparentemente estranhos.\n\n**Por que importa?** O padrão Module (encapsulamento de estado privado) é implementado com closures. Funções de alta ordem como map/filter só existem porque funções são valores. O this dinâmico, fonte clássica de confusão, exige entender em qual contexto a função foi chamada.\n\n**O que muda na prática:** Prefira arrow functions para callbacks, mas saiba que elas não têm this próprio. Use closures para criar contadores, memoização e estado privado sem classes [3]."
    ),
    "ZP1-05-objetos-prototipos-e-classes": (
        "Objetos, Protótipos e Classes em JavaScript",
        "Objetos, Protótipos e Classes: O Modelo de Herança do JavaScript na Prática",
        "Literais, propriedades, protótipos, herança, this e classes ES6",
        "O JavaScript não tem classes tradicionais: tem protótipos. Este livro explica o modelo de objetos da linguagem — literais, propriedades, o mecanismo de protótipos, herança, o this dinâmico e as classes do ES6 — revelando como o JavaScript realmente funciona por baixo da superfície sintática.",
        "Entender protótipos é entender o JavaScript de verdade. As classes do ES6 são açúcar sintático sobre o mecanismo de protótipos — e quem compreende a base enxerga o que as classes escondem. Este conhecimento é o que permite depurar heranças complexas e projetar hierarquias que funcionam.",
        "Todo objeto JavaScript tem um prototype — outro objeto do qual herda propriedades [1]. A cadeia de protótipos define a herança: ao acessar uma propriedade inexistente no objeto, o motor busca no protótipo, e assim por diante até null. As classes ES6 (class, extends, super) oferecem sintaxe familiar para esse mecanismo [2].\n\n**Por que importa?** O this é determinado por como a função é chamada, não onde é definida — fonte clássica de bugs em callbacks. A composição de objetos (mixins, Object.assign) muitas vezes é preferível à herança profunda, evitando as armadilhas de hierarquias frágeis.\n\n**O que muda na prática:** Use classes para domínios claros, mas prefira composição para reutilização de comportamento. Sempre que um this se perder em callback, use arrow functions ou bind explícito [3]."
    ),
    "ZP1-06-es6-moderno-destructuring-e-modulos": (
        "ES6+ Moderno: Destructuring, Spread e Módulos",
        "ES6+ Moderno: Destructuring, Spread, Rest, Módulos e os Recursos que Mudaram o JavaScript",
        "Template literals, destructuring, spread/rest, módulos ES e optional chaining",
        "O JavaScript moderno (ES6 em diante) mudou a linguagem: template literals, destructuring, spread/rest, módulos ES, optional chaining e nullish coalescing. Este livro cobre cada recurso moderno com exemplos práticos, mostrando como escrever código conciso, legível e profissional no padrão atual do mercado.",
        "Código profissional moderno não se parece com o JavaScript de dez anos atrás. Dominar os recursos ES6+ não é opcional: é o padrão exigido em qualquer código-base atual — frameworks, bibliotecas e entrevistas técnicas avaliam exatamente isso. Você está pronto para o nível profissional da linguagem.",
        "Template literals (crase) interpolam variáveis com ${} e permitem strings multilinha [1]. Destructuring extrai valores de objetos e arrays em variáveis: const { nome, idade } = pessoa. Spread (...) espalha elementos de iteráveis; Rest (...) agrupa argumentos. Módulos ES (import/export) organizam o código em unidades testáveis [2]. Optional chaining (?.) e nullish coalescing (??) evitam verificações defensivas.\n\n**Por que importa?** Esses recursos reduzem verbosidade e bugs. Módulos ES são o padrão de organização em qualquer projeto moderno — frameworks como React e Node.js os usam nativamente. O spread imutável é a base da programação com estado imutável.\n\n**O que muda na prática:** Reescreva código antigo com destructuring em parâmetros de função, prefira spread para clonar objetos/arrays e organize tudo em módulos ES. Seu código ficará mais curto e mais claro [3]."
    ),
    # ═══════════ NIVEL 2: DOM E INTERATIVIDADE ═══════════
    "ZP1-07-dom-e-manipulacao-de-elementos": (
        "DOM e Manipulação de Elementos",
        "DOM e Manipulação de Elementos: Selecionando, Criando e Atualizando a Página",
        "querySelector, criação de nós, atributos, classes e o Document Object Model",
        "O DOM (Document Object Model) é a ponte entre o JavaScript e a página HTML: a representação em árvore que o navegador mantém. Este livro ensina a selecionar, criar, modificar e remover elementos, atualizar atributos e classes, e construir interfaces dinâmicas — a essência do frontend.",
        "Manipular o DOM com eficiência é o primeiro passo para se tornar desenvolvedor frontend profissional. Saber quando atualizar o DOM, como evitar reflows custosos e como estruturar a página dinamicamente são habilidades que todo código web moderno exige.",
        "O DOM é uma árvore de nós que o navegador cria a partir do HTML [1]. A API moderna de seleção usa document.querySelector e querySelectorAll (seletores CSS) — mais flexíveis que os antigos getElementById. Criar elementos usa document.createElement; texto com textContent; e inserção com appendChild, append e insertBefore [2].\n\n**Por que importa?** Cada modificação do DOM pode disparar reflow (recalculo de layout) e repaint (redesenho), caros em páginas complexas. Manipulações em lote (DocumentFragment) e atualizações mínimas preservam a performance.\n\n**O que muda na prática:** Prefira textContent a innerHTML quando não houver HTML (evita risco XSS), cache elementos selecionados e agrupe atualizações para reduzir reflows. O DOM bem manipulado é a base de todo framework que você usará depois [3]."
    ),
    "ZP1-08-eventos-e-interatividade": (
        "Eventos e Interatividade no Navegador",
        "Eventos e Interatividade: Cliques, Teclado, Formulários e o Fluxo de Propagação",
        "addEventListener, propagação, bubbling, delegação e eventos de formulário",
        "Interatividade é o que torna uma página web uma aplicação. Este livro ensina o modelo de eventos do navegador: addEventListener, tipos de evento (clique, teclado, formulário), o fluxo de propagação (captura e bubbling), delegação de eventos e como construir interfaces que respondem ao usuário de forma eficiente.",
        "O modelo de eventos é o coração de qualquer aplicação web interativa. Dominar a propagação e a delegação permite escrever código que funciona em listas dinâmicas, formulários complexos e interfaces de alta performance — as habilidades centrais do frontend profissional.",
        "Eventos são sinais que o navegador dispara quando algo acontece: clique, teclado, scroll, submissão de formulário [1]. addEventListener registra a reação. A propagação tem duas fases: captura (da janela até o alvo) e bubbling (do alvo de volta à janela) — padrão no qual os handlers são executados [2]. A delegação de eventos registra um único listener no pai e identifica o alvo com event.target.\n\n**Por que importa?** A delegação é essencial para listas dinâmicas (itens criados depois do listener). Entender bubbling evita bugs de cliques acionando handlers inesperados e permite padrões como event.preventDefault e stopPropagation com intenção.\n\n**O que muda na prática:** Use delegação para listas e tabelas dinâmicas, valide formulários com eventos de input em tempo real e sempre limpe listeners em SPA para evitar memory leaks [3]."
    ),
    "ZP1-09-assincronicidade-promises-e-async-await": (
        "Assincronicidade: Promises e Async/Await",
        "Assincronicidade: Callbacks, Promises, Async/Await e o Event Loop",
        "Event loop, call stack, Promises, async/await, Promise.all e tratamento de erros",
        "O JavaScript é single-threaded, mas não bloqueia: a assincronicidade permite executar operações longas sem travar a interface. Este livro explica o event loop, callbacks, Promises, async/await e o tratamento de erros assíncronos — o conhecimento que separa iniciantes de profissionais.",
        "A assincronicidade é o conceito mais importante do JavaScript moderno — e o mais mal compreendido. Quem entende o event loop prevê a ordem de execução; quem domina Promises e async/await escreve código assíncrono legível e à prova de erros. Este é o divisor de águas da sua formação.",
        "O JavaScript roda em um thread único com um event loop: chamadas síncronas empilham na call stack; operações assíncronas (timers, fetch, I/O) são agendadas e executadas quando a stack esvazia [1]. Promises representam valores futuros com estados pending, fulfilled e rejected. async/await é açúcar sintático que torna o código assíncrono linear [2].\n\n**Por que importa?** Erros em código assíncrono não são capturados por try/catch comum — exigem .catch ou try/catch dentro de async. Promise.all executa em paralelo; Promise.allSettled tolera falhas. Um fetch sem tratamento de erro derruba a aplicação silenciosamente.\n\n**O que muda na prática:** Use async/await para legibilidade, sempre envolva em try/catch, use Promise.all para paralelismo real e nunca confie em código assíncrono sem tratamento de erro explícito [3]."
    ),
    "ZP1-10-consumo-de-apis-com-fetch": (
        "Consumo de APIs com Fetch e REST",
        "Consumo de APIs: Fetch, REST, Autenticação e Tratamento de Respostas",
        "fetch, métodos HTTP, status codes, JSON, headers, autenticação e erros",
        "Aplicações modernas consomem APIs: o frontend busca dados, envia formulários e autentica usuários. Este livro ensina o consumo profissional de APIs REST com fetch — métodos HTTP, status codes, headers, JSON, autenticação (Bearer, cookies) e tratamento robusto de erros e timeouts.",
        "Consumir APIs corretamente é uma habilidade profissional essencial: quase todo frontend moderno é uma camada sobre uma API. Saber montar requisições, interpretar status codes, autenticar e tratar falhas com elegância é o que transforma uma página estática em uma aplicação real.",
        "REST organiza recursos identificados por URLs, acessados por métodos HTTP: GET (ler), POST (criar), PUT/PATCH (atualizar), DELETE (remover) [1]. O fetch retorna uma Promise que resolve para a Response; o corpo JSON é extraído com response.json(). Status codes 2xx indicam sucesso, 4xx erro do cliente, 5xx erro do servidor [2]. Autenticação usa headers Authorization: Bearer <token> ou cookies.\n\n**Por que importa?** Erros de rede e status 4xx/5xx precisam ser tratados explicitamente — response.ok e try/catch são obrigatórios. Timeouts evitam requisições que travam para sempre. Headers corretos (Content-Type, Accept) evitam respostas inesperadas.\n\n**O que muda na prática:** Crie uma camada de API com funções tipadas (get, post, put, del), centralize o tratamento de erros e o token de autenticação, e sempre defina timeout. Essa camada será usada por toda a aplicação [3]."
    ),
    # ═══════════ NIVEL 3: TYPESCRIPT E ALGORITMOS ═══════════
    "ZP1-11-typescript-tipagem-estatica": (
        "TypeScript: Tipagem Estática na Prática",
        "TypeScript: Tipos, Interfaces, Generics e o Código que se Documenta Sozinho",
        "Tipos, interfaces, generics, narrowing, utilitários e integração com JavaScript",
        "TypeScript é JavaScript com tipos — e tipos mudam tudo: erros migram de runtime para compile-time, o código se documenta sozinho e o editor vira um aliado. Este livro ensina a tipagem estática na prática: tipos, interfaces, generics, type narrowing e os utilitários que todo dev TS usa diariamente.",
        "TypeScript é o padrão de fato do mercado: quase todo projeto web moderno é escrito em TS. Dominar o sistema de tipos é um multiplicador de produtividade — o compilador impede bugs inteiros de classes de erros e o editor oferece autocompletar e refatorações seguras.",
        "TypeScript adiciona um sistema de tipos estático ao JavaScript, compilado antes da execução [1]. Interfaces descrevem a forma de objetos; generics permitem funções e tipos parametrizados (Array<T>, função de identidade); type narrowing reduz tipos amplos a específicos via análise de fluxo (typeof, instanceof, discriminated unions) [2].\n\n**Por que importa?** Um percentual significativo de bugs em JavaScript é capturável em compile-time: typos, null/undefined, chamadas erradas. O strict mode maximiza a proteção. Tipos documentam contratos — o novo dev entende o código sem ler a implementação.\n\n**O que muda na prática:** Ative strict mode, modele o domínio com tipos e interfaces, use discriminated unions para estados, e deixe o TypeScript inferir sempre que possível. O tsconfig.json é o contrato do projeto [3]."
    ),
    "ZP1-12-estruturas-de-dados-e-algoritmos": (
        "Estruturas de Dados e Algoritmos em JavaScript",
        "Estruturas de Dados e Algoritmos: Pilhas, Filas, Listas, Busca e Ordenação em JS",
        "Complexidade Big-O, pilhas, filas, listas, árvores, busca binária e ordenação",
        "Estruturas de dados e algoritmos são o idioma universal da computação — e o filtro das entrevistas técnicas. Este livro implementa em JavaScript as estruturas fundamentais (pilhas, filas, listas, árvores, grafos) e os algoritmos clássicos (busca, ordenação, recursão), sempre analisando a complexidade Big-O.",
        "Conhecimento de estruturas de dados e algoritmos separa quem resolve problemas de quem apenas escreve código. É também o critério mais comum em processos seletivos. Este livro transforma o conhecimento teórico em implementações JavaScript práticas que você usará na carreira.",
        "Complexidade Big-O descreve como o tempo (ou memória) cresce com a entrada: O(1) constante, O(log n) logarítmico, O(n) linear, O(n log n), O(n²) quadrático [1]. Pilhas (LIFO) e filas (FIFO) organizam processamento. Busca binária encontra em listas ordenadas em O(log n). Ordenação: insertion O(n²), merge e quick O(n log n) [2]. Recursão resolve problemas divisíveis, como árvores.\n\n**Por que importa?** A mesma tarefa pode custar O(n) ou O(n²) dependendo da estrutura escolhida — em escala, isso é a diferença entre milissegundos e minutos. Entrevistas técnicas avaliam exatamente essa análise.\n\n**O que muda na prática:** Implemente cada estrutura do zero no seu editor para internalizar, depois reutilize em projetos reais. Pratique problemas no LeetCode/HackerRank com análise de complexidade em cada solução [3]."
    ),
    "ZP1-13-programacao-funcional-e-padroes": (
        "Programação Funcional e Padrões de Projeto",
        "Programação Funcional e Padrões: Imutabilidade, Funções Puras e os Padrões do JS",
        "Imutabilidade, funções puras, composição, currying e os padrões do ecossistema",
        "O estilo funcional — imutabilidade, funções puras e composição — é o que torna o código JavaScript previsível e testável. Este livro une a programação funcional aos padrões de projeto mais usados no ecossistema: Module, Observer, Factory, Middleware e o padrão de composição de componentes.",
        "Programação funcional e padrões de projeto são o vocabulário do código profissional. O estilo funcional reduz bugs (menos estado mutável), e os padrões fornecem soluções testadas para problemas recorrentes. Juntos, eles preparam você para ler e escrever código de nível sênior.",
        "Funções puras retornam o mesmo resultado para as mesmas entradas e não causam efeitos colaterais — fáceis de testar e prever [1]. Imutabilidade (não modificar dados, criar cópias) evita bugs de estado compartilhado. Composição combina funções pequenas em fluxos maiores; currying transforma funções de vários argumentos em cadeia de funções de um [2].\n\n**Por que importa?** O padrão Module encapsula estado privado; Observer é a base de eventos e reatividade; Factory centraliza criação; Middleware Chain é o coração do Express. React, Redux e Node.js são construídos sobre esses padrões.\n\n**O que muda na prática:** Prefira map/filter/reduce a loops com mutação, extraia funções puras testáveis e reconheça os padrões que você já usa — nomeá-los acelera a comunicação no time [3]."
    ),
    "ZP1-14-testes-automatizados-vitest-jest": (
        "Testes Automatizados com Vitest e Jest",
        "Testes Automatizados: Unitários, de Integração e E2E com Vitest, Jest e Testing Library",
        "Jest, Vitest, Testing Library, mocks, cobertura e testes de integração",
        "Testes não são opcionais: são a rede de segurança que permite evoluir código com confiança. Este livro ensina a estratégia completa de testes em JavaScript/TypeScript — unitários com Vitest e Jest, testes de componentes com Testing Library, mocks, cobertura e testes de integração.",
        "Desenvolvedor profissional escreve testes — e sabe o que testar. Testes unitários verificam unidades isoladas; testes de integração verificam a colaboração; testes E2E verificam o fluxo do usuário. Quem domina os três entrega software com qualidade e velocidade sustentáveis.",
        "Vitest é um test runner rápido do ecossistema Vite; Jest é o clássico do Node/React [1]. Um teste unitário tem três fases: arrange (preparar), act (executar), assert (verificar). Mocks substituem dependências externas (APIs, bancos) para isolar a unidade. Testing Library testa componentes pela perspectiva do usuário [2].\n\n**Por que importa?** A cobertura de testes protege contra regressões — mudanças que quebram comportamento existente. Testes que verificam implementação (detalhes internos) são frágeis; testes que verificam comportamento sobrevivem a refatorações.\n\n**O que muda na prática:** Teste por comportamento, não por implementação. Priorize os fluxos críticos (auth, pagamento, cadastro). Rode os testes no CI para quebrar o build automaticamente em caso de regressão [3]."
    ),
    # ═══════════ NIVEL 4: NODE.JS E BACKEND ═══════════
    "ZP1-15-nodejs-fundamentos-e-modulos": (
        "Node.js: Fundamentos e Módulos",
        "Node.js: O JavaScript no Servidor — Event Loop, Módulos, NPM e Ferramentas",
        "Event loop no servidor, módulos CommonJS/ESM, NPM, package.json e CLI",
        "Node.js levou o JavaScript para o servidor — e para o topo do mercado. Este livro cobre os fundamentos do Node: o event loop no servidor, o sistema de módulos (CommonJS e ESM), o gerenciador de pacotes NPM, o package.json e a construção de scripts de linha de comando.",
        "Node.js é a porta de entrada para o desenvolvimento fullstack: a mesma linguagem no frontend e no backend. Dominar módulos, NPM e o event loop no servidor é o alicerce para construir APIs, ferramentas CLI e aplicações escaláveis.",
        "Node.js executa JavaScript fora do navegador com o motor V8 e um event loop não-bloqueante orientado a eventos [1]. O sistema de módulos evoluiu: CommonJS (require/module.exports) e ESM (import/export) convivem hoje. O NPM gerencia dependências via package.json — scripts, versões e semver [2]. O globals e o módulo fs, path, os, http formam o núcleo da plataforma.\n\n**Por que importa?** O event loop do Node trata I/O (arquivos, rede, banco) sem bloquear — um único processo atende milhares de requisições. Compreender o package.json e o semver evita conflitos de dependências e permite scripts de build padronizados.\n\n**O que muda na prática:** Estruture projetos com ESM, padronize scripts no package.json (dev, build, test), e use o módulo nativo fs/promises para I/O assíncrono. Esses fundamentos sustentam Express, Fastify e todo o ecossistema [3]."
    ),
    "ZP1-16-nodejs-express-apis-e-autenticacao": (
        "Node.js: Express, APIs REST e Autenticação",
        "Node.js: Express, APIs REST, Middlewares, Validação e Autenticação JWT",
        "Express, rotas, middlewares, validação, JWT, bcrypt e boas práticas de API",
        "Chegou a hora de construir APIs reais. Este livro ensina o Express na prática: rotas, middlewares, validação de entrada, autenticação com JWT, senhas com bcrypt e as boas práticas que separam uma API amadora de uma API profissional e segura.",
        "APIs REST profissionais são a espinha dorsal de aplicações modernas. Express é o framework mais usado do Node, e dominá-lo — com middlewares, validação e autenticação — é a habilidade central do backend fullstack. Ao final, você constrói uma API completa e segura.",
        "Express organiza rotas com app.get/post/put/delete e usa middlewares — funções que interceptam requisições — para logs, autenticação e erros [1]. Validação de entrada (com zod ou express-validator) impede dados inválidos no banco. Autenticação JWT: o cliente envia token em cada requisição; o servidor valida assinatura. Senhas usam bcrypt (hash + salt) [2].\n\n**Por que importa?** Segurança não é opcional: injeção SQL, XSS e dados sensíveis expostos são riscos reais. Middlewares organizam responsabilidades transversais. Erros tratados centralmente devolvem respostas consistentes.\n\n**O que muda na prática:** Separe rotas, controllers e serviços; valide toda entrada; nunca armazene senha em texto puro; proteja rotas com middleware de autenticação. Uma API bem estruturada escala e evolui [3]."
    ),
    "ZP1-17-bancos-de-dados-com-javascript": (
        "Bancos de Dados com JavaScript",
        "Bancos de Dados: SQL com PostgreSQL e NoSQL com MongoDB no Ecossistema JavaScript",
        "SQL, PostgreSQL, Prisma, MongoDB, Mongoose, queries e integração no Node",
        "Nenhum sistema real vive sem dados. Este livro ensina a integrar bancos de dados ao ecossistema JavaScript: SQL com PostgreSQL, ORMs (Prisma), NoSQL com MongoDB, modelagem de dados e as queries que você usará todos os dias no trabalho.",
        "Dados são o ativo mais valioso de qualquer sistema — e o dev fullstack precisa dominar a persistência. Saber modelar, consultar e otimizar dados em SQL e NoSQL, com as ferramentas modernas (Prisma, Mongoose), é uma habilidade profissional obrigatória.",
        "SQL organiza dados em tabelas relacionais: CREATE/INSERT/SELECT/JOIN compõem a linguagem [1]. PostgreSQL é o banco relacional de código aberto mais avançado. Prisma é um ORM TypeScript que gera tipos das tabelas automaticamente — erro de schema vira erro de compilação. MongoDB, NoSQL, armazena documentos JSON com esquema flexível; Mongoose é seu ODM [2].\n\n**Por que importa?** Relacional é ideal para dados estruturados com relações (pedidos, clientes); NoSQL para escalabilidade horizontal e esquemas dinâmicos. A modelagem correta evita queries lentas e dados inconsistentes. Índices aceleram buscas em grandes volumes.\n\n**O que muda na prática:** Modele o schema antes do código, use Prisma para segurança de tipos, e sempre indexe as colunas de busca. Entenda as queries que o ORM gera — performance de banco é responsabilidade do dev [3]."
    ),
    "ZP1-18-react-componentes-estado-e-hooks": (
        "React: Componentes, Estado e Hooks",
        "React: Componentização, Estado, Hooks, Formulários e o Fluxo de Dados",
        "Componentes, JSX, props, estado, hooks, formulários e boas práticas",
        "React é a biblioteca frontend mais usada do mercado. Este livro leva você do primeiro componente à construção de interfaces completas: JSX, props, estado, hooks (useState, useEffect, useMemo), formulários, listas e o fluxo de dados unidirecional.",
        "Dominar React é dominar um modelo mental: UI como função do estado. Componentização, hooks e fluxo unidirecional formam a base de qualquer aplicação React — e entendê-los profundamente é o que separa quem copia exemplos de quem projeta interfaces.",
        "React constrói interfaces declarativas: o componente descreve a UI para um estado e o React atualiza o DOM [1]. JSX mistura HTML e JavaScript. Props fluem de pai para filho (fluxo unidirecional); eventos sobem via callbacks. Hooks: useState cria estado, useEffect executa efeitos (fetch, timers), useMemo memoriza cálculos caros [2].\n\n**Por que importa?** O fluxo unidirecional torna o comportamento previsível e testável. Hooks personalizados encapsulam lógica reutilizável. Formulários controlados (estado em cada input) são o padrão profissional. Entender re-renders evita problemas de performance.\n\n**O que muda na prática:** Componentes pequenos e focados, hooks personalizados para lógica de domínio, e estado mínimo — o que pode ser derivado não vira estado. Esse é o padrão exigido em qualquer vaga de frontend [3]."
    ),
    # ═══════════ NIVEL 5: PROJETO PROFISSIONAL E CARREIRA ═══════════
    "ZP1-19-projeto-profissional-fullstack": (
        "Projeto Profissional Fullstack Completo",
        "Projeto Profissional: Do Banco de Dados ao Deploy — Uma Aplicação Fullstack Real",
        "Arquitetura, CRUD completo, autenticação, testes, CI/CD e deploy de ponta a ponta",
        "Tudo que você aprendeu converge agora: este livro guia a construção completa de uma aplicação fullstack profissional — modelagem de banco, API com autenticação, frontend React, testes, CI/CD e deploy. Cada decisão é explicada com o raciocínio profissional por trás.",
        "Um projeto completo é o portfólio que abre portas — e a prova de que você domina o ciclo inteiro: dados, backend, frontend, testes e deploy. Este livro não é um tutorial: é uma mentoria de arquitetura aplicada, com as decisões e os trade-offs que profissionais fazem todos os dias.",
        "Uma aplicação fullstack profissional combina: banco relacional modelado com relações claras [1]; API REST com validação, autenticação e tratamento de erros centralizado; frontend React com componentes reutilizáveis e estado bem gerenciado; testes unitários e de integração no backend e frontend [2]. CI/CD automatiza lint, testes e deploy. Variáveis de ambiente isolam configurações por ambiente.\n\n**Por que importa?** A arquitetura em camadas (controller → service → repository) separa responsabilidades e facilita testes. O deploy automatizado reduz erros manuais. Segurança (validação, hash, tokens) protege dados reais de usuários.\n\n**O que muda na prática:** Divida o projeto em etapas verificáveis: schema → API → frontend → testes → deploy. Cada etapa com critérios de aceite. Esse projeto vira seu portfólio profissional [3]."
    ),
    "ZP1-20-carreira-entrevistas-e-portfolio": (
        "Carreira, Entrevistas Técnicas e Portfólio",
        "Carreira em JavaScript: Entrevistas Técnicas, Portfólio, CV e Primeiro Emprego",
        "Preparação para entrevistas, questões clássicas, portfólio, CV e mercado",
        "Você domina a tecnologia — agora domine a carreira. Este livro prepara você para o mercado de trabalho em JavaScript: como se preparar para entrevistas técnicas, as questões clássicas (closures, event loop, this, async), como montar um portfólio e currículo que chamam atenção e como conquistar o primeiro emprego.",
        "A jornada termina onde a carreira começa: no mercado de trabalho. Entrevistas técnicas avaliam exatamente o que você aprendeu — fundamentos, algoritmos, React, TypeScript. Um portfólio forte e um CV claro transformam conhecimento em oportunidade. Você está pronto para o próximo passo profissional.",
        "Entrevistas técnicas em JavaScript avaliam: fundamentos (closures, event loop, this, coerção), estruturas de dados e algoritmos (Big-O, arrays, strings), e stack prática (React, TypeScript, Node) [1]. Prepare-se resolvendo problemas em plataformas como LeetCode e simulando entrevistas. O portfólio deve mostrar projetos completos com código legível no GitHub, testes e deploy — não apenas tutoriais copiados [2].\n\n**Por que importa?** O processo seletivo tem etapas previsíveis: triagem de CV, entrevista comportamental, teste técnico (ao vivo ou assíncrono) e entrevista com o time. Conhecer o processo reduz a ansiedade e aumenta a performance. Um GitHub ativo é o CV que os recrutadores realmente olham.\n\n**O que muda na prática:** Monte um portfólio com 2-3 projetos completos, pratique questões clássicas em voz alta e prepare o pitch da sua trajetória. A carreira em JavaScript é uma das mais abertas do mercado — e você está pronto [3]."
    ),
}
