#!/usr/bin/env python3
"""
Dados do Livro de Marketing Digital (MK-01)
"O Manual Definitivo: O Plano Estratégico de Marketing Digital do Zero aos Resultados"

Estrutura: 5 Módulos × 5 Capítulos = 25 capítulos (EITA-V2).
Usado por gerar-livro-marketing.py e compilar-para-pdf.py
"""

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_MARKETING = {
    "MK-01-plano-estrategico-marketing-digital": (
        "O Plano Estratégico de Marketing Digital do Zero aos Resultados",
        "O Manual Definitivo: O Plano Estratégico de Marketing Digital do Zero aos Resultados",
        "Fundamentos, diagnóstico 360°, IA como copiloto estratégico, canais e funis de conversão, operações e escala com ROI real",
        "Este livro é o manual definitivo para empresas que querem transformar marketing digital em resultado mensurável. Organizado em cinco módulos progressivos, ele conduz o leitor do diagnóstico 360° da empresa até a escala com ROI real, passando pela infraestrutura de IA, arquitetura de canais e operação disciplinada. Cada capítulo entrega ferramentas práticas: planilhas, checklists, prompts e fórmulas prontas para aplicar no dia seguinte.",
        "Marketing digital não é gasto: é investimento com ROI mensurável. Este manual provou que qualquer empresa — do pequeno negócio à operação consolidada — pode estruturar um plano estratégico completo quando combina diagnóstico rigoroso, uso inteligente de IA, canais bem arquitetados e operação disciplinada. O caminho do zero aos resultados existe, está documentado e agora está em suas mãos.",
        "A Auditoria 360° é o ponto de partida inegociável de qualquer plano estratégico de marketing digital [1]. Antes de gastar um centavo em tráfego pago ou contratar agências, a empresa precisa conhecer seus custos fixos, margens de lucro, histórico de vendas e capacidade operacional [2].\\n\\n**Por que importa?** Empresas que pulam o diagnóstico tratam sintomas: investem em anúncios quando o problema é preço, produto ou atendimento. A auditoria separa fatos de achismos e define o orçamento real que pode ser investido sem quebrar o caixa.\\n\\n**O que muda na prática:** Com a planilha de auditoria preenchida, você descobre o ponto de equilíbrio mensal, a margem por produto e o CAC tolerável — a base matemática para todas as decisões de marketing que virão nos próximos capítulos [3]."
    ),
}

SLUGS_MARKETING = list(LIVROS_MARKETING.keys())

SERIES_MARKETING = {
    "MK": {"nome": "Marketing Digital", "prefixo": "MK"},
}

# Estrutura dos 5 módulos: (titulo_modulo, descricao_modulo, [5 títulos de capítulos])
MODULOS_MARKETING = [
    (
        "Fundamentos Absolutos e Diagnóstico 360° (Do Zero Real)",
        "Como auditar a saúde da empresa, entender o cenário atual e estruturar a fundação comercial sem achismos.",
        [
            "A Ferramenta de Auditoria 360°",
            "O Diagnóstico de Posicionamento Atual",
            "Definição de ICP e Personas Reais",
            "Matriz de Alinhamento Comercial (SLA)",
            "O Orçamento Base Zero (OBZ) para Marketing",
        ],
    ),
    (
        "A Infraestrutura de IAs no Dia a Dia (O Copiloto Estratégico)",
        "Como configurar e utilizar modelos de linguagem e agentes de IA como consultores operacionais para acelerar a execução sem perder a voz da marca.",
        [
            "A Arquitetura de Prompts Mestres para Negócios",
            "Construindo a sua Base de Dados Interna (Prompt Book)",
            "Simulação de Cenários com Personas Sintéticas",
            "Automação de Relatórios e Análise de Dados Brutos",
            "Governança e Limites Éticos do Uso de IA",
        ],
    ),
    (
        "Arquitetura de Canais, Tráfego e Funis de Conversão",
        "Desenhando a jornada do cliente omnicanal e estruturando os canais de captação de leads e vendas de alta performance.",
        [
            "O Desenho do Funil de Vendas de Alta Conversão",
            "Estruturando Landing Pages que Vendem",
            "Copywriting Persuasivo com Fórmulas Validadas",
            "Configuração de Tráfego Pago Eficiente (Meta, Google e TikTok)",
            "Automação de CRM e Nutrição de Leads",
        ],
    ),
    (
        "Operações, Processos e Gestão da Execução",
        "Transformando o planejamento em rotina diária através de métodos ágeis, documentação clara e controle de indicadores.",
        [
            "Metodologia Ágil Aplicada ao Marketing (Sprints e Kanban)",
            "Criação de SOPs (Procedimentos Operacionais Padrão)",
            "A Escolha do Stack de MarTech Ideal",
            "Gestão de Terceirizados e Agências",
            "O Painel de Controle Operacional (Dashboard Único)",
        ],
    ),
    (
        "Análise Financeira, Otimização e Escala (O ROI Real)",
        "Como medir o lucro líquido de cada ação, corrigir rotas em tempo real e preparar a empresa para o crescimento exponencial.",
        [
            "O Modelo Financeiro do Marketing para o CFO",
            "Auditoria de Canais (A Metodologia Kill or Fix)",
            "Análise de Cohort e Retenção",
            "Gestão de Crises e Mitigação de Riscos",
            "O Rito de Fechamento de Ciclo (A Revisão Trimestral)",
        ],
    ),
]

# Subtítulos dos capítulos (descrição curta para a seção Introdução)
SUBTITULOS_MARKETING = {
    "A Ferramenta de Auditoria 360°": "Planilhas e checklists práticos para mapear custos fixos, margens de lucro, histórico de vendas e capacidade operacional antes de gastar um centavo em marketing.",
    "O Diagnóstico de Posicionamento Atual": "Como preencher a Matriz de Diferenciação para encontrar o 'oceano azul' da sua empresa, mesmo em mercados altamente comoditizados.",
    "Definição de ICP e Personas Reais": "O método passo a passo para extrair dores, objeções e desejos reais de clientes atuais através de entrevistas e análise de dados de atendimento.",
    "Matriz de Alinhamento Comercial (SLA)": "Como desenhar o contrato interno exato entre o que o marketing atrai e o que o time de vendas precisa receber para fechar negócios.",
    "O Orçamento Base Zero (OBZ) para Marketing": "A fórmula matemática exata para calcular quanto a empresa deve investir no digital com base no LTV (Lifetime Value) e no CAC (Customer Acquisition Cost) tolerável.",
    "A Arquitetura de Prompts Mestres para Negócios": "O framework estruturado (Contexto + Tarefa + Restrição + Formato) para comandar IAs a gerarem estratégias corporativas de nível sênior.",
    "Construindo a sua Base de Dados Interna (Prompt Book)": "O repositório pronto de comandos que a equipe usará diariamente para criar copys, relatórios, análises de mercado e e-mails.",
    "Simulação de Cenários com Personas Sintéticas": "Como usar agentes de IA para simular o comportamento de clientes reais e testar a eficácia de uma nova oferta ou preço antes de lançá-la.",
    "Automação de Relatórios e Análise de Dados Brutos": "Scripts e prompts prontos para transformar planilhas complexas de faturamento e tráfego em insights acionáveis em segundos.",
    "Governança e Limites Éticos do Uso de IA": "Como estabelecer o manual de conformidade interna para evitar alucinações, plágio e vazamento de dados estratégicos da empresa.",
    "O Desenho do Funil de Vendas de Alta Conversão": "Mapeando o caminho exato do topo (atração), meio (nutrição) e fundo (conversão) alinhado ao modelo de negócio da empresa.",
    "Estruturando Landing Pages que Vendem": "O gabarito estrutural de blocos, textos e elementos de design focados estritamente em conversão e remoção de atrito.",
    "Copywriting Persuasivo com Fórmulas Validadas": "Aplicação prática de estruturas de escrita persuasiva para anúncios, páginas de vendas e sequências de mensagens.",
    "Configuração de Tráfego Pago Eficiente (Meta, Google e TikTok)": "O passo a passo técnico para estruturar campanhas focadas em ROI e conversão final, fugindo de métricas de vaidade.",
    "Automação de CRM e Nutrição de Leads": "Como estruturar fluxos automatizados de e-mail e mensagens via WhatsApp que educam o lead e fecham vendas no piloto automático.",
    "Metodologia Ágil Aplicada ao Marketing (Sprints e Kanban)": "Como organizar o fluxo de tarefas semanais da equipe para que o planejamento saia do papel sem sobrecarregar ninguém.",
    "Criação de SOPs (Procedimentos Operacionais Padrão)": "O modelo padrão para documentar cada processo de marketing, garantindo que qualquer colaborador execute com o mesmo padrão de qualidade.",
    "A Escolha do Stack de MarTech Ideal": "Como selecionar e integrar o CRM, ferramentas de automação e plataformas de análise sem desperdiçar dinheiro em softwares desnecessários.",
    "Gestão de Terceirizados e Agências": "O manual de cobrança de prazos, entregáveis e métricas de desempenho para quem contrata serviços externos.",
    "O Painel de Controle Operacional (Dashboard Único)": "Como construir a planilha ou painel central que resume todas as métricas vitais da empresa em uma única tela para a diretoria.",
    "O Modelo Financeiro do Marketing para o CFO": "A planilha mestre para traduzir impressões, cliques e leads em termos de margem de contribuição, ponto de equilíbrio e lucro.",
    "Auditoria de Canais (A Metodologia Kill or Fix)": "O protocolo passo a passo para analisar o desempenho de cada canal a cada 30 dias e decidir o que cortar, o que ajustar e o que escalar.",
    "Análise de Cohort e Retenção": "Como medir o comportamento de compra dos clientes ao longo do tempo para elevar o LTV (Lifetime Value) da base.",
    "Gestão de Crises e Mitigação de Riscos": "O plano de contingência para quedas de tráfego, bloqueios de contas de anúncios ou crises de reputação online.",
    "O Rito de Fechamento de Ciclo (A Revisão Trimestral)": "O processo definitivo para avaliar os resultados do trimestre, pivotar a estratégia com base em dados e reiniciar o ciclo de planejamento rumo à escala.",
}
