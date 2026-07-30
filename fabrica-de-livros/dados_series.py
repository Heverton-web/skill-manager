#!/usr/bin/env python3
"""
Dados das 10 Séries de Livros AIDD (E1-E5, F1-F5, ..., N1-N5)
Cada série tem 5 livros, cada livro tem 4 Partes e 16 Capítulos.
Usado por gerar-livros-aidd.py e preparar-series.py
"""

SERIES_INFO = {
    "E": {"nome": "Segurança e Governança (Security & Compliance)", "prefixo": "E"},
    "F": {"nome": "DevOps e Infraestrutura", "prefixo": "F"},
    "G": {"nome": "Testes e Qualidade", "prefixo": "G"},
    "H": {"nome": "Automação e Robótica", "prefixo": "H"},
    "I": {"nome": "Dados e Analytics", "prefixo": "I"},
    "J": {"nome": "Fintech", "prefixo": "J"},
    "K": {"nome": "Mobile", "prefixo": "K"},
    "L": {"nome": "Cloud", "prefixo": "L"},
    "M": {"nome": "Performance", "prefixo": "M"},
    "N": {"nome": "Corporativo (Enterprise)", "prefixo": "N"},
}

# slug -> (nome_livro, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_EXTRA = {
    # ═══ SÉRIE E — SEGURANÇA E GOVERNANÇA ═══
    "E1-seguranca-auth": (
        "Autenticação e Autorização com AIDD",
        "Autenticação e Autorização com AIDD: Protegendo Aplicações na Era dos Agentes",
        "JWT, OAuth, SSO, MFA, RBAC — Gerando Fluxos Seguros com Agentes de IA",
        "A segurança de aplicações na era AIDD não é responsabilidade apenas dos frameworks — ela começa na forma como você configura seus agentes. Este livro ensina como gerar fluxos de autenticação e autorização seguros por padrão, sem abrir brechas.",
        "A autenticação e autorização são a primeira linha de defesa de qualquer aplicação. No AIDD, o foco muda de implementar manualmente cada fluxo para orquestrar agentes que geram código seguro por padrão. Dominar essas técnicas é o que separa engenheiros que produzem sistemas seguros de quem deixa brechas.",
        "Autenticação é o processo de verificar quem um usuário é, enquanto autorização determina o que esse usuário pode fazer. No contexto AIDD, ambas precisam ser delegadas a agentes que seguem contratos de segurança rigorosos. A diferença crucial é que, em sistemas tradicionais, o engenheiro implementa cada fluxo manualmente; no AIDD, ele define as regras e os agentes geram a implementação automaticamente.\n\n**Por que importa?** Erros de autenticação são responsáveis por 81% das violações de dados segundo a Verizon. No AIDD, um system prompt mal escrito pode gerar código com falhas de autenticação em escala industrial.\n\n**O que muda com AIDD:** Em vez de escrever JWT verification manualmente, o engenheiro define parâmetros como algoritmo de assinatura, tempo de expiração e claims obrigatórios — e o agente gera o middleware completo, testado e documentado."
    ),
    "E2-seguranca-cripto": (
        "Criptografia e Proteção de Dados com AIDD",
        "Criptografia e Proteção de Dados: Implementando Segurança com Agentes de IA",
        "Encryption at Rest, TLS, Hashing, PKI — Gerando Criptografia Robusta com Prompts",
        "Criptografia é uma daquelas áreas onde errar é fatal e invisível. Um byte mal cifrado pode comprometer milhões de registros. Este livro ensina como usar agentes de IA para gerar implementações criptográficas corretas por construção.",
        "A criptografia no AIDD não é diferente da criptografia tradicional nos fundamentos — mas a forma de implementá-la muda radicalmente. Agentes podem gerar implementações corretas de TLS, AES, RSA e hashing, desde que o engenheiro saiba especificar os parâmetros certos.",
        "Criptografia é a prática de proteger informações transformando-as em formato ilegível para não autorizados. No AIDD, o engenheiro não precisa memorizar APIs de criptografia — ele precisa saber especificar o algoritmo, modo de operação, tamanho de chave e vector de inicialização corretos.\n\n**O perigo da alucinação criptográfica:** Agentes podem gerar código que parece criptograficamente correto mas usa modos inseguros como ECB, chaves fixas ou IVs nulos. O engenheiro AIDD precisa saber validar o output do agente contra padrões como NIST e OWASP.\n\n**Estratégia de defesa:** Sempre peça para o agente justificar a escolha do algoritmo e modo de operação, referenciar a fonte normativa (NIST SP 800-38A, etc.) e incluir testes de validação."
    ),
    "E3-seguranca-owasp": (
        "OWASP e Segurança de Aplicações com AIDD",
        "OWASP e Segurança de Aplicações: Top 10 na Era dos Agentes de IA",
        "SQLi, XSS, CSRF — Prompts que Geram Código Seguro por Construção",
        "OWASP Top 10 continua sendo o guia mais importante para segurança de aplicações. Este livro mostra como configurar agentes para que o código gerado seja imune às 10 categorias de vulnerabilidade mais críticas.",
        "O OWASP Top 10 não muda porque a web mudou — muda porque os atacantes evoluem. No AIDD, o engenheiro tem uma vantagem única: pode programar o agente para nunca gerar código vulnerável a SQLi, XSS ou CSRF.",
        "O OWASP Top 10 é uma lista das 10 categorias de vulnerabilidade mais críticas em aplicações web, atualizada periodicamente pela Open Web Application Security Project. No AIDD, cada categoria se traduz em uma regra de system prompt.\n\n**SQL Injection:** Configure o agente para sempre usar parameterized queries ou ORM seguro, nunca concatenar strings em SQL. O prompt deve incluir: \"Toda query SQL DEVE usar parâmetros vinculados. String concatenation é PROIBIDA.\"\n\n**XSS (Cross-Site Scripting):** Todo dado refletido na view deve passar por escaping contextual. O agente deve usar a função de escape apropriada para HTML, JavaScript, CSS ou URL.\n\n**CSRF (Cross-Site Request Forgery):** Toda mutação de estado deve incluir token CSRF. Configure o agente para incluir automaticamente o middleware CSRF em todo formulário e requisição POST."
    ),
    "E4-seguranca-compliance": (
        "Governança e Compliance com AIDD",
        "Governança e Compliance: LGPD, GDPR e SOC2 com Agentes de IA",
        "Auditoria Automática, Privacidade por Design, Agentes Compliant por Padrão",
        "Compliance não é opcional — é lei. LGPD, GDPR e SOC2 impõem requisitos rigosos de proteção de dados. Este livro ensina a configurar agentes que geram código compliant por padrão.",
        "Governança e compliance no AIDD significam que cada linha de código gerada por um agente deve respeitar requisitos legais e regulatórios. O engenheiro AIDD não é advogado — mas precisa saber traduzir requisitos legais em restrições de prompt.",
        "Compliance no AIDD começa no system prompt. Cada agente que gera código que processa dados pessoais deve ter regras explícitas sobre: minimização de dados, consentimento, direito ao esquecimento e portabilidade.\n\n**LGPD (Lei Geral de Proteção de Dados):** O agente nunca deve hardcodar dados pessoais. Toda coleta de dados deve ter campo de consentimento. Toda funcionalidade de exclusão deve realmente apagar os dados.\n\n**GDPR:** Similar à LGPD mas com requisitos adicionais de Data Protection Officer e notificação de violação em 72 horas.\n\n**SOC2:** Foco em controle de acesso, monitoramento e auditoria. O agente deve gerar logs imutáveis e alertas de segurança automaticamente."
    ),
    "E5-seguranca-redteam": (
        "Red Team com Agentes de IA",
        "Red Team com Agentes: Segurança Ofensiva na Era do AIDD",
        "Pen Testing Automatizado, Vulnerability Scanning, Segurança Ofensiva com Prompts",
        "Red Team tradicional é caro e lento. Com agentes de IA, você pode automatizar grande parte do trabalho de segurança ofensiva — desde scanning até exploração controlada.",
        "Red Team com agentes não substitui o profissional de segurança — potencializa. O agente faz o trabalho pesado de scanning, reconhecimento e enumeração; o humano foca em análise crítica, exploração criativa e relatório.",
        "Red Team é a prática de simular ataques reais contra sistemas para identificar vulnerabilidades antes que atacantes reais o façam. No AIDD, agentes podem automatizar as fases mais repetitivas do processo.\n\n**Fases do Red Team com Agentes:**\n1. Reconhecimento passivo: agente coleta informações públicas (OSINT)\n2. Scanning: agente varre portas, serviços e versões\n3. Enumeração: agente identifica endpoints, parâmetros e vulnerabilidades conhecidas\n4. Exploração: agente tenta exploits controlados em ambiente isolado\n5. Pós-exploração: agente documenta impacto e sugere correções"
    ),

    # ═══ SÉRIE F — DEVOPS E INFRAESTRUTURA ═══
    "F1-devops-cicd": (
        "CI/CD com Agentes de IA",
        "CI/CD com Agentes: Pipelines Inteligentes que se Autorregulam",
        "GitHub Actions, Jenkins, GitLab CI — Pipelines Gerados e Mantidos por IA",
        "CI/CD é o sistema circulatório do desenvolvimento moderno. Este livro ensina como usar agentes para criar, manter e otimizar pipelines que se adaptam automaticamente às necessidades do projeto.",
        "CI/CD com agentes significa pipelines que não apenas executam comandos — eles analisam código, detectam problemas, sugerem correções e até se autorreparam. O engenheiro AIDD projeta a estratégia, os agentes implementam os pipelines.",
        "CI/CD (Continuous Integration/Continuous Deployment) é a prática de automatizar a construção, teste e implantação de software. No AIDD, os pipelines se tornam inteligentes: agentes analisam o diff, sugerem quais testes rodar, e até corrigem problemas de build automaticamente.\n\n**Pipeline AIDD vs Tradicional:** Um pipeline tradicional segue uma receita fixa. Um pipeline AIDD analisa o contexto da mudança e decide dinamicamente quais etapas executar."
    ),
    "F2-devops-docker": (
        "Containerização e Docker com AIDD",
        "Containerização e Docker: Orquestrando Containers com Agentes de IA",
        "Dockerfiles, Compose, Registries — Gerando Ambientes Reproduzíveis com Prompts",
        "Containerizar aplicações é uma habilidade essencial que agentes de IA podem executar com alta precisão. Este livro ensina como gerar Dockerfiles otimizados, docker-compose multi-serviço e estratégias de image tagging.",
        "Docker com AIDD significa dizer ao agente: 'Crie um Dockerfile multi-stage para uma app Node.js com Redis, otimizado para produção' — e receber um Dockerfile pronto, com cache layers, segurança e tamanho mínimo.",
        "Containerização empacota aplicações e dependências em imagens leves e portáteis. No AIDD, o engenheiro especifica os requisitos em linguagem natural e o agente gera o Dockerfile completo.\n\n**Melhores práticas para agentes:** Sempre especificar versões explícitas de imagens base, nunca usar 'latest'. Usar multi-stage builds para reduzir tamanho. Incluir HEALTHCHECK e labels."
    ),
    "F3-devops-kubernetes": (
        "Kubernetes com Agentes de IA",
        "Kubernetes e Orquestração: Gerando Manifestos com Prompts Inteligentes",
        "Pods, Services, Deployments — YAML que Funciona na Primeira Tentativa",
        "Kubernetes é poderoso mas complexo. Um manifesto YAML mal escrito pode derrubar um cluster inteiro. Este livro ensina a usar agentes para gerar manifestos Kubernetes corretos, seguros e otimizados.",
        "K8s com AIDD: você descreve o que quer ('Deploy 3 réplicas de uma app Node.js com health check, HPA e service mesh') e o agente gera todos os YAMLs consistentes entre si.",
        "Kubernetes é o orquestrador de containers mais utilizado do mundo. No AIDD, o engenheiro não precisa memorizar a sintaxe YAML de cada recurso — ele descreve o objetivo e o agente gera os manifestos completos.\n\n**Cuidados críticos:** Todo manifesto gerado por agente deve ser validado com 'kubectl dry-run' e kubeval antes de aplicar. Agentes podem alucinar recursos que não existem na versão do cluster."
    ),
    "F4-devops-iac": (
        "Infraestrutura como Código com AIDD",
        "Infraestrutura como Código: Terraform, Pulumi e CloudFormation com Agentes",
        "IaC Declarativa, Módulos Reutilizáveis, Validação Automática com Prompts",
        "IaC é a espinha dorsal da nuvem moderna. Este livro ensina como usar agentes para gerar módulos Terraform, stacks Pulumi e templates CloudFormation que são seguros, reutilizáveis e bem documentados.",
        "IaC com AIDD transforma a forma como infraestrutura é projetada: em vez de copiar módulos prontos, você descreve a arquitetura desejada e o agente gera o código IaC completo com validação embutida.",
        "Infraestrutura como Código trata recursos de infraestrutura como software — versionado, testado e revisado. No AIDD, agentes geram módulos IaC completos a partir de descrições de alto nível.\n\n**Estratégia de contexto:** Forneça ao agente apenas o contexto das tags, naming conventions e providers — não o estado atual inteiro da infraestrutura, que estoura a janela de tokens."
    ),
    "F5-devops-observabilidade": (
        "Observabilidade e Monitoramento com AIDD",
        "Observabilidade e Monitoramento: Prometheus, Grafana e OpenTelemetry com Agentes",
        "Métricas, Logs, Traços Distribuídos — Agentes que Monitoram e se Autorregulam",
        "Observabilidade é a capacidade de entender o estado interno de um sistema a partir de seus outputs externos. Este livro ensina como agentes de IA podem gerar dashboards, alertas e pipelines de observabilidade.",
        "Observabilidade com AIDD significa agentes que não apenas geram código de monitoramento — eles analisam métricas, detectam anomalias e sugerem correções proativamente.",
        "Observabilidade se apoia em três pilares: métricas, logs e tracing distribuído. No AIDD, agentes podem gerar instrumentação para os três simultaneamente a partir de uma descrição do sistema.\n\n**OpenTelemetry como padrão:** Configure o agente para sempre usar OpenTelemetry SDK em vez de APIs proprietárias. Isso garante portabilidade entre backends (Prometheus, Datadog, New Relic)."
    ),

    # ═══ SÉRIE G — TESTES E QUALIDADE ═══
    "G1-testes-unitarios": (
        "Testes Unitários com Agentes de IA",
        "Testes Unitários: Gerando Suítes de Teste Automáticas com AIDD",
        "Jest, Vitest, Pytest — Cobertura Completa sem Esforço Manual",
        "Testes unitários são a base da pirâmide de testes. Este livro ensina como usar agentes para gerar suítes completas de testes unitários a partir do código fonte, sem especificação manual.",
        "Testes unitários com AIDD significam: você aponta o agente para um arquivo de código, ele analisa as funções, identifica edge cases e gera testes que cobrem 90%+ do código automaticamente.",
        "Testes unitários verificam o comportamento de unidades individuais de código (funções, métodos, classes) de forma isolada. No AIDD, agentes podem analisar o código fonte e gerar testes que cobrem: fluxo feliz, edge cases, condições de erro e valores limite.\n\n**Estratégia de prompt:** 'Analise este arquivo e gere testes unitários com Jest. Cobre fluxo principal, parâmetros inválidos, valores limite e exceções. Use mocks apenas para dependências externas.'"
    ),
    "G2-testes-integracao": (
        "Testes de Integração com Agentes de IA",
        "Testes de Integração: Validando Fluxos Inteiros com AIDD",
        "Supertest, Cypress, Playwright — Testando Rotas, APIs e Banco de Dados",
        "Testes de integração validam que diferentes partes do sistema funcionam juntas. Este livro ensina como agentes podem gerar cenários de integração complexos automaticamente.",
        "Testes de integração com AIDD: o agente analisa as rotas, schemas e regras de negócio, depois gera testes que exercitam o fluxo completo — request → validação → banco → response.",
        "Testes de integração verificam a interação entre componentes: API + banco + serviço externo. No AIDD, o agente precisa de contexto sobre a arquitetura completa para gerar testes realistas.\n\n**O desafio do contexto:** Para gerar bons testes de integração, o agente precisa entender o schema do banco, os contratos das APIs e as regras de negócio — muita informação para a janela de contexto. Estratégia: forneça apenas os schemas e contratos, não o código de implementação."
    ),
    "G3-testes-e2e": (
        "Testes E2E e Performance com AIDD",
        "Testes E2E e Performance: Garantindo Qualidade em Produção",
        "Cypress, Playwright, k6, Lighthouse — Cenários Realistas Gerados por IA",
        "Testes E2E simulam o usuário real. Testes de performance garantem que o sistema aguenta a carga. Este livro mostra como agentes podem gerar ambos a partir de user stories.",
        "Testes E2E com AIDD: o agente lê uma user story ('Como usuário, quero fazer login e ver meu dashboard') e gera o teste E2E completo no Playwright — incluindo setup, execução e asserções.",
        "Testes E2E simulam o caminho completo do usuário através do sistema. No AIDD, a abordagem é Behavior-Driven: o agente converte user stories em cenários de teste automaticamente.\n\n**Performance com k6:** Descreva 'Quero testar 1000 usuários simultâneos no endpoint /login' e o agente gera o script k6 completo com stages de ramp-up, thresholds e relatório."
    ),
    "G4-testes-codereview": (
        "Code Review com Agentes de IA",
        "Code Review Automatizado: Agentes que Revisam Agentes",
        "ESLint, SonarQube, CodeRabbit — Revisão Técnica em Escala com Prompts",
        "Code review é o processo mais importante para qualidade de código — e o mais gargalado. Este livro ensina a usar agentes para revisar código automaticamente, mantendo o humano no loop para decisões arquiteturais.",
        "Code review com AIDD: o agente analisa o diff, verifica style guide, detecta code smells, verifica cobertura de testes e sugere melhorias — tudo antes do revisor humano olhar.",
        "Code review automatizado usa ferramentas estáticas (ESLint, SonarQube) e agentes de IA para analisar código. A diferença no AIDD é que o agente pode entender o contexto do negócio, não apenas regras sintáticas.\n\n**Revisão em camadas:**\n1. Sintática: ESLint/Prettier → automático\n2. Semântica: Agente verifica lógica e edge cases\n3. Arquitetural: Humano decide sobre design patterns"
    ),
    "G5-testes-qualidade": (
        "Qualidade e Dívida Técnica com AIDD",
        "Qualidade e Dívida Técnica: Governança de Código na Era dos Agentes",
        "Métricas, Refatoração, Cobertura — Agentes que Mantêm a Qualidade ao Longo do Tempo",
        "Dívida técnica é inevitável — mas gerenciável. Este livro ensina como usar agentes para medir, monitorar e reduzir dívida técnica automaticamente, mantendo a qualidade do código ao longo do tempo.",
        "Qualidade com AIDD: agentes que analisam a codebase, identificam áreas com alta dívida técnica (complexidade ciclomática, acoplamento, falta de cobertura) e geram planos de refatoração priorizados.",
        "Dívida técnica é o custo implícito de retrabalho causado por escolhas de implementação que priorizam velocidade em detrimento da qualidade. No AIDD, agentes podem quantificar essa dívida e sugerir ações corretivas.\n\n**Métricas-chave para agentes monitorarem:** Complexidade ciclomática (< 10 ideal), cobertura de testes (> 80%), duplicação de código (< 5%), acoplamento entre módulos, tempo médio para adicionar nova feature."
    ),

    # ═══ SÉRIE H — AUTOMAÇÃO E ROBÓTICA ═══
    "H1-automacao-rpa": (
        "RPA com Agentes de IA",
        "RPA com Agentes: Automatizando Processos Repetitivos com Inteligência Artificial",
        "BotCity, UiPath, Automation Anywhere — RPA Inteligente com Prompts AIDD",
        "RPA tradicional automatiza tarefas repetitivas seguindo regras fixas. Com agentes de IA, o RPA se torna adaptativo: ele entende contexto, trata exceções e aprende com o tempo.",
        "RPA com AIDD transforma robôs de tarefas fixas em assistentes inteligentes que entendem variações nos processos e se adaptam automaticamente a mudanças nos sistemas alvo.",
        "RPA (Robotic Process Automation) automatiza tarefas repetitivas baseadas em regras. No AIDD, o RPA ganha capacidade de entender documentos, extrair informações não estruturadas e tomar decisões baseadas em contexto.\n\n**Diferença-chave:** RPA tradicional falha quando a interface do sistema alvo muda. RPA com AIDD usa visão computacional e理解 contextual para se adaptar automaticamente."
    ),
    "H2-automacao-pipeline": (
        "Pipelines de Automação com AIDD",
        "Pipelines de Automação: Orquestrando Fluxos de Trabalho com Agentes",
        "n8n, Zapier, Make — Pipelines Adaptativos que se Autorregulam",
        "Pipelines de automação conectam ferramentas e processos. Este livro ensina como projetar pipelines inteligentes onde agentes decidem dinamicamente o fluxo, tratam erros e otimizam recursos.",
        "Pipelines com AIDD: em vez de fluxos fixos if-this-then-that, agentes analisam o contexto de cada execução e decidem o melhor caminho — incluindo fallbacks, retries e notificações inteligentes.",
        "Pipelines de automação conectam sistemas, ferramentas e processos em fluxos coordenados. No AIDD, cada nó do pipeline pode ser um agente que toma decisões baseadas em contexto.\n\n**Arquitetura de pipeline AIDD:** n8n como orquestrador visual, MCPs como conectores, agentes como nós de decisão, e LLM como cérebro para casos complexos."
    ),
    "H3-automacao-iot": (
        "IoT e Agentes de IA",
        "IoT com Agentes: Dispositivos Inteligentes Orquestrados por IA",
        "Sensores, Atuadores, Edge Computing — Automação Física com Prompts",
        "Internet das Coisas conecta o mundo físico ao digital. Este livro mostra como agentes de IA podem gerenciar dispositivos IoT, processar dados de sensores e tomar decisões em tempo real.",
        "IoT com AIDD: agentes que analisam streams de dados de milhares de sensores, detectam anomalias em tempo real e acionam atuadores automaticamente — tudo coordenado por prompts de alto nível.",
        "IoT (Internet of Things) conecta dispositivos físicos à internet para coleta e troca de dados. No AIDD, agentes atuam como cérebro distribuído que processa dados na borda (edge) e na nuvem.\n\n**Edge AI:** Agentes leves rodam em dispositivos IoT para tomar decisões em milissegundos sem depender da nuvem. O prompt do agente edge é uma versão reduzida e especializada do agente cloud."
    ),
    "H4-automacao-processos": (
        "Automação de Processos com AIDD",
        "BPM e Automação de Processos: Modelagem e Execução com Agentes",
        "BPMN, Workflows, Regras de Negócio — Processos Inteligentes com Prompts",
        "Automação de processos de negócio (BPM) é a espinha dorsal da transformação digital. Este livro ensina como agentes de IA podem modelar, executar e otimizar processos de negócio complexos.",
        "BPM com AIDD: em vez de diagramas BPMN estáticos, processos vivos onde agentes decidem o fluxo baseado em dados reais, históricos e regras de negócio mutáveis.",
        "BPM (Business Process Management) é a disciplina de modelar, automatizar e otimizar processos de negócio. No AIDD, agentes podem interpretar descrições de processos em linguagem natural e gerar workflows executáveis.\n\n**Abordagem AIDD:** O engenheiro descreve o processo em texto ('Quando um pedido chega, verificar estoque, aprovar se < R$5000, notificar cliente') e o agente gera o BPMN, regras e integrações."
    ),
    "H5-automacao-lowcode": (
        "Low-Code/No-Code com AIDD",
        "Low-Code e No-Code: Construindo Aplicações sem Programar com Agentes",
        "Bubble, Retool, Appsmith — Plataformas Visuais com Cérebro de IA",
        "Low-code e no-code democratizam o desenvolvimento. Com agentes de IA, essas plataformas se tornam ainda mais poderosas — permitindo que usuários de negócio criem aplicações complexas sem escrever uma linha de código.",
        "Low-code com AIDD: o usuário descreve o que quer em linguagem natural, o agente configura os componentes visuais, conecta dados e define a lógica de negócio — tudo na plataforma low-code.",
        "Plataformas low-code/no-code permitem criar aplicações com mínimo de código escrito manualmente. No AIDD, agentes atuam como tradutores entre intenção humana e configuração visual.\n\n**O papel do engenheiro AIDD:** Configurar os MCPs que conectam o agente à plataforma low-code, definir os templates de componentes e estabelecer as regras de segurança que o agente deve seguir."
    ),

    # ═══ SÉRIE I — DADOS E ANALYTICS ═══
    "I1-dados-engenharia": (
        "Engenharia de Dados com AIDD",
        "Engenharia de Dados: Pipelines de Dados Gerenciados por Agentes de IA",
        "ETL, ELT, Data Lakes, Data Warehouses — Orquestrando Dados com Prompts",
        "Engenharia de dados é a base de qualquer iniciativa de analytics e ML. Este livro ensina como agentes de IA podem projetar, construir e manter pipelines de dados em escala.",
        "Engenharia de dados com AIDD: descreva a fonte e o destino ('Extrair dados do PostgreSQL, transformar com dbt, carregar no BigQuery') e o agente gera o pipeline completo com tratamentos de erro e monitoramento.",
        "Engenharia de dados envolve coletar, transformar e armazenar dados para análise posterior. No AIDD, agentes podem gerar pipelines ETL/ELT completos a partir de descrições de alto nível.\n\n**Stack típica AIDD:** Airflow/Dagster como orquestrador, dbt para transformações, Spark para processamento distribuído, e agentes para gerar e manter cada etapa do pipeline."
    ),
    "I2-dados-analytics": (
        "Analytics e BI com AIDD",
        "Analytics e BI: Dashboards e Relatórios Inteligentes com Agentes",
        "Metabase, Superset, Power BI — Visualizações que Respondem Perguntas",
        "Business Intelligence transforma dados brutos em decisões. Este livro ensina como agentes de IA podem analisar dados, gerar dashboards interativos e responder perguntas de negócio automaticamente.",
        "Analytics com AIDD: em vez de construir dashboards manuais, agentes analisam os dados, identificam padrões e geram visualizações que contam a história dos dados.",
        "Analytics e BI transformam dados em insights acionáveis. No AIDD, agentes podem atuar como analistas de dados: recebem perguntas em linguagem natural, consultam o banco e geram visualizações.\n\n**Exemplo:** 'Mostre a tendência de vendas dos últimos 6 meses por região, destacando outliers' → agente gera a query SQL, executa, analisa os resultados e gera o chart."
    ),
    "I3-dados-ml": (
        "Machine Learning com Agentes de IA",
        "Machine Learning: Modelos Treinados e Gerenciados por Agentes AIDD",
        "Scikit-learn, TensorFlow, PyTorch — ML Pipelines com Prompts e Automação",
        "Machine Learning é a fronteira mais avançada do AIDD. Este livro ensina como agentes podem auxiliar em todo o ciclo de vida de ML: desde a preparação dos dados até o deploy do modelo.",
        "ML com AIDD: agentes que analisam dados, sugerem algoritmos, geram código de treinamento, avaliam métricas e até propõem experimentos de hiperparâmetros automaticamente.",
        "Machine Learning cria modelos que aprendem padrões a partir de dados. No AIDD, agentes podem automatizar grande parte do ciclo de vida de ML: EDA, feature engineering, treinamento, avaliação e deploy.\n\n**AutoML vs AIDD:** AutoML automatiza a escolha de algoritmo e hiperparâmetros. AIDD vai além — o agente entende o problema de negócio e sugere a abordagem de ML mais adequada."
    ),
    "I4-dados-streaming": (
        "Stream Processing com AIDD",
        "Stream Processing: Dados em Tempo Real com Agentes de IA",
        "Kafka, Flink, Spark Streaming — Processamento Contínuo com Prompts",
        "Dados em movimento são tão importantes quanto dados em repouso. Este livro ensina como usar agentes para projetar, implementar e monitorar pipelines de streaming em tempo real.",
        "Streaming com AIDD: agentes que monitoram tópicos Kafka, detectam padrões em tempo real, e acionam alertas ou transformações automaticamente — sem intervenção humana.",
        "Stream processing processa dados em tempo real conforme eles chegam, sem armazenar primeiro. No AIDD, agentes podem gerar aplicações de streaming completas: producers, consumers, processors e sinks.\n\n**Padrão Kafka + AIDD:** O agente recebe o schema do evento Avro/Protobuf e gera automaticamente o consumer, o processador (com lógica de negócio em SQL ou Java) e o sink para o destino final."
    ),
    "I5-dados-governanca": (
        "Governança de Dados com AIDD",
        "Governança de Dados: Catálogo, Linhagem e Qualidade com Agentes",
        "Data Catalogs, Data Lineage, Data Quality — Dados Confiáveis com Prompts",
        "Governança de dados garante que os dados sejam confiáveis, acessíveis e seguros. Este livro ensina como agentes de IA podem automatizar catalogação, linhagem e qualidade de dados.",
        "Governança com AIDD: agentes que varrem o data lake, catalogam tabelas, mapeiam linhagem de dados e geram relatórios de qualidade — tudo em linguagem natural.",
        "Governança de dados é o conjunto de práticas que garantem qualidade, segurança e usabilidade dos dados. No AIDD, agentes podem automatizar: catalogação de schemas, detecção de anomalias, mapeamento de linhagem e geração de documentação.\n\n**Data Catalog automatizado:** O agente conecta-se ao banco, extrai metadados (tabelas, colunas, tipos, constraints) e gera um catálogo pesquisável com descrições em linguagem natural."
    ),

    # ═══ SÉRIE J — FINTECH ═══
    "J1-fintech-pagamentos": (
        "Pagamentos e Transações com AIDD",
        "Pagamentos e Transações: Sistemas Financeiros Robusto com Agentes de IA",
        "Pix, Cartões, Boletos — Orquestrando Fluxos de Pagamento com Prompts",
        "Sistemas de pagamento são os mais críticos em termos de confiabilidade e segurança. Este livro ensina como agentes de IA podem gerar código de processamento de transações com resiliência bancária.",
        "Pagamentos com AIDD: agentes que geram código de processamento de transações com atomicidade, consistência, isolamento e durabilidade — os pilares ACID aplicados a pagamentos digitais.",
        "Sistemas de pagamento processam transações financeiras com requisitos rigorosos de atomicidade, consistência, isolamento e durabilidade (ACID). No AIDD, agentes devem gerar código que respeite esses princípios.\n\n**Cuidados específicos:** Transações financeiras nunca podem ser perdidas ou duplicadas. O agente deve gerar código com idempotência, retry com backoff, e auditoria completa de cada operação."
    ),
    "J2-fintech-regulatorio": (
        "Regulatório e Compliance Financeiro com AIDD",
        "Regulatório Financeiro: BACEN, CVM, Susep com Agentes de IA",
        "Regulações Bancárias, Prevenção a Lavagem de Dinheiro, Relatórios Regulatórios",
        "O setor financeiro é o mais regulado do mundo. Este livro ensina como configurar agentes para gerar código que atende aos requisitos regulatórios do BACEN, CVM e Susep automaticamente.",
        "Compliance financeiro com AIDD: agentes que conhecem as regulações (Circular BACEN, Instruções CVM) e geram código que implementa os controles necessários — KYC, AML, PLD — por construção.",
        "O sistema financeiro brasileiro é regulado por BACEN, CVM e Susep, cada um com seu conjunto de normas. No AIDD, o system prompt do agente deve incluir referências às circulares aplicáveis.\n\n**PLD (Prevenção à Lavagem de Dinheiro):** O agente deve gerar código que monitore transações suspeitas baseado em regras como: valores acima de R$50.000, estruturas de fracionamento, múltiplas transações em curto período."
    ),
    "J3-fintech-blockchain": (
        "Blockchain e Web3 com AIDD",
        "Blockchain e Web3: Smart Contracts e DApps com Agentes de IA",
        "Solidity, Ethereum, Hyperledger — Contratos Inteligentes Gerados por Prompts",
        "Blockchain promete descentralização e transparência. Este livro ensina como agentes de IA podem gerar smart contracts seguros, testar vulnerabilidades e otimizar gas fees.",
        "Blockchain com AIDD: descreva a lógica do contrato ('Um token ERC-20 com governance e vesting de 4 anos') e o agente gera o Solidity completo com testes, deploy script e documentação.",
        "Smart contracts são programas que executam em blockchain, imutáveis e auto-executáveis. No AIDD, agentes podem gerar contratos completos a partir de especificações em linguagem natural.\n\n**Segurança crítica:** Erros em smart contracts podem resultar em perdas financeiras irreversíveis. Sempre peça ao agente para incluir testes de segurança: reentrância, overflow, access control, front-running."
    ),
    "J4-fintech-openbanking": (
        "Open Banking e Open Finance com AIDD",
        "Open Banking e Open Finance: APIs Abertas com Agentes de IA",
        "Integrações Bancárias, Consentimento, Compartilhamento de Dados — Open Finance com Prompts",
        "Open Banking transformou o sistema financeiro em uma plataforma aberta de APIs. Este livro ensina como agentes podem gerar integrações compatíveis com as especificações do Open Finance Brasil.",
        "Open Banking com AIDD: o agente conhece as especificações técnicas do Open Finance Brasil (fases 1-3) e gera endpoints que implementam corretamente os fluxos de consentimento, compartilhamento e iniciação de pagamentos.",
        "Open Finance Brasil é o sistema de compartilhamento de dados e serviços financeiros regulado pelo BACEN. No AIDD, agentes podem gerar implementações das APIs padronizadas.\n\n**Especificações-chave:** Fase 1 (dados cadastrais), Fase 2 (dados transacionais), Fase 3 (iniciação de pagamento e consentimento). O agente deve referenciar a especificação técnica oficial em cada prompt."
    ),
    "J5-fintech-fraud": (
        "Prevenção a Fraudes com AIDD",
        "Prevenção a Fraudes: Detecção e Mitigação com Agentes de IA",
        "Machine Learning Anti-Fraude, Regras em Tempo Real, Análise de Risco",
        "Fraude digital é um negócio de bilhões. Este livro ensina como usar agentes para construir sistemas de detecção de fraude em tempo real, combinando regras tradicionais com machine learning.",
        "Anti-fraude com AIDD: agentes que analisam transações em tempo real, aplicam regras de risco, consultam modelos de ML e decidem entre aprovar, rejeitar ou enviar para análise manual.",
        "Prevenção a fraudes combina regras de negócio, machine learning e análise comportamental para identificar transações suspeitas. No AIDD, agentes podem orquestrar todo o pipeline de decisão.\n\n**Regras típicas geradas por agentes:** Transações acima do limite do perfil, múltiplas transações em intervalos curtos, device fingerprint desconhecido, geolocalização incompatível."
    ),

    # ═══ SÉRIE K — MOBILE ═══
    "K1-mobile-reactnative": (
        "React Native com AIDD",
        "React Native: Apps Mobile Nativas com Agentes de IA",
        "Expo, Navigation, Native Modules — Componentes Cross-Platform com Prompts",
        "React Native permite criar apps nativas para iOS e Android com JavaScript. Este livro ensina como agentes de IA podem gerar componentes, navegação e integrações nativas de forma consistente.",
        "React Native com AIDD: descreva a tela em linguagem natural ('Tela de login com email, senha, botão de entrar e link para cadastro') e o agente gera o componente completo com estilo e navegação.",
        "React Native é o framework cross-platform mais popular para desenvolvimento mobile. No AIDD, agentes podem gerar componentes React Native que funcionam em iOS e Android sem modificações.\n\n**Especificidade mobile:** O prompt deve incluir considerações de plataforma: SafeAreaView no iOS, BackHandler no Android, e tratamento de teclado e orientação."
    ),
    "K2-mobile-flutter": (
        "Flutter com AIDD",
        "Flutter: Apps Multiplataforma com Agentes de IA",
        "Dart, Widgets, State Management — UI Consistente Gerada por Prompts",
        "Flutter é a aposta do Google para desenvolvimento multiplataforma. Este livro ensina como agentes podem gerar widgets, gerenciar estado e integrar com plataformas nativas usando Flutter.",
        "Flutter com AIDD: descreva a UI usando terminologia Flutter ('Um Column com um TextField e um ElevatedButton centralizados') e o agente gera o widget tree completo com Theme e responsividade.",
        "Flutter usa a linguagem Dart e um sistema de widgets para construir UIs nativas compiladas. No AIDD, agentes podem gerar árvores de widgets complexas a partir de descrições visuais.\n\n**Dica AIDD:** Inclua no prompt o tema do Material Design ou Cupertino que o agente deve usar, as cores primárias e secundárias, e os breakpoints de responsividade."
    ),
    "K3-mobile-ios": (
        "iOS e Swift com AIDD",
        "iOS e Swift: Apps Nativas Apple com Agentes de IA",
        "SwiftUI, UIKit, Combine — Ecossistema Apple com Prompts Inteligentes",
        "O ecossistema Apple tem requisitos únicos de design e performance. Este livro ensina como agentes podem gerar apps iOS nativas seguindo as Human Interface Guidelines da Apple.",
        "iOS com AIDD: agentes que conhecem SwiftUI e UIKit e geram views nativas que seguem as HIG da Apple — incluindo Dark Mode, Dynamic Type e VoiceOver.",
        "iOS development usa Swift e frameworks como SwiftUI (declarativo, moderno) e UIKit (imperativo, legado). No AIDD, o agente deve ser instruído sobre qual framework usar e as HIGs.\n\n**Prompt efetivo:** 'Gere uma tela de configurações em SwiftUI com List, NavigationStack, Toggle e Picker. Suporte Dynamic Type, Dark Mode e VoiceOver.'"
    ),
    "K4-mobile-android": (
        "Android e Kotlin com AIDD",
        "Android e Kotlin: Apps Nativas Google com Agentes de IA",
        "Jetpack Compose, Material Design 3, Coroutines — Android Nativo com Prompts",
        "Android é a plataforma mobile mais usada do mundo. Este livro ensina como agentes podem gerar apps Android nativas com Jetpack Compose, seguindo o Material Design 3.",
        "Android com AIDD: agentes que geram código Kotlin com Jetpack Compose, ViewModel, Room e Navigation — seguindo as recomendações oficiais do Android Architecture Guide.",
        "Android development moderno usa Kotlin e Jetpack Compose para UIs declarativas. No AIDD, agentes podem gerar componentes Android com ciclo de vida, injeção de dependência e navegação.\n\n**Prompt efetivo:** 'Crie uma tela de lista de tarefas em Jetpack Compose com LazyColumn, FloatingActionButton, SwipeToDismiss e navegação para tela de detalhes.'"
    ),
    "K5-mobile-multiplataforma": (
        "Estratégias Multiplataforma com AIDD",
        "Multiplataforma: React Native, Flutter e Kotlin Multiplatform com Agentes",
        "Code Sharing, Plataforma Target, Testes Cross-Platform — Decisões Estratégicas com Prompts",
        "Escolher entre React Native, Flutter e Kotlin Multiplatform é a decisão mais importante de um projeto mobile. Este livro compara as abordagens sob a ótica AIDD e ensina como agentes podem gerar código consistente em cada plataforma.",
        "Multiplataforma com AIDD: o mesmo prompt ('Tela de perfil com foto, nome e bio') gera implementações equivalentes em React Native, Flutter e Compose — cada uma otimizada para seu ecossistema.",
        "As três principais abordagens multiplataforma em 2026 são React Native (JavaScript/TypeScript), Flutter (Dart) e Kotlin Multiplatform (Kotlin compartilhado). No AIDD, a escolha impacta diretamente a produtividade dos agentes.\n\n**Comparação AIDD:** React Native tem o maior ecossistema de skills e MCPs. Flutter é mais previsível para geração de UI. KMP é melhor para compartilhar lógica de negócio entre plataformas."
    ),

    # ═══ SÉRIE L — CLOUD ═══
    "L1-cloud-aws": (
        "AWS com AIDD",
        "AWS: Cloud Computing com Agentes de IA",
        "EC2, Lambda, S3, RDS — Infraestrutura AWS Gerenciada por Prompts",
        "AWS é a cloud mais usada do mundo, com mais de 200 serviços. Este livro ensina como agentes de IA podem projetar arquiteturas AWS seguras, otimizadas e econômicas.",
        "AWS com AIDD: descreva a aplicação ('API REST serverless com autenticação, banco PostgreSQL e CDN global') e o agente gera o CloudFormation/Terraform completo com Well-Architected best practices.",
        "Amazon Web Services oferece centenas de serviços de cloud computing. No AIDD, agentes podem projetar arquiteturas completas seguindo o AWS Well-Architected Framework.\n\n**Prompt efetivo:** 'Projete uma arquitetura serverless com API Gateway + Lambda + DynamoDB + Cognito + CloudFront. Inclua WAF, KMS e CloudWatch. Gere o SAM template.'"
    ),
    "L2-cloud-azure": (
        "Azure com AIDD",
        "Azure: Cloud Microsoft com Agentes de IA",
        "Azure Functions, AKS, Cosmos DB, Entra ID — Infraestrutura Azure com Prompts",
        "Azure é a escolha natural para empresas Microsoft. Este livro ensina como agentes podem gerar arquiteturas Azure seguindo o Azure Well-Architected Framework.",
        "Azure com AIDD: agentes que conhecem o ecossistema Microsoft (Entra ID, Azure Functions, AKS, Cosmos DB) e geram infraestrutura integrada com Active Directory e Visual Studio.",
        "Microsoft Azure é a plataforma cloud com melhor integração com o ecossistema Microsoft. No AIDD, agentes podem gerar arquiteturas que aproveitam nativamente Entra ID, Azure DevOps e Power Platform.\n\n**Diferencial AIDD:** Azure tem o melhor suporte a ambientes híbridos (Azure Arc) e integração com GitHub Copilot para geração de infraestrutura."
    ),
    "L3-cloud-gcp": (
        "GCP com AIDD",
        "GCP: Cloud Google com Agentes de IA",
        "Cloud Run, GKE, BigQuery, Cloud Functions — Infraestrutura Google com Prompts",
        "Google Cloud Platform é líder em dados e machine learning. Este livro ensina como agentes podem gerar arquiteturas GCP otimizadas para dados, ML e containers.",
        "GCP com AIDD: agentes que conhecem o ecossistema Google (BigQuery, Vertex AI, Cloud Run, GKE) e geram infraestrutura que aproveita os diferenciais de dados e ML da Google.",
        "Google Cloud Platform se destaca em dados (BigQuery), ML (Vertex AI) e containers (GKE, Cloud Run). No AIDD, agentes podem gerar arquiteturas que aproveitam esses diferenciais.\n\n**Prompt AIDD:** 'Projete uma arquitetura de dados com Cloud Storage + Pub/Sub + Dataflow + BigQuery + Looker. Inclua IAM, VPC-SC e CMEK.'"
    ),
    "L4-cloud-serverless": (
        "Serverless com AIDD",
        "Serverless: Computação sem Servidor com Agentes de IA",
        "AWS Lambda, Cloud Functions, Cloud Run — Zero Servidor, Máxima Produtividade",
        "Serverless elimina a gestão de servidores. Este livro ensina como agentes podem gerar funções serverless, orquestrar workflows e gerenciar estado em arquiteturas event-driven.",
        "Serverless com AIDD: descreva o evento e a resposta ('Quando um arquivo chega no S3, processar e salvar no DynamoDB') e o agente gera a função Lambda completa com IAM, DLQ e observabilidade.",
        "Serverless computing executa código em resposta a eventos sem gerenciar servidores. No AIDD, agentes podem gerar funções serverless que são Stateless, efêmeras e escalam automaticamente.\n\n**Padrão AIDD serverless:** Evento → Função → Serviço Gerenciado. O agente gera: o handler, a configuração IAM (princípio do menor privilégio), a DLQ para falhas e o CloudWatch Alarm."
    ),
    "L5-cloud-multicloud": (
        "Estratégias Multi-Cloud com AIDD",
        "Multi-Cloud: AWS, Azure e GCP com Agentes de IA",
        "Cloud Agnóstico, Portabilidade, Disaster Recovery — Estratégias sem Vendor Lock-in",
        "Multi-cloud é a estratégia de usar múltiplos provedores para evitar dependência. Este livro ensina como agentes podem projetar arquiteturas portáveis entre clouds e estratégias de disaster recovery.",
        "Multi-cloud com AIDD: agentes que geram código Terraform que funciona em AWS, Azure e GCP com o mínimo de modificações — usando providers, módulos e padrões cloud-agnostic.",
        "Estratégia multi-cloud usa múltiplos provedores cloud para evitar vendor lock-in, otimizar custos e aumentar resiliência. No AIDD, agentes devem gerar infraestrutura portável.\n\n**Ferramentas cloud-agnostic:** Terraform, Kubernetes, Istio, e frameworks que abstraem o provedor. O agente deve preferir serviços gerenciados equivalentes e evitar APIs proprietárias."
    ),

    # ═══ SÉRIE M — PERFORMANCE ═══
    "M1-performance-web": (
        "Web Performance com AIDD",
        "Web Performance: Sites e Apps Rápidas com Agentes de IA",
        "Core Web Vitals, Lighthouse, CDN — Performance Frontend com Prompts",
        "Performance web impacta diretamente conversão e SEO. Este livro ensina como agentes podem gerar código otimizado para Core Web Vitals, o Google vai além da nota do Lighthouse.",
        "Web performance com AIDD: agentes que analisam o código e sugerem otimizações específicas — lazy loading, code splitting, compressão de imagens, caching estratégico — cada uma com justificativa de impacto.",
        "Web Performance otimiza o carregamento e a interatividade de sites e aplicações web. No AIDD, agentes podem analisar o código existente e sugerir otimizações baseadas nas métricas do Core Web Vitals.\n\n**Métricas Core Web Vitals:** LCP (Largest Contentful Paint) < 2.5s, FID (First Input Delay) < 100ms, CLS (Cumulative Layout Shift) < 0.1."
    ),
    "M2-performance-api": (
        "API Performance com AIDD",
        "API Performance: Rotas Rápidas e Eficientes com Agentes de IA",
        "Latência, Throughput, Caching, Rate Limiting — APIs Performáticas com Prompts",
        "APIs lentas matam produtos. Este livro ensina como agentes podem gerar APIs otimizadas para latência mínima e throughput máximo, com caching inteligente e rate limiting.",
        "API performance com AIDD: agentes que geram código de API com otimizações embutidas — connection pooling, query optimization, response compression, paginação cursor-based — sem necessidade de refatoração posterior.",
        "Performance de APIs é medida por latência (tempo de resposta), throughput (requests/segundo) e utilização de recursos. No AIDD, agentes devem gerar código com otimizações por construção.\n\n**Otimizações que agentes devem aplicar automaticamente:** Connection pooling, N+1 query prevention, paginação cursor-based, compressão gzip/brotli, caching com Redis/CDN, query optimization com EXPLAIN."
    ),
    "M3-performance-banco": (
        "Database Performance com AIDD",
        "Database Performance: Queries Rápidas e Índices Eficientes com Agentes",
        "Query Optimization, Indexação, Explain Plan — Banco de Dados Performático com Prompts",
        "Banco de dados lento derruba aplicações. Este livro ensina como agentes podem analisar queries, sugerir índices e otimizar schemas para performance máxima.",
        "Database performance com AIDD: mostre o schema e uma query lenta ao agente, e ele sugere índices, reescreve a query e recomenda mudanças no schema — tudo com justificativa baseada em EXPLAIN PLAN.",
        "Performance de banco de dados é sobre queries rápidas e uso eficiente de recursos. No AIDD, agentes podem analisar schemas e queries para identificar gargalos.\n\n**Análise que agentes fazem:** Identificar full table scans, sugerir índices compostos, reescrever subqueries como JOINs, identificar deadlocks e recomendar estratégias de sharding/particionamento."
    ),
    "M4-performance-mobile": (
        "Mobile Performance com AIDD",
        "Mobile Performance: Apps Leves e Responsivas com Agentes de IA",
        "APK Size, Frame Rate, Battery — Performance Mobile com Prompts",
        "Performance mobile é sobre bateria, memória e fluidez. Este livro ensina como agentes podem otimizar apps mobile para dispositivos de todos os níveis.",
        "Mobile performance com AIDD: agentes que analisam o código mobile e identificam problemas específicos: renderização lenta, vazamento de memória, consumo excessivo de bateria e network churn.",
        "Performance mobile envolve restrições únicas: bateria limitada, memória restrita, rede instável. No AIDD, agentes devem considerar esses fatores ao gerar código mobile.\n\n**Boas práticas que agentes devem seguir:** Lazy loading de imagens, paginação de listas, compressão de assets, minimização de wakes de rede, uso de workers para tarefas pesadas."
    ),
    "M5-performance-escala": (
        "Escala e Alta Disponibilidade com AIDD",
        "Escala e Alta Disponibilidade: Sistemas que não Param com Agentes",
        "Horizontal Scaling, Load Balancing, Chaos Engineering, SLA 99.99%",
        "Sistemas em escala falham de formas que sistemas pequenos não falham. Este livro ensina como agentes podem projetar sistemas que escalam horizontalmente e mantêm 99.99% de disponibilidade.",
        "Escala com AIDD: agentes que geram código com patterns de resiliência embutidos — circuit breaker, bulkhead, retry com backoff, timeout, fallback — cada um com configuração apropriada.",
        "Escala horizontal adiciona mais máquinas para aumentar capacidade. Alta disponibilidade garante que o sistema continue funcionando mesmo com falhas. No AIDD, agentes devem gerar código que suporta ambos.\n\n**Resilience patterns que agentes devem implementar:** Circuit Breaker (Hystrix/resilience4j), Bulkhead (thread pool isolation), Retry com exponential backoff, Timeout, Fallback, Rate Limiter."
    ),

    # ═══ SÉRIE N — CORPORATIVO ═══
    "N1-corporativo-microservicos": (
        "Microservices com AIDD",
        "Microservices: Arquiteturas Distribuídas com Agentes de IA",
        "Service Mesh, API Gateway, Observabilidade — Microsserviços Resilientes com Prompts",
        "Microservices são o padrão arquitetural dominante para sistemas corporativos. Este livro ensina como agentes podem projetar, implementar e orquestrar sistemas de microsserviços.",
        "Microservices com AIDD: descreva o domínio e os bounded contexts, e o agente gera a arquitetura completa — incluindo API Gateway, service mesh, comunicação síncrona/assíncrona e observabilidade.",
        "Arquitetura de microsserviços estrutura uma aplicação como um conjunto de serviços pequenos, independentes e fracamente acoplados. No AIDD, agentes podem gerar serviços completos a partir de descrições de domínio.\n\n**Prompt AIDD:** 'Projete o microsserviço de Catálogo de Produtos com API REST, eventos Kafka para sincronização de estoque, cache Redis, PostgreSQL e health checks.'"
    ),
    "N2-corporativo-eventos": (
        "Event-Driven Architecture com AIDD",
        "Event-Driven Architecture: Sistemas Reativos com Agentes de IA",
        "Kafka, RabbitMQ, Event Sourcing, CQRS — Arquitetura Orientada a Eventos com Prompts",
        "Arquitetura orientada a eventos é o padrão para sistemas reativos e escaláveis. Este livro ensina como agentes podem projetar sistemas event-driven com Kafka, Event Sourcing e CQRS.",
        "Event-Driven com AIDD: descreva o fluxo de eventos ('Quando um pedido é criado, enviar email, atualizar estoque, notificar logística') e o agente gera publishers, consumers e handlers.",
        "Event-Driven Architecture (EDA) é um padrão onde serviços se comunicam através de eventos assíncronos. No AIDD, agentes podem gerar a infraestrutura completa de eventos.\n\n**Componentes que agentes geram:** Event publishers, consumers, schemas de eventos (Avro/Protobuf), dead letter queues, retry policies, e dashboards de monitoramento de eventos."
    ),
    "N3-corporativo-legado": (
        "Modernização de Legado com AIDD",
        "Modernização de Legado: Transformando Sistemas Antigos com Agentes de IA",
        "Refatoração, Migração, Strangler Fig — Legado para Moderno com Prompts",
        "Sistemas legados são o maior passivo técnico das empresas. Este livro ensina como agentes podem analisar, documentar e transformar sistemas legados em arquiteturas modernas.",
        "Legado com AIDD: agentes que analisam código legado, geram documentação, identificam padrões, e propõem estratégias de migração — incluindo o Strangler Fig Pattern para migração incremental.",
        "Modernização de legado transforma sistemas antigos sem interromper operações. No AIDD, agentes podem acelerar cada fase do processo: análise, documentação, geração de testes e refatoração.\n\n**Estratégia Strangler Fig:** Agentes identificam funcionalidades independentes no legado, geram implementações modernas equivalentes, e roteiam tráfego gradualmente do antigo para o novo."
    ),
    "N4-corporativo-equipes": (
        "Gestão de Equipes AIDD",
        "Equipes AIDD: Liderança e Organização na Era dos Agentes",
        "Team Topologies, Squads, Produtividade — Times que Orquestram Agentes",
        "Equipes AIDD não são times de desenvolvedores tradicionais. Este livro ensina como estruturar, liderar e escalar equipes que usam agentes de IA como membros produtivos do time.",
        "Equipes AIDD com agentes como membros do time: cada agente é um 'funcionário' especializado, cada engenheiro um 'gerente' que coordena múltiplos agentes, e o tech lead projeta a estrutura organizacional de humanos + agentes.",
        "Equipes AIDD combinam humanos e agentes de IA em squads produtivas. Diferente de times tradicionais, cada engenheiro pode orquestrar múltiplos agentes, aumentando drasticamente a capacidade do time.\n\n**Estrutura recomendada:** 1 engenheiro sênior (orquestrador) + 3-5 agentes especializados + 1-2 juniores (aprendendo orquestração). O sênior projeta fluxos, os agentes executam, os juniores validam e aprendem."
    ),
    "N5-corporativo-governanca": (
        "Governança Corporativa AIDD",
        "Governança Corporativa: Estratégia e Controle na Era da IA",
        "ROI, SLA, Auditoria, Compliance — Gestão de Riscos com Agentes de IA",
        "Governança corporativa no AIDD não é sobre controlar humanos — é sobre controlar agentes. Este livro ensina como estabelecer políticas, métricas e auditorias para o uso de IA no desenvolvimento.",
        "Governança corporativa AIDD: políticas que definem o que agentes podem e não podem fazer, métricas que medem produtividade e qualidade do código gerado, e auditorias que garantem compliance.",
        "Governança corporativa no AIDD estabelece as regras, métricas e controles para o uso ético, seguro e produtivo de agentes de IA. Cada agente deve operar dentro de limites claros.\n\n**Políticas essenciais:** O que agentes podem acessar (MCPs, APIs, banco), o que não podem (produção, dados sensíveis sem aprovação), como são auditados (logs, sessões gravadas), e como são medidos (taxa de aceitação, tempo de entrega, qualidade do código gerado)."
    ),
}

# Auto-gerar lista completa de slugs e nomes
SLUGS_EXTRA = list(LIVROS_EXTRA.keys())

def get_partes_tema(serie):
    """Retorna o template de partes para uma série."""
    return [
        {"parte": 1, "titulo_parte": f"Fundamentos de {SERIES_INFO[serie]['nome']} com AIDD"},
        {"parte": 2, "titulo_parte": f"Técnicas de Utilização em {SERIES_INFO[serie]['nome']}"},
        {"parte": 3, "titulo_parte": f"Economia de Tokens em {SERIES_INFO[serie]['nome']}"},
        {"parte": 4, "titulo_parte": f"Configurações Avançadas de {SERIES_INFO[serie]['nome']}"},
    ]

def get_capitulos_por_parte(parte_num, tema_serie, tema_livro):
    """Gera títulos de capítulos para uma parte específica."""
    if parte_num == 1:
        return [
            {"capitulo": 1, "titulo": f"O que {tema_livro} Exige do Engenheiro AIDD", "subtitulo": f"Mentalidade, habilidades e ferramentas para {tema_livro.lower()}"},
            {"capitulo": 2, "titulo": f"Fundamentos de {tema_livro}", "subtitulo": f"Conceitos essenciais que todo engenheiro AIDD precisa dominar"},
            {"capitulo": 3, "titulo": f"Ferramentas e Ecossistema de {tema_livro}", "subtitulo": f"Principais tecnologias e plataformas para {tema_livro.lower()}"},
            {"capitulo": 4, "titulo": f"Primeiros Passos com {tema_livro} e Agentes", "subtitulo": f"Configurando o ambiente e gerando seu primeiro exemplo funcional"},
        ]
    elif parte_num == 2:
        return [
            {"capitulo": 5, "titulo": f"Prompt Engineering para {tema_livro}", "subtitulo": f"System prompts que geram código consistente de {tema_livro.lower()}"},
            {"capitulo": 6, "titulo": f"Padrões de Projeto em {tema_livro} com AIDD", "subtitulo": f"Design patterns específicos para {tema_livro.lower()} gerados por agentes"},
            {"capitulo": 7, "titulo": f"Testes e Validação em {tema_livro}", "subtitulo": f"Estratégias de teste para código gerado de {tema_livro.lower()}"},
            {"capitulo": 8, "titulo": f"Integração Contínua para {tema_livro}", "subtitulo": f"Pipelines CI/CD que validam e deployam {tema_livro.lower()} automaticamente"},
        ]
    elif parte_num == 3:
        return [
            {"capitulo": 9, "titulo": f"O Custo de Gerar {tema_livro} com Agentes", "subtitulo": f"Análise de tokens e custos específicos de {tema_livro.lower()}"},
            {"capitulo": 10, "titulo": f"Compressão de Contexto para {tema_livro}", "subtitulo": f"Estratégias para maximizar a janela de contexto em projetos de {tema_livro.lower()}"},
            {"capitulo": 11, "titulo": f"Cache e Reuso em {tema_livro}", "subtitulo": f"Mecanismos de cache para evitar regeneração desnecessária"},
            {"capitulo": 12, "titulo": f"Estratégias de Geração Incremental em {tema_livro}", "subtitulo": f"Construindo projetos complexos passo a passo sem estourar tokens"},
        ]
    else:  # parte_num == 4
        return [
            {"capitulo": 13, "titulo": f"Configurações Essenciais de {tema_livro}", "subtitulo": f"Parâmetros que ninguém explica mas fazem toda a diferença"},
            {"capitulo": 14, "titulo": f"Integração com MCPs e Skills para {tema_livro}", "subtitulo": f"Estendendo as capacidades dos agentes para {tema_livro.lower()}"},
            {"capitulo": 15, "titulo": f"Debug e Troubleshooting em {tema_livro}", "subtitulo": f"Diagnosticando e corrigindo problemas comuns em projetos de {tema_livro.lower()}"},
            {"capitulo": 16, "titulo": f"O Futuro de {tema_livro} com AIDD", "subtitulo": f"Tendências, inovações e o que esperar para os próximos anos"},
        ]
