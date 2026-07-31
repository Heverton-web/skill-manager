#!/usr/bin/env python3
"""
Dados das 5 Séries de Livros de Planejamento Estratégico de Marketing (MK1-MK5)
Cada série tem ~20 livros, cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-planejamento.py e compilar-para-pdf.py
"""

SERIES_PLANEJAMENTO = {
    "MK1": {"nome": "Fundamentos do Planejamento Integrado", "prefixo": "MK1"},
    "MK2": {"nome": "Inteligência Artificial Aplicada ao Planejamento", "prefixo": "MK2"},
    "MK3": {"nome": "Funil de Atração, Conversão e Tráfego", "prefixo": "MK3"},
    "MK4": {"nome": "Operações, Processos e Gestão de Equipes de Marketing", "prefixo": "MK4"},
    "MK5": {"nome": "Estudos de Caso Práticos, Métricas e Retorno Financeiro", "prefixo": "MK5"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
SERIES_PARTES = {
    "MK1": ["Fundamentos do Planejamento Integrado", "Diagnóstico e Estratégia", "Governança e Rotina de Alinhamento", "Execução e Evolução do Plano"],
    "MK2": ["Fundamentos da IA no Planejamento", "Técnicas de IA para Marketing", "Automação, Dados e Conteúdo", "Governança, Ética e Futuro"],
    "MK3": ["Fundamentos do Funil e Atração", "Conversão e Persuasão", "Relacionamento e Retenção", "Otimização e Escala"],
    "MK4": ["Fundamentos da Operação de Marketing", "Processos e Ferramentas", "Pessoas e Conhecimento", "Riscos, Conformidade e Melhoria"],
    "MK5": ["Fundamentos da Mensuração Financeira", "Análise de Canais e Retenção", "Modelos, Previsão e Relatórios", "Casos, Otimização e Fechamento"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_PLANEJAMENTO = {
    # ═══════════════ SÉRIE MK1 — FUNDAMENTOS DO PLANEJAMENTO INTEGRADO ═══════════════
    "MK1-01-alinhando-marketing-classico-digital": (
        "Alinhando o Marketing Clássico com o Digital",
        "Alinhando o Marketing Clássico com o Digital: Integrando os 4 Ps, posicionamento e canais físicos à pressão por eficiência",
        "Integrando os 4 Ps, posicionamento e canais físicos à pressão por eficiência de custos e à realidade digital",
        "O marketing clássico — os 4 Ps, o posicionamento e os canais físicos e offline — não morreu: ele foi absorvido por um ecossistema híbrido. Este livro ensina a alinhar as tradições do marketing com a realidade digital e a pressão por eficiência de custos, sem descartar o que já funcionava.",
        "Alinhar o marketing clássico com o digital não é abandonar um em favor do outro: é construir uma ponte. Quem domina essa integração multiplica o alcance dos canais físicos, dá novo significado aos 4 Ps e transforma a pressão por eficiência em vantagem competitiva.",
        "O marketing clássico foi estruturado por McCarthy em torno dos 4 Ps — Produto, Preço, Praça e Promoção — e consolidado por Kotler como a espinha dorsal da disciplina [1]. O que mudou não foram os pilares, mas o ambiente em que operam: o digital acrescentou dados, velocidade e mensuração a cada um deles [2].\\n\\n**Por que importa?** Empresas que ignoram o clássico reinventam a roda com prejuízo; empresas que ignoram o digital ficam invisíveis. A integração exige traduzir cada P para o ecossistema híbrido: a Praça virou omnichannel, a Promoção virou tráfego e conteúdo, e o Preço passou a ser testado em tempo real [3].\\n\\n**O que muda na prática:** Em vez de escolher entre panfleto e anúncio pago, o planejamento integrado define onde cada centavo cria atrito mínimo e retorno máximo — medindo ambos com as mesmas métricas."
    ),
    "MK1-02-diagnostico-360-do-negocio": (
        "Diagnóstico 360° do Negócio",
        "Diagnóstico 360° do Negócio: Como auditar a saúde atual da empresa cruzando dados financeiros, operacionais e comerciais",
        "Como auditar a saúde atual da empresa cruzando dados financeiros, operacionais e comerciais",
        "Nenhum plano de marketing sobrevive ao primeiro mês se a empresa não conhece a própria saúde. O Diagnóstico 360° cruza dados financeiros, operacionais e comerciais para revelar, com números, onde o negócio está forte e onde sangra. Este livro entrega a ferramenta completa para essa auditoria.",
        "O diagnóstico não é uma formalidade: é a fundação do planejamento. Cruzar finanças, operação e comércio em uma única leitura transforma suposições em hipóteses testáveis e revela as alavancas reais de crescimento antes de qualquer investimento em marketing.",
        "O diagnóstico 360° é um processo estruturado de auditoria que combina três lentes: financeira (caixa, margem, custos fixos), operacional (capacidade de entrega, estoque, processo) e comercial (vendas, canais, clientes) [1]. O cruzamento dessas lentes revela gargalos invisíveis a uma análise isolada [2].\\n\\n**Por que importa?** Investir em tráfego antes do diagnóstico é regar uma planta sem saber se ela tem raiz. Empresas que auditam primeiro descobrem, por exemplo, que a margem de um produto carro-chefe não suporta o CAC dos anúncios — e corrigem a oferta antes de escalar [3].\\n\\n**O que muda na prática:** Uma planilha única, alimentada mensalmente, cruza ponto de equilíbrio, ticket médio e capacidade operacional — e vira o painel de referência de todas as decisões de marketing."
    ),
    "MK1-03-matriz-de-posicionamento-e-proposta-de-valor": (
        "Matriz de Posicionamento e Proposta de Valor",
        "Matriz de Posicionamento e Proposta de Valor: Definindo o diferencial competitivo real em mercados altamente saturados",
        "Definindo o diferencial competitivo real em mercados altamente saturados",
        "Em mercados saturados, quem não se posiciona vira commodity. A Matriz de Posicionamento combina a percepção do cliente com a proposta de valor da empresa para encontrar o espaço defensável. Este livro ensina a construir essa matriz e a transformá-la em mensagens, preço e canais.",
        "Posicionamento não é slogan: é a decisão sobre o espaço que a marca ocupará na mente do cliente e o motivo real para preferi-la. Com uma matriz bem construída, até mercados comoditizados oferecem um oceano azul — desde que a proposta de valor seja verdadeira e comunicada com consistência.",
        "A matriz de posicionamento cruza dois eixos: o que o cliente valoriza (eixos de percepção) e o que a empresa entrega de forma superior (capacidades reais) [1]. A proposta de valor — popularizada por Osterwalder no Value Proposition Canvas — detalha as dores, ganhos e tarefas do cliente que a oferta atende [2].\\n\\n**Por que importa?** Em mercados saturados, o diferencial raramente é o produto: é a combinação de atributos que ninguém mais entrega com aquela consistência. Posicionar é escolher o que a marca promete e, principalmente, o que ela se recusa a prometer [3].\\n\\n**O que muda na prática:** Preencha a matriz com dados de pesquisa (não com achismos), valide a proposta de valor com clientes reais e derive dela a mensagem, o preço e a seleção de canais."
    ),
    "MK1-04-novo-mix-de-marketing-4ps-expandidos": (
        "O Novo Mix de Marketing (4 Ps Expandidos)",
        "O Novo Mix de Marketing (4 Ps Expandidos): Adaptando Produto, Preço, Praça e Promoção para ecossistemas híbridos",
        "Adaptando Produto, Preço, Praça e Promoção para ecossistemas híbridos (físico + digital)",
        "Os 4 Ps continuam vivos, mas expandidos: o Produto virou experiência, o Preço virou dinâmico, a Praça virou omnichannel e a Promoção virou conteúdo e tráfego. Este livro adapta o mix clássico para ecossistemas híbridos, onde físico e digital se alimentam.",
        "O mix expandido não substitui McCarthy — o expande. Cada P ganha novas dimensões que o marketing clássico não previa, e o planejamento integrado precisa dominar ambas as linguagens para desenhar ofertas que vendam na loja e no site com a mesma coerência.",
        "O mix de marketing clássico — Produto, Preço, Praça e Promoção — foi proposto por McCarthy e popularizado por Kotler como as variáveis controláveis da oferta [1]. No ecossistema híbrido, cada P se expande: o Produto inclui a experiência digital e o pós-venda; o Preço incorpora testes A/B e precificação dinâmica; a Praça integra loja física, e-commerce e marketplaces; a Promoção combina tráfego pago, orgânico e relacionamento [2].\\n\\n**Por que importa?** Decisões tomadas em silo quebram a coerência da oferta: um preço agressivo no site canibaliza a loja, uma promoção digital promete o que a operação física não entrega. O mix expandido força a visão integrada [3].\\n\\n**O que muda na prática:** Revise os 4 Ps como um sistema único a cada trimestre, com métricas próprias por P, e garanta que a promessa de um P seja cumprida pelos outros três."
    ),
    "MK1-05-analise-de-concorrencia-e-inteligencia-competitiva": (
        "Análise de Concorrência e Inteligência Competitiva",
        "Análise de Concorrência e Inteligência Competitiva: Mapeando o posicionamento de rivais diretos e indiretos no cenário local e online",
        "Mapeando o posicionamento de rivais diretos e indiretos no cenário local e online",
        "Você não compete apenas com a loja da esquina: compete com todo mundo que disputa a atenção e o bolso do seu cliente, online e offline. Este livro ensina a mapear concorrentes diretos e indiretos, monitorar seus movimentos e transformar inteligência competitiva em decisão.",
        "Inteligência competitiva não é espionagem: é observação sistemática. Saber onde os rivais atacam, o que oferecem e onde vacilam permite antecipar movimentos, encontrar espaços vagos e calibrar preço, mensagem e canais com base em evidência.",
        "A análise competitiva distingue rivais diretos (mesma oferta, mesmo cliente) de indiretos (mesmo cliente, oferta diferente que resolve a mesma dor) [1]. O framework de Porter para as cinco forças amplia a lente para substitutos, novos entrantes e poder de barganha [2].\\n\\n**Por que importa?** Concorrentes locais competem por rua; concorrentes digitais competem por atenção 24 horas por dia. Mapear preço, posicionamento, canais e conteúdo dos rivais — com rotinas de monitoramento — gera um mapa de oportunidades que o marketing transforma em campanha [3].\\n\\n**O que muda na prática:** Monte uma tabela de concorrentes (oferta, preço, canais, pontos fortes e fracos), revise-a mensalmente e use-a para decidir onde atacar e onde se diferenciar."
    ),
    "MK1-06-personas-baseadas-em-comportamento-real": (
        "Definição de Personas Baseadas em Comportamento Real",
        "Definição de Personas Baseadas em Comportamento Real: Indo além da demografia para entender dores, desejos e jornadas de decisão reais",
        "Indo além da demografia para entender dores, desejos e jornadas de decisão reais",
        "Persona não é um cartaz demográfico com nome e idade: é um modelo de comportamento. Este livro ensina a construir personas a partir de dados reais — entrevistas, histórico de compras e comportamento digital — para entender dores, desejos e jornadas de decisão de verdade.",
        "Personas baseadas em comportamento sobrevivem à mudança de moda: elas descrevem como o cliente decide, não apenas quem ele é. Com essas personas, o marketing fala a língua da dor e da motivação, e cada campanha nasce de uma hipótese testável sobre o comportamento real.",
        "Personas demográficas descrevem quem é o cliente; personas comportamentais explicam por que ele compra — quais dores o motivam, quais gatilhos ativam a decisão e por quais etapas ele passa até a compra [1]. A construção usa fontes reais: entrevistas com clientes atuais, análise de dados de atendimento, comportamento em site e redes, e conversas perdidas [2].\\n\\n**Por que importa?** Mensagens construídas sobre demografia convertem menos porque falam com um retrato, não com uma decisão. Personas comportamentais orientam oferta, copy, canais e objeções com base no que o cliente realmente vive [3].\\n\\n**O que muda na prática:** Entreviste 5 a 10 clientes reais, categorize dores e gatilhos, e transforme os achados em 2 a 4 personas que orientam toda a comunicação da empresa."
    ),
    "MK1-07-alinhamento-marketing-vendas-sla": (
        "Alinhamento entre Marketing e Vendas (SLA)",
        "Alinhamento entre Marketing e Vendas (SLA): Estabelecendo acordos claros de passagem de bastão entre leads gerados e o time comercial",
        "Estabelecendo acordos claros de passagem de bastão entre leads gerados e o time comercial",
        "O marketing gera leads que o comercial ignora; o comercial reclama de leads que o marketing considera ótimos. O SLA entre as áreas — um acordo explícito de passagem de bastão — resolve o conflito com definições, prazos e responsabilidades. Este livro ensina a desenhá-lo e operá-lo.",
        "O SLA não é burocracia: é o contrato que transforma o funil em uma operação previsível. Quando marketing e vendas concordam sobre o que é um lead qualificado, em quanto tempo ele deve ser contatado e o que cada lado entrega, a taxa de conversão deixa de depender de relacionamento pessoal.",
        "O SLA (Service Level Agreement) entre marketing e vendas define o contrato de passagem de bastão: critérios de qualificação (MQL vs. SQL), velocidade de resposta, responsabilidades de cada área e métricas compartilhadas [1]. O Marketing Qualified Lead (MQL) é o lead que demonstrou interesse; o Sales Qualified Lead (SQL) é o que está pronto para negociar [2].\\n\\n**Por que importa?** Estudos mostram que leads contatados em minutos convertem muito mais que leads contatados em dias. Sem SLA, o marketing otimiza volume e o comercial otimiza fechamento — objetivos opostos que sabotam o funil [3].\\n\\n**O que muda na prática:** Defina os critérios de MQL e SQL por escrito, estabeleça o tempo máximo de resposta e crie uma reunião semanal única onde ambos os times olham as mesmas métricas."
    ),
    "MK1-08-orcamento-e-alocacao-de-recursos": (
        "Orçamento e Alocação de Recursos (Budget Inteligente)",
        "Orçamento e Alocação de Recursos (Budget Inteligente): Como definir quanto investir no ciclo sem queimar caixa em ações sem retorno",
        "Como definir quanto investir no ciclo sem queimar caixa em ações sem retorno",
        "Investir em marketing sem definir o orçamento é uma roleta-russa com o caixa da empresa. O Budget Inteligente parte do ponto de equilíbrio e do CAC tolerável para definir quanto investir, em que canal e com que prazo de retorno. Este livro entrega a matemática e o processo de alocação.",
        "Orçamento inteligente é aquele que a empresa consegue sustentar sem quebrar o caixa: ele parte de margem, ponto de equilíbrio e LTV, e só então define verba. Com essa base, cada real investido tem critério de corte e prazo de retorno definidos antes do primeiro clique.",
        "O orçamento de marketing precisa derivar de três números: ponto de equilíbrio (quanto a empresa precisa faturar para não perder dinheiro), margem de contribuição (quanto sobra por venda) e LTV (valor do cliente ao longo do tempo) [1]. Com eles, define-se o CAC máximo tolerável e, a partir daí, a verba de aquisição [2].\\n\\n**Por que importa?** Empresas que definem orçamento por 'quanto sobrar' ou por imitação da concorrência queimam caixa em ações sem retorno. A alocação por canal, por sua vez, deve seguir o retorno comprovado — e não a preferência do gestor [3].\\n\\n**O que muda na prática:** Crie a planilha de orçamento com margem, break-even e CAC máximo; aloque verba por canal com base em retorno histórico e revise a alocação mensalmente."
    ),
    "MK1-09-mapeamento-da-jornada-do-cliente-omnicanal": (
        "Mapeamento da Jornada do Cliente Omnicanal",
        "Mapeamento da Jornada do Cliente Omnicanal: Desenhando todos os pontos de contato do consumidor com a marca, do offline ao online",
        "Desenhando todos os pontos de contato do consumidor com a marca, do offline ao online",
        "O cliente não vive em funil: vive em jornada — e essa jornada atravessa Instagram, loja física, WhatsApp e avaliações online. O mapeamento omnicanal desenha todos os pontos de contato e revela onde a experiência flui e onde ela quebra. Este livro ensina a construir e usar esse mapa.",
        "Mapear a jornada é enxergar o negócio pelos olhos do cliente. O mapa omnicanal mostra como os canais se conectam (ou se ignoram) e onde estão os momentos de verdade que decidem a compra — permitindo investir exatamente nos pontos de maior impacto.",
        "A jornada do cliente é o caminho completo — desde a descoberta até o pós-venda — atravessando múltiplos canais físicos e digitais [1]. O mapeamento (customer journey mapping) documenta cada etapa, os pontos de contato, as emoções e os atritos do cliente [2].\\n\\n**Por que importa?** Em uma jornada omnicanal, o cliente pesquisa no celular, visita a loja, confere avaliações e fecha no WhatsApp. Cada ruptura entre canais — preço diferente, atendimento perdido, promessa quebrada — gera abandono. O mapa revela esses momentos [3].\\n\\n**O que muda na prática:** Liste as etapas da jornada, os canais envolvidos e os atritos de cada uma; priorize as correções de maior impacto e meça a jornada com dados reais de cada ponto de contato."
    ),
    "MK1-10-metas-e-okrs-comerciais": (
        "Definição de Metas e OKRs Comerciais",
        "Definição de Metas e OKRs Comerciais: Metodologias práticas para desdobrar a meta de faturamento em objetivos de marketing executáveis",
        "Metodologias práticas para desdobrar a meta de faturamento em objetivos de marketing executáveis",
        "A meta de faturamento do ano vira pó se ninguém sabe como o marketing contribui para ela. OKRs — Objetivos e Resultados-Chave — desdobram a meta financeira em objetivos de marketing mensuráveis. Este livro ensina a aplicar a metodologia do faturamento ao time.",
        "OKR é a ponte entre a meta da diretoria e a agenda semanal do time de marketing. Quando cada objetivo tem resultados-chave mensuráveis e alinhados ao funil, o faturamento deixa de ser um desejo e vira uma equação que a equipe entende e opera.",
        "OKR (Objectives and Key Results) é uma metodologia de definição de metas criada por Andy Grove e popularizada no Google: objetivos são direções qualitativas; resultados-chave são métricas quantificáveis que provam o avanço [1]. No marketing, o objetivo deriva do faturamento e os resultados-chave cobrem funil, CAC e receita [2].\\n\\n**Por que importa?** Metas vagas ('aumentar vendas') não geram ação; OKRs forçam a decomposição: se a meta é R$ 1 milhão, quantos leads, com que conversão e qual CAC sustentam a equação? Essa decomposição é o plano executável [3].\\n\\n**O que muda na prática:** Desdobre a meta anual em OKRs trimestrais de marketing, com 2 a 4 resultados-chave por objetivo, e revise o progresso a cada semana em reunião de 30 minutos."
    ),
    "MK1-11-governanca-e-rotina-de-alinhamento": (
        "Governança e Rotina de Alinhamento",
        "Governança e Rotina de Alinhamento: Criando comitês semanais e mensais de acompanhamento de performance de marketing na empresa",
        "Criando comitês semanais e mensais de acompanhamento de performance de marketing na empresa",
        "O plano de marketing morre quando não há rotina para acompanhá-lo. Comitês semanais e mensais de performance criam a governança que mantém a estratégia viva: decisões rápidas na semana, correções de rota no mês. Este livro desenha essa rotina de alinhamento.",
        "Governança é o sistema que garante que o planejamento não vire um documento esquecido. Com reuniões curtas, pautas fixas e métricas únicas, a empresa cria o hábito de decidir com dados — e o time de marketing ganha o patrocínio e o alinhamento que precisa para executar.",
        "A governança de marketing define os ritos de acompanhamento: reunião semanal de operação (o que entregamos, o que está travado, o que ajustar) e reunião mensal de estratégia (resultados, lições, realocação de recursos) [1]. Cada rito tem pauta fixa, participantes definidos e decisões registradas [2].\\n\\n**Por que importa?** Sem rotina, o plano é uma foto; com rotina, é um ciclo vivo. A reunião semanal detecta desvios em dias; a mensal corrige rota com dados suficientes. Juntas, elas blindam a execução contra o caos do dia a dia [3].\\n\\n**O que muda na prática:** Institua a reunião semanal (30 min, métricas do funil) e a mensal (1h, estratégia e orçamento), com pauta fixa e atas curtas que geram decisões rastreáveis."
    ),
    "MK1-12-gestao-de-cac-e-ltv": (
        "Gestão de Custos de Aquisição (CAC) e LTV",
        "Gestão de Custos de Aquisição (CAC) e LTV: Calculando a sustentabilidade financeira das campanhas de captação de clientes",
        "Calculando a sustentabilidade financeira das campanhas de captação de clientes",
        "CAC e LTV são os dois números que decidem se a empresa cresce ou afunda: quanto custa conquistar um cliente e quanto ele vale ao longo do tempo. Este livro ensina a calcular ambos com precisão e a usá-los para avaliar a sustentabilidade de cada campanha.",
        "A relação LTV/CAC é o termômetro da saúde comercial: abaixo de 3, a empresa paga para crescer; acima, cresce com margem. Dominar esses indicadores transforma decisões de campanha — canal, verba, oferta — em escolhas matemáticas e não em apostas.",
        "CAC (Customer Acquisition Cost) é o custo total de aquisição dividido pelo número de clientes conquistados no período — incluindo mídia, ferramentas e salários do time [1]. LTV (Lifetime Value) é o lucro que o cliente gera durante todo o relacionamento com a empresa [2].\\n\\n**Por que importa?** A regra prática de sustentabilidade é LTV ≥ 3× CAC: abaixo disso, cada cliente novo destrói valor. A gestão ativa envolve reduzir o CAC (melhor conversão, melhor segmentação) e elevar o LTV (retenção, upsell, recorrência) [3].\\n\\n**O que muda na prática:** Monte a planilha de CAC e LTV por canal e por campanha, calcule o payback do investimento e estabeleça o gatilho de corte: campanha com LTV/CAC abaixo do piso é pausada e corrigida."
    ),
    "MK1-13-sazonalidade-e-calendario-promocional": (
        "Planejamento de Sazonalidade e Calendário Promocional",
        "Planejamento de Sazonalidade e Calendário Promocional: Antecipando picos de vendas, datas comemorativas e campanhas sazonais do ano",
        "Antecipando picos de vendas, datas comemorativas e campanhas sazonais do ano",
        "Vender bem em datas comemorativas não é sorte: é planejamento. O calendário promocional antecipa picos de demanda, datas de varejo e sazonalidade do negócio para que a operação, o estoque e o marketing estejam prontos no momento certo. Este livro ensina a construí-lo.",
        "O calendário promocional transforma o ano em uma sequência de oportunidades planejadas: cada data relevante tem objetivo, oferta, verba e criativo definidos com antecedência. Planejar a sazonalidade evita correr atrás do prejuízo quando a demanda explode.",
        "A sazonalidade é o padrão regular de variação da demanda ao longo do ano — determinada por clima, datas comemorativas, época escolar e ciclos do negócio [1]. O calendário promocional organiza as datas relevantes do ano e define para cada uma: objetivo (lucro, caixa, giro), oferta, verba e criativos [2].\\n\\n**Por que importa?** Datas como Black Friday concentram parte relevante do faturamento anual do varejo. Quem planeja com meses de antecedência negocia estoque, prepara a operação e domina o tráfego; quem improvisa paga mais caro e entrega pior [3].\\n\\n**O que muda na prática:** Construa o calendário anual com as datas relevantes do seu negócio, defina o objetivo de cada campanha e prepare conteúdo, verba e estoque com 60 a 90 dias de antecedência."
    ),
    "MK1-14-modelos-de-atribuicao-de-vendas": (
        "Modelos de Atribuição de Vendas",
        "Modelos de Atribuição de Vendas: Descobrindo qual canal (físico, indicação, anúncio ou orgânico) realmente traz dinheiro para o caixa",
        "Descobrindo qual canal (físico, indicação, anúncio ou orgânico) realmente traz dinheiro para o caixa",
        "Qual canal realmente vende: o anúncio, o orgânico, a indicação ou a loja física? A atribuição de vendas responde essa pergunta com método — e impede que o orçamento vá para o canal errado. Este livro ensina os modelos de atribuição e como aplicá-los no dia a dia.",
        "Sem atribuição, o marketing comemora leads que não vendem e corta canais que vendem por baixo dos panos. A atribuição distribui o crédito da venda entre os pontos de contato e revela o custo real de cada canal — a base para alocar verba com precisão.",
        "A atribuição de vendas determina como o crédito de uma conversão é distribuído entre os canais que participaram da jornada [1]. Os modelos variam em complexidade: last-click (tudo para o último toque), first-click (tudo para o primeiro), linear (média) e data-driven (pesos calculados por dados) [2].\\n\\n**Por que importa?** O last-click supervaloriza o canal final e mata o topo do funil; o first-click faz o oposto. Em jornadas omnicanal — offline e online — a atribuição exige código de cupom, QR code e pesquisa de origem para rastrear a loja física [3].\\n\\n**O que muda na prática:** Escolha um modelo alinhado à sua jornada, rastreie as origens de cada venda (cupons, QR, UTM, pesquisa) e revise a alocação de verba com base no crédito real de cada canal."
    ),
    "MK1-15-gestao-de-riscos-e-planos-de-contingencia": (
        "Gestão de Riscos e Planos de Contingência",
        "Gestão de Riscos e Planos de Contingência: Como proteger o negócio de crises de reputação, oscilações de mercado ou quedas de tráfego",
        "Como proteger o negócio de crises de reputação, oscilações de mercado ou quedas de tráfego",
        "Crises não avisam: avaliação negativa em massa, bloqueio de conta de anúncios, oscilação de mercado. A gestão de riscos mapeia as ameaças ao plano de marketing e os planos de contingência definem a resposta antes que o problema vire tragédia. Este livro entrega o framework completo.",
        "Risco não é pessimismo: é preparo. Empresas que mapeiam ameaças e ensaiam respostas atravessam crises com dano mínimo — e saem mais fortes que as que improvisaram. O plano de contingência transforma o caos em um procedimento conhecido.",
        "A gestão de riscos identifica, avalia e prioriza as ameaças ao negócio — reputação, dependência de canais, concentração de tráfego, oscilações de mercado [1]. Para cada risco relevante, o plano de contingência define gatilhos de acionamento, responsáveis e passos de resposta [2].\\n\\n**Por que importa?** A maior parte das crises de marketing é previsível em categoria: bloqueios de conta, mudanças de algoritmo, crise de avaliações, problemas de reputação. Ter o playbook pronto reduz o tempo de resposta de dias para horas — e o dano proporcionalmente [3].\\n\\n**O que muda na prática:** Liste os riscos top 5 do seu negócio, defina gatilho, resposta e responsável para cada um e revise a lista a cada trimestre, ensaiando a resposta dos riscos críticos."
    ),
    "MK1-16-documentacao-do-plano-estrategico-masterbook": (
        "Documentação do Plano Estratégico (O Masterbook)",
        "Documentação do Plano Estratégico (O Masterbook): Estruturando o documento final de planejamento para ser lido e executado por toda a equipe",
        "Estruturando o documento final de planejamento para ser lido e executado por toda a equipe",
        "Um plano estratégico que ninguém lê não existe. O Masterbook é o documento final de planejamento — organizado para ser lido, entendido e executado por toda a equipe. Este livro ensina a estruturá-lo: da visão e diagnóstico até as metas, canais e calendário.",
        "O Masterbook transforma meses de análise em um instrumento de execução. Bem estruturado, ele alinha a equipe inteira — diretoria, marketing, vendas e operação — em torno das mesmas prioridades e se torna o documento de referência de todas as decisões do ano.",
        "Um masterbook de planejamento é um documento vivo que condensa: visão e objetivos, diagnóstico 360°, posicionamento, personas, metas e OKRs, mix de canais, orçamento, calendário e governança [1]. A estrutura segue uma lógica narrativa: onde estamos, para onde vamos, como chegamos e como medimos [2].\\n\\n**Por que importa?** Documentos de 200 páginas viram enfeite; documentos executáveis são lidos e consultados. O masterbook bom é curto na leitura (sumário executivo para a diretoria), completo na profundidade (anexos por área) e vivo (revisado trimestralmente) [3].\\n\\n**O que muda na prática:** Estruture o masterbook em 7 seções fixas, escreva o sumário executivo de 1 página para a diretoria e defina a cadência de revisão trimestral com responsáveis por seção."
    ),
    "MK1-17-cultura-orientada-a-dados": (
        "Cultura Orientada a Dados na Pequena e Média Empresa",
        "Cultura Orientada a Dados na Pequena e Média Empresa: Criando o hábito de decidir com base em métricas e não em achismos",
        "Criando o hábito de decidir com base em métricas e não em achismos",
        "Na pequena e média empresa, a maioria das decisões de marketing ainda é tomada por achismo — e isso custa caro. A cultura orientada a dados cria o hábito de perguntar 'o que os números dizem?' antes de cada decisão. Este livro mostra como implantá-la sem burocracia.",
        "Cultura de dados não é sobre ferramentas caras: é sobre o hábito. Quando cada decisão de campanha, preço e canal é precedida de uma pergunta respondível com números, o time aprende mais rápido, erra menos e acumula um ativo raro: a capacidade de prever resultados.",
        "A cultura orientada a dados é o conjunto de hábitos, ferramentas e rituais que colocam as métricas no centro das decisões [1]. Ela exige três elementos: dados confiáveis (coleta limpa), métricas acordadas (definições únicas) e rituais de leitura (reuniões que olham os números antes de opinar) [2].\\n\\n**Por que importa?** O achismo tem um custo invisível: campanhas que poderiam ter sido otimizadas, canais que sugavam verba sem retorno e decisões repetidas que não acumulavam aprendizado. A cultura de dados transforma erro em insumo de melhoria [3].\\n\\n**O que muda na prática:** Comece pequeno: defina as 5 métricas-mestre da empresa, crie a reunião semanal de números e institua a regra de 'todo debate termina com uma métrica acordada'."
    ),
    "MK1-18-integracao-de-canais-tradicionais-com-digital": (
        "Integração de Canais Tradicionais (PDV/Mídia Local) com o Digital",
        "Integração de Canais Tradicionais (PDV/Mídia Local) com o Digital: Unindo panfletos, fachadas, eventos e feiras ao ecossistema online",
        "Unindo panfletos, fachadas, eventos e feiras ao ecossistema online",
        "O panfleto não morreu: ganhou QR code. O PDV não perdeu espaço: virou ponto de conversão do digital. A integração de canais tradicionais — panfletos, fachadas, eventos e feiras — com o ecossistema online multiplica o alcance de ambos. Este livro ensina a união na prática.",
        "Canais tradicionais geram confiança e presença local; canais digitais geram alcance e mensuração. Integrá-los — cada material offline com destinação online, cada evento com captura digital — transforma o marketing local em um sistema com retorno rastreável.",
        "A integração de mídia local com o digital usa os canais tradicionais como porta de entrada para o ecossistema online: QR codes em panfletos e embalagens, fachadas que direcionam para o WhatsApp, eventos que capturam leads via landing page [1]. Cada ponto de contato offline ganha um destino digital mensurável [2].\\n\\n**Por que importa?** O cliente local confia no que vê na rua, mas decide pelo que vê online. Integrar os canais permite medir o retorno do offline (via cupom, QR e pesquisa de origem) e alimentar o digital com a autoridade da presença local [3].\\n\\n**O que muda na prática:** Dê a cada material offline um destino digital rastreável (QR/URL única), padronize a captação em eventos e feiras e meça a conversão de cada ação física como se fosse uma campanha digital."
    ),
    "MK1-19-auditoria-de-ativos-de-marca": (
        "Auditoria de Ativos de Marca",
        "Auditoria de Ativos de Marca: Organizando logotipos, manuais de identidade visual, domínios, redes sociais e materiais impressos",
        "Organizando logotipos, manuais de identidade visual, domínios, redes sociais e materiais impressos",
        "Sua marca está organizada ou espalhada? A auditoria de ativos de marca mapeia logotipos, manuais, domínios, redes sociais e materiais impressos — e revela inconsistências que corroem a confiança. Este livro ensina a auditar, organizar e proteger esses ativos.",
        "Ativos de marca desorganizados geram comunicação inconsistente, retrabalho e até perda de domínio ou conta. A auditoria transforma o caos em um acervo único e versionado — e garante que qualquer material produzido reforce, em vez de enfraquecer, a marca.",
        "A auditoria de ativos de marca inventaria tudo que comunica a marca: logotipos em todas as versões, manual de identidade visual, tipografia e cores, domínios e hospedagens, perfis em redes sociais, materiais impressos e modelos de apresentação [1]. O inventário revela inconsistências — logo antigo no PDV, cores divergentes, domínio perdido [2].\\n\\n**Por que importa?** Cada material fora do padrão é um micro-dano à percepção da marca. Além disso, ativos digitais (domínios, redes, contas de anúncio) são patrimônio real: sem controle de acesso documentado, a empresa pode perder anos de construção em uma senha esquecida [3].\\n\\n**O que muda na prática:** Inventarie todos os ativos com versão e localização, centralize em uma pasta padrão com controle de acesso e estabeleça o checklist obrigatório antes de qualquer material ser publicado."
    ),
    "MK1-20-analise-de-viabilidade-de-novos-produtos": (
        "Análise de Viabilidade de Novos Produtos/Serviços",
        "Análise de Viabilidade de Novos Produtos/Serviços: Como testar a aceitação de uma nova oferta antes de investir pesado em produção",
        "Como testar a aceitação de uma nova oferta antes de investir pesado em produção",
        "Lançar um produto novo é caro — e errar custa mais. A análise de viabilidade testa a aceitação da oferta antes do investimento pesado: pesquisa, protótipo, pré-venda e teste com clientes reais. Este livro ensina a validar uma nova oferta com método e risco controlado.",
        "Viabilidade não é opinião: é evidência. Antes de produzir em escala, o negócio precisa saber se existe demanda, a que preço e com que margem. Testar a aceitação com métodos baratos e rápidos reduz drasticamente o risco de lançar um produto que ninguém quer.",
        "A análise de viabilidade combina dimensões: mercado (existe demanda?), financeira (a margem sustenta o negócio?), operacional (conseguimos entregar?) e estratégica (alinha com a marca?) [1]. O teste de aceitação usa métodos como entrevistas, landing page com pré-venda, protótipo funcional e pesquisa de disposição a pagar [2].\\n\\n**Por que importa?** A maioria dos lançamentos fracassados falha na validação: a empresa investe em produção antes de validar a demanda. Testar com o mercado — mesmo com amostra pequena — gera dados reais de intenção de compra que valem mais que qualquer pesquisa interna [3].\\n\\n**O que muda na prática:** Antes de produzir, valide com pré-venda ou landing page de interesse, meça a disposição a pagar e estime a demanda; só então decida sobre o investimento em produção e estoque."
    ),
    "MK1-21-revisao-trimestral-de-rota": (
        "Revisão Trimestral de Rota (Quarterly Review)",
        "Revisão Trimestral de Rota (Quarterly Review): Como pivotar o planejamento estratégico no meio do caminho sem desestruturar a operação",
        "Como pivotar o planejamento estratégico no meio do caminho sem desestruturar a operação",
        "O plano anual foi feito em janeiro, mas o mundo mudou em março. A Revisão Trimestral de Rota (Quarterly Review) é o rito que permite pivotar a estratégia no meio do caminho sem desestruturar a operação. Este livro ensina a revisar, decidir e comunicar mudanças de rota.",
        "A revisão trimestral separa o que funcionou do que precisa mudar — com dados, não com ansiedade. Ela preserva a visão, ajusta o caminho e comunica as mudanças com clareza, mantendo o time executando mesmo durante o pivot.",
        "A Quarterly Review é um rito de gestão que avalia o trimestre contra as metas e define o trimestre seguinte: resultados alcançados, causas dos desvios, decisões de continuar, corrigir ou abandonar iniciativas [1]. O pivot estruturado preserva o que funciona e realoca recursos do que não funciona [2].\\n\\n**Por que importa?** O planejamento estático morre no primeiro imprevisto — mas pivotar sem método gera desestruturação. A revisão trimestral dá o espaço seguro para mudar: o time sabe que a rota será revista, então executa sem medo e sem improviso [3].\\n\\n**O que muda na prática:** Agende a revisão trimestral com pauta fixa (resultados, causas, decisões), defina critérios objetivos para manter/pivotar/cortar e comunique as mudanças em documento único atualizando o masterbook."
    ),

    # ═══════════════ SÉRIE MK2 — IA APLICADA AO PLANEJAMENTO ═══════════════
    "MK2-01-arquitetura-de-prompts-estrategicos": (
        "Arquitetura de Prompts Estratégicos para Negócios",
        "Arquitetura de Prompts Estratégicos para Negócios: Técnicas avançadas para comandar IAs na criação de estratégias corporativas",
        "Técnicas avançadas para comandar IAs na criação de estratégias corporativas de alto nível",
        "Pedir uma estratégia a uma IA sem método gera um texto bonito e inútil. A arquitetura de prompts estratégicos ensina a estruturar comandos — contexto, tarefa, restrição e formato — para extrair análises e planos de nível sênior. Este livro entrega o framework e os exemplos.",
        "O prompt é o volante da IA: a mesma ferramenta produz achismo genérico ou análise profunda dependendo de como é comandada. Arquitetar prompts com contexto empresarial, restrições de negócio e formato estruturado transforma a IA em um consultor estratégico sob demanda.",
        "A arquitetura de prompts estrutura o comando em camadas: papel (quem a IA deve assumir), contexto (dados da empresa e do mercado), tarefa (o que produzir), restrições (limites e vieses a evitar) e formato (estrutura de saída) [1]. Técnicas como chain-of-thought — pedir raciocínio passo a passo — elevam a qualidade de análises complexas [2].\\n\\n**Por que importa?** A diferença entre um prompt amador e um profissional não é o tema: é a estrutura. Com contexto empresarial rico e saída formatada, a IA entrega diagnósticos, planos e hipóteses que o time pode executar — em vez de generalidades [3].\\n\\n**O que muda na prática:** Adote o template (papel + contexto + tarefa + restrição + formato) para todos os prompts estratégicos e crie uma biblioteca de prompts mestres por tipo de decisão."
    ),
    "MK2-02-biblioteca-de-prompts-corporativa": (
        "Construção de uma Biblioteca de Prompts Corporativa",
        "Construção de uma Biblioteca de Prompts Corporativa: Padronizando os comandos que a equipe usa para gerar relatórios, copies e análises",
        "Padronizando os comandos que a equipe usa para gerar relatórios, copies e análises",
        "Cada pessoa da equipe usa a IA do seu jeito — e os resultados variam. A biblioteca de prompts corporativa padroniza os comandos usados para relatórios, copies e análises, garantindo consistência e qualidade. Este livro ensina a criar, versionar e governar essa biblioteca.",
        "A biblioteca de prompts é o manual de uso da IA na empresa: em vez de cada um reinventar o comando, a equipe reutiliza prompts testados e aprovados. O resultado é consistência de tom, qualidade mínima garantida e menos tempo gasto em tentativa e erro.",
        "Uma biblioteca de prompts corporativa organiza os comandos reutilizáveis da empresa por categoria — relatórios, copies, análise de dados, planejamento — com cada prompt documentado (objetivo, quando usar, variáveis, exemplo de saída) [1]. A governança define quem cria, quem aprova e como os prompts evoluem com versionamento [2].\\n\\n**Por que importa?** Prompts soltos geram saída inconsistente e dependência de poucas pessoas. Uma biblioteca versionada transforma o conhecimento de IA em patrimônio da empresa — novo colaborador chega e já usa os prompts padrão [3].\\n\\n**O que muda na prática:** Comece com 10 prompts de alto uso (relatório mensal, copy de anúncio, análise de concorrente), documente cada um com variáveis e aprovação, e versione as melhorias a cada trimestre."
    ),
    "MK2-03-criacao-de-agentes-especializados-de-planejamento": (
        "Criação de Agentes Especializados de Planejamento",
        "Criação de Agentes Especializados de Planejamento: Como configurar instâncias de IA personalizadas para atuar como consultores internos",
        "Como configurar instâncias de IA personalizadas para atuar como consultores de marketing internos",
        "Em vez de um assistente genérico, a empresa configura agentes especializados: um consultor de posicionamento, um analista de concorrência, um redator de campanhas. Cada um com personalidade, conhecimento e limites próprios. Este livro ensina a criar e operar esses agentes.",
        "Agentes especializados são a forma madura de usar IA: cada instância assume um papel com instruções, base de conhecimento e restrições dedicadas. O resultado é uma equipe virtual de consultores que trabalha com consistência e escalabilidade.",
        "Um agente especializado combina três elementos: instruções de sistema (o papel, as regras e o tom), base de conhecimento (documentos, dados e histórico da empresa) e ferramentas (acesso a dados ou ações permitidas) [1]. Cada agente é configurado para um domínio — posicionamento, mídia, conteúdo, métricas — e opera dentro dos limites definidos [2].\\n\\n**Por que importa?** Agentes generalistas entregam respostas médias para qualquer assunto; agentes especializados entregam profundidade consistente no seu domínio. Eles padronizam o conhecimento do time e liberam o gestor do trabalho repetitivo de briefing [3].\\n\\n**O que muda na prática:** Defina os 3 a 5 papéis de maior uso (analista de mercado, redator, planejador), configure cada agente com instruções e base de dados da empresa, e documente as saídas esperadas de cada um."
    ),
    "MK2-04-auditoria-de-mercado-automatizada-via-ia": (
        "Auditoria de Mercado Automatizada via IA",
        "Auditoria de Mercado Automatizada via IA: Utilizando ferramentas de IA para sintetizar pesquisas, tendências e relatórios complexos",
        "Utilizando ferramentas de IA para sintetizar pesquisas de mercado, tendências e relatórios complexos",
        "Pesquisa de mercado não falta: falta leitura. A auditoria automatizada via IA sintetiza pesquisas, relatórios e tendências — transformando horas de leitura em insights acionáveis. Este livro ensina a configurar e operar auditorias de mercado com IA.",
        "A IA não substitui a pesquisa: multiplica a capacidade de absorvê-la. Com a auditoria automatizada, a empresa monitora tendências, sintetiza relatórios de mercado e atualiza seu diagnóstico competitivo com regularidade — algo que poucas equipes conseguem fazer manualmente.",
        "A auditoria de mercado automatizada usa IA para coletar, resumir e cruzar fontes: relatórios setoriais, tendências de busca, movimentos de concorrentes e discussões relevantes [1]. O processo define as fontes de monitoramento, a frequência de coleta e o formato do relatório sintetizado [2].\\n\\n**Por que importa?** A maioria das empresas não audita o mercado por falta de tempo, não por falta de dados. A automação mantém a auditoria contínua e entrega, mensalmente, um panorama atualizado que alimenta o planejamento estratégico [3].\\n\\n**O que muda na prática:** Defina as fontes-chave do seu mercado, configure o fluxo de coleta e síntese com IA, e agende o relatório mensal de auditoria com formato executivo de uma página."
    ),
    "MK2-05-geracao-de-personas-sinteticas-para-testes": (
        "Geração de Personas Sintéticas para Testes",
        "Geração de Personas Sintéticas para Testes: Simulando o comportamento de clientes ideais através de agentes para validar hipóteses de campanha",
        "Simulando o comportamento de clientes ideais através de agentes para validar hipóteses de campanhas",
        "Antes de gastar com campanha, teste a hipótese com clientes simulados: personas sintéticas são agentes de IA que assumem o papel do cliente ideal e reagem à oferta, ao copy e ao preço. Este livro ensina a criar e usar essas simulações para validar campanhas.",
        "Personas sintéticas não substituem a pesquisa real — mas barateiam a validação. Elas permitem testar hipóteses de mensagem, oferta e preço com feedback imediato, revelando objeções e pontos cegos antes do investimento em mídia.",
        "Personas sintéticas são perfis de cliente construídos em IA: cada uma carrega as dores, objetivos, objeções e padrões de decisão do cliente real [1]. Em simulações de campanha, a IA assume o papel da persona e reage ao copy, à oferta e ao preço — gerando objeções plausíveis e sinais de aceitação [2].\\n\\n**Por que importa?** Campanhas mal testadas morrem na primeira semana por objeções previsíveis. A simulação com personas sintéticas antecipa essas objeções e orienta ajustes de mensagem antes da verba — e os testes reais com clientes confirmam as hipóteses [3].\\n\\n**O que muda na prática:** Construa personas sintéticas com base nas personas comportamentais reais, simule a reação a novas campanhas e ofertas, e use os resultados para priorizar testes A/B reais."
    ),
    "MK2-06-planejamento-de-conteudo-anual-automatizado": (
        "Planejamento de Conteúdo Anual Automatizado",
        "Planejamento de Conteúdo Anual Automatizado: Desdobrando pilares de autoridade em um cronograma editorial completo em minutos",
        "Desdobrando pilares de autoridade em um cronograma editorial completo em minutos",
        "Um ano de conteúdo planejado em minutos: a IA desdobra os pilares de autoridade da marca em um cronograma editorial completo — temas, formatos, canais e datas. Este livro ensina a configurar e refinar esse planejamento automatizado.",
        "O planejamento editorial anual é o mapa da autoridade: ele garante que o conteúdo construa reputação de forma consistente, em vez de reagir ao acaso. Automatizar o desdobramento libera a equipe para o que importa — produzir com qualidade.",
        "O planejamento editorial parte dos pilares de autoridade: os temas centrais que a marca domina e pelos quais quer ser lembrada [1]. A IA desdobra cada pilar em uma matriz: formatos (artigo, vídeo, post, podcast), canais e cadência, gerando o cronograma anual [2].\\n\\n**Por que importa?** Conteúdo sem plano vira ruído: publica-se o que dá tempo, não o que constrói posicionamento. Com o calendário derivado dos pilares, cada peça reforça a autoridade da marca e alimenta o funil de atração [3].\\n\\n**O que muda na prática:** Defina os 3 a 5 pilares de autoridade, use a IA para desdobrar o calendário anual (temas × formatos × canais), e revise mensalmente priorizando o que conversa com as campanhas do momento."
    ),
    "MK2-07-analise-de-dados-de-vendas-com-ia": (
        "Análise de Dados de Vendas com IA",
        "Análise de Dados de Vendas com IA: Usando inteligência artificial para cruzar planilhas de faturamento e identificar padrões de consumo",
        "Usando inteligência artificial para cruzar planilhas de faturamento e identificar padrões de consumo",
        "A planilha de faturamento esconde padrões: produtos que vendem juntos, sazonalidade por cliente, queda silenciosa de ticket. A IA cruza essas planilhas e identifica padrões de consumo que o olho humano demoraria semanas para ver. Este livro ensina a extrair esses insights.",
        "Dados de vendas são o histórico mais fiel do negócio — mas ficam inertes sem análise. Com a IA cruzando faturamento, clientes e canais, a empresa enxerga padrões de consumo reais e transforma a análise de vendas em insumo direto para o planejamento.",
        "A análise de dados de vendas com IA combina a organização dos dados (planilhas limpas e estruturadas) com a capacidade do modelo de identificar padrões: produtos associados, comportamento de compra por segmento, variações sazonais e anomalias [1]. As perguntas certas ao modelo — 'quais clientes mais churn', 'quais produtos puxam o ticket' — produzem análises acionáveis [2].\\n\\n**Por que importa?** A maioria das empresas sente o sintoma (vendas caindo) mas não vê a causa (padrão de consumo). A IA transforma o histórico em hipóteses testáveis que orientam oferta, estoque e campanha [3].\\n\\n**O que muda na prática:** Padronize as planilhas de vendas (data, produto, cliente, canal, valor), use a IA para análise de padrões mensal e transforme os insights em ações de marketing e oferta priorizadas."
    ),
    "MK2-08-politicas-e-regras-de-uso-de-ia-na-empresa": (
        "Redigindo Políticas e Regras de Uso de IA na Empresa",
        "Redigindo Políticas e Regras de Uso de IA na Empresa: Estabelecendo limites éticos, de segurança de dados e originalidade",
        "Estabelecendo limites éticos, de segurança de dados e originalidade para o uso de tecnologias",
        "A IA entrou na empresa mais rápido que as regras. Políticas de uso definem limites éticos, proteção de dados e originalidade — protegendo a marca e os clientes. Este livro ensina a redigir e implantar essas políticas sem travar a adoção.",
        "Política de IA não é controle por medo: é proteção com direção. Com regras claras de dados, ética e originalidade, a equipe usa a IA com confiança e a empresa evita vazamentos, plágio e danos de reputação.",
        "A política de uso de IA define: quais dados podem ser enviados a ferramentas externas (proibição de dados sensíveis de clientes), como garantir originalidade (revisão humana de conteúdo gerado), limites éticos (não gerar enganos, não criar avaliações falsas) e responsabilidades [1]. A política ganha vida com treinamento e exemplos práticos [2].\\n\\n**Por que importa?** Dados de clientes enviados a ferramentas externas podem violar a LGPD; conteúdo gerado sem revisão pode plagiar ou enganar. A política reduz esses riscos e documenta a responsabilidade da empresa — essencial também para contratos com clientes [3].\\n\\n**O que muda na prática:** Redija a política em 2 páginas (dados permitidos, revisão obrigatória, ética e exemplos de uso aceitável), comunique em treinamento e revise anualmente conforme a tecnologia evolui."
    ),
    "MK2-09-criacao-rapida-de-mvps": (
        "Criação Rápida de MVPs (Minimum Viable Products)",
        "Criação Rápida de MVPs (Minimum Viable Products): Validando ideias de novos produtos ou campanhas utilizando protótipos gerados por IA",
        "Validando ideias de novos produtos ou campanhas utilizando protótipos gerados por IA",
        "MVP é a forma de validar uma ideia com o mínimo de investimento — e a IA acelera a criação: landing pages, campanhas-teste e até protótipos simples gerados em horas. Este livro ensina a usar IA para criar e lançar MVPs rápidos.",
        "A IA reduziu o custo de testar ideias a quase zero: em vez de meses e equipes, um MVP funcional em dias. Isso muda a lógica do marketing — cada campanha e produto novo pode ser validado com dados antes do investimento pesado.",
        "Um MVP (Minimum Viable Product) é a versão mínima de uma oferta capaz de gerar aprendizado real do mercado: lançar, medir, aprender [1]. Com IA, o MVP acelera em todos os estágios: copy da página, estrutura da oferta, protótipo de produto e análise dos resultados do teste [2].\\n\\n**Por que importa?** A validação rápida substitui a aposta: em vez de investir pesado em um lançamento, a empresa testa uma campanha ou oferta mínima, mede a aceitação e decide com dados. A IA reduz o custo e o tempo de cada ciclo de teste [3].\\n\\n**O que muda na prática:** Para cada ideia nova, defina a hipótese, crie o MVP mínimo com IA (página, oferta, copy), lance para um público pequeno e defina o critério de aceite antes de escalar."
    ),
    "MK2-10-transcriacao-de-mensagens-por-canal": (
        "Transcriação e Adaptação de Mensagens por Canal",
        "Transcriação e Adaptação de Mensagens por Canal: Usando IA para adaptar a mesma narrativa estratégica para o físico, e-mail, redes sociais e anúncios",
        "Usando IA para adaptar a mesma narrativa estratégica para o físico, e-mail, redes sociais e anúncios",
        "A mesma estratégia precisa falar línguas diferentes: o cartaz da loja, o e-mail, o post e o anúncio. A transcriação adapta a narrativa central a cada canal — mantendo a essência e ajustando forma, tom e limite. Este livro ensina a usar IA nessa adaptação em escala.",
        "Transcriar não é traduzir: é recontar a mesma história no idioma de cada canal. Com IA, a equipe gera dezenas de variações consistentes — e mantém a estratégia coerente do PDV ao feed.",
        "A transcriação adapta uma mensagem-fonte a diferentes canais, preservando a intenção e ajustando formato, tom e restrições de cada meio [1]. Com IA, a adaptação ganha escala: a partir da narrativa estratégica, o modelo gera variações para anúncio (curto, persuasivo), e-mail (informativo), rede social (conversacional) e material físico [2].\\n\\n**Por que importa?** Mensagens idênticas em todos os canais soam robotizadas e desperdiçam o potencial de cada meio. A transcriação garante consistência estratégica com adaptação tática — e a IA torna isso viável em volume [3].\\n\\n**O que muda na prática:** Escreva a narrativa-fonte única da campanha, use a IA para gerar variações por canal com as restrições de cada um e revise o tom antes da publicação em massa."
    ),
    "MK2-11-simulacao-de-cenarios-de-crise-com-agentes": (
        "Simulação de Cenários de Crise com Agentes",
        "Simulação de Cenários de Crise com Agentes: Testando a resiliência do planejamento de marketing frente a cenários adversos simulados",
        "Testando a resiliência do planejamento de marketing frente a cenários adversos simulados por modelos",
        "Como seu plano de marketing reagiria a uma crise de reputação ou a um bloqueio de contas? A simulação de cenários usa agentes de IA para testar a resiliência do planejamento diante de adversidades — antes que elas aconteçam. Este livro ensina a simular e aprender.",
        "Simular o pior cenário não é pessimismo: é treinamento. Quando o time ensaia respostas a crises — reputação, queda de tráfego, mudança de algoritmo — a empresa reage com calma e método quando o problema real chega.",
        "A simulação de cenários de crise usa agentes de IA para modelar adversidades e testar as respostas do plano: o modelo assume o papel de público, imprensa ou concorrência reagindo às decisões da empresa [1]. O exercício revela lacunas no plano de contingência e prepara o time com respostas ensaiadas [2].\\n\\n**Por que importa?** A primeira reação a uma crise é emocional; a segunda é estratégica. Treinar a resposta com simulação reduz o tempo de reação e aumenta a qualidade da decisão — a empresa já viu aquele cenário antes, mesmo que simulado [3].\\n\\n**O que muda na prática:** Selecione os 3 cenários de crise mais prováveis do seu negócio, simule cada um com agentes, registre as respostas eficazes e integre o aprendizado ao plano de contingência."
    ),
    "MK2-12-automacao-de-relatorios-de-desempenho": (
        "Automação de Relatórios de Desempenho Mensal",
        "Automação de Relatórios de Desempenho Mensal: Integrando dados de plataformas para que a IA resuma os resultados em formato executivo",
        "Integrando dados de plataformas para que a IA resuma os resultados em um formato executivo",
        "O relatório mensal de marketing não pode depender de uma tarde de planilhas. A automação integra dados das plataformas — anúncios, site, CRM — e a IA resume os resultados em formato executivo. Este livro ensina a montar esse fluxo de ponta a ponta.",
        "Relatório automático não elimina análise: elimina o trabalho braçal de coleta. Com os dados integrados e a IA resumindo, o gestor recebe o relatório executivo pronto e dedica seu tempo ao que importa — decidir.",
        "A automação de relatórios combina integração de dados (exportações ou APIs de anúncios, analytics, CRM e vendas) com a síntese da IA: o modelo transforma tabelas em um resumo executivo com destaques, tendências e alertas [1]. O fluxo roda mensalmente e entrega o relatório no formato padrão da empresa [2].\\n\\n**Por que importa?** Relatórios manuais consomem horas, atrasam e dependem de uma pessoa. Automatizados, eles chegam pontuais e consistentes — e a IA acrescenta a leitura crítica dos números que transforma o relatório em decisão [3].\\n\\n**O que muda na prática:** Defina o formato padrão do relatório mensal, integre as fontes de dados em uma planilha única e configure a IA para resumir com destaques e recomendações — revisando o primeiro relatório antes de automatizar de vez."
    ),
    "MK2-13-pesquisa-de-palavras-chave-e-intencao-de-busca": (
        "Pesquisa de Palavras-Chave e Intenção de Busca Avançada",
        "Pesquisa de Palavras-Chave e Intenção de Busca Avançada: Mapeando o que os clientes buscam online usando análises semânticas profundas de IA",
        "Mapeando o que os clientes buscam online usando análises semânticas profundas de IA",
        "Palavra-chave não é mais só 'termo com volume': é sinal de intenção. A pesquisa avançada mapeia o que os clientes buscam — incluindo as perguntas que a IA responde — usando análise semântica. Este livro ensina a usar IA para ir além do volume e entender a intenção.",
        "Entender a intenção por trás da busca orienta todo o conteúdo: quem pesquisa 'quanto custa' está no fundo do funil; quem pesquisa 'o que é' está no topo. A pesquisa semântica com IA revela essas nuances e posiciona a marca em cada etapa da jornada.",
        "A pesquisa de palavras-chave avançada combina dados de volume e concorrência com análise semântica: a IA agrupa termos por intenção (informativa, comercial, transacional), identifica sinônimos e variações de linguagem natural, e mapeia as perguntas que os clientes fazem [1]. Esse mapa alimenta conteúdo e SEO [2].\\n\\n**Por que importa?** Com a ascensão das respostas de IA (GEO), otimizar apenas para o buscador clássico não basta: a marca precisa aparecer nas respostas das ferramentas de IA, que respondem a perguntas de linguagem natural. A intenção é a ponte [3].\\n\\n**O que muda na prática:** Liste os temas centrais do negócio, use a IA para expandir termos por intenção e perguntas, e organize o conteúdo do site para responder a cada intenção — do topo ao fundo do funil."
    ),
    "MK2-14-geracao-e-teste-de-variantes-de-anuncios": (
        "Geração e Teste de Variantes de Anúncios em Escala",
        "Geração e Teste de Variantes de Anúncios em Escala: Criando dezenas de variações de copies e copides para campanhas de tráfego pago",
        "Criando dezenas de variações de copies e copides para campanhas de tráfego pago",
        "O anúncio vencedor não nasce pronto: nasce de variações. A IA gera dezenas de copies e criativos em minutos — e o teste em escala revela qual ressoa com cada público. Este livro ensina a produzir e testar variantes de anúncios com método.",
        "Testar variantes é a diferença entre campanha mediana e campanha otimizada: cada versão ensina algo sobre o público. Com IA, o custo de gerar variações despenca — e a equipe testa hipóteses de mensagem, oferta e gatilho em escala.",
        "A geração de variantes com IA produz dezenas de versões de copy a partir de variações controladas: diferentes ângulos de dor, formatos (curto, longo, listas), apelos (urgência, prova social, desconto) e chamadas para ação [1]. O teste estruturado (A/B em lotes) mede cada variável e alimenta a otimização contínua [2].\\n\\n**Por que importa?** O custo de mídia sobe; a criatividade é a alavanca mais barata de performance. Campanhas que testam variantes continuamente reduzem o CAC e atrasam a fadiga do público — cada anúncio novo reengaja [3].\\n\\n**O que muda na prática:** Para cada campanha, gere 10 a 20 variantes de copy com IA, lance em estrutura de teste com orçamento pequeno, identifique os vencedores por métrica de negócio e escale os melhores criativos."
    ),
    "MK2-15-otimizacao-de-funis-com-diagnostico-cognitivo": (
        "Otimização de Funis com Diagnóstico Cognitivo",
        "Otimização de Funis de Vendas com Diagnóstico Cognitivo: Pedindo para a IA apontar gargalos e pontos de atrito na jornada digital",
        "Pedindo para a IA apontar gargalos e pontos de atrito na jornada do cliente digital",
        "O funil tem um vazamento e ninguém sabe onde: a IA analisa a jornada digital e aponta os gargalos — onde os visitantes desistem, onde o formulário atrita, onde a oferta confunde. Este livro ensina o diagnóstico cognitivo do funil com IA.",
        "O diagnóstico cognitivo trata o funil como um sistema a ser interrogado: com os dados de cada etapa, a IA aponta padrões de desistência e atrito que a visão de planilha esconde. O resultado é uma lista priorizada de correções com impacto esperado.",
        "O diagnóstico cognitivo do funil usa a IA para analisar as métricas de cada etapa — tráfego → engajamento → lead → venda — e apontar onde a queda é anormal [1]. A IA também analisa qualitativamente: feedbacks, perguntas de atendimento e gravações são resumidas em padrões de objeção e atrito [2].\\n\\n**Por que importa?** Melhorar 1% na conversão do checkout vale mais que dobrar o tráfego. O diagnóstico aponta onde o próximo ganho está — e a IA acelera a análise de dados e feedbacks que revelam o porquê da desistência [3].\\n\\n**O que muda na prática:** Alimente a IA com os dados do funil (etapas e taxas) e os feedbacks de clientes, peça o diagnóstico de gargalos com prioridade de impacto e implemente as correções testando cada mudança."
    ),
    "MK2-16-traducao-de-dados-brutos-em-insights": (
        "Tradução de Dados Brutos em Insights Acionáveis",
        "Tradução de Dados Brutos em Insights Acionáveis: Filtrando o excesso de métricas das plataformas digitais para focar no que importa",
        "Filtrando o excesso de métricas das plataformas digitais para focar no que importa",
        "As plataformas entregam mil métricas e nenhuma direção. A tradução de dados brutos em insights acionáveis filtra o excesso — e foca no que importa para o caixa. Este livro ensina a usar IA para transformar painéis cheios em decisões claras.",
        "Dado demais é o novo dado de menos: sem filtro, o gestor se afoga em métricas de vaidade. A tradução em insights conecta as métricas das plataformas às métricas de negócio — e revela o que o gestor deve fazer na segunda-feira.",
        "A tradução de dados brutos em insights segue o princípio da pirâmide: métricas de plataforma (impressões, cliques, CTR) são meio; métricas de negócio (leads, vendas, margem) são fim [1]. A IA filtra e conecta: dado o excesso de métricas, o modelo resume as 3 a 5 que importam e traduz cada uma em ação recomendada [2].\\n\\n**Por que importa?** Painéis cheios geram paralisia: o gestor não sabe o que é sinal. A tradução em insights cria o hábito de olhar para as métricas que respondem 'estamos ganhando dinheiro?' e agir sobre elas [3].\\n\\n**O que muda na prática:** Defina as métricas de negócio-alvo, peça à IA para resumir mensalmente 'o que mudou, por que, e o que fazer', e transforme o relatório em lista de ações com responsável e prazo."
    ),
    "MK2-17-criacao-de-manuais-de-atendimento-e-scripts-comerciais": (
        "Criação de Manuais de Atendimento e Scripts Comerciais",
        "Criação de Manuais de Atendimento e Scripts Comerciais: Estruturando falas de vendas alinhadas ao posicionamento estratégico da marca",
        "Estruturando falas de vendas alinhadas ao posicionamento estratégico da marca",
        "A equipe comercial vende com a própria intuição — e cada atendimento é uma roleta. Manuais e scripts comerciais estruturam as falas de vendas alinhadas ao posicionamento da marca. Este livro ensina a criar esses materiais com IA, sem engessar a humanidade do vendedor.",
        "Script não é robô: é consistência. Com as falas de abertura, objeções e fechamento padronizadas, qualquer vendedor entrega o mesmo padrão de qualidade — e a IA acelera a criação e a atualização desses materiais.",
        "O script comercial estrutura a conversa por etapas: abertura, qualificação, apresentação de valor, tratamento de objeções e fechamento — cada uma com falas alinhadas ao posicionamento e à proposta de valor da marca [1]. O manual de atendimento documenta os processos e as respostas padrão para dúvidas e objeções frequentes [2].\\n\\n**Por que importa?** Sem script, cada vendedor inventa a própria história da marca — e o posicionamento se dilui. Com material estruturado, o time vende com consistência e a IA permite atualizar os scripts conforme as lições das conversas reais [3].\\n\\n**O que muda na prática:** Registre as melhores conversas do time, use a IA para extrair padrões (aberturas, objeções, fechamentos), estruture o script por etapa e revise com os vendedores antes de implantar."
    ),
    "MK2-18-uso-de-dados-sinteticos-para-ampliacao-de-audiencia": (
        "Uso de Dados Sintéticos para Ampliação de Audiência",
        "Uso de Dados Sintéticos para Ampliação de Audiência: Expandindo públicos semelhantes com o auxílio de modelagem preditiva de IA",
        "Expandindo públicos semelhantes com o auxílio de modelagem preditiva de IA",
        "A base de clientes é pequena, mas o potencial de mercado é grande. Dados sintéticos e modelagem preditiva ajudam a ampliar audiências — construindo públicos semelhantes onde os dados reais não alcançam. Este livro ensina a usar essas técnicas com ética e precisão.",
        "Públicos semelhantes (lookalikes) são a forma de escalar a aquisição a partir do que já funciona: a IA encontra padrões nos clientes atuais e os projeta em audiências maiores. Dados sintéticos complementam onde a amostra é pequena — sempre com cuidado ético.",
        "A ampliação de audiência usa modelagem preditiva para encontrar novos públicos parecidos com os clientes atuais: a IA analisa os atributos e comportamentos dos compradores e identifica padrões que orientam a segmentação em plataformas de anúncio [1]. Dados sintéticos — exemplos gerados artificialmente — complementam amostras pequenas para treinar modelos sem expor dados reais [2].\\n\\n**Por que importa?** Bases pequenas limitam o alcance e o aprendizado das campanhas. Ampliar públicos com método aumenta o alcance qualificado — e o uso de dados sintéticos expande a modelagem sem comprometer a privacidade dos clientes [3].\\n\\n**O que muda na prática:** Comece com os públicos semelhantes nativos das plataformas, use a IA para refinar os atributos dos melhores clientes e valide o CAC dos públicos ampliados antes de escalar a verba."
    ),
    "MK2-19-eliminacao-de-tarefas-manuais-repetitivas": (
        "Eliminação de Tarefas Manuais Repetitivas (Workflow Automation)",
        "Eliminação de Tarefas Manuais Repetitivas (Workflow Automation): Mapeando processos internos de marketing aptos à automação ponta a ponta",
        "Mapeando processos internos de marketing aptos à automação ponta a ponta",
        "O time de marketing gasta horas em tarefas que uma máquina faria: extrair dados, formatar relatórios, responder dúvidas padrão, postar conteúdo. A automação de fluxos elimina essas tarefas repetitivas — liberando as pessoas para o que exige criatividade e decisão. Este livro ensina a mapear e automatizar.",
        "Automação não é sobre demitir gente: é sobre devolver tempo. Cada tarefa repetitiva automatizada libera horas semanais do time — e a automação de fluxos de trabalho é uma das alavancas de produtividade mais rápidas e baratas do marketing.",
        "A automação de fluxos mapeia os processos internos e identifica os candidatos à automação: tarefas repetitivas, regulares e baseadas em regras — coleta de dados, geração de relatórios, triagem de leads, publicação de conteúdo, respostas padrão [1]. Cada processo é documentado, priorizado por ganho e automatizado com as ferramentas adequadas [2].\\n\\n**Por que importa?** O tempo gasto em tarefas braçais é o custo invisível mais alto do marketing. Automatizar libera horas para o que gera diferencial — estratégia, relacionamento e criatividade — e reduz erros manuais [3].\\n\\n**O que muda na prática:** Liste as tarefas repetitivas da semana do time, estime o tempo gasto em cada, priorize as de maior ganho e automatize em lotes — começando pelas 3 tarefas que mais consomem horas."
    ),
    "MK2-20-futuro-do-profissional-de-marketing": (
        "O Futuro do Profissional de Marketing como Diretor de Orquestra",
        "O Futuro do Profissional de Marketing como Diretor de Orquestra: Como a liderança foca em estratégia e direção enquanto a IA executa",
        "Como a liderança de marketing foca em estratégia e direção enquanto a IA executa",
        "O profissional de marketing do futuro não escreve cada post ou configura cada anúncio: orquestra — define a estratégia, comanda as ferramentas de IA e garante a qualidade da execução. Este livro explora essa transição e as habilidades necessárias.",
        "O valor do profissional de marketing migra da execução para a direção: quem define o quê, por quê e com que critério vale mais que quem executa o como. A IA executa em escala; o humano dirige com estratégia e julgamento.",
        "A metáfora do diretor de orquestra captura a nova função do profissional de marketing: ele não toca cada instrumento (não executa cada tarefa), mas define a partitura (estratégia), comanda os músicos (agentes e ferramentas de IA) e garante a harmonia (qualidade e coerência) [1]. As habilidades-chave mudam: de técnica para curadoria, briefing, avaliação e ética [2].\\n\\n**Por que importa?** Quem só executa será substituído pela ferramenta; quem dirige multiplica a ferramenta. A carreira do profissional de marketing se torna mais estratégica, mais valorizada e menos repetitiva — desde que ele domine a orquestração [3].\\n\\n**O que muda na prática:** Desenvolva as habilidades de direção — briefing preciso, avaliação crítica de resultados gerados, curadoria de agentes — e reorganize o dia a dia para delegar o executável à IA e concentrar-se no estratégico."
    ),
}
