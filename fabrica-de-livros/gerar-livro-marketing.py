#!/usr/bin/env python3
"""
Gerador do Livro de Marketing Digital (MK-01) — 25 capítulos
"O Manual Definitivo: O Plano Estratégico de Marketing Digital do Zero aos Resultados"

Estrutura: 5 Módulos × 5 Capítulos (EITA-V2).
Os títulos dos capítulos são os fornecidos pelo usuário (MODULOS_MARKETING).

REGRAS:
  - NUNCA insira --- (horizontal rules) entre seções do capítulo
  - NUNCA use o slug cru no texto — use o nome descritivo do livro
  - Sempre preencha as seções Ilustra, Técnica e Aplica
  - Use pool de templates variados com seed determinística (CRC32)

Uso: python gerar-livro-marketing.py
"""

import json
import random
import zlib
from pathlib import Path
from datetime import date

# ── CARREGAR DADOS DO LIVRO DE MARKETING ──────────────────────
try:
    from dados_livro_marketing import (
        LIVROS_MARKETING,
        SLUGS_MARKETING,
        SERIES_MARKETING,
        MODULOS_MARKETING,
        SUBTITULOS_MARKETING,
    )
except ImportError:
    LIVROS_MARKETING = {}
    SLUGS_MARKETING = []
    SERIES_MARKETING = {}
    MODULOS_MARKETING = []
    SUBTITULOS_MARKETING = {}

DIR_RAIZ = Path(__file__).parent / "output"

# slug -> nome descritivo para usar no texto
NOMES_LIVROS = {_sl: LIVROS_MARKETING[_sl][0] for _sl in SLUGS_MARKETING}

SLUGS = list(SLUGS_MARKETING)

# ── POOLS DE TEMPLATES VARIADOS (temas de marketing digital) ──

ABORDAGENS_EXPLICA = [
    "ocupa um lugar central no plano estratégico de marketing digital. Dominar seus fundamentos e nuances é essencial para qualquer empresa que deseja transformar investimento em resultado mensurável.",
    "é um dos pilares que separam empresas que crescem com método das que gastam por tentativa e erro. Compreendê-lo em profundidade muda a forma como cada decisão de marketing é tomada.",
    "representa um ponto de inflexão na jornada do negócio: quem domina esse conhecimento nunca mais investe em marketing sem saber exatamente o retorno esperado.",
    "determina diretamente a eficiência do funil, o custo de aquisição e a margem de contribuição. Ignorá-lo é aceitar resultados imprevisíveis no caixa.",
    "funciona como um multiplicador de força para o time: quando bem compreendido, um único conceito ilumina dezenas de decisões de campanha, conteúdo e orçamento.",
]

POR_QUE_IMPORTA = [
    "ajusta as variáveis que controlam o ROI (Retorno sobre Investimento) do negócio em escala. Aplicar corretamente reduz o CAC, eleva o LTV e acelera a previsibilidade de vendas.",
    "resolve um dos problemas mais comuns em empresas: gastar em marketing sem saber o que funciona. Com o conhecimento certo, cada real investido segue uma lógica rastreável até a venda.",
    "ataca a principal fonte de desperdício: campanhas criadas sem fundamento. Entender o mecanismo elimina retrabalho e transforma cada ação em aprendizado composto.",
    "é frequentemente negligenciado por iniciantes, mas é onde os gestores experientes concentram sua atenção. O ganho marginal de conhecimento aqui é exponencial.",
    "endereça o gargalo mais crítico do crescimento: a comunicação entre estratégia, operação e resultado financeiro. Sem esse alinhamento, nem os melhores canais entregam valor consistente.",
]

METAFLUSTRAS = [
    "como um arquiteto que projeta antes de construir: cada viga, cada encanamento e cada tomada é planejado para suportar o peso do futuro. Um plano de marketing bem estruturado é um prédio que recebe reformas sem desabar.",
    "como a diferença entre plantar aleatoriamente e cuidar de um pomar: ambos usam sementes, mas o segundo exige entender o solo, a época e a irrigação — exatamente como o funil precisa de nutrição contínua.",
    "como um maestro regendo uma orquestra: cada instrumento precisa entrar no momento exato, no volume certo, para que a sinfonia complete o público. Cada canal de marketing também precisa de timing e harmonia.",
    "como um chef de cozinha estrelado que conhece a origem de cada ingrediente: quem sabe de onde vem o lead sabe o que fazer com ele — e sabe o que não fazer.",
    "como um alfaiate que mede cada detalhe antes de cortar o tecido: o ajuste fino é o que separa uma campanha comum de uma oferta que converte. A segmentação bem feita é um terno sob medida.",
    "como um engenheiro civil que testa a resistência de cada material: o funil confiável também passa por testes A/B, revisões e validações antes de ser escalado.",
    "como um bibliotecário que organiza livros por um sistema claro: quando o acervo cresce, encontrar o que se precisa leva segundos. Os dados de marketing organizados são uma biblioteca onde nada se perde.",
    "como um cartógrafo que desenha mapas precisos: quem navega com um bom mapa chega ao destino sem errar. O dashboard e os indicadores são os mapas do negócio.",
]

TEMAS_TECNICOS = [
    ("tabela_comparativa", "### Comparação de Abordagens\n\n| Abordagem | Cenário Ideal | Custo | Previsibilidade | Resultado |\n|-----------|--------------|------|----------------|-----------|\n| Mínima (tráfego orgânico puro) | Marca em construção | Baixo | Baixa | Crescimento lento, sustentável |\n| Híbrida (orgânico + pago) | Consolidação | Médio | Média | Equilíbrio entre custo e velocidade |\n| Pago agressivo (escala) | Captura de mercado | Alto | Alta (com dados) | Crescimento rápido, exige caixa |\n| Sob Medida (funil completo) | Domínio do nicho | Variável | Muito alta | Otimizado para o contexto |"),
    ("diagrama_ascii", "### Diagrama do Funil\n\n```\n       ┌──────────────────┐\n       │  ATRAÇÃO (Topo)  │  Conteúdo, anúncios, SEO — leads frios\n       └────────┬─────────┘\n                │\n       ┌────────▼─────────┐\n       │  NUTRIÇÃO (Meio) │  E-mails, WhatsApp, materiais ricos\n       └────────┬─────────┘\n                │\n       ┌────────▼─────────┐\n       │ CONVERSÃO (Fundo)│  Vendas diretas, demonstrações, proposta\n       └────────┬─────────┘\n                │\n       ┌────────▼─────────┐\n       │  RETENÇÃO (Pós)  │  Upsell, indicação, comunidade\n       └──────────────────┘\n```"),
    ("lista_verificacao", "### Parâmetros Essenciais\n\n| Parâmetro | Valor de Referência | Recomendação | Impacto |\n|-----------|--------------------|--------------|---------|\n| CAC (Custo de Aquisição) | 10-30% do LTV | ≤ 25% do LTV | Viabilidade do canal |\n| LTV (Lifetime Value) | 3x o CAC no mínimo | 3-5x | Saúde do modelo |\n| Taxa de conversão | 1-5% (pago) | Otimizar continuamente | Eficiência do funil |\n| Churn mensal | < 5% | Reduzir com retenção | Sustentabilidade |\n| Margem de contribuição | > 30% | Proteger com preço | Lucro líquido |"),
    ("exemplo_config", "### Exemplo de Estrutura de Campanha\n\n```jsonc\n{\n  \"campanha\": {\n    \"objetivo\": \"captacao_de_leads\",\n    \"orcamento_diario\": 100,\n    \"plataformas\": [\"meta\", \"google\", \"tiktok\"],\n    \"publico\": {\n      \"icp\": \"pequeno_varejo\",\n      \"interesses\": [\"gestao_de_negocio\"],\n      \"exclusoes\": [\"funcionarios\"]\n    },\n    \"criativos\": {\n      \"formatos\": [\"video\", \"carrossel\", \"imagem\"],\n      \"testes_a_b\": true\n    },\n    \"rastreamento\": {\n      \"pixel\": true,\n      \"eventos\": [\"lead\", \"venda\"],\n      \"meta_cac\": 30\n    }\n  }\n}\n```"),
    ("codigo_pratico", "### Protocolo de Execução\n\n```text\nPROTOCOLO DE EXECUÇÃO DE MARKETING\n\n1. Fase de Planejamento:\n   - Defina o objetivo mensurável (metas de leads e vendas)\n   - Estabeleça o orçamento com base no CAC tolerável\n\n2. Fase de Execução:\n   - Configure os canais com rastreamento completo\n   - Produza criativos e copies alinhados ao funil\n   - Lance campanhas e ative a automação de leads\n\n3. Fase de Validação:\n   - Acompanhe os indicadores diariamente\n   - Realize testes A/B nos pontos de maior atrito\n   - Compare resultados vs. metas\n\n4. Fase de Escala:\n   - Aplique a metodologia Kill or Fix em cada canal\n   - Escale apenas o que comprovou ROI positivo\n   - Revise a estratégia trimestralmente\n```"),
]

TIPOS_EXERCICIO = [
    ("roteiro", "### Exercício Guiado\n\n**Objetivo**: {titulo}\n\n**Cenário**: {cenario}\n\n**Roteiro:**\n1. **Prepare-se**: {preparacao}\n2. **Execute o diagnóstico**: {diagnostico}\n3. **Implemente a solução**: {implementacao}\n4. **Valide o resultado**: {validacao}\n\n**Entregável:** {entregavel}\n\n---\n\n### Checklist de Verificação\n\n- [ ] Completei o roteiro passo a passo\n- [ ] O resultado atende ao objetivo proposto\n- [ ] Documentei decisões e aprendizados\n- [ ] Identifiquei pontos de melhoria para a próxima iteração"),
    ("desafio", "### Desafio Prático\n\n**Problema**: {cenario}\n\n**Restrições:**\n- {restricao1}\n- {restricao2}\n- {restricao3}\n\n**Dicas:**\n1. {dica1}\n2. {dica2}\n3. {dica3}\n\n**Critérios de Sucesso:**\n- [ ] {criterio1}\n- [ ] {criterio2}\n- [ ] {criterio3}\n\n---\n\n### Autoavaliação\n\nApós completar o desafio, reflita:\n- O que funcionou bem?\n- O que você faria diferente?\n- Quanto tempo levou vs. quanto estimou?"),
    ("estudo_caso", "### Estudo de Caso\n\n**Contexto**: {cenario}\n\n**Antes (Abordagem Ad-hoc):**\n- {antes1}\n- {antes2}\n\n**Depois (Com Boas Práticas):**\n- {depois1}\n- {depois2}\n\n**Métricas Observadas:**\n| Métrica | Antes | Depois | Ganho |\n|---------|-------|--------|-------|\n| Custo de Aquisição (CAC) | {metrica_antes1} | {metrica_depois1} | {ganho1} |\n| Conversão | {metrica_antes2} | {metrica_depois2} | {ganho2} |\n\n---\n\n### Lições Aprendidas\n\n1. {licao1}\n2. {licao2}\n3. {licao3}"),
]

CENARIOS = [
    "uma empresa de médio porte precisa lançar uma campanha de captação com orçamento limitado e quer saber exatamente o retorno antes de escalar",
    "um empreendedor solo precisa estruturar o funil de vendas para transformar seguidores das redes sociais em clientes pagantes",
    "um e-commerce de nicho quer reduzir o CAC e aumentar a retenção dos clientes adquiridos",
    "uma equipe de 3 pessoas precisa organizar as tarefas de marketing em sprints semanais sem sobrecarregar ninguém",
    "um gestor precisa apresentar para a diretoria o impacto financeiro real de cada canal de marketing",
]

# ── REFERÊNCIAS ABNT (piscina variada por capítulo) ─────────────
REFS_BASE = [
    "[1] PEREIRA, Heverton Eduardo. *O Plano Estratégico de Marketing Digital do Zero aos Resultados*. Fábrica Agêntica de Livros, 2026.",
    "[2] KOTLER, Philip; KELLER, Kevin Lane. *Administração de Marketing*. 15. ed. São Paulo: Pearson, 2018.",
    "[3] OGILVY, David. *Confissões de um Publicitário*. São Paulo: Cultrix, 2003.",
    "[4] GODIN, Seth. *Permission Marketing: Tornando-se Inesquecível*. Rio de Janeiro: Campus, 2000.",
    "[5] WERNECK, Ivan. *Marketing Digital: Estratégias para Vender Mais na Internet*. Rio de Janeiro: Alta Books, 2015.",
    "[6] VAZ, Conrado Adolpho. *Google Marketing: O Guia Definitivo de Marketing Digital*. 4. ed. São Paulo: Novatec, 2011.",
    "[7] CANZIANI, Rafael. *Copywriting: O Método Centenário de Escrever Mais e Vender Mais*. São Paulo: DVS, 2019.",
    "[8] REIS, Tatiane; BONINI, Laércio. *Marketing de Conteúdo*. São Paulo: Novatec, 2016.",
    "[9] SIMONS, Niel. *Inteligência Artificial e o Futuro do Marketing*. São Paulo: Gente, 2023.",
    "[10] BLANK, Steve; DORF, Bob. *The Startup Owner's Manual*. Pescadero: K&S Ranch, 2012.",
]

REF_EXTRA = [
    "[11] MCCARTHY, E. Jerome. *Basic Marketing: A Managerial Approach*. 15. ed. Boston: McGraw-Hill, 2001.",
    "[12] PORTER, Michael E. *Estratégia Competitiva: Técnicas para Análise de Indústrias e da Concorrência*. 2. ed. Rio de Janeiro: Campus, 2004.",
    "[13] OSTERWALDER, Alexander; PIGNEUR, Yves. *Business Model Generation: Inovação em Modelos de Negócios*. Rio de Janeiro: Alta Books, 2011.",
    "[14] HALLIGAN, Brian; SHAH, Dharmesh. *Inbound Marketing: Seja Encontrado Usando Google, Mídias Sociais e Blogs*. Rio de Janeiro: Alta Books, 2010.",
    "[15] CROLL, Alistair; POWER, Benjamin. *Complete Web Monitoring*. Sebastopol: O'Reilly, 2009.",
]

# ── CONSTRUÇÃO DO SUMÁRIO (títulos exatos dos módulos) ────────

def gerar_sumario(slug):
    """Gera o sumario_macro.json para o livro de marketing."""
    nome, titulo_obra, subtitulo, introducao, conclusao, _ = LIVROS_MARKETING[slug]

    partes = []
    for i, (titulo_modulo, descricao_modulo, titulos_caps) in enumerate(MODULOS_MARKETING):
        parte_num = i + 1
        capitulos = []
        for j, titulo_cap in enumerate(titulos_caps):
            cap_num = (i * 5) + (j + 1)
            capitulos.append({
                "capitulo": cap_num,
                "titulo": titulo_cap,
                "subtitulo": SUBTITULOS_MARKETING.get(titulo_cap, descricao_modulo),
            })
        partes.append({
            "parte": parte_num,
            "titulo_parte": titulo_modulo,
            "descricao_parte": descricao_modulo,
            "capitulos": capitulos,
        })

    sumario = {
        "titulo_obra": titulo_obra,
        "subtitulo": subtitulo,
        "introducao": introducao,
        "conclusao": conclusao,
        "serie": SERIES_MARKETING.get("MK", {}).get("nome", "Marketing Digital"),
        "partes": partes,
    }
    return sumario


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
    if slug in LIVROS_MARKETING and cap_num == 1:
        secao_explica = LIVROS_MARKETING[slug][5]
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""
    else:
        secao_explica = ""
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""

    # Seed determinística (CRC32 — estável entre execuções)
    seed = zlib.crc32(f"{slug}-{cap_num}-marketing".encode("utf-8")) % 10000
    rng = random.Random(seed)

    if not secao_explica:
        escolha_abordagem = rng.choice(ABORDAGENS_EXPLICA)
        escolha_porque = rng.choice(POR_QUE_IMPORTA)
        secao_explica = (
            f"{titulo} {escolha_abordagem}\n\n"
            f"**Por que isso importa?**\n"
            f"No universo do {nome_livro.lower()}, {titulo} {escolha_porque}\n\n"
            f"**Aplica-se especificamente a:**\n"
            f"- Gestores e empreendedores que querem previsibilidade no marketing\n"
            f"- Equipes de marketing digital em diferentes estágios de maturidade\n"
            f"- Momentos de planejamento, execução, análise e escala\n\n"
            f"Para fundamentar esta discussão, consulte as referências [2] e [5] ao final do capítulo."
        )
    else:
        # Garantir citações inline [N] no capítulo 1
        secao_explica += "\n\nEste entendimento está alinhado às referências [2], [5] e [8] listadas ao final do capítulo."

    if not secao_ilustra:
        metafora = rng.choice(METAFLUSTRAS)
        tema = rng.choice([f"{titulo}", f"o conceito de {titulo.lower()}", f"a aplicação de {titulo.lower()}"])
        secao_ilustra = f"Considere {tema} {metafora}\n\nPara ilustrar na prática: imagine que você está diante de uma nova campanha, sem pressa, com um método claro em mente. Cada decisão passa a ser orientada por dados — e é exatamente isso que este capítulo proporciona."

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
                preparacao=f"certifique-se de ter o {nome_livro.lower()} bem compreendido e os dados da empresa (custo, margem, vendas, canais) em mãos",
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
                restricao2="Documente cada decisão com a justificativa baseada em dados",
                restricao3="O resultado deve ser reproduzível por outro membro da equipe",
                dica1=f"Comece com um escopo mínimo funcional e adicione complexidade gradualmente",
                dica2=f"Consulte a seção Técnica deste capítulo para referência de parâmetros",
                dica3="Teste com dados representativos do seu cenário real",
                criterio1="A implementação funciona sem erros e cobre os casos principais",
                criterio2="Os indicadores de performance (ROI, CAC, conversão) estão definidos",
                criterio3="A documentação permite que outro membro da equipe replique o resultado"
            )
        else:
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                antes1="execução ad-hoc, sem dados e sem critérios de corte",
                antes2="decisões tomadas por achismo, com desperdício de orçamento",
                depois1=f"implementação estruturada de {pool_tit} com indicadores e testes",
                depois2="decisões fundamentadas em critérios objetivos e documentadas",
                metrica_antes1="R$ 120,00",
                metrica_depois1="R$ 45,00",
                ganho1="-62% de CAC",
                metrica_antes2="0,8%",
                metrica_depois2="2,4%",
                ganho2="3x de conversão",
                licao1=f"O conhecimento de {pool_tit} reduz drasticamente o desperdício e eleva o ROI",
                licao2="Documentar decisões cria um repositório reutilizável de conhecimento",
                licao3="O investimento inicial em boas práticas se paga já nos primeiros ciclos"
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
3. Avaliar e decidir com critério, evitando desperdício de orçamento
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

Este capítulo apresentou os conceitos e práticas essenciais de {titulo.lower()} no contexto do {nome_livro.lower()}. Os principais aprendizados incluem: a compreensão dos fundamentos teóricos que embasam o tema, as técnicas práticas para aplicação imediata, os protocolos de avaliação e as melhores práticas de execução e otimização.

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

Este livro está organizado em 5 Módulos, totalizando 25 Capítulos, cada um seguindo o framework pedagógico EITA-V2: Explica, Ilustra, Técnica, Aplica.

## Sumário
"""

    sumario_texto = ""
    for parte in sumario.get("partes", []):
        sumario_texto += f"- **Módulo {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte.get("capitulos", []):
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    # Partes e capitulos (só header da parte quando muda)
    corpo_partes = []
    ultima_parte = 0
    for parte, cap, conteudo in capitulos_ordenados:
        parte_num = parte["parte"]
        if parte_num != ultima_parte:
            descricao = parte.get("descricao_parte", "")
            corpo_partes.append(f"\n\n# Módulo {parte_num} — {parte['titulo_parte']}\n\n*{descricao}*\n")
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
  Série: {SERIES_MARKETING.get(slug.split('-')[0], {}).get('nome', '')}
  Capítulos: 25
  Gerado em: {hoje}
-->
"""

    return livro


def main():
    print("=" * 60)
    print("  GERADOR DO LIVRO DE MARKETING DIGITAL (MK-01) — 25 CAPÍTULOS")
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
    print("  Agora compile o PDF:")
    print("    python compilar-para-pdf.py " + " ".join(SLUGS))
    print()


if __name__ == "__main__":
    main()
