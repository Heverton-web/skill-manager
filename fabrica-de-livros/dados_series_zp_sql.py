#!/usr/bin/env python3
"""
Dados da Serie ZP3 — SQL e Bancos de Dados: Do Zero ao Profissional (20 livros)
Jornada progressiva: Livro 1 = absoluto zero, Livro 20 = pronto para o mercado.
Cada livro tem 4 Partes e 16 Capitulos (EITA-V2).
Usado por gerar-livros-zp.py e compilar-para-pdf.py
"""

LIVROS_ZP_SQL = {
    # ═══════════ NIVEL 0-1: ZERO ABSOLUTO E MODELAGEM ═══════════
    "ZP3-01-fundamentos-de-bancos-de-dados": (
        "Fundamentos de Bancos de Dados",
        "Fundamentos de Bancos de Dados: Do Conceito de Tabela ao Primeiro Banco",
        "Do zero: o que é banco, tabelas, registros, chaves e o primeiro banco",
        "Bancos de dados são o coração de todo sistema — e o assunto mais procurado em qualquer carreira técnica. Este livro leva quem nunca trabalhou com dados do zero absoluto: o que é um banco, o que são tabelas, registros, chaves e como criar o primeiro banco relacional.",
        "Entender bancos de dados é entender como o mundo moderno armazena informação. O modelo relacional — tabelas com linhas e colunas — domina o mercado há décadas, e sua lógica é a base de tudo que vem depois: SQL, modelagem, otimização e análise.",
        "Um banco de dados relacional organiza dados em tabelas: linhas (registros) e colunas (campos) [1]. Cada tabela tem uma chave primária (identificador único) e pode referenciar outras por chaves estrangeiras, criando relações. O Sistema de Gerenciamento (SGBD) — como PostgreSQL, MySQL, SQL Server — gerencia armazenamento, consulta e concorrência [2].\n\n**Por que importa?** Planilhas não escalam: bancos garantem consistência, integridade e consultas em bilhões de registros. A lógica relacional aparece em todo sistema — do e-commerce ao banco financeiro — e é o pré-requisito para SQL.\n\n**O que muda na prática:** Instale o PostgreSQL (ou use o SQLite, embutido no Python), crie seu primeiro banco e uma tabela com chave primária. A prática com um banco real desde o início acelera tudo o que vem depois [3]."
    ),
    "ZP3-02-modelagem-relacional-e-diagrama-er": (
        "Modelagem Relacional e Diagrama Entidade-Relacionamento",
        "Modelagem Relacional: Diagrama ER, Cardinalidades e Normalização",
        "Entidades, relacionamentos, cardinalidades, chaves e modelagem conceitual",
        "Antes de escrever SQL, é preciso desenhar: a modelagem define a estrutura do banco — e erros aqui custam caro depois. Este livro ensina o diagrama Entidade-Relacionamento (ER), cardinalidades, chaves primárias e estrangeiras e a modelagem conceitual, lógica e física.",
        "Modelar bem é a diferença entre um banco que evolui e um que trava o projeto. O diagrama ER comunica a estrutura antes de qualquer código; as cardinalidades definem os relacionamentos; a normalização elimina redundância. É a habilidade que todo profissional de dados usa para projetar.",
        "O modelo ER representa entidades (coisas do domínio: Cliente, Pedido, Produto) e relacionamentos (um Cliente faz muitos Pedidos) [1]. Cardinalidades definem a multiplicidade: 1:1, 1:N, N:N. A chave primária identifica cada registro; a estrangeira liga tabelas. A modelagem avança do conceitual (entidades) ao lógico (tabelas e chaves) e ao físico (SQL DDL) [2].\n\n**Por que importa?** Um relacionamento N:N exige tabela de ligação; ignorar isso gera dados duplicados e inconsistentes. A normalização (eliminar redundância em 1FN, 2FN, 3FN) evita anomalias de inserção e atualização. Modelos ruins obrigam retrabalho de migração.\n\n**O que muda na prática:** Desenhe o diagrama ER no papel antes de criar tabelas: liste entidades, defina relações e cardinalidades e só então escreva o CREATE TABLE. Desenhar primeiro evita meses de retrabalho [3]."
    ),
    "ZP3-03-sql-essencial-select-where-order": (
        "SQL Essencial: SELECT, WHERE e ORDER BY",
        "SQL Essencial: Consultas Fundamentais, Filtros e Ordenação",
        "SELECT, FROM, WHERE, operadores, ORDER BY, LIMIT e primeiras consultas",
        "SQL é a linguagem universal dos dados — e SELECT é seu verbo principal. Este livro ensina as consultas fundamentais: SELECT, FROM, WHERE com operadores, ORDER BY, LIMIT e as boas práticas de leitura de dados que você usará em toda consulta da carreira.",
        "Quase toda pergunta sobre dados começa com um SELECT. Dominar filtros (WHERE), ordenação (ORDER BY) e limites (LIMIT) é o primeiro nível de fluência em SQL — a base sobre a qual JOINs, agregações e subconsultas serão construídos.",
        "A consulta fundamental é SELECT colunas FROM tabela [1]. WHERE filtra com operadores: =, <>, >, <, BETWEEN, IN, LIKE (padrões) e IS NULL. ORDER BY ordena (ASC/DESC); LIMIT limita o número de linhas. A ordem de execução lógica difere da ordem escrita: FROM → WHERE → SELECT → ORDER BY → LIMIT [2].\n\n**Por que importa?** Entender a ordem de execução explica comportamentos: não se usa alias do SELECT no WHERE. LIKE '%texto%' é caro em grandes tabelas (evita índice). Filtrar no banco (WHERE) é sempre melhor que filtrar na aplicação.\n\n**O que muda na prática:** Pratique em um banco real: selecione colunas específicas (evite SELECT *), filtre com WHERE preciso e ordene com ORDER BY. Consulte o plano de execução para ver o custo das suas queries [3]."
    ),
    "ZP3-04-joins-e-relacionamentos": (
        "JOINs e Relacionamentos entre Tabelas",
        "JOINs: INNER, LEFT, RIGHT, FULL e a Combinação de Tabelas Relacionadas",
        "INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, aliases e relações 1:N e N:N",
        "Dados vivem espalhados em tabelas — e os JOINs os reúnem. Este livro ensina a combinar tabelas relacionadas: INNER, LEFT, RIGHT e FULL JOIN, aliases, condições de junção e como navegar relações 1:N e N:N, a habilidade que liberta suas consultas.",
        "JOIN é onde o SQL se torna poderoso: uma consulta reúne cliente, pedidos e produtos em um único resultado. Dominar os tipos de JOIN e saber qual usar em cada situação é o divisor entre consultas triviais e análises reais de dados relacionais.",
        "JOIN combina linhas de duas tabelas por uma condição: SELECT c.nome, p.total FROM clientes c JOIN pedidos p ON p.cliente_id = c.id [1]. INNER retorna apenas combinações que casam; LEFT mantém todas as linhas da esquerda (com NULL à direita quando não há correspondência); RIGHT e FULL completam o espectro [2]. Relações N:N passam por tabela de ligação com dois JOINs.\n\n**Por que importa?** A escolha errada de JOIN perde dados silenciosamente: LEFT quando deveria ser INNER esconde pedidos sem cliente. Aliases (c, p) tornam consultas legíveis. JOINs mal indexados são a causa nº 1 de queries lentas.\n\n**O que muda na prática:** Desenhe o relacionamento antes de escrever o JOIN, escolha o tipo pela pergunta de negócio ('todos os clientes, mesmo sem pedidos' = LEFT) e verifique se as colunas de junção estão indexadas [3]."
    ),
    "ZP3-05-agregacao-group-by-e-funcoes": (
        "Agregação, GROUP BY e Funções SQL",
        "Agregação: GROUP BY, COUNT, SUM, AVG e as Funções que Resumem Dados",
        "COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING e funções de string/data",
        "Resumir milhões de linhas em um número é o poder analítico do SQL. Este livro ensina as funções de agregação (COUNT, SUM, AVG, MIN, MAX), o GROUP BY com HAVING e as funções de string e data que transformam dados brutos em relatórios.",
        "Agregação é o coração da análise de dados: total de vendas por mês, ticket médio por cliente, contagem por categoria. Dominar GROUP BY e HAVING — e as funções de string e data — permite responder às perguntas de negócio que movem decisões.",
        "Funções agregadas resumem grupos: COUNT(*), SUM(valor), AVG(valor), MIN, MAX [1]. GROUP BY agrupa linhas por coluna(s); HAVING filtra grupos (diferente de WHERE, que filtra linhas antes da agregação): SELECT mes, SUM(total) FROM vendas GROUP BY mes HAVING SUM(total) > 10000. Funções de string (CONCAT, SUBSTRING, UPPER) e data (DATE_TRUNC, EXTRACT) moldam valores [2].\n\n**Por que importa?** A confusão WHERE vs HAVING é o erro clássico: WHERE filtra antes, HAVING depois da agregação. Agregar no banco (em vez de trazer tudo para a aplicação) é ordens de magnitude mais eficiente. COUNT(DISTINCT) conta valores únicos.\n\n**O que muda na prática:** Para cada pergunta analítica, escreva: o que agrupar (GROUP BY), o que medir (função agregada) e como filtrar o resultado (WHERE antes, HAVING depois). Esse é o padrão de todo relatório SQL [3]."
    ),
    "ZP3-06-subqueries-e-ctes": (
        "Subqueries e CTEs: Consultas Avançadas",
        "Subqueries e CTEs: Consultas Aninhadas, Comuns e a Legibilidade do SQL Moderno",
        "Subqueries, IN/EXISTS, CTEs, WITH, recursão e refatoração de queries",
        "Consultas que consultam consultas: as subqueries e as Common Table Expressions (CTEs) resolvem problemas que um único SELECT não alcança. Este livro ensina subqueries correlacionadas, IN/EXISTS, CTEs com WITH e a recursão — o nível de consulta que profissionais usam no dia a dia.",
        "CTEs transformaram a escrita de SQL complexo: em vez de uma consulta gigante ilegível, você escreve etapas nomeadas e legíveis. Subqueries resolvem comparações com agregados e filtros de existência. Dominar ambas é o que separa consultas funcionais de consultas elegantes.",
        "Uma subquery é uma consulta dentro de outra: SELECT nome FROM clientes WHERE id IN (SELECT cliente_id FROM pedidos) [1]. EXISTS testa existência de forma eficiente. CTEs nomeiam consultas intermediárias: WITH top_clientes AS (SELECT ... ) SELECT * FROM top_clientes. A recursão (WITH RECURSIVE) percorre hierarquias (organogramas, categorias) [2].\n\n**Por que importa?** CTEs melhoram a legibilidade e são o padrão moderno de escrita (também em bancos analíticos como BigQuery). EXISTS costuma ser mais eficiente que IN em subqueries grandes. Subqueries correlacionadas executam por linha — cuidado com performance.\n\n**O que muda na prática:** Escreva consultas complexas em etapas com CTEs, teste cada etapa isoladamente e prefira EXISTS para testar existência. Queries legíveis são revisáveis e mantíveis [3]."
    ),
    # ═══════════ NIVEL 2: OTIMIZAÇÃO E TRANSAÇÕES ═══════════
    "ZP3-07-indices-e-otimizacao-de-performance": (
        "Índices e Otimização de Performance",
        "Índices e Performance: EXPLAIN, Planos de Execução e Queries Rápidas",
        "Índices, B-tree, EXPLAIN, plano de execução, indexação e tuning",
        "A mesma consulta pode levar milissegundos ou minutos — a diferença chama-se índice. Este livro ensina otimização de performance: como funcionam os índices (B-tree), como ler o plano de execução com EXPLAIN e como indexar para acelerar consultas reais.",
        "Performance é a habilidade que separa o analista do especialista. Índices bem escolhidos tornam consultas instantâneas; consultas mal escritas derrubam sistemas. Ler um plano de execução é a competência mais valorizada em vagas de banco de dados — e a mais rara.",
        "Um índice é uma estrutura (tipicamente B-tree) que acelera buscas por colunas específicas: CREATE INDEX idx_clientes_email ON clientes(email) [1]. O otimizador escolhe se usa o índice; o EXPLAIN ANALYZE mostra o plano de execução real, incluindo scans (Seq Scan vs Index Scan) e estimativas de custo [2].\n\n**Por que importa?** Sem índice, uma busca em 10 milhões de linhas varre tudo (Seq Scan). Com índice B-tree, a busca é logarítmica — segundos viram milissegundos. Cuidado: índices aceleram leitura mas custam escrita e espaço. Indexar demais ou pouco é um equilíbrio que se aprende lendo o EXPLAIN.\n\n**O que muda na prática:** Antes de otimizar, rode EXPLAIN ANALYZE e identifique o Scan mais caro; indexe as colunas dos WHERE e JOIN mais frequentes; e meça o antes/depois. Decisão de índice é decisão baseada em evidência [3]."
    ),
    "ZP3-08-transacoes-acid-e-concorrencia": (
        "Transações, ACID e Controle de Concorrência",
        "Transações: ACID, Commit, Rollback, Isolation e a Integridade dos Dados",
        "Transações, ACID, commit/rollback, níveis de isolamento, locks e concorrência",
        "Bancos de dados precisam sobreviver a falhas e concorrência: é o papel das transações. Este livro ensina o modelo ACID (Atomicidade, Consistência, Isolamento, Durabilidade), COMMIT/ROLLBACK, os níveis de isolamento e o controle de concorrência — a teoria que protege os dados de sistemas reais.",
        "Transações são o que torna bancos confiáveis: uma transferência bancária não pode deixar o dinheiro pela metade. Entender ACID, isolamento e concorrência é o que permite construir sistemas corretos sob falhas e múltiplos usuários — o coração da engenharia de dados profissional.",
        "Uma transação agrupa operações que devem ser atômicas: BEGIN; UPDATE ...; COMMIT (ou ROLLBACK em erro) [1]. ACID garante: Atomicidade (tudo ou nada), Consistência (estado válido), Isolamento (transações não interferem) e Durabilidade (dados persistem após falha). Níveis de isolamento (Read Committed, Repeatable Read, Serializable) equilibram consistência e performance; locks e MVCC gerenciam a concorrência [2].\n\n**Por que importa?** Sem isolamento adequado, surgem leituras sujas, leituras não repetíveis e fantasma. Deadlocks ocorrem quando transações competem na ordem errada. Aplicações reais precisam escolher o nível de isolamento certo e tratar conflitos de concorrência.\n\n**O que muda na prática:** Use transações para operações multi-passos, defina o nível de isolamento pela necessidade do negócio e trate deadlocks com retry. Integridade de dados é responsabilidade de quem escreve as transações [3]."
    ),
    "ZP3-09-views-e-stored-procedures": (
        "Views, Stored Procedures e Functions",
        "Views, Procedures e Functions: Lógica de Banco Reutilizável e Segura",
        "Views, materialized views, stored procedures, functions e triggers",
        "A lógica de dados pode — e deve — viver no banco. Este livro ensina views (consultas nomeadas), materialized views, stored procedures, functions e triggers: como encapsular lógica no banco para reuso, segurança e performance.",
        "Views simplificam consultas complexas em 'tabelas virtuais'; procedures encapsulam lógica transacional; functions retornam valores; triggers reagem automaticamente a eventos. Colocar lógica no banco certo — nem sempre, mas quando faz sentido — é uma decisão de arquitetura profissional.",
        "Uma view é uma consulta nomeada: CREATE VIEW v_vendas_por_mes AS SELECT ... — usada como tabela [1]. Materialized views armazenam o resultado (mais rápidas, precisam refresh). Stored procedures encapsulam fluxos: CREATE PROCEDURE ... com BEGIN/COMMIT. Functions retornam valores (escalares ou tabelas). Triggers disparam em INSERT/UPDATE/DELETE [2].\n\n**Por que importa?** Views escondem complexidade e garantem consistência de consultas repetidas. Procedures centralizam regras transacionais no banco, usadas por várias aplicações. Triggers garantem auditoria automática. Materialized views aceleram relatórios pesados.\n\n**O que muda na prática:** Comece com views para consultas frequentes, evolua para functions (mais testáveis que procedures) e use triggers apenas para auditoria e regras críticas. Lógica de dados bem colocada reduz código na aplicação [3]."
    ),
    "ZP3-10-normalizacao-e-design-de-esquemas": (
        "Normalização e Design de Esquemas",
        "Normalização: 1FN, 2FN, 3FN e o Design de Esquemas que Escalam",
        "Formas normais, denormalização, integridade referencial e design de esquemas",
        "Um bom esquema nasce da normalização — e evolui com a denormalização consciente. Este livro ensina as formas normais (1FN, 2FN, 3FN), integridade referencial, constraints e o design de esquemas que equilibram consistência e performance para sistemas reais.",
        "O design de esquemas é a decisão de arquitetura mais difícil e mais permanente do banco: mudar um esquema mal feito exige migrações dolorosas. Normalizar elimina redundância e anomalias; denormalizar (com intenção) acelera leituras. Este livro forma o julgamento por trás das duas.",
        "Normalização elimina redundância em estágios: 1FN (valores atômicos), 2FN (dependência total da chave), 3FN (sem dependência transitiva) [1]. Constraints garantem integridade: PRIMARY KEY, FOREIGN KEY (com ON DELETE), UNIQUE, CHECK. A denormalização — duplicar dados de propósito para performance — é aplicada conscientemente em relatórios e leituras frequentes [2].\n\n**Por que importa?** Redundância gera anomalias: atualizar o preço do produto em 50 pedidos duplicados é um bug esperando acontecer. Integridade referencial no banco (FOREIGN KEY) é a última linha de defesa contra dados órfãos. O equilíbrio normalizar/denormalizar é decisão de especialista.\n\n**O que muda na prática:** Normalize até 3FN por padrão, documente qualquer denormalização com o motivo, e use constraints para proteger a integridade no banco — nunca só na aplicação [3]."
    ),
    # ═══════════ NIVEL 3: BANCOS NA PRÁTICA E NoSQL ═══════════
    "ZP3-11-postgresql-na-pratica": (
        "PostgreSQL na Prática",
        "PostgreSQL: Instalação, Configuração, Tipos, JSONB e Recursos Avançados",
        "Instalação, psql, tipos, JSONB, full-text search, extensões e administração",
        "PostgreSQL é o banco relacional open source mais avançado do mundo — e o mais procurado no mercado. Este livro ensina o PostgreSQL na prática: instalação, psql, tipos de dados, JSONB (híbrido relacional/NoSQL), full-text search e as extensões que o tornam uma plataforma completa.",
        "Dominar PostgreSQL é dominar o banco mais valorizado do mercado de dados. JSONB permite documentos dentro do relacional; full-text search busca texto nativamente; extensões (PostGIS, pgvector) expandem o banco para geoespacial e IA. É o banco que cresce com a carreira.",
        "O PostgreSQL é instalado com o serviço rodando e acessado via psql (terminal) ou clientes gráficos [1]. Tipos ricos: numéricos, texto, datas, arrays, JSONB (binário otimizado para JSON), UUID, enum. JSONB permite consultar documentos: data->>'campo' e índices GIN para busca. Full-text search: to_tsvector + to_tsquery. Extensões: CREATE EXTENSION pgvector (embeddings para IA), PostGIS (geoespacial) [2].\n\n**Por que importa?** O PostgreSQL combina o relacional robusto com capacidades NoSQL (JSONB) e de IA (pgvector) — uma plataforma única para aplicações modernas. Sua fama de confiabilidade e recursos justifica sua liderança em bancos open source.\n\n**O que muda na prática:** Instale, pratique o psql, explore JSONB para dados semi-estruturados e full-text search para busca. Cada recurso dominado amplia o tipo de aplicação que você consegue construir [3]."
    ),
    "ZP3-12-mysql-e-mariadb-na-pratica": (
        "MySQL e MariaDB na Prática",
        "MySQL e MariaDB: O Banco Open Source Mais Usado do Mundo em Produção",
        "Instalação, engine InnoDB, usuários, backups, replication e tuning",
        "MySQL é o banco mais usado do mundo — o coração da web (WordPress, e-commerce, startups). Este livro ensina MySQL e MariaDB na prática: instalação, a engine InnoDB, gestão de usuários e permissões, backups, replicação e o tuning básico de produção.",
        "O MySQL domina a web: a maioria dos sites e aplicações de pequeno e médio porte roda sobre ele. Dominar InnoDB, usuários, backups e replicação é o conhecimento prático que sustenta sistemas em produção — e uma das habilidades mais pedidas em vagas de backend e DBA.",
        "MySQL (e seu fork MariaDB) oferecem engines: InnoDB é o padrão — transacional, com ACID e foreign keys [1]. Usuários e permissões: CREATE USER, GRANT com privilégios granulares. Backups: mysqldump para lógico, snapshots para físico. Replicação: um master replica para slaves (leitura). Tuning: configurações de buffer pool e cache [2].\n\n**Por que importa?** A escolha entre MySQL e PostgreSQL depende do contexto: MySQL brilha em leitura pesada e simplicidade de operação; a web tradicional roda nele. InnoDB é obrigatório para transações. Backups testados são a diferença entre um susto e uma tragédia.\n\n**O que muda na prática:** Instale, crie usuários com privilégios mínimos, agende backups testados e pratique a replicação em um ambiente local. Operar o banco em produção é uma habilidade que diferencia o perfil [3]."
    ),
    "ZP3-13-nosql-mongodb-e-documentos": (
        "NoSQL: MongoDB e Modelos de Documentos",
        "MongoDB: Documentos JSON, Coleções, Agregações e Escala Horizontal",
        "Documentos, coleções, agregações, índices, sharding e quando usar NoSQL",
        "Nem todo dado é relacional: o NoSQL resolve escalabilidade e flexibilidade de esquema. Este livro ensina o MongoDB — o banco de documentos mais popular — na prática: documentos JSON, coleções, o pipeline de agregação, índices, sharding e, principalmente, quando escolher NoSQL em vez de SQL.",
        "O MongoDB domina o cenário NoSQL e é usado por empresas de todos os tamanhos. Sua flexibilidade de esquema acelera o desenvolvimento, e o pipeline de agregação analisa documentos com poder comparável ao SQL. Saber quando usá-lo — e quando não — é o julgamento profissional que este livro forma.",
        "O MongoDB armazena documentos BSON (JSON binário) em coleções — sem esquema fixo [1]. O pipeline de agregação processa documentos por estágios: $match, $group, $project, $sort — o equivalente analítico do SQL. Índices (incluindo text e geográficos) aceleram consultas. O sharding distribui dados em vários servidores para escala horizontal [2].\n\n**Por que importa?** Documentos modelam bem dados aninhados (pedido com itens) sem JOINs. A flexibilidade de esquema acelera mudanças — mas exige disciplina para não virar caos. A consistência eventual e a ausência de transações multi-documento (parcial) são trade-offs reais que exigem escolha consciente.\n\n**O que muda na prática:** Escolha MongoDB quando os dados são naturalmente documentais (catálogos, perfis, logs) e a escala horizontal importa. Modele o documento pelo padrão de leitura e use agregações para relatórios [3]."
    ),
    "ZP3-14-redis-cache-e-estruturas-de-dados": (
        "Redis: Cache e Estruturas de Dados em Memória",
        "Redis: Cache, Filas, Sessões e Estruturas de Dados em Memória",
        "Strings, hashes, listas, pub/sub, TTL, cache-aside e persistência",
        "Velocidade em produção vem do cache — e Redis é o cache padrão da indústria. Este livro ensina o Redis na prática: estruturas de dados em memória (strings, hashes, listas, sets), TTL, padrões de cache (cache-aside), filas, pub/sub, sessões e persistência.",
        "Redis roda em memória e responde em microssegundos — o que o torna o cache e a fila padrão de aplicações modernas. Dominar suas estruturas e padrões (cache-aside, filas, rate limiting) é uma habilidade prática de altíssima demanda em backend e sistemas de alta performance.",
        "Redis é um armazenamento de chave-valor em memória com estruturas ricas: strings, hashes (objetos), lists (filas), sets (unicidade), sorted sets (rankings) [1]. TTL expira chaves automaticamente. O padrão cache-aside: verifica o cache, se não há, busca no banco e popula o cache. Pub/sub conecta publicadores e assinantes. Persistência opcional (RDB/AOF) sobrevive a reinícios [2].\n\n**Por que importa?** O cache reduz a carga no banco de ordens de magnitude — as leituras mais quentes saem da memória. Filas Redis desacoplam tarefas (e-mail, jobs). Rate limiting com INCR + TTL protege APIs. Session store compartilha sessões entre servidores.\n\n**O que muda na prática:** Implemente cache-aside com TTL consciente (invalidação é o desafio real), use lists como filas com BRPOP e sorted sets para rankings. Cache bem projetado é a diferença entre uma API rápida e uma lenta [3]."
    ),
    # ═══════════ NIVEL 4: ANALÍTICA E BIG DATA ═══════════
    "ZP3-15-data-warehouse-e-modelagem-dimensional": (
        "Data Warehouse e Modelagem Dimensional",
        "Data Warehouse: Star Schema, Fato e Dimensão para Análise de Negócio",
        "Star schema, fatos, dimensões, OLTP vs OLAP e modelagem dimensional",
        "Dados analíticos pedem uma modelagem própria: a dimensional. Este livro ensina o Data Warehouse — star schema, tabelas fato e dimensão, OLTP vs OLAP e a modelagem dimensional — a base de todo BI e analytics que as empresas usam para decidir.",
        "O Data Warehouse é onde a análise vive: dados consolidados de várias fontes, modelados para perguntas de negócio. A modelagem dimensional (fatos + dimensões) é a técnica consagrada — e dominá-la abre portas em BI, analytics e engenharia de dados.",
        "OLTP (transacional) otimiza escrita e operação; OLAP (analítico) otimiza leitura e agregação — o Data Warehouse é OLAP [1]. O star schema centraliza fatos (medidas: vendas, valor) cercados por dimensões (contexto: tempo, cliente, produto). O modelo dimensional responde 'quanto vendeu por região e mês' com rapidez [2].\n\n**Por que importa?** Modelar para análise é diferente de modelar para operação: dimensões desnormalizadas e fatos agregáveis. O star schema é a base de ferramentas de BI (Power BI, Tableau, Looker). Consultas analíticas em bilhões de linhas dependem desse design.\n\n**O que muda na prática:** Identifique as medidas (fatos) e os contextos (dimensões) de um negócio, desenhe o star schema e carregue dados com ETL. O pensamento dimensional é a base de qualquer carreira em dados analíticos [3]."
    ),
    "ZP3-16-etl-e-pipelines-de-dados": (
        "ETL e Pipelines de Dados",
        "ETL e Pipelines: Extração, Transformação e Carga com Python e SQL",
        "ETL, ELT, extração, transformação, carga, dbt e orquestração",
        "Dados brutos viram insights através de pipelines. Este livro ensina ETL/ELT na prática: extração de fontes, transformação com SQL/Python, carga em Data Warehouse e orquestração — os fluxos que sustentam toda a área de dados das empresas.",
        "O pipeline é o sistema circulatório da área de dados: sem ele, não há análise nem BI. Dominar ETL/ELT — extrair, transformar, carregar — com ferramentas modernas (dbt, Airflow) é a competência central do engenheiro de dados, um dos cargos mais demandados do mercado.",
        "ETL clássico: extrai, transforma fora do destino e carrega [1]. ELT moderno: carrega bruto e transforma no destino (ex.: no próprio Data Warehouse), aproveitando a potência do banco. dbt transforma com SQL versionado em modelos testáveis. Orquestração (Apache Airflow, Prefect) agenda e gerencia dependências dos pipelines com retries e monitoramento [2].\n\n**Por que importa?** Pipelines precisam ser idempotentes (re-executáveis sem duplicar dados), monitorados e versionados. A qualidade dos dados depende das transformações — e da documentação delas. Falhas de pipeline precisam alertar e se recuperar automaticamente.\n\n**O que muda na prática:** Construa um pipeline simples: extraia de uma fonte, transforme com SQL/Python e carregue no destino; depois agende com orquestração e adicione alertas. O ciclo completo é a rotina do engenheiro de dados [3]."
    ),
    "ZP3-17-sql-para-analise-de-dados": (
        "SQL para Análise de Dados",
        "SQL Analítico: Window Functions, Rankings e Análises Avançadas",
        "Window functions, ROW_NUMBER, RANK, LAG/LEAD, e análise temporal",
        "O SQL analítico vai além das agregações: window functions calculam tendências, rankings e comparações sem perder o detalhe. Este livro ensina as funções de janela (ROW_NUMBER, RANK, LAG, LEAD, SUM OVER), as análises temporais e os padrões que analistas usam todos os dias.",
        "Window functions são a ferramenta analítica mais poderosa do SQL — e a mais mal compreendida. Elas calculam métricas por partição preservando as linhas: ranking de vendas por vendedor, crescimento mês a mês, média móvel. Dominá-las é o que separa consultas básicas de análises profissionais.",
        "Window functions executam sobre uma 'janela' definida pelo OVER: SELECT ..., RANK() OVER (PARTITION BY regiao ORDER BY total DESC) [1]. ROW_NUMBER numera, RANK/DENSE_RANK classificam, LAG/LEAD acessam linhas anteriores/posteriores (crescimento mês a mês: total - LAG(total) OVER (ORDER BY mes)), e SUM/AVG OVER calculam acumulados e médias móveis [2].\n\n**Por que importa?** Análises de tendência, rankings e comparações temporais — as perguntas mais comuns de negócio — exigem window functions. Sem elas, o analista recorre a self-joins complicados e lentos. São também tema recorrente em entrevistas de dados.\n\n**O que muda na prática:** Para cada pergunta 'por grupo e em ordem', identifique a janela (PARTITION BY) e a ordenação (ORDER BY). Pratique com dados de vendas: top 10 por região, crescimento mensal, média móvel de 3 meses [3]."
    ),
    "ZP3-18-big-data-data-lakes-e-spark": (
        "Big Data, Data Lakes e Spark",
        "Big Data: Data Lakes, Spark e o Processamento Distribuído em Escala",
        "Data lake, Hadoop, Spark, DataFrames, particionamento e processamento distribuído",
        "Quando os dados ultrapassam uma máquina, entra o processamento distribuído. Este livro introduz o Big Data: data lakes, o ecossistema Hadoop, Apache Spark com DataFrames, particionamento e os conceitos de processamento distribuído que sustentam a engenharia de dados moderna.",
        "O volume de dados das empresas cresceu além dos bancos tradicionais — e o processamento distribuído (Spark) é a resposta. Entender data lakes, particionamento e DataFrames em escala é o conhecimento que abre portas para a engenharia de dados e o data engineering moderno.",
        "Um data lake armazena dados brutos em qualquer formato (Parquet, JSON, CSV) em armazenamento barato (S3, HDFS) [1]. Apache Spark processa dados em cluster com DataFrames distribuídos: spark.read.parquet(...), filter, groupBy — a mesma API de dados, em escala. Particionamento organiza arquivos por chave (data, região) para leituras seletivas. O formato Parquet é colunar e comprimido, ideal para análise [2].\n\n**Por que importa?** O data lake é o coração da arquitetura de dados moderna (lakehouse), alimentando warehouses e analytics. Spark processa terabytes em minutos distribuindo o trabalho. Entender particionamento e formato colunar é essencial para performance em escala.\n\n**O que muda na prática:** Pratique com PySpark em dados locais: leia, transforme com DataFrames e escreva em Parquet particionado por data. Os conceitos se transferem diretamente para plataformas de nuvem [3]."
    ),
    # ═══════════ NIVEL 5: PROJETO E CARREIRA ═══════════
    "ZP3-19-projeto-completo-de-banco-de-dados": (
        "Projeto Completo de Banco de Dados",
        "Projeto Profissional: Um Banco de Dados Completo — do ER ao Data Warehouse",
        "Modelagem, schema, queries, índices, relatórios e documentação",
        "Este é o projeto final: construir um banco de dados completo e profissional — da modelagem Entidade-Relacionamento ao schema físico, das queries analíticas aos índices e relatórios. Cada etapa é executada com o rigor que empresas esperam de um profissional de dados.",
        "Um projeto completo de banco demonstra todo o ciclo: modelar, criar, consultar, otimizar e documentar. É o portfólio que prova domínio de modelagem, SQL, performance e análise — as quatro competências centrais de qualquer cargo de dados. Você está pronto para mostrar o que construiu.",
        "O projeto segue o ciclo profissional: 1) modelagem conceitual (diagrama ER com entidades, relações e cardinalidades) [1]; 2) schema físico com constraints, chaves e índices; 3) carga de dados realista; 4) queries analíticas com JOINs, agregações e window functions; 5) otimização com EXPLAIN e índices; 6) relatórios e documentação do design [2].\n\n**Por que importa?** Um banco bem modelado e documentado é um ativo: o time inteiro o usa. O portfólio de banco de dados — com schema versionado (migrações) e queries documentadas — é o que recrutadores de dados avaliam. A modelagem correta economiza anos de retrabalho.\n\n**O que muda na prática:** Escolha um domínio real (e-commerce, biblioteca, clínica), execute as 6 etapas e publique com documentação (README com diagrama ER e exemplos de queries). Esse projeto vira a vitrine da sua carreira em dados [3]."
    ),
    "ZP3-20-carreira-em-dados-dba-analista-engenheiro": (
        "Carreira em Dados: Analista, DBA e Engenheiro de Dados",
        "Carreira em Dados: Trilhas, Entrevistas, Portfólio e o Mercado de SQL",
        "Trilhas de carreira, entrevistas técnicas, portfólio, CV e certificações",
        "Você domina SQL e bancos — agora escolha a trilha: analista de dados, DBA, engenheiro de dados ou especialista em BI. Este livro prepara você para o mercado: as trilhas com suas ferramentas, a preparação para entrevistas técnicas, o portfólio e o caminho do primeiro emprego em dados.",
        "O mercado de dados tem trilhas claras e bem pagas — e SQL é o requisito comum de todas elas. Escolher a trilha certa, preparar-se para entrevistas e montar um portfólio que demonstra domínio prático transforma conhecimento em carreira. Você está pronto para o mercado de dados.",
        "As trilhas: analista de dados (SQL, Excel, BI, storytelling), DBA (operação, performance, backup, alta disponibilidade), engenheiro de dados (ETL, pipelines, Spark, cloud) e especialista BI (modelagem dimensional, dashboards) [1]. Entrevistas avaliam: SQL prático (JOINs, agregações, window functions), modelagem (ER, normalização) e cenários de performance. Portfólio: projetos completos com schema, queries documentadas e análises [2].\n\n**Por que importa?** Cada trilha tem stack e expectativas próprias — escolher cedo foca o estudo. O mercado de dados cresce mais que a oferta de profissionais. Certificações (SQL, cloud) complementam, mas o portfólio prático pesa mais na contratação.\n\n**O que muda na prática:** Escolha a trilha, monte 2-3 projetos completos (banco modelado + queries + análise), pratique SQL em entrevistas simuladas e construa um CV orientado a resultados. O mercado de dados está entre os mais aquecidos — e você está pronto [3]."
    ),
}
