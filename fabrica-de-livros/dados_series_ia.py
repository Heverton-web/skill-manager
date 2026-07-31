#!/usr/bin/env python3
"""
Dados das 5 Séries de Livros de IA e Agentes Fullstack (IA1-IA5)
Cada série tem 10 livros, cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-ia.py e compilar-para-pdf.py
"""

SERIES_IA = {
    "IA1": {"nome": "Fundamentos e Arquitetura de Agentes de IA", "prefixo": "IA1"},
    "IA2": {"nome": "Ecossistema Fullstack Integrado a LLMs", "prefixo": "IA2"},
    "IA3": {"nome": "Engenharia de Software Guiada por Agentes", "prefixo": "IA3"},
    "IA4": {"nome": "Automação de Fluxos, Low-Code e DevOps com IA", "prefixo": "IA4"},
    "IA5": {"nome": "Projetos Práticos e O Futuro da Profissão", "prefixo": "IA5"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
SERIES_PARTES = {
    "IA1": ["Fundamentos de Agentes de IA", "Arquitetura e Memória", "Padrões e Protocolos", "Segurança e Operação"],
    "IA2": ["Integração com LLMs", "Dados Vetoriais e RAG", "Interface e Comunicação em Tempo Real", "Orquestração e Escala"],
    "IA3": ["Ambientes Agênticos", "Geração de Código", "Qualidade e Testes", "Segurança e Manutenção"],
    "IA4": ["Automação de Fluxos", "DevOps e Infraestrutura", "Dados e Integrações", "Observabilidade e Conteúdo"],
    "IA5": ["Projetos Práticos Fullstack", "Produtos com Agentes", "Carreira e Transformação", "Ética e Futuro"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_IA = {
    # ═══════════════ SÉRIE IA1 — FUNDAMENTOS E ARQUITETURA DE AGENTES DE IA ═══════════════
    "IA1-01-anatomia-de-um-agente-de-ia": (
        "Anatomia de um Agente de IA",
        "Anatomia de um Agente de IA: O ciclo de percepção, raciocínio, planejamento e ação em sistemas de software",
        "O ciclo de percepção, raciocínio, planejamento e ação em sistemas de software",
        "Um agente de IA não é apenas um chatbot: é um sistema que percebe o ambiente, raciocina sobre ele, planeja ações e as executa — em um ciclo contínuo. Este livro disseca essa anatomia camada por camada e mostra como construir agentes de software que resolvem problemas reais.",
        "Compreender a anatomia de um agente — percepção, raciocínio, planejamento e ação — é a base de tudo que vem depois: memória, ferramentas, segurança e orquestração. Dominar esse ciclo é o que separa demos de sistemas em produção.",
        "Um agente de IA é um sistema que interage com um ambiente por meio de um ciclo: percepção (observar o estado), raciocínio (interpretar com o modelo de linguagem), planejamento (decidir os próximos passos) e ação (executar, usando ferramentas quando necessário) [1]. Cada etapa alimenta a seguinte, e o ciclo se repete até o objetivo ser alcançado [2].\n\n**Por que importa?** Agentes sem ciclo claro são apenas chamadas avulsas ao LLM. O ciclo percepção-raciocínio-planejamento-ação é o que dá autonomia, contexto e propósito ao sistema — e é o padrão por trás dos frameworks modernos de orquestração.\n\n**O que muda na prática:** Modele seu agente com estados explícitos do ciclo, registre cada etapa para depuração e defina critérios de parada claros para evitar loops infinitos [3]."
    ),
    "IA1-02-modelos-de-linguagem-como-nucleo": (
        "Modelos de Linguagem como Núcleo Computacional",
        "Modelos de Linguagem como Núcleo Computacional: Compreendendo tokens, janelas de contexto, temperatura e alucinações",
        "Compreendendo tokens, janelas de contexto, temperatura e alucinações",
        "Os LLMs são o núcleo computacional dos agentes — e entendê-los por dentro é essencial. Tokens, janelas de contexto, temperatura, sampling e alucinações determinam o comportamento de qualquer sistema agêntico. Este livro explica esses mecanismos com precisão técnica.",
        "O LLM não é uma caixa mágica: é um modelo estatístico com limites, custos e comportamentos previsíveis. Dominar tokens, contexto, temperatura e alucinações permite projetar agentes que extraem o máximo do modelo sem cair nas armadilhas clássicas.",
        "LLMs processam texto em tokens (unidades sublexicais), com janelas de contexto que limitam o que o modelo pode considerar por chamada [1]. A temperatura controla a aleatoriedade do sampling: baixa para tarefas determinísticas, alta para criatividade. Alucinações são gerações plausíveis mas incorretas, mais prováveis em domínios pouco cobertos [2].\n\n**Por que importa?** O custo e a latência escalam com o número de tokens; a janela de contexto define o orçamento de informações por chamada; e a alucinação é o risco central de qualquer sistema em produção.\n\n**O que muda na prática:** Meça tokens por requisição, gerencie o contexto com sumarização e retrieval, ajuste a temperatura por tarefa e valide saídas críticas antes de agir [3]."
    ),
    "IA1-03-engenharia-de-prompts-estruturada": (
        "Engenharia de Prompts Estruturada para Sistemas",
        "Engenharia de Prompts Estruturada para Sistemas: Técnicas avançadas (Chain-of-Thought, ReAct, Tree-of-Thoughts) aplicadas a código",
        "Técnicas avançadas (Chain-of-Thought, ReAct, Tree-of-Thoughts) aplicadas a código",
        "Prompt engineering em sistemas não é escrever frases bonitas: é projetar protocolos de instrução com técnicas estruturadas. Chain-of-Thought, ReAct e Tree-of-Thoughts são as ferramentas avançadas. Este livro ensina a aplicá-las em sistemas de código reais, com avaliação e versionamento.",
        "A engenharia de prompts estruturada é a disciplina que transforma a capacidade bruta do LLM em comportamento confiável de sistema. Técnicas de raciocínio, formatos de saída rígidos e avaliação contínua compõem o método que separa protótipos de produtos.",
        "Chain-of-Thought (CoT) instrui o modelo a raciocinar passo a passo antes de responder, melhorando a precisão em problemas de múltiplas etapas [1]. ReAct (Reason + Act) intercala raciocínio e chamadas de ferramentas, permitindo que o agente decida quando consultar fontes externas. Tree-of-Thoughts explora múltiplas linhas de raciocínio em paralelo [2].\n\n**Por que importa?** Em sistemas, o prompt é o contrato: formato de saída (JSON schema), limites, tom e fallbacks precisam ser definidos de forma determinística. O versionamento e a avaliação do prompt fazem parte do ciclo de vida.\n\n**O que muda na prática:** Use CoT para raciocínio, ReAct para agentes com ferramentas, validação de saída com schema e testes de regressão sobre um conjunto fixo de prompts [3]."
    ),
    "IA1-04-arquitetura-de-memoria-para-agentes": (
        "Arquitetura de Memória para Agentes",
        "Arquitetura de Memória para Agentes: Gerenciamento de memória de curto prazo (buffer de contexto) e longo prazo (bancos vetoriais)",
        "Gerenciamento de memória de curto prazo (buffer de contexto) e longo prazo (bancos vetoriais)",
        "Sem memória, um agente esquece tudo entre chamadas; com memória mal projetada, ele se afoga em contexto irrelevante. A arquitetura de memória combina o buffer de curto prazo com o armazenamento de longo prazo em bancos vetoriais. Este livro ensina a projetar ambas com critério.",
        "A memória é o que dá continuidade e personalidade ao agente. Curto prazo (buffer de contexto), longo prazo (vetores e recuperação) e memória de trabalho (estado da tarefa) precisam ser desenhados em conjunto — com custo de tokens sempre em mente.",
        "A memória de curto prazo corresponde ao buffer de contexto: o histórico recente da conversa, limitado pela janela de tokens [1]. A memória de longo prazo usa bancos vetoriais (pgvector, Qdrant, Chroma) para armazenar embeddings e recuperar informações relevantes por similaridade semântica [2].\n\n**Por que importa?** O buffer cheio degrada respostas; a recuperação imprecisa injeta ruído. Estratégias como sumarização do histórico, janela deslizante e metadados de recência controlam o equilíbrio entre lembrança e custo.\n\n**O que muda na prática:** Defina o que precisa ficar na conversa (buffer), o que vai para o banco vetorial (conhecimento) e o que é efêmero (estado de execução) — e aplique TTL e poda no buffer [3]."
    ),
    "IA1-05-protocolos-de-comunicacao-entre-agentes": (
        "Protocolos de Comunicação entre Agentes",
        "Protocolos de Comunicação entre Agentes: Como estruturar trocas de mensagens JSON seguras e determinísticas",
        "Como estruturar trocas de mensagens JSON seguras e determinísticas",
        "Quando múltiplos agentes conversam, a mensagem é o contrato. Protocolos de comunicação — mensagens JSON com schema, rotas e validação — garantem que a troca seja segura, determinística e auditável. Este livro define os padrões de comunicação entre agentes em sistemas distribuídos.",
        "A comunicação entre agentes é o sistema nervoso dos sistemas multi-agentes. Mensagens tipadas, determinísticas e auditáveis evitam os erros de interpretação que transformam colaboração em caos — e são a base de padrões como hierarquia e pipeline.",
        "Mensagens entre agentes devem ser estruturadas: JSON com campos tipados (sender, receiver, type, payload, id, timestamp) e validação de schema na recepção [1]. A determinismo vem de contratos rígidos: cada tipo de mensagem tem um schema esperado, e agentes que não o cumprem são rejeitados ou corrigidos [2].\n\n**Por que importa?** Mensagens soltas (texto livre) geram ambiguidade, injeções e rastreamento impossível. Com contratos JSON, cada troca é validável, logável e reproduzível — essencial para depurar sistemas com dezenas de agentes.\n\n**O que muda na prática:** Defina schemas JSON para cada tipo de mensagem, valide na borda, inclua IDs e timestamps para tracing e registre todas as trocas para auditoria [3]."
    ),
    "IA1-06-o-papel-do-llm-como-compilador": (
        "O Papel do LLM como Compilador e Tradutor",
        "O Papel do LLM como Compilador e Tradutor: Convertendo linguagem natural em código executável de forma confiável",
        "Convertendo linguagem natural em código executável de forma confiável",
        "O LLM atua como um compilador de linguagem natural para código: entradas imprecisas, saídas que precisam ser executáveis. Compreender esse papel — e as técnicas de validação, geração e correção de código — é o coração da engenharia de software guiada por IA. Este livro explora o tema em profundidade.",
        "Tratar o LLM como um compilador de linguagem natural muda a forma de projetar: a saída precisa ser sintaticamente válida, semanticamente correta e verificável. As técnicas — geração assistida por testes, auto-correção e sandboxes — transformam geração em engenharia.",
        "O LLM converte linguagem natural em código por predição de tokens, mas a confiabilidade vem do processo em volta: validação sintática, execução em sandbox, testes e iteração [1]. O padrão generate-test-repair (gerar, testar, corrigir) é o ciclo que transforma geração bruta em código confiável [2].\n\n**Por que importa?** Código gerado sem validação é uma promessa: só a execução em ambiente seguro comprova que funciona. A auto-correção usa erros de compilação e de teste como feedback para o modelo.\n\n**O que muda na prática:** Sempre execute o código gerado em sandbox, alimente os erros de volta ao modelo para correção e use testes como oráculo de aceite [3]."
    ),
    "IA1-07-design-patterns-multi-agentes": (
        "Design Patterns para Sistemas Multi-Agentes",
        "Design Patterns para Sistemas Multi-Agentes: Padrões de hierarquia, votação, pipeline e debate entre modelos",
        "Padrões de hierarquia, votação, pipeline e debate entre modelos",
        "Sistemas multi-agentes resolvem problemas complexos dividindo trabalho — e os padrões de coordenação definem como: hierarquia, votação, pipeline, debate e federação. Este livro cataloga esses padrões e orienta quando aplicar cada um, com trade-offs reais de custo e latência.",
        "Os padrões multi-agentes são o vocabulário da coordenação: cada um resolve uma classe de problema (divisão, consenso, sequência, crítica). Escolher o padrão certo — e saber combinar — determina a qualidade e o custo do sistema.",
        "Os padrões clássicos de sistemas multi-agentes incluem: hierarquia (um supervisor delega a especialistas), pipeline (cada agente processa e passa adiante), votação (múltiplas respostas e consenso), debate (agentes argumentam até convergir) e federação (especialistas em domínios distintos) [1]. Cada padrão equilibra qualidade, custo de tokens e latência de forma diferente [2].\n\n**Por que importa?** Votação e debate aumentam a qualidade com custo multiplicado; hierarquia organiza a complexidade; pipeline otimiza fluxos sequenciais. O padrão errado infla custos sem ganho.\n\n**O que muda na prática:** Comece com o padrão mais simples que resolve o problema e adicione complexidade apenas quando a qualidade exigir — medindo custo por melhoria [3]."
    ),
    "IA1-08-seguranca-e-guardrails": (
        "Segurança e Barreiras (Guardrails)",
        "Segurança e Barreiras (Guardrails): Validação de inputs e outputs para evitar injeções de prompt e vazamento de dados",
        "Validação de inputs e outputs para evitar injeções de prompt e vazamento de dados",
        "O maior risco dos agentes não é o modelo: é a falta de barreiras. Prompt injection, vazamento de dados e saídas inseguras são ameaças reais. Guardrails — validação de entrada, sanitização e controle de saída — são a camada de segurança que todo sistema agêntico exige. Este livro define o framework completo.",
        "Segurança em sistemas de IA é uma disciplina de camadas: nunca confiar no input, nunca confiar na saída. Guardrails implementam essa desconfiança com validação, sanitização, limites de escopo e auditoria — a base para operar agentes em produção.",
        "Prompt injection ocorre quando conteúdo externo manipula o comportamento do modelo — a defesa inclui delimitar instruções do usuário, validar e classificar inputs [1]. O vazamento de dados acontece quando informações sensíveis chegam ao contexto ou à saída — exige sanitização e redação automática [2].\n\n**Por que importa?** Um agente com ferramentas pode executar ações reais: a falha de validação de saída pode disparar uma ação indesejada. Guardrails de output (filtros, formatos, limites) são o último posto de controle.\n\n**O que muda na prática:** Separe instruções de dados, valide entradas com classificadores e schemas, filtre saídas por políticas e audite todas as interações [3]."
    ),
    "IA1-09-gerenciamento-de-custos-e-latencia": (
        "Gerenciamento de Custos e Latência",
        "Gerenciamento de Custos e Latência: Estratégias de cache semântico e roteamento dinâmico entre modelos (local vs. nuvem)",
        "Estratégias de cache semântico e roteamento dinâmico entre modelos (local vs. nuvem)",
        "LLMs custam dinheiro e tempo: cada chamada pesa no orçamento e na experiência do usuário. Cache semântico, roteamento dinâmico entre modelos e estratégias de tamanho de contexto são as alavancas de controle. Este livro ensina a otimizar custo e latência em sistemas de IA sem sacrificar qualidade.",
        "O gerenciamento de custo e latência é o que torna sistemas de IA viáveis em escala. Cache, roteamento e compressão de contexto reduzem gastos em até 80% enquanto mantêm a qualidade — mas exigem instrumentação e decisões por tarefa.",
        "O cache semântico armazena respostas de consultas similares (por embedding), evitando chamadas redundantes [1]. O roteamento dinâmico envia cada tarefa ao modelo mais adequado: modelos locais (Ollama) para tarefas simples e baratas, modelos de nuvem para raciocínio complexo [2].\n\n**Por que importa?** Modelos de nuvem têm custo por token e latência de rede; modelos locais são baratos e privados, mas mais fracos. Combiná-los por complexidade da tarefa otimiza o custo total.\n\n**O que muda na prática:** Instrumente tokens e latência por chamada, cacheie consultas repetidas por similaridade e roteie por complexidade com fallback para o modelo forte [3]."
    ),
    "IA1-10-ambientes-de-execucao-isolados": (
        "Ambientes de Execução Isolados (Sandboxes)",
        "Ambientes de Execução Isolados (Sandboxes): Como permitir que agentes rodem código com segurança sem derrubar o servidor",
        "Como permitir que agentes rodeem código com segurança sem derrubar o servidor",
        "Código gerado por agentes precisa ser executado — e executar código arbitrário no servidor principal é um convite ao desastre. Sandboxes (containers, VMs, isolamento de processo) permitem que agentes executem código com segurança. Este livro cobre as arquiteturas de isolamento e seus trade-offs.",
        "O sandbox é o que torna a geração de código segura na prática: execução isolada, limites de recursos e rede controlada. Escolher o nível de isolamento — do container ao microVM — define o equilíbrio entre segurança, latência e custo.",
        "Sandboxes isolam a execução de código com limites de CPU, memória, rede e tempo de vida [1]. As opções vão de containers efêmeros (Docker), passando por gVisor e Firecracker (microVMs), até serviços como E2B — cada uma com trade-offs de segurança e latência [2].\n\n**Por que importa?** Um agente que executa código pode rodar comandos destrutivos, consumir recursos ou acessar a rede interna. O sandbox define o perímetro de confiança e o que um agente pode ou não fazer.\n\n**O que muda na prática:** Execute todo código gerado em sandbox com rede bloqueada por padrão, limites de tempo e recursos, e capture a saída de forma controlada [3]."
    ),

    # ═══════════════ SÉRIE IA2 — ECOSSISTEMA FULLSTACK INTEGRADO A LLMS ═══════════════
    "IA2-01-apis-e-providers-de-ia": (
        "APIs e Providers de IA",
        "APIs e Providers de IA: Integração robusta com OpenAI, Anthropic, Google Gemini e modelos open-source (Llama, Mistral)",
        "Integração robusta com OpenAI, Anthropic, Google Gemini e modelos open-source (Llama, Mistral)",
        "Integrar LLMs ao seu backend é mais do que colar uma chave de API: é projetar uma camada de abstração que funcione com múltiplos providers. OpenAI, Anthropic, Gemini e modelos open-source têm APIs diferentes, custos diferentes e capacidades diferentes. Este livro ensina a integração robusta e portável.",
        "A camada de integração com providers de IA é a porta de entrada do ecossistema LLM. Abstrair o provider, padronizar formatos e gerenciar falhas permite trocar de modelo sem reescrever o sistema — e negociar o melhor custo/qualidade por tarefa.",
        "Cada provider expõe uma API própria: OpenAI (Chat Completions), Anthropic (Messages), Google (Generative AI) e open-source via servidores compatíveis (Ollama, vLLM) [1]. A integração robusta abstrai essas diferenças por trás de uma interface comum (chat, embed, stream), padroniza erros e gerencia retries [2].\n\n**Por que importa?** A portabilidade entre providers é estratégica: preços, capacidades e disponibilidade mudam. Uma camada de abstração com fallback entre providers aumenta a resiliência e permite escolher o melhor custo/qualidade por tarefa.\n\n**O que muda na prática:** Implemente uma interface comum com adapters por provider, normalize erros e rate limits, e adicione fallback automático quando um provider falhar [3]."
    ),
    "IA2-02-bancos-de-dados-vetoriais": (
        "Bancos de Dados Vetoriais",
        "Bancos de Dados Vetoriais: PostgreSQL com pgvector, Qdrant, Chroma e Pinecone para busca semântica em aplicações web",
        "PostgreSQL com pgvector, Qdrant, Chroma e Pinecone para busca semântica em aplicações web",
        "Busca semântica é a base do RAG e das aplicações cognitivas: converter texto em vetores e recuperar por similaridade. pgvector, Qdrant, Chroma e Pinecone representam as opções — do Postgres que você já usa ao serviço gerenciado dedicado. Este livro compara e implementa cada abordagem.",
        "O banco vetorial é a memória de longo prazo da aplicação de IA. Escolher entre pgvector (simplicidade, sem infra extra), Qdrant (performance dedicada) e Pinecone (gerenciado) depende de escala, custo e latência — e a decisão certa evita reescritas caras.",
        "Bancos vetoriais armazenam embeddings (vetores numéricos de texto) e recuperam vizinhos por similaridade de cosseno ou distância [1]. pgvector estende o PostgreSQL com busca vetorial nativa (HNSW, IVFFlat), evitando infraestrutura adicional; Qdrant e Pinecone são dedicados, com filtros e escala horizontal [2].\n\n**Por que importa?** A busca semântica supera a busca por palavras-chave em linguagem natural: sinônimos e paráfrases retornam resultados. O índice vetorial (HNSW) determina a velocidade e a precisão do recall.\n\n**O que muda na prática:** Comece com pgvector se já usa Postgres; migre para um banco dedicado quando a escala ou os filtros de metadados exigirem — medindo recall e latência em cada etapa [3]."
    ),
    "IA2-03-rag-avancado": (
        "RAG (Retrieval-Augmented Generation) Avançado",
        "RAG (Retrieval-Augmented Generation) Avançado: Indexação de bases de código, chunking inteligente e reranking de resultados",
        "Indexação de bases de código, chunking inteligente e reranking de resultados",
        "RAG é a técnica que conecta LLMs ao seu conhecimento: indexar, recuperar e gerar com base no que foi recuperado. Mas RAG ingênuo falha — a qualidade está no chunking, nos metadados, no reranking e na avaliação. Este livro cobre o RAG avançado para bases de código e documentos.",
        "O RAG bem projetado é o que torna os agentes úteis com dados específicos. Chunking inteligente, indexação por metadados, reranking e avaliação contínua são as diferenças entre um protótipo de busca e um sistema de conhecimento confiável.",
        "RAG combina recuperação (embeddings + busca) com geração: o contexto recuperado alimenta o LLM [1]. O RAG avançado adiciona: chunking semântico (dividir por significado, não por tamanho fixo), metadados ricos (fonte, função, módulo), reranking (reordenar resultados por relevância fina) e avaliação de retrieval [2].\n\n**Por que importa?** A qualidade do RAG é limitada pela recuperação: se o contexto certo não é encontrado, a resposta falha. Rerankers e metadados aumentam drasticamente o recall relevante.\n\n**O que muda na prática:** Indexe com chunks semânticos e metadados, use um reranker (cross-encoder) para reordenar os top-k e avalie o pipeline com um conjunto de perguntas de referência [3]."
    ),
    "IA2-04-streaming-de-respostas": (
        "Streaming de Respostas no Frontend",
        "Streaming de Respostas no Frontend: Implementando Server-Sent Events (SSE) e WebSockets para interfaces reativas em tempo real",
        "Implementando Server-Sent Events (SSE) e WebSockets para interfaces reativas em tempo real",
        "Ninguém espera dez segundos por uma resposta completa: o streaming entrega os tokens assim que são gerados, criando interfaces reativas. SSE e WebSockets são os canais — e a escolha depende do cenário. Este livro ensina a implementar streaming de LLM ponta a ponta, do backend ao frontend.",
        "O streaming é o que torna aplicações de IA agradáveis: o usuário vê a resposta fluindo, como em um chat. SSE é simples e unidirecional; WebSockets permitem bidirecionalidade. A implementação correta — buffers, cancelamento e reconexão — define a qualidade da experiência.",
        "Server-Sent Events (SSE) é um protocolo HTTP de streaming unidirecional, perfeito para respostas de LLM: o servidor empurra eventos de texto incremental [1]. WebSockets oferecem comunicação bidirecional, úteis quando o cliente também envia comandos frequentes [2].\n\n**Por que importa?** O tempo até o primeiro token é a métrica de percepção: com streaming, a resposta começa em segundos. O frontend precisa gerenciar estados parciais, cancelamento (abort controller) e reconexão.\n\n**O que muda na prática:** Prefira SSE para respostas de chat, use WebSocket quando a interação for contínua, e implemente abort/cancelamento e indicadores de estado parcial no frontend [3]."
    ),
    "IA2-05-gerenciamento-de-estado-cognitivo": (
        "Gerenciamento de Estado em Aplicações Cognitivas",
        "Gerenciamento de Estado em Aplicações Cognitivas: Controlando o histórico de conversas e o estado de tarefas longas no frontend",
        "Controlando o histórico de conversas e o estado de tarefas longas no frontend",
        "Aplicações cognitivas têm estado duplo: o histórico da conversa (que alimenta o contexto do LLM) e o estado de tarefas longas (que pode levar minutos). Gerenciar ambos no frontend — persistência, concorrência e retomada — é um desafio de arquitetura. Este livro cobre o tema por completo.",
        "O estado é o coração das aplicações cognitivas: sem histórico persistente, a conversa morre no refresh; sem gerenciamento de tarefas longas, o usuário fica preso. Projetar esse estado no frontend — com persistência, filas e retomada — define a robustez do produto.",
        "O histórico de conversas precisa ser persistido (banco de dados) e sincronizado com o frontend, servindo tanto à UI quanto ao contexto do LLM (resumo + janela de mensagens) [1]. Tarefas longas exigem modelo de estado (pending, running, done, failed), polling ou eventos, e retomada após falha [2].\n\n**Por que importa?** O contexto do LLM é finito: o frontend precisa enviar apenas o histórico relevante. Tarefas longas (análise de documentos, geração em lote) precisam de progresso visível e continuidade entre sessões.\n\n**O que muda na prática:** Persista o histórico por sessão, modele estados de tarefa com eventos, e use polling ou SSE para progresso com retomada segura [3]."
    ),
    "IA2-06-function-calling-e-tool-use": (
        "Function Calling e Tool Use",
        "Function Calling e Tool Use: Capacitando agentes a consultar APIs REST, bancos de dados e ferramentas externas",
        "Capacitando agentes a consultar APIs REST, bancos de dados e ferramentas externas",
        "Um agente que só conversa é limitado; um agente que usa ferramentas transforma-se em sistema. Function calling permite que o LLM declare intenção de chamar funções — consultar APIs, bancos e serviços. Este livro ensina a implementar tool use com segurança e confiabilidade.",
        "Function calling é o mecanismo que transforma LLMs em agentes operacionais: o modelo decide quando chamar uma ferramenta, com argumentos estruturados. A execução segura e a validação dos resultados completam o ciclo que conecta IA a sistemas reais.",
        "Function calling permite que o LLM retorne chamadas estruturadas de funções (nome + argumentos JSON) em vez de texto livre, quando detecta a necessidade de uma ferramenta [1]. O backend executa a função, valida o resultado e devolve ao modelo para continuar o raciocínio [2].\n\n**Por que importa?** Ferramentas ampliam o agente: consultar banco, chamar APIs, calcular, buscar na web. A segurança exige: whitelist de funções, validação de argumentos, autorização e limites de chamadas.\n\n**O que muda na prática:** Defina o schema das ferramentas, execute com validação e sandbox quando necessário, e inclua o resultado da ferramenta no contexto para o próximo passo [3]."
    ),
    "IA2-07-frameworks-de-orquestracao": (
        "Frameworks de Orquestração (LangChain e LlamaIndex)",
        "Frameworks de Orquestração (LangChain e LlamaIndex): Construção rápida de pipelines de dados e cadeias de raciocínio",
        "Construção rápida de pipelines de dados e cadeias de raciocínio",
        "LangChain e LlamaIndex aceleram a construção de sistemas de IA com componentes prontos: chains, retrievers, agentes e integrações. Este livro ensina os dois frameworks na prática — quando usar cada um e como evitar o lock-in e a complexidade oculta.",
        "Os frameworks de orquestração entregam produtividade imediata, mas exigem discernimento: abstrações demais escondem custo e dificultam o controle fino. Dominar LangChain e LlamaIndex — e saber quando prescindir deles — é a marca da maturidade.",
        "LangChain organiza chains (sequências de chamadas ao LLM), agentes, memória e integrações em um ecossistema amplo [1]. LlamaIndex foca em dados: indexação, retrieval e RAG sobre documentos, com abstrações de Document, Node e Index [2].\n\n**Por que importa?** Ambos aceleram protótipos e dão acesso a dezenas de integrações. O risco é a complexidade oculta: abstrações opacas dificultam depuração e otimização de custo — e o lock-in do framework.\n\n**O que muda na prática:** Use LangChain para agentes e chains, LlamaIndex para RAG sobre documentos, e abstraia as interfaces para permitir sair do framework quando o controle fino for necessário [3]."
    ),
    "IA2-08-orquestracao-avancada-com-langgraph": (
        "Orquestração Avançada com LangGraph",
        "Orquestração Avançada com LangGraph: Criando fluxos cíclicos, checkpoints e gerenciamento de estado complexo para agentes",
        "Criando fluxos cíclicos, checkpoints e gerenciamento de estado complexo para agentes",
        "Chains lineares não bastam para agentes reais: eles precisam de loops, condicionais e estado persistente. LangGraph modela agentes como grafos — nós, arestas, checkpoints e fluxos cíclicos. Este livro ensina a orquestração avançada que resolve problemas que frameworks lineares não conseguem.",
        "LangGraph representa o agente como um grafo de estados: cada nó processa, cada aresta decide o próximo passo, e checkpoints persistem o estado. Isso habilita loops, retornos, intervenção humana e retomada — o padrão de produção para agentes complexos.",
        "LangGraph modela o fluxo do agente como um grafo com nós (funções) e arestas (transições), incluindo ciclos controlados [1]. Checkpoints salvam o estado em cada etapa, permitindo retomada, depuração e intervenção humana no fluxo [2].\n\n**Por que importa?** Agentes reais não são lineares: um agente que decide buscar mais informação e voltar ao raciocínio é um ciclo. LangGraph torna esses fluxos explícitos, testáveis e persistíveis.\n\n**O que muda na prática:** Modele o agente como grafo com estados explícitos, use checkpoints para retomada e depuração e introduza intervenção humana como um nó do fluxo [3]."
    ),
    "IA2-09-sdks-openai-e-anthropic": (
        "Desenvolvimento com o SDK da OpenAI e Anthropic",
        "Desenvolvimento com o SDK da OpenAI e Anthropic: Construindo camadas de abstração limpas no backend Node.js/Python",
        "Construindo camadas de abstração limpas no backend Node.js/Python",
        "Os SDKs oficiais da OpenAI e Anthropic são a porta de entrada — mas usá-los direto no código de negócio cria acoplamento. A prática madura é construir uma camada de abstração limpa no backend. Este livro ensina o desenvolvimento com os dois SDKs e a arquitetura que os isola.",
        "O SDK é uma ferramenta; a camada de abstração é a arquitetura. Isolar o provider em um serviço dedicado permite testar com mocks, trocar de modelo e controlar custo sem espalhar dependências pelo código de negócio.",
        "Os SDKs da OpenAI e Anthropic oferecem clientes tipados para chat, streaming, embeddings e function calling [1]. A camada de abstração concentra: a configuração do provider, o tratamento de erros/retries, a instrumentação de tokens e o formato das respostas [2].\n\n**Por que importa?** Código de negócio não deve conhecer o SDK: ele deve chamar uma interface (ex.: gerarResposta, gerarRespostaStream) implementada por um serviço. Isso permite mocks em testes e troca de provider sem tocar na aplicação.\n\n**O que muda na prática:** Crie um serviço LLM com interface própria, implemente com o SDK de cada provider e injete configuração, instrumentação e fallback nessa camada [3]."
    ),
    "IA2-10-microsservicos-de-ia": (
        "Microsserviços de IA",
        "Microsserviços de IA: Separando o processamento pesado de LLMs da aplicação principal através de filas (BullMQ, Celery)",
        "Separando o processamento pesado de LLMs da aplicação principal através de filas (BullMQ, Celery)",
        "Processamento de LLM é lento e caro: deixá-lo no caminho da requisição compromete a experiência. A solução arquitetural é separar em um microsserviço de IA consumindo filas (BullMQ, Celery). Este livro ensina a arquitetura que escala IA sem derrubar o serviço principal.",
        "Microsserviços de IA com filas desacoplam o trabalho pesado da resposta ao usuário: a aplicação publica um job, o worker processa com o LLM e o resultado volta por callback ou consulta. Isso protege a latência e permite escala independente.",
        "Filas (BullMQ no Node, Celery no Python) desacoplam produtores e consumidores: a aplicação enfileira o trabalho de IA, um worker dedicado consome e processa [1]. O microsserviço de IA concentra o acesso ao LLM, permitindo escala horizontal, retries e isolamento de falhas [2].\n\n**Por que importa?** Chamadas de LLM podem levar dezenas de segundos: bloquear a requisição HTTP é inaceitável. Com filas, a API responde rápido e o resultado chega assíncrono — com progresso e estado rastreáveis.\n\n**O que muda na prática:** Mova todo processamento de LLM para workers em fila, exponha endpoints de status por job e escale os workers independentemente da API [3]."
    ),

    # ═══════════════ SÉRIE IA3 — ENGENHARIA DE SOFTWARE GUIADA POR AGENTES ═══════════════
    "IA3-01-ides-autonomas-e-ambientes-agencios": (
        "IDEs Autônomas e Ambientes Agênticos",
        "IDEs Autônomas e Ambientes Agênticos: Como configurar e estender frameworks como Cursor, Antigravity e VSCode com IA",
        "Como configurar e estender frameworks como Cursor, Antigravity e VSCode com IA",
        "A IDE virou um ambiente agêntico: autocomplete, edição multi-arquivo, comandos em linguagem natural e agentes que executam tarefas completas. Cursor, Antigravity e VSCode com IA representam essa nova geração. Este livro ensina a configurar e estender esses ambientes para o seu fluxo real.",
        "A IDE agêntica é o posto de trabalho do desenvolvedor moderno: regras de projeto, modelos configurados e agentes que executam tarefas no seu repositório. Configurar bem esse ambiente — e entender seus limites — multiplica a produtividade.",
        "IDEs agênticas integram LLMs ao editor com: autocomplete contextual, chat sobre o código, edição multi-arquivo e execução de comandos [1]. Cursor e VSCode+IA configuram-se com regras de projeto (CLAUDE.md, .cursorrules), modelos e ferramentas (linters, testes, terminal) [2].\n\n**Por que importa?** O ambiente agêntico entende o contexto do repositório inteiro, não só o arquivo aberto. As regras de projeto definem o comportamento do agente: padrões, tecnologias e limites.\n\n**O que muda na prática:** Escreva regras de projeto claras, configure os modelos e ferramentas permitidas e adote o fluxo: tarefa → agente → revisão do diff → ajuste [3]."
    ),
    "IA3-02-geracao-automatizada-frontend": (
        "Geração Automatizada de Código Frontend",
        "Geração Automatizada de Código Frontend: Prompts e componentes para criar interfaces em React e Tailwind via agentes",
        "Prompts e componentes para criar interfaces em React e Tailwind via agentes",
        "Interfaces completas em React e Tailwind geradas por agentes: de um prompt à tela funcional. A prática combina prompts estruturados, bibliotecas de componentes e validação visual. Este livro ensina a geração automatizada de frontend com qualidade consistente.",
        "A geração de frontend por agentes é uma das aplicações mais produtivas da IA: descrições viram componentes, telas e layouts. A técnica está nos prompts, nos componentes reutilizáveis e na revisão sistemática do resultado.",
        "Agentes geram interfaces a partir de descrições: prompts que especificam layout, estados, responsividade e design system (Tailwind) [1]. A consistência vem de bibliotecas de componentes (shadcn/ui, headless UI) que o agente reutiliza em vez de recriar do zero [2].\n\n**Por que importa?** O risco é a inconsistência visual e a acessibilidade deficiente. Prompts com especificação exata + componentes validados + revisão visual (screenshot) garantem qualidade.\n\n**O que muda na prática:** Descreva a tela com estrutura e estados, mande o agente usar o design system do projeto e valide cada geração com execução local e screenshot [3]."
    ),
    "IA3-03-geracao-automatizada-backend": (
        "Geração Automatizada de Backend",
        "Geração Automatizada de Backend: Agentes criando rotas, migrações de banco de dados e regras de negócio estruturadas",
        "Agentes criando rotas, migrações de banco de dados e regras de negócio estruturadas",
        "O backend é o terreno fértil da geração por agentes: rotas, migrações, services e regras de negócio seguem padrões que agentes aprendem rapidamente. Este livro ensina a gerar backend estruturado — do schema à API — com contratos, testes e qualidade.",
        "Agentes geram backend de alta qualidade quando o padrão está definido: arquitetura em camadas, contratos de API e migrations versionadas. A geração ganha robustez com testes gerados junto e validação automática de cada camada.",
        "A geração de backend por agentes cobre: rotas e controllers a partir do contrato, migrações de banco derivadas do schema, services com regras de negócio e repositórios de acesso a dados [1]. O padrão em camadas dá estrutura à geração [2].\n\n**Por que importa?** Backend segue convenções fortes (REST, camadas, ORM), o que torna a geração consistente. O contrato (OpenAPI, Zod schemas) é o que conecta a geração ao frontend.\n\n**O que muda na prática:** Defina o padrão de arquitetura nas regras do agente, gere schema → migração → rotas → testes em sequência e valide com a suíte de testes [3]."
    ),
    "IA3-04-refatoracao-inteligente-em-lote": (
        "Refatoração Inteligente em Lote",
        "Refatoração Inteligente em Lote: Utilizando agentes para atualizar dependências, migrar frameworks e limpar legados",
        "Utilizando agentes para atualizar dependências, migrar frameworks e limpar legados",
        "Atualizar dependências, migrar de framework e limpar código legado são tarefas repetitivas em escala — perfeitas para agentes. A refatoração inteligente em lote combina análise de código, geração de mudanças e validação contínua. Este livro ensina a metodologia.",
        "A refatoração em lote com agentes transforma semanas de trabalho manual em dias supervisionados. A metodologia — mapear, gerar mudanças pequenas, testar e repetir — mantém o código seguro durante a transformação.",
        "Refatoração em lote usa agentes para: atualizar versões de dependências, migrar entre frameworks (ex.: CRA → Vite, REST → tRPC) e remover código morto [1]. A segurança vem das mudanças incrementais com testes rodando entre cada etapa [2].\n\n**Por que importa?** Migrações grandes à mão geram conflitos e regressões invisíveis. Agentes executam transformações mecânicas com consistência, e o humano supervisiona as decisões de arquitetura.\n\n**O que muda na prática:** Divida a migração em etapas testáveis, delegue cada etapa a um agente com escopo claro e rode a suíte de testes entre etapas [3]."
    ),
    "IA3-05-documentacao-viva-e-automatizada": (
        "Documentação Viva e Automatizada",
        "Documentação Viva e Automatizada: Agentes que analisam o código-fonte e geram documentações técnicas atualizadas em tempo real",
        "Agentes que analisam o código-fonte e geram documentações técnicas atualizadas em tempo real",
        "A documentação morre quando ninguém a atualiza — agentes a mantêm viva: analisam o código-fonte e geram documentação técnica sincronizada. READMEs, docs de API e guias de arquitetura gerados e revisados por agentes a cada mudança. Este livro ensina a pipeline de documentação viva.",
        "Documentação viva é aquela que reflete o código de hoje, não o de seis meses atrás. Agentes que analisam o repositório e geram/atualizam docs — disparados por CI ou sob demanda — eliminam a defasagem e o trabalho manual.",
        "Agentes geram documentação analisando o código: extraem assinaturas, fluxos, schemas e exemplos de uso [1]. A pipeline pode rodar no CI a cada merge, atualizando README, docs de API (OpenAPI) e guias de módulo automaticamente [2].\n\n**Por que importa?** Docs desatualizadas enganam mais do que a ausência. A documentação viva reduz onboarding e erros de uso, mantendo a fonte da verdade no código.\n\n**O que muda na prática:** Gere docs de API a partir do schema, README por módulo no CI, e configure um agente para revisar a documentação quando arquivos-chave mudarem [3]."
    ),
    "IA3-06-testes-unitarios-autonomos": (
        "Testes Unitários Autônomos",
        "Testes Unitários Autônomos: Agentes gerando casos de teste, mocks e cobrindo 100% de branches em funções críticas",
        "Agentes gerando casos de teste, mocks e cobrindo 100% de branches em funções críticas",
        "Testes são a rede de segurança do código — e gerá-los à mão consome tempo precioso. Agentes geram casos de teste, mocks e cobrem branches críticas automaticamente. Este livro ensina a geração autônoma de testes com qualidade de engenheiro sênior.",
        "A geração autônoma de testes muda a economia da qualidade: funções críticas ganham cobertura sem esforço manual, e o agente encontra casos de borda que humanos frequentemente esquecem. A revisão humana continua sendo o filtro final.",
        "Agentes analisam funções e geram testes: fluxo feliz, casos de erro, valores limite e mocks de dependências [1]. A cobertura de branches é medida com ferramentas (c8, Istanbul) e o agente itera até atingir o alvo [2].\n\n**Por que importa?** Testes gerados por agente reduzem o custo da rede de segurança e liberam o time para features. A qualidade depende do oráculo: o agente deve ver o comportamento esperado, não só o código.\n\n**O que muda na prática:** Peça testes por comportamento (given/when/then), mocks explícitos de fronteiras e rodada de cobertura com feedback ao agente até o alvo [3]."
    ),
    "IA3-07-testes-e2e-com-visao-computacional": (
        "Testes End-to-End com Visão Computacional",
        "Testes End-to-End com Visão Computacional: Agentes navegando em aplicações web como usuários reais para validar fluxos",
        "Agentes navegando em aplicações web como usuários reais para validar fluxos",
        "Agentes com visão computacional navegam na aplicação como usuários reais: clicam, preenchem e verificam o que veem na tela. Isso transforma o teste E2E — capturando regressões visuais e fluxos que seletores não alcançam. Este livro ensina a técnica e as ferramentas.",
        "O teste E2E com visão computacional une o agente ao navegador: além do DOM, o agente interpreta o que está renderizado. Isso valida experiência real, acessibilidade e regressões visuais — com a flexibilidade de quem entende contexto.",
        "Frameworks como Playwright e agentes com modelos multimodais permitem que a IA navegue pela aplicação: o agente recebe a screenshot, decide a próxima ação e verifica o resultado visual [1]. Isso complementa os seletores tradicionais, cobrindo o que o DOM não expressa [2].\n\n**Por que importa?** Fluxos complexos (checkout, onboarding) com muitas variações visuais são difíceis de cobrir com seletores rígidos. A visão computacional valida a experiência percebida, não apenas o estado técnico.\n\n**O que muda na prática:** Use o agente para fluxos críticos de ponta a ponta, combine com assertions de DOM para precisão e execute em CI com screenshots de falha [3]."
    ),
    "IA3-08-analise-estatica-de-seguranca": (
        "Análise Estática de Segurança com IA",
        "Análise Estática de Segurança com IA: Agentes identificando vulnerabilidades (OWASP Top 10) diretamente no pull request",
        "Agentes identificando vulnerabilidades (OWASP Top 10) diretamente no pull request",
        "A segurança precisa acompanhar a velocidade do código — e agentes de análise estática revisam cada pull request contra o OWASP Top 10. SQL injection, XSS, CSRF e auth quebrada são detectados antes do merge. Este livro ensina a integrar agentes de segurança ao fluxo de desenvolvimento.",
        "A análise estática com IA complementa as ferramentas tradicionais (SAST): o agente entende contexto e fluxos, encontrando vulnerabilidades que regras estáticas não capturam. Integrado ao PR, o feedback de segurança chega no momento da escrita.",
        "Agentes de segurança revisam o diff do PR contra o OWASP Top 10: procuram inputs não validados, queries concatenadas, headers ausentes e controle de acesso frágil [1]. O agente comenta no PR com o problema, a evidência e a correção sugerida [2].\n\n**Por que importa?** Vulnerabilidades encontradas no PR custam minutos; em produção, custam incidentes. A análise por IA cobre o contexto do fluxo de dados, indo além de padrões fixos.\n\n**O que muda na prática:** Configure um agente de revisão de segurança no CI que comenta no PR, priorize por severidade e bloqueie merges de vulnerabilidades críticas [3]."
    ),
    "IA3-09-code-review-automatizado": (
        "Code Review Automatizado por Agentes",
        "Code Review Automatizado por Agentes: Configurando revisores de código virtuais com regras e padrões personalizados da equipe",
        "Configurando revisores de código virtuais com regras e padrões personalizados da equipe",
        "O code review é o gargalo e o guardião da qualidade — agentes revisores virtuais aliviam o gargalo mantendo o padrão. Configurados com as regras do time, eles analisam cada PR: estilo, arquitetura, edge cases e testes. Este livro ensina a configurar e calibrar revisores virtuais.",
        "O revisor virtual não substitui o humano: tria e acelera. Com as regras da equipe — padrões de código, arquitetura e casos de borda — o agente encontra o que o olho cansado perde, e o humano foca nas decisões de design.",
        "Revisores de código virtuais analisam o diff com o contexto do projeto: regras personalizadas (style guide, arquitetura, nomes), verificação de testes e detecção de code smells [1]. Eles comentam com severidade, evidência e sugestão [2].\n\n**Por que importa?** O tempo de review é um dos maiores custos do fluxo; o agente reduz a carga repetitiva e padroniza o feedback. A calibração — ajustar as regras pelo comportamento — melhora a precisão ao longo do tempo.\n\n**O que muda na prática:** Documente as regras do time no prompt do revisor, exija aprovação humana para merge e calibre com exemplos de revisões boas e ruins [3]."
    ),
    "IA3-10-correcao-automatica-de-bugs": (
        "Correção Automática de Bugs (Self-Healing Code)",
        "Correção Automática de Bugs (Self-Healing Code): Sistemas que capturam logs de erro em produção, analisam o stack trace e aplicam patches",
        "Sistemas que capturam logs de erro em produção, analisam o stack trace e aplicam patches",
        "O sonho do software que se corrige sozinho: capturar erros em produção, analisar o stack trace com um agente e gerar o patch — com supervisão humana. Este livro ensina a arquitetura do self-healing code: da coleta de erros à aplicação do fix.",
        "O self-healing code não remove o engenheiro: remove o tempo de resposta. O sistema coleta o erro, o agente diagnostica e propõe o patch, e o humano aprova. O ciclo — detectar, diagnosticar, corrigir, validar — é a espinha dorsal de sistemas resilientes.",
        "A arquitetura captura erros em produção (Sentry, logs estruturados), o agente analisa o stack trace e o código envolvido, diagnostica a causa raiz e gera um patch candidato [1]. O patch passa por testes e revisão humana antes do deploy [2].\n\n**Por que importa?** O tempo entre o erro e o fix é a métrica mais cara da operação. A automação comprime esse ciclo de dias para horas, mantendo a supervisão humana como gate de segurança.\n\n**O que muda na prática:** Centralize erros com contexto rico, delegue o diagnóstico e o patch ao agente, e valide com testes + revisão antes do deploy [3]."
    ),

    # ═══════════════ SÉRIE IA4 — AUTOMAÇÃO DE FLUXOS, LOW-CODE E DEVOPS COM IA ═══════════════
    "IA4-01-agentes-em-plataformas-low-code": (
        "Agentes em Plataformas Low-Code (N8N)",
        "Agentes em Plataformas Low-Code (N8N): Construindo workflows inteligentes que tomam decisões e processam dados não estruturados",
        "Construindo workflows inteligentes que tomam decisões e processam dados não estruturados",
        "O n8n conecta ferramentas visualmente — e com nós de IA, os workflows deixam de ser fixos e passam a decidir. Agentes em plataformas low-code processam dados não estruturados, classificam e encaminham. Este livro ensina a construir automações inteligentes com n8n e LLMs.",
        "Plataformas low-code com IA democratizam a automação: fluxos que classificam e-mails, extraem dados de documentos e decidem o próximo passo sem código. O n8n com nós de LLM é a ponte entre automação visual e inteligência.",
        "O n8n oferece nós de IA (LLM, embeddings, agentes) dentro de workflows visuais [1]. Com eles, fluxos processam dados não estruturados: extraem informações de textos, classificam por intenção e encaminham para a ferramenta certa [2].\n\n**Por que importa?** Automação tradicional exige dados estruturados; com IA, o fluxo entende linguagem natural. O resultado: e-mails triados, documentos resumidos e decisões automatizadas com custo baixo de manutenção.\n\n**O que muda na prática:** Comece com um fluxo de triagem (extrair → classificar → encaminhar), use nós de LLM com prompts testados e monitore os casos que o fluxo não resolveu [3]."
    ),
    "IA4-02-automacao-de-tarefas-de-repositorio": (
        "Automação de Tarefas de Repositório (GitHub Actions + IA)",
        "Automação de Tarefas de Repositório (GitHub Actions + IA): Criando bots que gerenciam issues, fecham PRs e organizam boards",
        "Criando bots que gerenciam issues, fecham PRs e organizam boards",
        "GitHub Actions automatiza o fluxo do repositório — e com IA, os bots passam a entender contexto: triam issues, rotulam, revisam PRs e organizam boards. Este livro ensina a criar bots de repositório com GitHub Actions e LLMs.",
        "Os bots de repositório com IA transformam o manutenção do GitHub em automação: issues triadas por relevância, PRs rotulados automaticamente e boards organizados sem esforço manual. O humano supervisiona as decisões que o bot toma.",
        "GitHub Actions executa workflows em eventos do repositório (issue aberta, PR criado) [1]. Com chamadas a LLMs no workflow, o bot entende o conteúdo: classifica a issue, sugere rótulos, responde com orientações e até atualiza o board [2].\n\n**Por que importa?** Projetos ativos recebem dezenas de issues e PRs por dia; a triagem manual consome tempo valioso. Bots com IA triam no ritmo do fluxo, com regras claras de quando agir e quando escalar para humanos.\n\n**O que muda na prática:** Crie um workflow que chama o LLM em issues novas (classificar, rotular), configure limites de ação do bot e revise periodicamente as decisões automáticas [3]."
    ),
    "IA4-03-devops-cognitivo": (
        "DevOps Cognitivo",
        "DevOps Cognitivo: Agentes monitorando infraestrutura em servidores VPS, interpretando logs e sugerindo otimizações",
        "Agentes monitorando infraestrutura em servidores VPS, interpretando logs e sugerindo otimizações",
        "O DevOps ganha um copiloto: agentes que monitoram servidores, interpretam logs e métricas e sugerem otimizações em linguagem natural. Do diagnóstico de incidentes ao tuning de performance, o DevOps cognitivo acelera a operação. Este livro ensina a arquitetura.",
        "O DevOps cognitivo coloca a inteligência sobre a operação: o agente correlaciona logs e métricas, diagnostica a causa provável e sugere a ação. O engenheiro valida e executa — com o tempo de diagnóstico drasticamente reduzido.",
        "Agentes de DevOps monitoram infraestrutura (CPU, memória, disco, logs) e interpretam o estado em linguagem natural [1]. Integrados a métricas e logs centralizados, correlacionam eventos, identificam padrões e sugerem otimizações ou correções [2].\n\n**Por que importa?** Incidentes exigem diagnóstico rápido: o agente encurta o tempo de detecção→compreensão. As sugestões vêm com contexto e prioridade, e o humano executa com a visão completa.\n\n**O que muda na prática:** Conecte logs e métricas ao agente, defina consultas padrão de diagnóstico e use o agente como primeiro respondedor de alertas, com ação humana para mudanças [3]."
    ),
    "IA4-04-geracao-de-queries-sql": (
        "Geração de Queries SQL Complexas",
        "Geração de Queries SQL Complexas: Agentes atuando como tradutores de linguagem natural para bancos relacionais otimizados",
        "Agentes atuando como tradutores de linguagem natural para bancos relacionais otimizados",
        "Traduzir linguagem natural em SQL otimizado é uma das aplicações mais valiosas dos agentes: o usuário pergunta e o agente consulta o banco. Do schema à query com joins e agregações, a qualidade depende do contexto fornecido e da validação. Este livro ensina a técnica de ponta a ponta.",
        "O text-to-SQL com agentes dá acesso direto aos dados: perguntas em linguagem natural viram queries seguras e otimizadas. O schema, as convenções e a validação de execução determinam a precisão — e a segurança define os limites.",
        "Agentes traduzem linguagem natural em SQL fornecendo o schema (tabelas, colunas, tipos, relações) como contexto e gerando a query [1]. A validação inclui: execução em ambiente seguro (read-only), revisão do plano (EXPLAIN) e limites de escopo [2].\n\n**Por que importa?** A precisão depende do contexto: sem schema e convenções, o agente inventa colunas. A segurança exige read-only e row-level security para impedir consultas destrutivas ou fora do escopo do usuário.\n\n**O que muda na prática:** Forneça o schema como contexto, gere a query com EXPLAIN, execute read-only com limite de linhas e valide o resultado contra a pergunta [3]."
    ),
    "IA4-05-extracao-de-dados-nao-estruturados": (
        "Extração de Dados Não Estruturados (ETL Inteligente)",
        "Extração de Dados Não Estruturados (ETL Inteligente): Transformando faturas, PDFs e contratos em JSON limpo e estruturado",
        "Transformando faturas, PDFs e contratos em JSON limpo e estruturado",
        "Faturas, PDFs e contratos são dados valiosos presos em formatos que máquinas não leem. O ETL inteligente usa LLMs para extrair e estruturar: documento entra, JSON limpo sai. Este livro ensina a pipeline de extração com validação e confiabilidade.",
        "A extração de dados não estruturados com LLMs substitui o retrabalho manual: o documento é convertido em JSON estruturado com os campos do domínio. A confiabilidade vem da validação de schema, dos exemplos e das regras de revisão.",
        "O ETL inteligente processa documentos com LLMs: o texto (extraído de PDF, OCR quando necessário) é enviado com um schema-alvo e instruções, e o modelo retorna o JSON estruturado [1]. A validação com JSON schema e a revisão de baixa confiança completam o fluxo [2].\n\n**Por que importa?** Dados não estruturados são a maioria dos dados empresariais. Extração com LLM reduz horas de digitação e erros, mas exige validação: campos ausentes ou inventados devem ser sinalizados.\n\n**O que muda na prática:** Extraia o texto, defina o schema-alvo com exemplos, peça saída JSON validada e sinalize baixa confiança para revisão humana [3]."
    ),
    "IA4-06-chatbots-text-to-sql": (
        "Chatbots com Conexão a Bancos de Dados (Text-to-SQL)",
        "Chatbots com Conexão a Bancos de Dados (Text-to-SQL): Criando interfaces onde o usuário interage diretamente com os dados da empresa",
        "Criando interfaces onde o usuário interage diretamente com os dados da empresa",
        "O usuário de negócio pergunta no chat e recebe dados da empresa: 'qual a receita do último trimestre?'. O chatbot text-to-SQL conecta linguagem natural ao banco, com segurança e validação. Este livro ensina a construir essa interface ponta a ponta.",
        "O chatbot com acesso ao banco democratiza os dados: quem não sabe SQL consulta com a linguagem do dia a dia. A construção exige schema bem descrito, permissões por usuário e validação rigorosa das queries geradas.",
        "O chatbot text-to-SQL combina RAG (instruções e schema no contexto) com geração de SQL e execução segura [1]. A interface de chat mostra a query gerada e o resultado, permitindo que o usuário confie e valide [2].\n\n**Por que importa?** A confiança depende da transparência: mostrar o SQL gerado e os dados de origem. A segurança exige RBAC por linha/coluna e limites de consulta para proteger dados sensíveis.\n\n**O que muda na prática:** Descreva o schema e as convenções no contexto, gere SQL com validação read-only, mostre a query ao usuário e aplique permissões por perfil [3]."
    ),
    "IA4-07-multi-agentes-para-desenvolvimento-agil": (
        "Sistemas Multi-Agentes para Desenvolvimento Ágil",
        "Sistemas Multi-Agentes para Desenvolvimento Ágil: Agentes simulando Product Owners, Desenvolvedores e QAs em um backlog",
        "Agentes simulando Product Owners, Desenvolvedores e QAs em um backlog",
        "Imagine um time onde cada papel tem um agente: o Product Owner descreve, o Desenvolvedor implementa, o QA testa — todos trabalhando sobre o mesmo backlog. Sistemas multi-agentes simulam o fluxo ágil com papéis especializados. Este livro ensina a arquitetura e os limites.",
        "O desenvolvimento ágil com multi-agentes automatiza o ciclo: requisito → tarefa → implementação → testes → revisão. Cada papel especializado usa prompts e ferramentas próprias, e a coordenação entre eles reproduz o fluxo de um time real.",
        "A arquitetura simula papéis com agentes especializados: PO (traduz requisitos em histórias), Desenvolvedor (gera código com base nas tarefas), QA (testa e reporta) e Revisor (aprova) [1]. A coordenação segue o backlog, com estado compartilhado entre os papéis [2].\n\n**Por que importa?** A simulação de papéis reduz o gargalo entre requisito e código e dá visibilidade do fluxo. Os limites: agentes não substituem decisões de produto nem a responsabilidade humana final.\n\n**O que muda na prática:** Modele os papéis com prompts especializados, compartilhe o estado do backlog e use o agente QA como gate antes da entrega [3]."
    ),
    "IA4-08-web-scraping-inteligente": (
        "Web Scraping Inteligente com Agentes",
        "Web Scraping Inteligente com Agentes: Ferramentas de navegação autônoma para extração de dados dinâmicos da web",
        "Ferramentas de navegação autônoma para extração de dados dinâmicos da web",
        "Sites modernos renderizam com JavaScript, bloqueiam scrapers e mudam o layout sem aviso. Agentes com navegação autônoma — que entendem a página, clicam e extraem — resolvem o que scrapers fixos não conseguem. Este livro ensina o scraping inteligente com ferramentas como browser-use e Playwright.",
        "O scraping inteligente une o agente ao navegador: a IA interpreta a página renderizada, decide a navegação e extrai os dados estruturados. A robustez vem da compreensão de contexto, não de seletores fixos que quebram a cada redesign.",
        "Ferramentas como Playwright MCP e browser-use permitem que o agente navegue: recebe o estado da página (DOM/texto/screenshot), decide a ação (clicar, preencher, rolar) e extrai os dados [1]. A extração é guiada por instruções e validada contra o resultado [2].\n\n**Por que importa?** Scrapers fixos quebram com mudanças de layout; agentes adaptam-se compreendendo o novo conteúdo. A ética e a legalidade (robots.txt, termos de uso) definem o que pode ser coletado.\n\n**O que muda na prática:** Use o agente para navegação dinâmica e extração semântica, respeite robots.txt e rate limits, e valide os dados extraídos contra o schema [3]."
    ),
    "IA4-09-geracao-de-conteudo-programatico": (
        "Geração de Conteúdo e Marketing Programático",
        "Geração de Conteúdo e Marketing Programático: Agentes fullstack que alimentam blogs, SEO e páginas de e-commerce dinamicamente",
        "Agentes fullstack que alimentam blogs, SEO e páginas de e-commerce dinamicamente",
        "Blogs, descrições de produtos e páginas de destino gerados dinamicamente por agentes: o marketing programático escala a produção de conteúdo com SEO e personalização. Este livro ensina a pipeline fullstack que gera, publica e mede conteúdo automaticamente.",
        "O marketing programático com IA produz conteúdo em escala: descrições de produtos, artigos otimizados para SEO e páginas dinâmicas — gerados, revisados e publicados por pipelines de agentes. A qualidade é controlada por templates, revisão e métricas.",
        "Pipelines de agentes geram conteúdo: o agente de escrita produz o texto a partir de briefing e dados de produto, o agente de SEO otimiza palavras-chave e estrutura, e o agente de publicação integra ao CMS ou à página [1]. A personalização usa dados do usuário e do catálogo [2].\n\n**Por que importa?** O volume de conteúdo necessário para SEO e e-commerce é enorme; a geração programática entrega escala com consistência de marca — quando os prompts e os dados de entrada são bem curados.\n\n**O que muda na prática:** Defina templates e tom de marca nos prompts, alimente o agente com dados reais de produto e meça o desempenho para iterar a qualidade [3]."
    ),
    "IA4-10-monitoramento-de-custos-e-performance": (
        "Monitoramento de Custos e Performance de Prompts",
        "Monitoramento de Custos e Performance de Prompts: Métricas de observabilidade para rastrear o comportamento de agentes em produção",
        "Métricas de observabilidade para rastrear o comportamento de agentes em produção",
        "Agentes em produção são caixas pretas caras: quantos tokens por requisição? Qual a latência por modelo? Qual prompt está falhando? A observabilidade de IA responde — tokens, custo, latência, erros e qualidade por chamada. Este livro ensina a instrumentar agentes em produção.",
        "A observabilidade é o que torna os agentes operáveis: métricas de custo, latência e erros por chamada e por fluxo. Com tracing e dashboards, o time identifica degradação, otimiza prompts e controla o orçamento de IA.",
        "A observabilidade de IA instrumenta cada chamada ao LLM: modelo, provider, tokens de input/output, custo estimado, latência, status e prompt/resposta (com redação de dados sensíveis) [1]. Plataformas como Langfuse e Helicone oferecem tracing, avaliação e dashboards [2].\n\n**Por que importa?** O custo de LLM cresce silenciosamente com o uso; a degradação de qualidade passa despercebida sem avaliação. Métricas por fluxo revelam onde o orçamento e a experiência estão sendo consumidos.\n\n**O que muda na prática:** Instrumente tokens, custo e latência em toda chamada, use tracing para acompanhar fluxos multi-agentes e avalie a qualidade das respostas com datasets de referência [3]."
    ),

    # ═══════════════ SÉRIE IA5 — PROJETOS PRÁTICOS E O FUTURO DA PROFISSÃO ═══════════════
    "IA5-01-chatgpt-customizado-do-zero": (
        "Construindo um ChatGPT Customizado do Zero",
        "Construindo um ChatGPT Customizado do Zero: Arquitetura fullstack de um SaaS de chat com múltiplos modelos e histórico persistente",
        "Arquitetura fullstack de um SaaS de chat com múltiplos modelos e histórico persistente",
        "Nada ensina mais que construir: este livro guia a criação de um ChatGPT customizado do zero — frontend React, backend Node, múltiplos modelos, streaming, histórico persistente e autenticação. Um projeto completo de SaaS que consolida todo o ecossistema.",
        "Construir um chat com múltiplos modelos é o projeto que amarra o ecossistema: streaming, histórico, providers, custo e UX. Ao final do livro, você terá um SaaS funcional — e o entendimento profundo de cada decisão de arquitetura.",
        "A arquitetura de um ChatGPT customizado combina: frontend React com streaming e estados de conversa, backend Node com camada de abstração de providers, banco para persistir histórico e autenticação [1]. O fluxo central: o usuário envia a mensagem, o backend roteia para o modelo configurado, transmite a resposta em stream e salva a conversa [2].\n\n**Por que importa?** Cada camada deste projeto exercita o ecossistema: abstração de providers, gerenciamento de contexto, streaming e persistência. É o projeto que consolida as habilidades Fullstack + IA.\n\n**O que muda na prática:** Implemente em etapas: chat sem histórico → streaming → múltiplos modelos → persistência → autenticação → multiusuário [3]."
    ),
    "IA5-02-assistente-de-programacao-local": (
        "Criando um Assistente de Programação Local",
        "Criando um Assistente de Programação Local: Configurando Llama 3 via Ollama integrado ao seu editor para total privacidade de dados",
        "Configurando Llama 3 via Ollama integrado ao seu editor para total privacidade de dados",
        "E se o seu assistente de código rodasse 100% na sua máquina? Com Ollama e modelos abertos (Llama 3, Mistral, Qwen), é possível: autocomplete e chat privados, sem enviar código para a nuvem. Este livro ensina a configurar o assistente local do zero.",
        "A privacidade do código é um requisito em muitos contextos — e modelos locais entregam isso com custo zero por token. Configurar Ollama + editor com autocomplete e chat local transforma a IDE num ambiente agêntico privado.",
        "Ollama executa modelos de linguagem abertos localmente (Llama 3, Mistral, Qwen) via API compatível com OpenAI [1]. A integração ao editor usa plugins (Continue, Cody, Cline) que apontam para o endpoint local, habilitando chat sobre o código e autocomplete [2].\n\n**Por que importa?** Nenhum código sai da máquina: ideal para código proprietário e ambientes regulados. O custo é a capacidade do modelo (menor que os de nuvem) e a necessidade de hardware razoável.\n\n**O que muda na prática:** Instale o Ollama, baixe o modelo adequado ao seu hardware, aponte o plugin do editor para o endpoint local e avalie a qualidade com tarefas reais [3]."
    ),
    "IA5-03-saas-de-geracao-de-landing-pages": (
        "SaaS de Geração de Landing Pages com IA",
        "SaaS de Geração de Landing Pages com IA: Desenvolvendo uma plataforma onde o usuário descreve o site e o agente constrói e publica",
        "Desenvolvendo uma plataforma onde o usuário descreve o site e o agente constrói e publica",
        "O usuário descreve a landing page em linguagem natural — e o agente gera o código, renderiza o preview e publica. Este é o projeto completo de um SaaS: frontend, backend de geração, sandbox de preview e deploy. Este livro guia a construção ponta a ponta.",
        "O SaaS de landing pages com IA é o caso de uso perfeito para agentes: descrição → código (React/Tailwind) → preview → publicação. O projeto exercita geração, sandbox, filas e deploy — a stack completa do Fullstack agêntico.",
        "A plataforma: o usuário descreve o site (seção, estilo, cores), o backend gera o código com o agente (React + Tailwind), renderiza um preview em sandbox e publica quando aprovado [1]. As filas isolam o trabalho de geração da resposta rápida [2].\n\n**Por que importa?** O produto depende da qualidade da geração e do preview fiel. O sandbox isola a execução do código gerado; o deploy automatizado publica em minutos.\n\n**O que muda na prática:** Construa em etapas: geração com prompt estruturado → preview em iframe/sandbox → edição → deploy via Vercel ou VPS [3]."
    ),
    "IA5-04-atendimento-omnichannel-autonomo": (
        "Sistema de Atendimento Omnichannel Autônomo",
        "Sistema de Atendimento Omnichannel Autônomo: Integrando agentes de IA com WhatsApp, Evolution API e Supabase",
        "Integrando agentes de IA com WhatsApp, Evolution API e Supabase",
        "Atendimento em todos os canais — WhatsApp, site, Instagram — com um agente de IA no centro: o cliente conversa, o agente entende, consulta dados e responde. Evolution API conecta o WhatsApp, e Supabase guarda o estado. Este livro ensina o sistema completo.",
        "O atendimento omnichannel autônomo une o agente de IA ao canal do cliente: mensagens de vários canais entram, o agente responde com contexto e as conversas persistem. A integração com WhatsApp via Evolution API e o backend com Supabase formam a base.",
        "Evolution API expõe a API do WhatsApp (receber e enviar mensagens) via Node [1]. O agente de IA processa cada mensagem: entende a intenção, consulta o conhecimento (RAG) ou a base de clientes, e responde — com escalada para humano quando necessário [2].\n\n**Por que importa?** O atendimento 24/7 com qualidade muda a operação de empresas: triagem, resposta imediata e registro de todas as conversas. A escalada inteligente protege a experiência quando o agente não resolve.\n\n**O que muda na prática:** Integre o canal (Evolution), monte o agente com RAG sobre o conhecimento da empresa, persista conversas no Supabase e defina regras de escalada para humano [3]."
    ),
    "IA5-05-analise-de-contratos-juridicos": (
        "Plataforma de Análise de Contratos Jurídicos",
        "Plataforma de Análise de Contratos Jurídicos: Um sistema fullstack focado em RAG jurídico e extração de cláusulas de risco",
        "Um sistema fullstack focado em RAG jurídico e extração de cláusulas de risco",
        "Contratos são documentos longos, densos e críticos: a IA extrai cláusulas, identifica riscos e resume obrigações. A plataforma jurídica combina RAG, extração estruturada e revisão humana. Este livro guia a construção de um sistema fullstack de análise contratual.",
        "A análise de contratos com IA reduz horas de leitura a minutos: o sistema indexa o contrato, extrai cláusulas estruturadas e sinaliza riscos. A precisão vem do RAG bem montado e da revisão humana nos pontos críticos.",
        "A plataforma: o contrato (PDF) é indexado (chunking semântico + embeddings), e o agente responde perguntas com RAG e extrai campos estruturados (partes, valores, prazos, cláusulas de risco) [1]. O frontend exibe o contrato anotado com os riscos encontrados [2].\n\n**Por que importa?** A precisão é essencial: cláusulas mal interpretadas geram prejuízo. O sistema marca confiança, exige revisão humana para cláusulas críticas e mantém a rastreabilidade das respostas.\n\n**O que muda na prática:** Indexe o contrato com chunks por cláusula, extraia com schema tipado, anote o documento no frontend e exija confirmação humana para riscos altos [3]."
    ),
    "IA5-06-gerenciador-de-projetos-inteligente": (
        "Gerenciador de Projetos Inteligente",
        "Gerenciador de Projetos Inteligente: Um app que decompõe épicos e histórias de usuário em tarefas técnicas detalhadas via agentes",
        "Um app que decompõe épicos e histórias de usuário em tarefas técnicas detalhadas via agentes",
        "Épicos vagos viram tarefas técnicas detalhadas: o gerenciador de projetos com IA decompõe histórias de usuário em tarefas com critérios de aceite, estimativas e dependências. Este livro guia a construção do app que automatiza o planejamento.",
        "A decomposição de trabalho é a parte mais valiosa — e mais manual — do planejamento. Um app com agentes transforma épicos em histórias e tarefas técnicas acionáveis, dando ao time um backlog pronto para execução.",
        "O app recebe o épico ou a história e o agente decompõe: quebra em tarefas técnicas, define critérios de aceite, estima complexidade e identifica dependências [1]. O resultado é um backlog estruturado, revisável e exportável para a ferramenta de gestão [2].\n\n**Por que importa?** A decomposição consistente reduz o viés do planejamento e acelera o refinamento. A revisão humana ajusta o que o agente errou — mas o trabalho pesado de estruturação já está feito.\n\n**O que muda na prática:** Descreva o épico com contexto, peça a decomposição com formato padrão (tarefas, critérios, estimativa) e revise antes de integrar ao board [3]."
    ),
    "IA5-07-o-desenvolvedor-como-diretor-de-orquestra": (
        "O Desenvolvedor como Diretor de Orquestra",
        "O Desenvolvedor como Diretor de Orquestra: Como a transição de escrever código sintático para gerenciar agentes altera a produtividade",
        "Como a transição de escrever código sintático para gerenciar agentes altera a produtividade",
        "O desenvolvedor não escreve cada linha: orquestra. A transição de escrever código sintático para gerenciar agentes — definir intenções, revisar resultados e arquitetar fluxos — muda a produtividade de forma exponencial. Este livro explora a nova natureza do trabalho de engenharia.",
        "A era dos agentes reposiciona o desenvolvedor: de executor de sintaxe a diretor que define o que deve ser feito, como validar e quando intervir. Dominar essa transição é o multiplicador de produtividade da década.",
        "A transição tem três níveis: assistido (autocomplete), delegado (agentes executam tarefas com revisão) e orquestrado (sistemas de agentes coordenados) [1]. A produtividade muda de linear (escrever mais) para exponencial (orquestrar mais) — mas exige novas habilidades: especificação, revisão e arquitetura [2].\n\n**Por que importa?** Escrever código rápido deixa de ser a vantagem; especificar com precisão e revisar com critério tornam-se as habilidades centrais. O valor move-se para o julgamento humano sobre o que construir e como validar.\n\n**O que muda na prática:** Pratique especificar tarefas com critérios de aceite claros, revisar diffs de agentes com rigor e desenhar fluxos de agentes com supervisão nos pontos críticos [3]."
    ),
    "IA5-08-etica-direitos-autorais-lgpd": (
        "Ética, Direitos Autorais e LGPD na Era dos Agentes",
        "Ética, Direitos Autorais e LGPD na Era dos Agentes: Desafios legais do uso de código e dados gerados por inteligência artificial",
        "Desafios legais do uso de código e dados gerados por inteligência artificial",
        "Quem é o dono do código gerado por IA? Dados de clientes podem alimentar modelos? A LGPD exige transparência sobre o uso de IA? As respostas definem riscos legais e éticos reais para quem constrói com agentes. Este livro mapeia o terreno legal e ético.",
        "A era dos agentes levanta questões que o direito ainda está assimilando: autoria de código gerado, responsabilidade por erros, proteção de dados pessoais e uso de conteúdo protegido. Conhecer o terreno reduz riscos e orienta decisões de produto.",
        "A LGPD (Lei Geral de Proteção de Dados) exige base legal, minimização e transparência no tratamento de dados pessoais — inclusive quando alimentam LLMs [1]. A autoria do código gerado por IA é disputada: a maioria das jurisdições não reconhece direitos autorais de máquina, mas a responsabilidade pelo uso é de quem publica [2].\n\n**Por que importa?** Usar dados de clientes para treinar ou contextuar modelos pode violar a LGPD; depender de código gerado sem revisão transfere risco; e o uso de conteúdo protegido em treinamento gera disputas em andamento.\n\n**O que muda na prática:** Documente a base legal dos dados, evite enviar dados pessoais a providers sem anonimização, revise e teste código gerado e mantenha política clara de uso de IA [3]."
    ),
    "IA5-09-arquitetura-resiliente-a-falhas-de-llm": (
        "Arquitetura de Sistemas Resilientes a Falhas de LLM",
        "Arquitetura de Sistemas Resilientes a Falhas de LLM: Como projetar aplicações fullstack que continuam funcionando quando o modelo de IA falha",
        "Como projetar aplicações fullstack que continuam funcionando quando o modelo de IA falha",
        "O modelo de IA vai falhar: rate limits, timeouts, respostas ruins e indisponibilidade são parte da operação. A arquitetura resiliente antecipa essas falhas — fallbacks, cache, degradação graciosa e circuit breakers. Este livro ensina a projetar sistemas que sobrevivem à queda do modelo.",
        "Depender de um único provider sem plano de contingência é o erro arquitetural mais comum em IA. Resiliência significa: fallback entre providers, cache de respostas comuns, degradação graciosa e isolamento da falha para que o resto do sistema continue.",
        "A resiliência a falhas de LLM usa padrões clássicos adaptados: fallback entre providers, retry com backoff, circuit breaker (parar de chamar o modelo após falhas sucessivas), cache de respostas e modo degradado (respostas pré-definidas ou alternativas locais) [1]. A aplicação principal não pode depender da disponibilidade do modelo [2].\n\n**Por que importa?** Um rate limit do provider não deve derrubar o chat do usuário. A degradação graciosa — avisar, usar cache, sugerir alternativa — preserva a experiência mesmo na falha.\n\n**O que muda na prática:** Implemente fallback multi-provider, cache semântico para consultas comuns, circuit breaker por provider e modos de degradação documentados [3]."
    ),
    "IA5-10-o-futuro-do-desenvolvimento-fullstack": (
        "O Futuro do Desenvolvimento Fullstack (2030+)",
        "O Futuro do Desenvolvimento Fullstack (2030+): Tendências de computação autônoma, computação quântica assistida e o novo perfil profissional",
        "Tendências de computação autônoma, computação quântica assistida e o novo perfil profissional",
        "Para onde vamos? Computação autônoma (agentes que constroem e operam sistemas), assistência quântica em problemas de otimização e um perfil profissional que orquestra em vez de implementar. Este livro explora as tendências que definirão a próxima década do desenvolvimento.",
        "O futuro não é substituição: é transformação do papel. Computação autônoma, integração com modelos cada vez mais capazes e a evolução do perfil do desenvolvedor — de escritor de código a arquiteto de sistemas cognitivos — definem a próxima década.",
        "As tendências: computação autônoma (agentes que projetam, codificam, testam e operam com supervisão humana), modelagem de domínio mais forte, e a computação quântica assistida em problemas de otimização específicos [1]. O perfil profissional evolui para o diretor de sistemas: especificar, orquestrar, revisar e garantir qualidade [2].\n\n**Por que importa?** As habilidades de maior valor mudam: pensamento sistêmico, ética, arquitetura e julgamento. O desenvolvedor que domina a orquestração de agentes e a leitura crítica de resultados se posiciona à frente da curva.\n\n**O que muda na prática:** Invista em fundamentos (arquitetura, domínio, testes), aprenda a especificar e revisar trabalho de agentes e acompanhe as plataformas de computação autônoma que emergem [3]."
    ),
}

# Auto-gerar lista completa de slugs
SLUGS_IA = list(LIVROS_IA.keys())
