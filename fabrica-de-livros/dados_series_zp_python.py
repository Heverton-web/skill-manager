#!/usr/bin/env python3
"""
Dados da Serie ZP2 — Python: Do Zero ao Profissional (20 livros)
Jornada progressiva: Livro 1 = absoluto zero, Livro 20 = pronto para o mercado.
Cada livro tem 4 Partes e 16 Capitulos (EITA-V2).
Usado por gerar-livros-zp.py e compilar-para-pdf.py
"""

LIVROS_ZP_PYTHON = {
    # ═══════════ NIVEL 0-1: ZERO ABSOLUTO E FUNDAMENTOS ═══════════
    "ZP2-01-logica-de-programacao-com-python": (
        "Lógica de Programação com Python",
        "Lógica de Programação com Python: Do Zero Absoluto ao Primeiro Programa",
        "Do zero absoluto: variáveis, tipos, condicionais, laços e o primeiro programa",
        "Python é a linguagem mais recomendada para quem começa — e a mais versátil do mercado. Este livro leva quem nunca programou do zero absoluto ao primeiro programa funcional: variáveis, tipos, condicionais, laços e funções, com a sintaxe limpa que tornou Python famosa.",
        "A lógica de programação é a mesma em qualquer linguagem: sequência, decisão e repetição. Python apenas a torna mais fácil de aprender. Você acabou de construir a fundação de uma carreira que abre portas em web, dados, automação e inteligência artificial.",
        "Programar é traduzir um raciocínio em instruções que a máquina executa. Três estruturas básicas sustentam tudo: sequência, decisão (if/elif/else) e repetição (for/while) [1]. No Python, variáveis não declaram tipo — o interpretador infere: x = 10 (int), nome = 'Ana' (str), ativo = True (bool) [2].\n\n**Por que importa?** A sintaxe do Python usa indentação para definir blocos — código bem indentado é obrigatório, o que treina a organização desde o primeiro dia. A legibilidade natural do Python reduz a curva de aprendizado e acelera a produtividade.\n\n**O que muda na prática:** Escreva algoritmos em pseudocódigo primeiro, depois traduza para Python. Use o REPL (interpretador interativo) para testar cada conceito imediatamente [3]."
    ),
    "ZP2-02-fundamentos-da-linguagem-python": (
        "Fundamentos da Linguagem Python",
        "Fundamentos da Linguagem Python: Sintaxe, Tipos, Operadores e Estruturas de Controle",
        "Sintaxe, tipos nativos, operadores, strings, listas e estruturação de código",
        "Python é uma linguagem pequena na sintaxe e imensa no poder. Este livro domina os fundamentos: sintaxe e indentação, tipos nativos (int, float, str, bool), operadores, strings, formatação e as estruturas de controle que estruturam qualquer programa.",
        "Os fundamentos do Python são elegantes e consistentes — e dominá-los é rápido. Quem entende tipos, operadores e controle de fluxo escreve código correto desde o início e está pronto para avançar para funções, estruturas de dados e os frameworks que movem o mercado.",
        "Python tem tipagem dinâmica e forte: os tipos são inferidos (x = 10), e operações inválidas geram erro em vez de conversão silenciosa (1 + 'a' lança TypeError) [1]. Strings são imutáveis e ricas em métodos (upper, split, join, replace). F-strings (f'Olá, {nome}') são o padrão moderno de formatação [2].\n\n**Por que importa?** A consistência da linguagem reduz surpresas: o mesmo padrão funciona em script pequeno e em aplicação grande. A tipagem dinâmica acelera a escrita; a tipagem forte evita bugs silenciosos de coerção.\n\n**O que muda na prática:** Explore cada tipo no REPL, use f-strings sempre, e leia os erros do interpretador com atenção — Python descreve o problema com precisão, e a mensagem é sua melhor documentação [3]."
    ),
    "ZP2-03-estruturas-de-controle-e-dados": (
        "Estruturas de Controle e Dados em Python",
        "Estruturas de Controle e Dados: Listas, Tuplas, Dicionários e Conjuntos",
        "Listas, tuplas, dicionários, conjuntos, compreensões e escolha da estrutura certa",
        "Código real é feito de decisões, repetições e dados. Este livro aprofunda o controle de fluxo e as estruturas de dados nativas do Python — listas, tuplas, dicionários e conjuntos — incluindo as compreensões (list/dict comprehension) que tornam o código Python idiomático e elegante.",
        "As estruturas de dados nativas do Python são excepcionalmente bem projetadas. Dicionários para mapeamentos, listas para sequências, conjuntos para unicidade — escolher a estrutura certa transforma algoritmos complexos em soluções simples e legíveis. Este é o coração do Python idiomático.",
        "Listas são sequências mutáveis com métodos ricos (append, extend, sort) [1]. Tuplas são imutáveis e usadas como registros. Dicionários mapeiam chaves a valores com busca O(1). Conjuntos (set) garantem unicidade e operações de teoria de conjuntos. Compreensões constroem estruturas em uma linha: [x*2 for x in range(10)] [2].\n\n**Por que importa?** O Python idiomático usa compreensões no lugar de laços manuais — mais curto, mais legível e mais rápido. A imutabilidade de tuplas e a unicidade de conjuntos resolvem classes inteiras de bugs.\n\n**O que muda na prática:** Prefira compreensões a loops de construção, use dicionários para mapeamentos (nunca listas paralelas) e escolha a estrutura pelo problema, não pelo hábito [3]."
    ),
    "ZP2-04-funcoes-modulos-e-pacotes": (
        "Funções, Módulos e Pacotes em Python",
        "Funções, Módulos e Pacotes: Reutilização, Escopo e Organização do Código",
        "Definição, argumentos, escopo, docstrings, módulos, pacotes e imports",
        "Funções são as unidades de reutilização do Python — e módulos e pacotes, a forma de organizar projetos. Este livro ensina a definir funções corretas (argumentos, retorno, escopo, docstrings), importar módulos e estruturar projetos em pacotes, seguindo as convenções da comunidade.",
        "Código profissional é código organizado. Funções bem definidas com docstrings são a base da legibilidade; módulos e pacotes permitem projetos grandes sem caos. As convenções do Python (PEP 8) e a filosofia 'explicit is better than implicit' guiam cada decisão.",
        "Funções são definidas com def e têm argumentos posicionais, nomeados, padrão e *args/**kwargs [1]. O escopo segue a regra LEGB (Local, Enclosing, Global, Built-in). Docstrings ('''...''') documentam a função e geram help automático. Módulos são arquivos .py; pacotes são diretórios com __init__.py, importados com import, from e aliases (import numpy as np) [2].\n\n**Por que importa?** Módulos organizam o código em unidades testáveis e reutilizáveis. O ecossistema inteiro do Python — pandas, flask, django — é consumido via import. Conhecer as convenções (PEP 8, nomes snake_case) alinha seu código ao padrão do mercado.\n\n**O que muda na prática:** Dê nomes verbosos e claros (snake_case), escreva docstrings em toda função pública e organize projetos em pacotes por domínio. Código idiomático é o padrão de qualquer code review profissional [3]."
    ),
    "ZP2-05-programacao-orientada-a-objetos": (
        "Programação Orientada a Objetos em Python",
        "POO em Python: Classes, Herança, Encapsulamento e os Padrões de Projeto",
        "Classes, objetos, herança, polimorfismo, encapsulamento, dunder methods e dataclasses",
        "A orientação a objetos organiza o código em torno de entidades do domínio — e Python a implementa de forma pragmática. Este livro ensina classes, objetos, herança, polimorfismo, encapsulamento, os métodos dunder (__init__, __str__) e as dataclasses modernas.",
        "POO é o paradigma dominante no Python profissional — de frameworks web a bibliotecas de dados. Dominar classes, herança e encapsulamento permite modelar domínios complexos e ler qualquer framework com fluência. As dataclasses modernas reduzem a cerimônia e aumentam a clareza.",
        "Classes definem moldes: atributos (estado) e métodos (comportamento) [1]. A herança permite reutilização (class Aluno(Pessoa)); o polimorfismo permite tratar objetos diferentes pela interface comum. Encapsulamento usa convenções: _protegido e __privado. Métodos dunder (__init__, __str__, __eq__) integram classes à sintaxe da linguagem. Dataclasses (from dataclasses import dataclass) geram __init__ e __repr__ automaticamente [2].\n\n**Por que importa?** Frameworks como Django e SQLAlchemy são construídos sobre POO — modelos, views e serviços são classes. Compor objetos (has-a) é frequentemente melhor que herança profunda (is-a), evitando hierarquias frágeis.\n\n**O que muda na prática:** Modele o domínio com classes simples e dataclasses, prefira composição a herança e implemente dunder methods para que suas classes se comportem como nativas [3]."
    ),
    "ZP2-06-arquivos-excecoes-e-contextos": (
        "Arquivos, Exceções e Context Managers",
        "Arquivos, Exceções e Context Managers: I/O, Tratamento de Erros e Recursos",
        "Leitura/escrita de arquivos, with, exceções, logging e tratamento robusto",
        "Programas reais leem arquivos, falham e precisam se recuperar. Este livro ensina o tratamento de erros com exceções (try/except), a leitura e escrita de arquivos, o gerenciamento de contexto com with e o logging profissional — as habilidades de robustez que todo código de produção exige.",
        "Código robusto antecipa falhas. Exceções estruturadas, context managers que liberam recursos automaticamente e logs profissionais são o que diferencia software de demos. Este é o nível em que o código começa a ser 'de produção'.",
        "Exceções interrompem o fluxo e são tratadas com try/except/else/finally [1]. O padrão with garante que recursos (arquivos, conexões) sejam liberados mesmo em erro: with open('dados.txt') as f: f.read(). O logging (logging module) substitui print em produção — com níveis debug/info/warning/error e destinos configuráveis [2].\n\n**Por que importa?** Erros não tratados derrubam aplicações. O with é a forma idiomática e segura de gerenciar recursos — usado por arquivos, conexões de banco e sessões HTTP. Logs bem configurados são a base da observabilidade e do diagnóstico.\n\n**O que muda na prática:** Trate exceções específicas (não bare except), use with para todo recurso e configure logging no lugar de print. Um sistema que falha com elegância é um sistema profissional [3]."
    ),
    "ZP2-07-colecoes-avancadas-e-compreensoes": (
        "Coleções Avançadas e Compreensões Idiomáticas",
        "Coleções Avançadas: Compreensões, Generators, itertools e Estruturas Aninhadas",
        "Compreensões, generators, yield, itertools, defaultdict e estruturas aninhadas",
        "O Python idiomático é conciso e expressivo — e isso vem das compreensões e dos generators. Este livro domina as coleções avançadas: compreensões de lista/dict/set, generators e yield, o módulo itertools e as estruturas do collections (defaultdict, Counter, namedtuple).",
        "Compreensões e generators são a assinatura do código Python profissional. Eles tornam o código mais curto, mais rápido e mais legível — e são usados em toda biblioteca que você usará. Dominá-los é o que separa quem escreve Python de quem escreve Python idiomático.",
        "Compreensões constroem coleções em uma linha: [x*x for x in range(10) if x % 2 == 0] [1]. Generators (yield) produzem valores sob demanda, sem carregar tudo em memória — ideais para fluxos grandes. itertools oferece combinatória e iteração infinita (chain, groupby, product). collections: defaultdict (chaves com padrão), Counter (contagem), namedtuple (tuplas nomeadas) [2].\n\n**Por que importa?** Um generator processa milhões de registros sem estourar a memória; uma compreensão substitui um loop inteiro. Essas ferramentas aparecem em código de dados, web e automação — e em entrevistas técnicas.\n\n**O que muda na prática:** Reescreva loops de construção como compreensões, use generators para fluxos grandes e explore itertools para lógica combinatória. Código idiomático é mais fácil de revisar e manter [3]."
    ),
    "ZP2-08-automacao-de-tarefas-com-python": (
        "Automação de Tarefas com Python",
        "Automação de Tarefas: Scripts, Arquivos, Planilhas, E-mails e Agendamento",
        "Scripts CLI, manipulação de arquivos, CSV/Excel, e-mail, agendamento e ferramentas",
        "Python brilha na automação: tarefas repetitivas que consomem horas viram scripts de segundos. Este livro ensina a automatizar o dia a dia — scripts de linha de comando, manipulação de arquivos, planilhas (CSV, openpyxl), e-mails e agendamento (cron/task scheduler).",
        "Automação é a habilidade mais rapidamente valorizada do Python: o profissional que automatiza processos economiza horas toda semana e se torna indispensável. De scripts simples a pipelines de dados, este livro entrega as ferramentas do dia a dia.",
        "Scripts Python usam os módulos padrão: pathlib para caminhos, shutil para copiar/mover, csv para planilhas [1]. openpyxl manipula Excel nativamente. smtplib e email enviam mensagens. O agendamento roda scripts em horários definidos (cron no Linux, Task Scheduler no Windows). Argumentos de linha de comando usam argparse [2].\n\n**Por que importa?** Tarefas manuais são caras, lentas e propensas a erro. Um script que processa 1.000 arquivos em segundos paga seu custo no primeiro uso. A automação de relatórios, backups e ingestão de dados é demanda constante no mercado.\n\n**O que muda na prática:** Identifique a tarefa repetitiva mais comum da sua rotina, escreva um script que a resolva e agende a execução. Cada script automatizado é uma vitória profissional [3]."
    ),
    "ZP2-09-analise-de-dados-com-pandas-e-numpy": (
        "Análise de Dados com Pandas e NumPy",
        "Análise de Dados: NumPy para Cálculo e Pandas para Manipulação de Dados",
        "NumPy, arrays, Pandas, DataFrame, filtragem, agregação e limpeza de dados",
        "Pandas é a ferramenta nº 1 de análise de dados em Python — e NumPy, o motor numérico por trás dela. Este livro ensina a carregar, limpar, filtrar, agrupar e visualizar dados com DataFrames, as operações que todo analista e cientista de dados executa diariamente.",
        "Dominar Pandas é a porta de entrada para análise de dados, ciência de dados e IA. O DataFrame — a tabela bidimensional — é o formato universal de trabalho com dados. Quem domina Pandas transforma dados brutos em insights acionáveis com poucas linhas de código.",
        "NumPy oferece arrays multidimensionais e operações vetorizadas — cálculos em array inteiro sem loops Python [1]. Pandas constrói sobre NumPy com o DataFrame: carregar dados (read_csv, read_excel), inspecionar (head, info, describe), filtrar (df[df['idade'] > 30]), agrupar (groupby), e limpar dados (dropna, fillna, renomear colunas) [2].\n\n**Por que importa?** A limpeza de dados consome a maior parte do tempo real de análise. Operações vetorizadas são ordens de magnitude mais rápidas que loops. O groupby com agregações responde às perguntas de negócio: por região, por mês, por categoria.\n\n**O que muda na prática:** Carregue um dataset real, explore com info/describe, limpe valores ausentes e responda 3 perguntas de negócio com groupby. Esse é o fluxo profissional diário [3]."
    ),
    "ZP2-10-visualizacao-de-dados-com-matplotlib": (
        "Visualização de Dados com Matplotlib e Seaborn",
        "Visualização de Dados: Matplotlib e Seaborn para Gráficos Profissionais",
        "Matplotlib, pyplot, Seaborn, estilos, subplots e visualizações para relatórios",
        "Dados contam histórias — e gráficos as contam melhor. Este livro ensina a visualização de dados com Matplotlib e Seaborn: gráficos de linha, barras, dispersão, histogramas, heatmaps e a composição de figuras profissionais para relatórios e apresentações.",
        "Visualização é a habilidade de comunicação do analista: o mesmo dado que ninguém entende em uma planilha vira insight claro em um gráfico. Matplotlib e Seaborn são as ferramentas padrão — e dominá-las eleva qualquer análise ao nível profissional.",
        "Matplotlib (pyplot) oferece controle total sobre a figura: plt.plot, plt.bar, plt.scatter, plt.hist, com rótulos, títulos e legendas [1]. Seaborn constrói sobre Matplotlib com estatísticas embutidas: sns.barplot, sns.heatmap, sns.pairplot, estilos profissionais prontos [2]. Subplots (plt.subplots) compõem múltiplos gráficos em uma figura.\n\n**Por que importa?** Um gráfico mal feito engana; um gráfico claro decide. Escolher o tipo certo (linha para tendência, barra para comparação, dispersão para correlação) é uma habilidade de julgamento, não só de código. Estilo consistente comunica profissionalismo.\n\n**O que muda na prática:** Ao analisar qualquer dataset, gere 3-5 visualizações respondendo perguntas específicas. Salve em formato de alta qualidade para relatórios e documente a leitura de cada gráfico [3]."
    ),
    # ═══════════ NIVEL 3: BANCO DE DADOS E WEB ═══════════
    "ZP2-11-sql-e-bancos-de-dados-com-python": (
        "SQL e Bancos de Dados com Python",
        "SQL e Bancos de Dados: PostgreSQL, SQLite e Consultas Profissionais em Python",
        "SQL, PostgreSQL, SQLite, sqlite3, SQLAlchemy, transações e modelagem",
        "Dados vivem em bancos — e o profissional de Python precisa conversar com eles. Este livro ensina SQL na prática (SELECT, INSERT, JOIN, GROUP BY), a integração com Python (sqlite3, psycopg, SQLAlchemy) e a modelagem de dados que sustenta aplicações e análises.",
        "SQL é a linguagem universal dos dados — e a mais requisitada em qualquer cargo técnico. Combinar SQL com Python permite consultar, transformar e analisar dados de qualquer fonte. Este é o alicerce de dados de toda a carreira Python.",
        "SQL organiza dados em tabelas relacionais; a consulta fundamental é SELECT ... FROM ... WHERE [1]. JOIN relaciona tabelas; GROUP BY agrega. Em Python: sqlite3 para bancos locais, psycopg2 para PostgreSQL. SQLAlchemy é o ORM moderno que mapeia tabelas para objetos Python e gera SQL seguro (evita injeção) [2]. Transações garantem atomicidade.\n\n**Por que importa?** Quase todo sistema Python — web, análise, automação — persiste dados em banco relacional. Consultas bem escritas e indexadas respondem em milissegundos; ORMs evitam erros de SQL manual e mudanças de schema geram tipos.\n\n**O que muda na prática:** Modele o schema antes do código, use SQLAlchemy para aplicações e SQL puro para análises. Sempre parametrize queries — injeção SQL é o risco nº 1 [3]."
    ),
    "ZP2-12-apis-e-consumo-de-servicos": (
        "Consumo de APIs e Serviços Web com Python",
        "APIs e Serviços Web: requests, REST, JSON, Autenticação e Integrações",
        "requests, HTTP, REST, JSON, headers, autenticação e integrações externas",
        "Python conversa com o mundo via APIs: este livro ensina o consumo profissional de serviços web com a biblioteca requests — métodos HTTP, JSON, headers, autenticação, tratamento de erros e integrações com serviços externos.",
        "Integrações são o dia a dia do desenvolvedor moderno: pagamentos, mensageria, dados de terceiros, IA. Dominar o consumo de APIs com requests — e o tratamento robusto de respostas — habilita qualquer integração que o mercado pede.",
        "A biblioteca requests simplifica o HTTP: requests.get(url, params=...), requests.post(url, json=...), com a resposta em response.json() [1]. Métodos mapeiam ações (GET ler, POST criar, PUT atualizar, DELETE remover). Autenticação varia: Bearer tokens, API keys, OAuth2. Erros: response.raise_for_status() lança exceção em status 4xx/5xx [2].\n\n**Por que importa?** APIs têm contratos: status codes, formatos de erro e limites de rate. Consumir corretamente exige tratar timeouts, retries e respostas parciais. Integrações bem feitas são robustas a falhas externas.\n\n**O que muda na prática:** Crie funções de acesso tipadas por serviço, centralize autenticação e tratamento de erros, e use timeouts com retries exponenciais para resiliência [3]."
    ),
    "ZP2-13-flask-fundamentos-de-desenvolvimento-web": (
        "Flask: Fundamentos de Desenvolvimento Web",
        "Flask: Rotas, Templates, Formulários e APIs com o Microframework Python",
        "Rotas, Jinja2, formulários, blueprints, sessões e APIs com Flask",
        "Flask é o microframework que ensina web do jeito certo: simples, explícito e poderoso. Este livro cobre rotas, templates (Jinja2), formulários, sessões, blueprints e construção de APIs REST — a base completa de desenvolvimento web em Python.",
        "Flask é a porta de entrada profissional para web em Python — usado por startups e empresas. Sua simplicidade permite entender cada peça: rota, template, formulário, sessão. Com blueprints, o projeto cresce organizado. Este livro entrega a fundação completa.",
        "Flask define rotas com decorators: @app.route('/') [1]. Jinja2 renderiza templates com herança (base.html) e variáveis. Formulários (WTF) validam entrada. Sessões mantêm estado do usuário com cookies assinados. Blueprints organizam módulos da aplicação. Para APIs, retornar dict/JSON com @app.get('/api') [2].\n\n**Por que importa?** Flask é ensinado primeiro porque expõe o que frameworks maiores escondem — você entende HTTP, rotas e sessões de verdade. O conhecimento transfere para Django, FastAPI e qualquer framework. Blueprints mantêm projetos grandes organizados.\n\n**O que muda na prática:** Estruture com blueprints desde o início (auth, users, api), valide toda entrada e renderize com templates Jinja2 reutilizáveis. Uma base Flask sólida é a fundação de projetos reais [3]."
    ),
    "ZP2-14-django-aplicacoes-web-completas": (
        "Django: Aplicações Web Completas",
        "Django: Modelos, Admin, ORM, Autenticação e Aplicações Web de Produção",
        "Projeto Django, models, ORM, admin, autenticação, views e templates",
        "Django é o framework 'batteries included' do Python: traz admin, ORM, autenticação e segurança prontos. Este livro ensina o Django completo — projetos, apps, models, o ORM, o painel admin, autenticação, views, templates e o deploy de aplicações reais.",
        "Django é a escolha de produção de milhares de empresas — e quem o domina constrói aplicações completas com velocidade e segurança. O ORM, o admin e a autenticação prontos reduzem meses de trabalho. Este é o framework que profissionaliza seu perfil web.",
        "Django organiza projetos em apps: python manage.py startapp [1]. Models definem o banco com Python (class Post(models.Model): ...) e o ORM gera as tabelas e queries. O admin (/admin) oferece CRUD pronto. Autenticação (usuários, login, permissões) vem integrada. Views + templates renderizam páginas; class-based views organizam padrões [2].\n\n**Por que importa?** O ORM do Django gera SQL seguro (anti injeção) e migrações versionam o schema. O admin acelera a gestão de conteúdo. A segurança integrada (CSRF, XSS, SQL injection) é um padrão de produção que o Django aplica por padrão.\n\n**O que muda na prática:** Modele o domínio em models primeiro, use o admin para gestão, e construa views com class-based views para padrões repetitivos. Django recompensa quem segue suas convenções [3]."
    ),
    "ZP2-15-testes-com-pytest": (
        "Testes Automatizados com Pytest",
        "Testes com Pytest: Unitários, Fixtures, Parametrização e Cobertura",
        "Pytest, fixtures, parametrize, mocks, cobertura e testes de integração",
        "Pytest é o framework de testes padrão do Python — e testes são a marca do código profissional. Este livro ensina a estratégia completa: testes unitários, fixtures, parametrização, mocks e medição de cobertura, aplicados a código real.",
        "Desenvolvedor profissional testa — sempre. Pytest torna os testes rápidos de escrever e ler, com fixtures que preparam o ambiente e parametrização que cobre casos em massa. Testes são a rede de segurança que permite refatorar com confiança e evoluir o produto.",
        "Pytest descobre e executa testes com simplicidade: funções test_* e asserts nativos [1]. Fixtures preparam dependências (banco, clientes HTTP) com setup/teardown automático. Parametrize roda o mesmo teste com várias entradas. Mocks (monkeypatch, unittest.mock) isolam dependências externas. A cobertura (pytest-cov) mede o quanto do código é exercitado [2].\n\n**Por que importa?** Testes previnem regressões e documentam o comportamento esperado. Testes que verificam comportamento (não implementação) sobrevivem a refatorações. Cobertura alta nas regras críticas reduz bugs em produção.\n\n**O que muda na prática:** Escreva testes junto com o código, use fixtures para setup e parametrize para casos múltiplos. Rode o pytest no CI para bloquear regressões automaticamente [3]."
    ),
    "ZP2-16-web-scraping-e-automacao-web": (
        "Web Scraping e Automação Web",
        "Web Scraping: BeautifulSoup, Selenium e Extração de Dados da Web",
        "BeautifulSoup, requests, Selenium, Playwright, seletores e extração em escala",
        "A web é a maior fonte de dados do mundo — e o scraping é a forma de acessá-la programaticamente. Este livro ensina a extração de dados com BeautifulSoup e requests, a automação de navegador com Selenium e Playwright, e as práticas éticas e legais do scraping.",
        "Scraping abre um mundo de possibilidades: monitoramento de preços, coleta de dados para análise, automação de tarefas web. BeautifulSoup parseia HTML, Selenium/Playwright automatizam o navegador completo. Dominar essas ferramentas é uma habilidade valiosa e procurada.",
        "O scraping combina requests (baixar a página) e BeautifulSoup (parsear o HTML): soup.find_all('div', class_='produto') [1]. Sites dinâmicos (JavaScript) exigem automação de navegador: Selenium ou Playwright executam a página completa e interagem com ela [2]. Seletores CSS e XPath localizam elementos.\n\n**Por que importa?** Respeitar o robots.txt, o ritmo de requisições e os termos de uso é obrigatório — scraping agressivo quebra sites e pode violar leis. Sites modernos usam JavaScript, paginação e proteção anti-bot, exigindo técnicas mais avançadas.\n\n**O que muda na prática:** Comece com requests + BeautifulSoup em sites estáticos, respeite robots.txt e limites de ritmo, e avance para Playwright quando o conteúdo for dinâmico [3]."
    ),
    # ═══════════ NIVEL 4: IA E MACHINE LEARNING ═══════════
    "ZP2-17-python-para-machine-learning": (
        "Python para Machine Learning",
        "Machine Learning com Python: scikit-learn, Regressão, Classificação e Avaliação",
        "scikit-learn, treino/teste, regressão, classificação, métricas e pipelines",
        "Python é a linguagem do Machine Learning — e o scikit-learn, a porta de entrada. Este livro ensina o ciclo completo: preparação de dados, treino/teste, modelos de regressão e classificação, métricas de avaliação e pipelines — o fluxo que todo profissional de ML executa.",
        "Machine Learning é a habilidade mais valorizada do mercado Python. O scikit-learn oferece os algoritmos clássicos com uma API consistente: fit (treinar), predict (prever), score (avaliar). Dominar o ciclo completo — de dados a métricas — é a base de qualquer carreira em IA.",
        "O ciclo de ML: carregar e limpar dados, dividir em treino/teste (train_test_split), treinar um modelo (model.fit(X_train, y_train)) e avaliar [1]. Regressão prevê valores contínuos (LinearRegression); classificação prevê categorias (LogisticRegression, RandomForest). Métricas: acurácia, precisão, recall, F1, e matriz de confusão. Pipelines encadeiam transformações e modelo [2].\n\n**Por que importa?** Avaliar no mesmo conjunto de treino engana (overfitting) — por isso treino/teste e validação cruzada são obrigatórios. Entender as métricas certas para o problema (desbalanceado, por exemplo) evita modelos que parecem bons e falham na prática.\n\n**O que muda na prática:** Siga o ciclo completo: dados → treino/teste → modelo → métricas → ajuste. Use pipelines para reproduzir o fluxo inteiro em produção [3]."
    ),
    "ZP2-18-introducao-a-llms-e-ia-com-python": (
        "Introdução a LLMs e IA com Python",
        "LLMs e IA com Python: OpenAI, Prompts, Embeddings e Aplicações com Modelos de Linguagem",
        "APIs de LLM, prompts, embeddings, RAG, agentes e aplicações de IA",
        "Os modelos de linguagem (LLMs) transformaram o desenvolvimento — e Python é a linguagem oficial desse ecossistema. Este livro ensina a integrar LLMs em aplicações: chamadas de API, engenharia de prompts, embeddings, busca semântica (RAG) e os primeiros agentes de IA.",
        "Integrar IA em produtos é a habilidade mais demandada do momento. Com poucas linhas de Python, você adiciona geração de texto, análise, busca semântica e automação inteligente a qualquer aplicação. Este livro entrega a base para construir com LLMs de forma profissional.",
        "LLMs são acessados via API: chamadas com um prompt e parâmetros (temperatura, max_tokens) retornam texto gerado [1]. Engenharia de prompts estrutura instruções com contexto e formato. Embeddings transformam texto em vetores numéricos, permitindo busca semântica por similaridade. RAG (Retrieval-Augmented Generation) combina documentos recuperados com geração — a base dos chatbots de conhecimento [2].\n\n**Por que importa?** LLMs alucinam: RAG ancora as respostas em dados próprios, reduzindo erros. Tokens custam dinheiro: prompts bem projetados economizam custo. Segurança: dados sensíveis não devem ir para APIs externas sem política clara.\n\n**O que muda na prática:** Comece com chamadas de API simples, experimente parâmetros, construa um RAG com documentos próprios e estruture prompts como componentes reutilizáveis [3]."
    ),
    # ═══════════ NIVEL 5: PROJETO E CARREIRA ═══════════
    "ZP2-19-projeto-profissional-completo-em-python": (
        "Projeto Profissional Completo em Python",
        "Projeto Profissional: Uma Aplicação Python Completa — do Banco ao Deploy",
        "Arquitetura, aplicação completa, testes, Docker, CI/CD e deploy",
        "Tudo converge neste projeto final: este livro guia a construção completa de uma aplicação Python profissional — modelagem, backend, integração, testes, Docker, CI/CD e deploy. Cada decisão é explicada com o raciocínio que profissionais aplicam em produção.",
        "Um projeto completo é o portfólio que abre portas — e a prova de domínio do ciclo inteiro. Arquitetura limpa, testes, containers e deploy automatizado são os diferenciais exigidos em vagas de nível profissional. Você está pronto para mostrar o que construiu.",
        "A aplicação combina: banco modelado com relações claras [1]; camada de acesso a dados (ORM); lógica de negócio separada da apresentação; testes unitários e de integração; Docker para empacotar a aplicação (Dockerfile, compose); CI/CD que roda testes e faz o deploy automaticamente; variáveis de ambiente isolando configurações [2].\n\n**Por que importa?** A arquitetura em camadas separa responsabilidades e permite testes. Docker elimina o 'funciona na minha máquina'. O CI/CD automatiza qualidade e entrega. Essas práticas são o padrão exigido em qualquer equipe profissional.\n\n**O que muda na prática:** Divida o projeto em etapas com critérios de aceite: banco → backend → testes → Docker → deploy. Esse projeto vira a peça central do seu portfólio profissional [3]."
    ),
    "ZP2-20-carreira-entrevistas-e-portfolio": (
        "Carreira em Python: Entrevistas, Portfólio e Primeiro Emprego",
        "Carreira em Python: Entrevistas Técnicas, Portfólio, CV e Oportunidades de Mercado",
        "Entrevistas, questões clássicas, portfólio, CV, trilhas de carreira e mercado",
        "Você domina Python — agora domine a carreira. Este livro prepara você para o mercado: as trilhas possíveis (web, dados, IA, automação), como se preparar para entrevistas técnicas, as questões clássicas, como montar portfólio e currículo e como conquistar a primeira oportunidade.",
        "Python abre portas em quatro trilhas principais: web, dados, IA e automação. Escolher a trilha, construir portfólio, preparar-se para entrevistas e entender o processo seletivo transforma conhecimento em carreira. Você está pronto para o mercado.",
        "O mercado Python oferece trilhas claras: desenvolvedor web (Django/Flask), analista/engenheiro de dados (Pandas, SQL), cientista de dados (ML, estatística) e engenheiro de IA (LLMs) [1]. Entrevistas avaliam fundamentos (estruturas de dados, compreensões, POO), SQL e projeto. O portfólio com projetos completos no GitHub — código limpo, testes e documentação — é o que recrutadores realmente avaliam [2].\n\n**Por que importa?** Cada trilha tem ferramentas e expectativas próprias — escolher cedo foca o estudo. Projetos reais valem mais que certificados. Um GitHub ativo demonstra prática contínua e habilidade de comunicação de código.\n\n**O que muda na prática:** Escolha sua trilha, publique 2-3 projetos completos, pratique questões clássicas em voz alta e construa um CV orientado a resultados. A carreira em Python está entre as mais abertas do mercado [3]."
    ),
}
