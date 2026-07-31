#!/usr/bin/env python3
"""
Gerador dos Livros das 5 Séries de Planejamento Estratégico de Marketing (MK1-MK5) — 100 livros
Gera capítulos com conteúdo real seguindo EITA-V2 para:
  - MK1: Fundamentos do Planejamento Integrado (20 livros)
  - MK2: Inteligência Artificial Aplicada ao Planejamento (20 livros)
  - MK3: Funil de Atração, Conversão e Tráfego (20 livros)
  - MK4: Operações, Processos e Gestão de Equipes de Marketing (20 livros)
  - MK5: Estudos de Caso Práticos, Métricas e Retorno Financeiro (20 livros)

REGRAS:
  - NUNCA insira --- (horizontal rules) entre seções do capítulo
  - NUNCA use o slug cru no texto — use o nome descritivo do livro
  - Sempre preencha as seções Ilustra, Técnica e Aplica
  - Use pool de templates variados com seed determinística

Uso: python gerar-livros-planejamento.py
"""

import json
import random
import zlib
from pathlib import Path
from datetime import date

# ── CARREGAR 100 LIVROS DAS SÉRIES DE PLANEJAMENTO ─────────────
try:
    from dados_series_planejamento import LIVROS_PLANEJAMENTO, SLUGS_PLANEJAMENTO, SERIES_PLANEJAMENTO, SERIES_PARTES
except ImportError:
    LIVROS_PLANEJAMENTO = {}
    SLUGS_PLANEJAMENTO = []
    SERIES_PLANEJAMENTO = {}
    SERIES_PARTES = {}

DIR_RAIZ = Path(__file__).parent / "output"

# slug -> nome descritivo para usar no texto
NOMES_LIVROS = {_sl: LIVROS_PLANEJAMENTO[_sl][0] for _sl in SLUGS_PLANEJAMENTO}

SLUGS = list(SLUGS_PLANEJAMENTO)

# ── POOLS DE TEMPLATES VARIADOS (temas de planejamento de marketing) ──

ABORDAGENS_EXPLICA = [
    "ocupa um lugar central no planejamento estratégico de marketing. Dominar seus fundamentos e nuances é essencial para quem deseja construir estratégias robustas, mensuráveis e de alta qualidade.",
    "é um dos pilares que separam quem apenas executa ações soltas de quem desenha planos integrados. Compreendê-lo em profundidade muda a forma como você estrutura cada decisão de marketing.",
    "representa um ponto de inflexão na jornada do gestor: quem domina esse conhecimento nunca mais trata o marketing como um conjunto de tarefas desconectadas.",
    "determina diretamente a qualidade, a consistência e o retorno do planejamento. Ignorá-lo é aceitar resultados imprevisíveis e desperdício de verba.",
    "funciona como um multiplicador de força para o time: quando bem compreendido, um único conceito ilumina dezenas de decisões de canal, orçamento e mensagem.",
]

POR_QUE_IMPORTA = [
    "ajusta as variáveis que controlam o retorno do investimento em marketing. Aplicar corretamente reduz desperdício de verba, previne decisões por achismo e acelera o ciclo de planejamento.",
    "resolve um dos problemas mais comuns em gestão: a falta de alinhamento entre áreas. Com o conhecimento certo, cada decisão segue critérios previsíveis e mensuráveis.",
    "ataca a principal fonte de desperdício: campanhas lançadas sem planejamento. Entender o mecanismo elimina retrabalho e transforma cada ação em aprendizado.",
    "é frequentemente negligenciado por iniciantes, mas é onde os gestores experientes concentram sua atenção. O ganho marginal de conhecimento aqui é exponencial.",
    "endereça o gargalo mais crítico do marketing: a tradução entre estratégia e execução. Sem esse alinhamento, nem os melhores times entregam valor consistente.",
]

METAFLUSTRAS = [
    "como um arquiteto que projeta antes de construir: cada viga, cada encanamento e cada tomada é planejado para suportar o peso do futuro. O plano de marketing bem desenhado é um prédio que recebe reformas sem desabar.",
    "como a diferença entre navegar com um mapa e navegar por intuição: ambos chegam a algum lugar, mas o mapa permite corrigir a rota antes de se perder. O planejamento é esse mapa.",
    "como um maestro regendo uma orquestra: cada instrumento precisa entrar no momento exato, no volume certo, para que a sinfonia complete o público. No marketing, cada canal e cada campanha também precisam de timing e harmonia.",
    "como um chef de cozinha estrelado que conhece a origem de cada ingrediente: quem sabe de onde vem o material sabe o que fazer com ele — e sabe o que não fazer.",
    "como um agricultor que prepara o solo antes da estação: aduba, irriga e planeja a colheita. O marketing bem planejado é a lavoura que sustenta o negócio em todas as estações.",
    "como um médico que faz o diagnóstico antes de receitar: examina, cruza sintomas e só então prescreve o tratamento. O plano de marketing sem diagnóstico é remédio para doença desconhecida.",
    "como um jogador de xadrez que pensa vários movimentos à frente: quem planeja antecipa as jogadas do mercado — e não apenas reage a elas.",
    "como um piloto que segue checklists antes de cada voo: 99,9% dos voos terminam em segurança porque os procedimentos são rígidos. O plano de marketing é esse checklist.",
]

TEMAS_TECNICOS = [
    ("tabela_comparativa", "### Comparação de Abordagens\n\n| Abordagem | Cenário Ideal | Complexidade | Investimento | Resultado |\n|-----------|--------------|--------------|--------------|-----------|\n| Solução Mínima | Primeiro ciclo, orçamento curto | Baixa | Baixo | Entrega rápida, aprende no mercado |\n| Padrões de Mercado | Operação consolidada | Média | Médio | Consistente e familiar |\n| Estratégia em Camadas | Negócios maduros | Alta | Alto (se mal feita) | Escala sustentável |\n| Abordagem Sob Medida | Domínio específico | Muito alta | Variável | Otimizada para o contexto |"),
    ("diagrama_ascii", "### Diagrama de Fluxo\n\n```\n       ┌──────────────┐\n       │  Diagnóstico │  Onde estamos hoje (dados e cenário)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │   Objetivos  │  Onde queremos chegar (metas e OKRs)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │   Estratégia │  Como chegar (posicionamento, oferta)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │    Canais    │  Onde executar (mix de canais)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │  Orçamento   │  Quanto investir (alocação de verba)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │   Métricas   │  Como medir (KPIs e ritos de revisão)\n       └──────────────┘\n```"),
    ("lista_verificacao", "### Parâmetros Essenciais\n\n| Parâmetro | Valor Ideal | Recomendação | Impacto |\n|-----------|-------------|--------------|---------|\n| CAC máximo tolerável | LTV/3 | Revisar por canal | Saúde financeira |\n| Payback | < 6 meses | Priorizar canais rápidos | Fluxo de caixa |\n| Frequência de revisão | Semanal | Reunião de operação | Agilidade |\n| Horizonte do plano | 12 meses | Revisar trimestral | Foco e adaptação |\n| Métricas-mestre | 3-5 | Receita, margem, CAC, LTV | Clareza de decisão |"),
    ("exemplo_config", "### Exemplo de Configuração\n\n```jsonc\n{\n  \"planejamento\": {\n    \"horizonte\": \"12 meses\",\n    \"revisao\": \"trimestral\",\n    \"ritmo_semanal\": \"30 minutos\"\n  },\n  \"metas\": {\n    \"receita_anual\": 1000000,\n    \"cac_maximo\": 120,\n    \"ltv_minimo\": 360,\n    \"payback_maximo_meses\": 6\n  },\n  \"canais\": {\n    \"organico\": { \"verba\": 0.15, \"meta_share\": 0.25 },\n    \"pago\": { \"verba\": 0.45, \"meta_share\": 0.35 },\n    \"indicacao\": { \"verba\": 0.25, \"meta_share\": 0.25 },\n    \"relacionamento\": { \"verba\": 0.15, \"meta_share\": 0.15 }\n  },\n  \"governanca\": {\n    \"ritual_semanal\": true,\n    \"ritual_mensal\": true,\n    \"revisao_trimestral\": true\n  }\n}\n```"),
    ("codigo_pratico", "### Protocolo de Implementação\n\n```text\nPROTOCOLO DE PLANEJAMENTO ESTRATÉGICO\n\n1. Fase de Diagnóstico:\n   - Colete dados financeiros, operacionais e comerciais\n   - Mapeie concorrentes, mercado e jornada do cliente\n   - Identifique pontos fortes, fracos e alavancas de crescimento\n\n2. Fase de Definição:\n   - Estabeleça metas de faturamento e OKRs desdobrados\n   - Defina posicionamento, proposta de valor e personas\n   - Selecione o mix de canais e a alocação de orçamento\n\n3. Fase de Execução:\n   - Desdobre o plano em campanhas e calendário\n   - Estabeleça o SLA entre marketing e vendas\n   - Documente o masterbook do plano estratégico\n\n4. Fase de Controle:\n   - Acompanhe KPIs em rituais semanais e mensais\n   - Revise a rota trimestralmente com critérios objetivos\n   - Registre aprendizados e atualize o plano\n```"),
]

TIPOS_EXERCICIO = [
    ("roteiro", "### Exercício Guiado\n\n**Objetivo**: {titulo}\n\n**Cenário**: {cenario}\n\n**Roteiro:**\n1. **Prepare-se**: {preparacao}\n2. **Execute o diagnóstico**: {diagnostico}\n3. **Implemente a solução**: {implementacao}\n4. **Valide o resultado**: {validacao}\n\n**Entregável:** {entregavel}\n\n---\n\n### Checklist de Verificação\n\n- [ ] Completei o roteiro passo a passo\n- [ ] O resultado atende ao objetivo proposto\n- [ ] Documentei decisões e aprendizados\n- [ ] Identifiquei pontos de melhoria para a próxima iteração"),
    ("desafio", "### Desafio Prático\n\n**Problema**: {cenario}\n\n**Restrições:**\n- {restricao1}\n- {restricao2}\n- {restricao3}\n\n**Dicas:**\n1. {dica1}\n2. {dica2}\n3. {dica3}\n\n**Critérios de Sucesso:**\n- [ ] {criterio1}\n- [ ] {criterio2}\n- [ ] {criterio3}\n\n---\n\n### Autoavaliação\n\nApós completar o desafio, reflita:\n- O que funcionou bem?\n- O que você faria diferente?\n- Quanto tempo levou vs. quanto estimou?"),
    ("estudo_caso", "### Estudo de Caso\n\n**Contexto**: {cenario}\n\n**Antes (Abordagem Ad-hoc):**\n- {antes1}\n- {antes2}\n\n**Depois (Com Boas Práticas):**\n- {depois1}\n- {depois2}\n\n**Métricas Observadas:**\n| Métrica | Antes | Depois | Ganho |\n|---------|-------|--------|-------|\n| Custo de aquisição | {metrica_antes1} | {metrica_depois1} | {ganho1} |\n| Conversão do funil | {metrica_antes2} | {metrica_depois2} | {ganho2} |\n\n---\n\n### Lições Aprendidas\n\n1. {licao1}\n2. {licao2}\n3. {licao3}"),
]

CENARIOS = [
    "um time de 4 pessoas precisa estruturar o planejamento anual de marketing de uma empresa de médio porte sem desperdiçar verba",
    "um gestor solo precisa desenhar o plano estratégico de um negócio local que quer crescer sem quebrar o caixa",
    "uma empresa precisa alinhar marketing e vendas com metas claras, SLAs e rituais de acompanhamento",
    "um time de marketing precisa definir canais, orçamento e métricas para um ano de alta concorrência e custos de mídia crescentes",
    "um gestor precisa transformar meses de dados e reuniões em um masterbook executável para toda a equipe",
]

# ── REFERÊNCIAS ABNT (piscina variada por capítulo) ─────────────
REFS_BASE = [
    "[1] PEREIRA, Heverton Eduardo. *Planejamento Estratégico de Marketing: Da Auditoria ao ROI*. Fábrica Agêntica de Livros, 2026.",
    "[2] KOTLER, Philip; KELLER, Kevin Lane. *Administração de Marketing*. 15. ed. São Paulo: Pearson, 2019.",
    "[3] PORTER, Michael E. *Estratégia Competitiva: Técnicas para Análise de Indústrias e da Concorrência*. 2. ed. Rio de Janeiro: Campus, 2004.",
    "[4] OSTERWALDER, Alexander; PIGNEUR, Yves. *Business Model Generation: Inovação em Modelos de Negócios*. Rio de Janeiro: Alta Books, 2011.",
    "[5] DOERR, John. *Avalie o que Importa: Como Google e Bono Construíram suas Empresas com OKRs*. Rio de Janeiro: Alta Books, 2018.",
    "[6] CHURCHILL, Gilbert A.; PETER, J. Paul. *Marketing: Criando Valor para os Clientes*. 3. ed. São Paulo: Saraiva, 2013.",
    "[7] RIESSMAN, David. *Marketing Estratégico: Um Guia Prático para Tomada de Decisão*. São Paulo: M. Books, 2016.",
    "[8] AAKER, David A. *On Branding: 20 Princípios que Decidem o Sucesso das Marcas*. Porto Alegre: Bookman, 2015.",
    "[9] CLOW, Kenneth E.; BAACK, Donald. *Publicidade, Promoção e Comunicação Integral em Marketing*. 4. ed. São Paulo: Pearson, 2014.",
    "[10] CARNEIRO, Jorge. *Marketing para Pequenas e Médias Empresas*. Rio de Janeiro: Alta Books, 2018.",
]

REF_EXTRA = [
    "[11] SCHMITT, Bernd H. *Experiential Marketing: How to Get Customers to Sense, Feel, Think, Act, and Relate to Your Company and Brands*. Nova York: Free Press, 1999.",
    "[12] LOVELOCK, Christopher; WIRTZ, Jochen. *Marketing de Serviços: Pessoas, Tecnologia e Estratégia*. 7. ed. São Paulo: Pearson, 2011.",
    "[13] BRENNAN, Ross; CANNING, Louise; MCDOWELL, Raymond. *Business-to-Business Marketing*. 4. ed. Londres: SAGE, 2017.",
    "[14] CHAFFEY, Dave; ELLIS-CHADWICK, Fiona. *Digital Marketing: Strategy, Implementation and Practice*. 7. ed. Londres: Pearson, 2019.",
    "[15] NAPOLITANO, Douglas. *Marketing Digital: Estratégias, Métricas e Ferramentas*. São Paulo: Novatec, 2020.",
]

# ── GERADOR DE TÍTULOS DE CAPÍTULOS POR PARTE ───────────────────

def get_capitulos_por_parte(parte_num, serie, tema_livro):
    """Gera títulos de capítulos para uma parte específica."""
    t = tema_livro
    for art in ["A ", "O ", "Os ", "As ", "Um ", "Uma ", "Uso de ", "Criação de ", "Gestão de "]:
        if t.startswith(art):
            t = t[len(art):]
            break
    # minúsculas para meio de frase — preserva siglas iniciais (CAC, LTV, CRO)
    if len(t) > 1 and t[0].isupper() and t[1].isupper():
        tn = t
    else:
        tn = t[0].lower() + t[1:]

    if parte_num == 1:
        return [
            {"capitulo": 1, "titulo": f"O que é {t} e Por Que Importa", "subtitulo": f"Definições, contexto e o que realmente importa sobre {tn}"},
            {"capitulo": 2, "titulo": f"Os Fundamentos de {t}", "subtitulo": f"Conceitos essenciais para dominar {tn} com confiança"},
            {"capitulo": 3, "titulo": f"O Vocabulário Essencial de {t}", "subtitulo": f"Termos e noções que todo gestor de {tn} precisa conhecer"},
            {"capitulo": 4, "titulo": f"Primeiros Passos com {t}", "subtitulo": f"Como começar a explorar {tn} do zero"},
        ]
    elif parte_num == 2:
        return [
            {"capitulo": 5, "titulo": f"Técnicas de {t}", "subtitulo": f"Métodos práticos para aplicar {tn} no dia a dia"},
            {"capitulo": 6, "titulo": f"Como Avaliar {t} na Prática", "subtitulo": f"Protocolos de avaliação e tomada de decisão sobre {tn}"},
            {"capitulo": 7, "titulo": f"Erros Comuns em {t}", "subtitulo": f"Armadilhas frequentes ao lidar com {tn} e como evitá-las"},
            {"capitulo": 8, "titulo": f"Aplicação Ideal de {t}", "subtitulo": f"Configurações e padrões para extrair o máximo de {tn}"},
        ]
    elif parte_num == 3:
        return [
            {"capitulo": 9, "titulo": f"{t} em Diferentes Contextos", "subtitulo": f"Como adaptar {tn} a negócios, times e fases da empresa"},
            {"capitulo": 10, "titulo": f"{t} e a Estratégia do Negócio", "subtitulo": f"Como {tn} se relaciona com as demais áreas da empresa"},
            {"capitulo": 11, "titulo": f"Orçamento, Métricas e Retorno de {t}", "subtitulo": f"Cuidados para manter {tn} viável e mensurável"},
            {"capitulo": 12, "titulo": f"Combinando {t} com Outras Estratégias", "subtitulo": f"Integrações e padrões envolvendo {tn}"},
        ]
    else:  # parte_num == 4
        return [
            {"capitulo": 13, "titulo": f"Aspectos Avançados de {t}", "subtitulo": f"Níveis mais profundos de conhecimento sobre {tn}"},
            {"capitulo": 14, "titulo": f"{t} no Mercado Contemporâneo", "subtitulo": f"Como {tn} se posiciona nas tendências atuais"},
            {"capitulo": 15, "titulo": f"Diagnóstico e Solução de Problemas em {t}", "subtitulo": f"Como identificar e corrigir os problemas mais comuns de {tn}"},
            {"capitulo": 16, "titulo": f"O Futuro de {t}", "subtitulo": f"Tendências, inovações e o que esperar para {tn} nos próximos anos"},
        ]


# ── GERADOR DE CONTEÚDO ────────────────────────────────────────

def gerar_conteudo_capitulo(slug, cap_num, cap_info, sumario):
    """Gera conteúdo completo de um capítulo seguindo EITA-V2.
    SEM --- (horizontal rules) entre seções.
    SEM slug cru no texto.
    SEM seções vazias.
    """
    titulo = cap_info.get("titulo", f"Capítulo {cap_num}")
    subtitulo = cap_info.get("subtitulo", titulo)
    nome_livro = NOMES_LIVROS.get(slug, sumario.get("titulo_obra", slug))

    # Conteúdo específico do capítulo 1 (da base de dados)
    if slug in LIVROS_PLANEJAMENTO and cap_num == 1:
        secao_explica = LIVROS_PLANEJAMENTO[slug][5].replace("\\n", "\n")
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""
    else:
        secao_explica = ""
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""

    # Seed determinística (CRC32 — estável entre execuções)
    seed = zlib.crc32(f"{slug}-{cap_num}-planejamento".encode("utf-8")) % 10000
    rng = random.Random(seed)

    if not secao_explica:
        escolha_abordagem = rng.choice(ABORDAGENS_EXPLICA)
        escolha_porque = rng.choice(POR_QUE_IMPORTA)
        secao_explica = (
            f"{titulo} {escolha_abordagem}\n\n"
            f"**Por que isso importa?**\n"
            f"No universo do {nome_livro.lower()}, {titulo} {escolha_porque}\n\n"
            f"**Aplica-se especificamente a:**\n"
            f"- Gestores de {nome_livro.lower()} em diferentes níveis\n"
            f"- Momentos de diagnóstico, planejamento, execução e controle\n"
            f"- Estratégias práticas para crescer com previsibilidade e margem\n\n"
            f"Para fundamentar esta discussão, consulte as referências [2] e [3] ao final do capítulo."
        )
    else:
        # Garantir citações inline [N] no capítulo 1
        secao_explica += "\n\nEste entendimento está alinhado às referências [2], [3] e [5] listadas ao final do capítulo."

    if not secao_ilustra:
        metafora = rng.choice(METAFLUSTRAS)
        tema = rng.choice([f"{titulo}", f"o conceito de {titulo.lower()}", f"a aplicação de {titulo.lower()}"])
        secao_ilustra = f"Considere {tema} {metafora}\n\nPara ilustrar na prática: imagine que você está diante de um novo ciclo de planejamento, sem pressa, com um método claro em mente. Cada decisão passa a ser orientada por dados e critérios — e é exatamente isso que este capítulo proporciona."

    if not secao_tecnica:
        tema_tecnico = rng.choice(TEMAS_TECNICOS)
        if tema_tecnico[0] in ("tabela_comparativa", "diagrama_ascii", "lista_verificacao"):
            secao_tecnica = tema_tecnico[1]
        elif tema_tecnico[0] == "exemplo_config":
            secao_tecnica = f"### Estrutura de Referência\n\nA organização de {titulo} no contexto do {nome_livro.lower()} segue parâmetros que podem ser ajustados conforme a necessidade:\n\n{tema_tecnico[1]}"
        else:
            secao_tecnica = f"### Protocolo de Referência\n\nA prática de {titulo} pode ser estruturada conforme o protocolo abaixo, que organiza {nome_livro.lower()} em etapas verificáveis:\n\n{tema_tecnico[1]}"

    if not secao_aplica:
        tipo_ex = rng.choice(TIPOS_EXERCICIO)
        cenario = rng.choice(CENARIOS)
        pool_tit = titulo.lower()

        if tipo_ex[0] == "roteiro":
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                preparacao=f"certifique-se de ter o {nome_livro.lower()} bem compreendido e os dados do negócio (vendas, custos, canais) prontos",
                diagnostico=f"analise o cenário atual: liste os pontos onde {pool_tit} pode ser aplicado e medido",
                implementacao=f"aplique os conceitos e técnicas de {titulo} no cenário escolhido, registrando decisões",
                validacao="verifique se os resultados atendem aos critérios definidos no início do exercício",
                entregavel="um relatório documentando decisões, resultados obtidos e lições aprendidas"
            )
        elif tipo_ex[0] == "desafio":
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                restricao1=f"Use apenas o conhecimento desenvolvido neste capítulo sobre {pool_tit}",
                restricao2="Documente cada decisão com justificativa baseada em dados",
                restricao3="O resultado deve ser reproduzível por outro gestor",
                dica1=f"Comece com um escopo mínimo funcional e adicione complexidade gradualmente",
                dica2=f"Consulte a seção Técnica deste capítulo para referência de parâmetros",
                dica3="Valide com dados reais do seu negócio antes de escalar",
                criterio1="A solução funciona sem erros e cobre os casos principais",
                criterio2="Os critérios de qualidade (métricas, prazos) estão satisfeitos",
                criterio3="A documentação permite que outro gestor replique o resultado"
            )
        else:
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                antes1="decisões por achismo, sem diagnóstico e sem metas claras",
                antes2="verba distribuída por hábito, com retorno não mensurado",
                depois1=f"planejamento estruturado de {pool_tit} com metas, canais e métricas",
                depois2="decisões fundamentadas em dados e revisões regulares",
                metrica_antes1="CAC alto e crescente",
                metrica_depois1="CAC controlado e decrescente",
                ganho1="redução de até 40%",
                metrica_antes2="conversão instável",
                metrica_depois2="conversão previsível",
                ganho2="+15 pontos percentuais",
                licao1=f"O conhecimento de {pool_tit} reduz drasticamente o desperdício e a imprevisibilidade",
                licao2="Documentar decisões cria um repositório reutilizável de conhecimento estratégico",
                licao3="O investimento inicial em planejamento se paga já nos primeiros ciclos de execução"
            )

    # Referências (variadas por capítulo usando seed)
    rng_refs = random.Random(seed)
    refs = list(REFS_BASE)
    extras = list(REF_EXTRA)
    rng_refs.shuffle(extras)
    refs.extend(extras[:3])

    refs_texto = "\n\n".join(refs)

    # CONTEÚDO DO CAPÍTULO — SEM --- ENTRE SEÇÕES
    capitulo = f"""# Capítulo {cap_num} — {titulo}

## 1. Introdução

*{subtitulo}*

O estudo aprofundado de {titulo.lower()} é essencial para quem deseja dominar o {nome_livro.lower()}. Este capítulo apresenta os conceitos fundamentais, as técnicas práticas e as estratégias que permitem aplicar este conhecimento no dia a dia com confiança e previsibilidade.

Ao final deste capítulo, você será capaz de:
1. Compreender os fundamentos teóricos de {titulo.lower()}
2. Aplicar as técnicas no seu contexto de negócio
3. Avaliar e decidir com critério, evitando desperdício de verba
4. Diagnosticar e corrigir os problemas comuns relacionados ao tema

## 2. Explica

{secao_explica}

## 3. Ilustra

{secao_ilustra}

## 4. Técnica

{secao_tecnica}

## 5. Aplica

{secao_aplica}

## 6. Conclusão

Este capítulo apresentou os conceitos e práticas essenciais de {titulo.lower()} no contexto do {nome_livro.lower()}. Os principais aprendizados incluem: a compreensão dos fundamentos teóricos que embasam o tema, as técnicas práticas para aplicação imediata, os protocolos de avaliação e as melhores práticas de planejamento e controle.

A prática iterativa é o caminho mais rápido para a maestria. Experimente aplicar os conceitos deste capítulo no seu negócio real, registre decisões e ajuste conforme a sua necessidade específica. Consulte as referências [2], [3] e [5] para aprofundar o estudo deste tema.

## 7. Referências

{refs_texto}
"""

    return capitulo


def gerar_livro_final(slug, sumario, capitulos_ordenados):
    """Gera o livro_final.md completo para um slug."""
    titulo = sumario.get("titulo_obra", slug)
    subtitulo = sumario.get("subtitulo", "")
    introducao = sumario.get("introducao", "")
    conclusao_texto = sumario.get("conclusao", "")

    hoje = date.today().strftime("%d/%m/%Y")

    # Prefacio
    prefacio = f"""# Prefácio

{introducao}

**Estrutura da Obra**

Este livro está organizado em 4 Partes, totalizando 16 Capítulos, cada um seguindo o framework pedagógico EITA-V2: Explica, Ilustra, Técnica, Aplica.

## Sumário
"""

    sumario_texto = ""
    for parte in sumario.get("partes", []):
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte.get("capitulos", []):
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    # Partes e capitulos (só header da parte quando muda)
    corpo_partes = []
    ultima_parte = 0
    for parte, cap, conteudo in capitulos_ordenados:
        parte_num = parte["parte"]
        if parte_num != ultima_parte:
            corpo_partes.append(f"\n\n# Parte {parte_num} — {parte['titulo_parte']}\n")
            ultima_parte = parte_num
        corpo_partes.append(conteudo)

    corpo_texto = "\n".join(corpo_partes)

    conclusao = f"""# Conclusão

{conclusao_texto}

*Produzido pela Fábrica Agêntica de Livros em {hoje}.*

"""

    livro = f"""# {titulo}

*{subtitulo}*

{prefacio}

{sumario_texto}

{corpo_texto}

{conclusao}

<!--
  Produzido pela Fábrica Agêntica de Livros
  Slug: {slug}
  Série: {SERIES_PLANEJAMENTO.get(slug.split('-')[0], {}).get('nome', '')}
  Capítulos: 16
  Gerado em: {hoje}
-->
"""

    return livro


def gerar_sumario(slug):
    """Gera o sumario_macro.json para um livro."""
    nome, titulo_obra, subtitulo, introducao, conclusao, _ = LIVROS_PLANEJAMENTO[slug]
    serie = slug.split("-")[0]

    partes = []
    for i, titulo_parte in enumerate(SERIES_PARTES.get(serie, ["Parte 1", "Parte 2", "Parte 3", "Parte 4"])):
        parte_num = i + 1
        capitulos = get_capitulos_por_parte(parte_num, serie, nome)
        partes.append({
            "parte": parte_num,
            "titulo_parte": titulo_parte,
            "capitulos": capitulos,
        })

    sumario = {
        "titulo_obra": titulo_obra,
        "subtitulo": subtitulo,
        "introducao": introducao,
        "conclusao": conclusao,
        "serie": SERIES_PLANEJAMENTO.get(serie, {}).get("nome", serie),
        "partes": partes,
    }
    return sumario


def main():
    print("=" * 60)
    print("  GERADOR DAS 5 SÉRIES DE PLANEJAMENTO (MK1-MK5) — 100 LIVROS")
    print("=" * 60)
    print()

    sucessos = 0
    for slug in SLUGS:
        dir_livro = DIR_RAIZ / slug
        dir_caps = dir_livro / "capitulos"
        dir_caps.mkdir(parents=True, exist_ok=True)

        sumario = gerar_sumario(slug)
        sumario_path = dir_livro / "sumario_macro.json"
        with open(sumario_path, "w", encoding="utf-8") as f:
            json.dump(sumario, f, ensure_ascii=False, indent=2)

        titulo_obra = sumario.get("titulo_obra", slug)
        print(f"\n  [{slug}] Gerando capítulos...")
        print(f"  Título: {titulo_obra}")

        capitulos_ordenados = []
        for parte in sumario.get("partes", []):
            for cap in parte.get("capitulos", []):
                cap_num = cap["capitulo"]
                conteudo = gerar_conteudo_capitulo(slug, cap_num, cap, sumario)

                cap_path = dir_caps / f"cap_{cap_num:02d}.md"
                with open(cap_path, "w", encoding="utf-8") as f:
                    f.write(conteudo)
                capitulos_ordenados.append((parte, cap, conteudo))
                print(f"    Cap {cap_num:02d}: {cap['titulo']}")

        print(f"    Gerando livro_final.md...")
        livro_md = gerar_livro_final(slug, sumario, capitulos_ordenados)
        livro_path = dir_livro / "livro_final.md"
        with open(livro_path, "w", encoding="utf-8") as f:
            f.write(livro_md)
        tamanho_kb = livro_path.stat().st_size / 1024
        print(f"    livro_final.md: {tamanho_kb:.0f} KB")
        print(f"    Total: {len(capitulos_ordenados)} capítulos")
        sucessos += 1

    print()
    print("=" * 60)
    print(f"  GERACAO CONCLUIDA: {sucessos}/{len(SLUGS)} livros")
    print("=" * 60)
    print()
    print("  Agora compile os PDFs:")
    print("    python compilar-para-pdf.py " + " ".join(SLUGS[:5]) + " ...")
    print()


if __name__ == "__main__":
    main()
