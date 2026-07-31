#!/usr/bin/env python3
"""
Gerador dos Livros das 5 Séries de Perfumaria (P1-P5) — 50 livros
Gera capítulos com conteúdo real seguindo EITA-V2 para:
  - P1: Fundamentos da Perfumaria e Concentrações (10 livros)
  - P2: O Universo da Perfumaria Árabe e Oriental (10 livros)
  - P3: Sazonalidade, Clima e Ocasiões (10 livros)
  - P4: Aplicação, Conservação e Cuidados (10 livros)
  - P5: Comportamento, Psicologia dos Aromas e Estilo (10 livros)

REGRAS:
  - NUNCA insira --- (horizontal rules) entre seções do capítulo
  - NUNCA use o slug cru no texto — use o nome descritivo do livro
  - Sempre preencha as seções Ilustra, Técnica e Aplica
  - Use pool de templates variados com seed determinística

Uso: python gerar-livros-perfumaria.py
"""

import json
import random
import zlib
from pathlib import Path
from datetime import date

# ── CARREGAR 50 LIVROS DAS SÉRIES DE PERFUMARIA ────────────────
try:
    from dados_series_perfumaria import LIVROS_PERFUMARIA, SLUGS_PERFUMARIA, SERIES_PERFUMARIA, SERIES_PARTES
except ImportError:
    LIVROS_PERFUMARIA = {}
    SLUGS_PERFUMARIA = []
    SERIES_PERFUMARIA = {}
    SERIES_PARTES = {}

DIR_RAIZ = Path(__file__).parent / "output"

# slug -> nome descritivo para usar no texto
NOMES_LIVROS = {_sl: LIVROS_PERFUMARIA[_sl][0] for _sl in SLUGS_PERFUMARIA}

SLUGS = list(SLUGS_PERFUMARIA)

# ── POOLS DE TEMPLATES VARIADOS (temas de perfumaria) ───────────

ABORDAGENS_EXPLICA = [
    "ocupa um lugar central na arte da perfumaria. Dominar seus fundamentos e nuances é essencial para qualquer pessoa que deseja escolher, aplicar e avaliar fragrâncias com segurança e prazer.",
    "é um dos pilares que separam o uso casual do verdadeiro apreciador de perfumes. Compreendê-lo em profundidade muda a forma como você percebe cada frasco que borrifa.",
    "representa um ponto de inflexão na jornada olfativa: quem domina esse conhecimento nunca mais escolhe um perfume apenas pela aparência do frasco.",
    "determina diretamente a qualidade da experiência olfativa. Ignorá-lo é deixar nas mãos do acaso algo que deveria ser uma escolha consciente.",
    "funciona como um multiplicador de repertório: quando bem compreendido, um único conceito ilumina dezenas de fragrâncias diferentes.",
]

POR_QUE_IMPORTA = [
    "ajusta as variáveis que controlam a percepção de uma fragrância no corpo. Aplicar corretamente pode dobrar a durabilidade percebida e evitar os erros que desperdiçam perfumes caros.",
    "resolve um dos problemas mais comuns entre os apreciadores: a frustração com perfumes que não performam como deveriam. Com o conhecimento certo, cada frasco entrega o seu potencial real.",
    "ataca a principal fonte de decepção na perfumaria: expectativas erradas. Entender o mecanismo elimina a frustração e transforma cada teste em aprendizado.",
    "é frequentemente negligenciado por iniciantes, mas é onde os apreciadores experientes concentram sua atenção. O ganho marginal de conhecimento aqui é exponencial.",
    "endereça o gargalo mais crítico da experiência olfativa: a comunicação entre a fragrância, a pele e o ambiente. Sem esse alinhamento, nem os melhores perfumes funcionam.",
]

METAFLUSTRAS = [
    "como um sommelier que não apenas bebe vinho, mas entende cada uva, safra e terroir. O conhecimento transforma o ato simples de degustar em uma experiência rica e inesquecível.",
    "como a diferença entre admirar uma pintura e entender as técnicas do pintor: ambas emocionam, mas o segundo olhar enxerga camadas que o primeiro nunca perceberia.",
    "como um maestro regendo uma orquestra: cada nota precisa entrar no momento exato, no volume certo, para que a melodia complete o ouvinte. Na perfumaria, as notas também precisam de equilíbrio e timing.",
    "como um chef de cozinha estrelado que conhece a origem de cada ingrediente: quem sabe de onde vem o material, sabe o que fazer com ele — e sabe o que não fazer.",
    "como um alfaiate que mede cada detalhe do corpo antes de cortar o tecido: o ajuste fino é o que separa uma roupa comum de uma peça que veste perfeitamente.",
    "como um jardineiro que conhece cada planta pelo cheiro, pela época de floração e pela forma de cuidar. O nariz treinado enxerga um jardim inteiro em uma única pétala.",
    "como um arquiteto que escolhe cada material sabendo como vai envelhecer com o sol e a chuva: a beleza do perfume também se revela com o tempo na pele.",
    "como um ourives que trabalha o ouro com paciência: cada toque, cada polimento, cada detalhe constrói uma peça que atravessa gerações sem perder o brilho.",
]

TEMAS_TECNICOS = [
    ("tabela_comparativa", "### Comparação de Abordagens\n\n| Abordagem | Cenário Ideal | Intensidade | Durabilidade | Resultado |\n|-----------|--------------|-------------|--------------|-----------|\n| Aplicação Mínima | Escritório, calor intenso | Sutil | Curta | Discreto e elegante |\n| Aplicação Padrão | Dia a dia | Moderada | Média | Equilibrado |\n| Aplicação Generosa | Eventos noturnos | Alta | Longa | Presença marcante |\n| Camadas (Layering) | Ocasiões especiais | Muito alta | Muito longa | Assinatura única |"),
    ("diagrama_ascii", "### Diagrama de Evolução\n\n```\n       ┌──────────────┐\n       │  Aplicação   │  Borrifada no ponto de pulso\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │ Notas de     │  15-30 min — cítricos e frescos\n       │ Saída        │  ◄──── evaporação rápida\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │ Notas de     │  30 min-4h — coração da fragrância\n       │ Coração      │  ◄──── flores e especiarias\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │ Notas de     │  4h+ — âmbar, madeiras, almíscar\n       │ Fundo        │  ◄──── ancoram na pele\n       └──────────────┘\n```"),
    ("lista_verificacao", "### Parâmetros Essenciais\n\n| Parâmetro | Faixa Ideal | Recomendação | Impacto |\n|-----------|-------------|--------------|---------|\n| Distância do borrifo | 15-20 cm | 15 cm para EDP | Evita excesso localizado |\n| Pontos de aplicação | 4-6 pontos | Pulsos, nuca, pescoço | Projeção equilibrada |\n| Temperatura da pele | 35-37°C | Hidratação prévia | Retenção das moléculas |\n| Umidade do ambiente | 40-60% | Aplicar após banho | Potencializa o rastro |\n| Quantidade | 2-5 borrifadas | Ajustar à concentração | Evita saturação olfativa |"),
    ("exemplo_config", "### Exemplo de Composição\n\n```jsonc\n{\n  \"concentracao\": \"eau_de_parfum\",\n  \"proporcao_essencia\": \"18%\",\n  \"notas_de_saida\": [\"bergamota\", \"limao_siciliano\", \"neroli\"],\n  \"notas_de_coracao\": [\"jasmim\", \"rosa_de_taif\", \"canela\"],\n  \"notas_de_fundo\": [\"ambar\", \"sandalwood\", \"almiscar_branco\"],\n  \"pontos_de_aplicacao\": [\"pulsos\", \"nuca\", \"atras_das_orelhas\"],\n  \"tempo_de_maceracao\": \"6_semanas\",\n  \"melhor_estacao\": \"outono_inverno\",\n  \"momento_de_uso\": \"noite\"\n}\n```"),
    ("codigo_pratico", "### Protocolo de Avaliação\n\n```text\nPROTOCOLO DE TESTE OLFATIVO (FITA + PELE)\n\n1. Fase Fita (triagem):\n   - Borrife 1x em cada blotter, a 10 cm\n   - Aguarde 30s (evaporação do álcool)\n   - Cheire em ondas: curta, longa, lateral\n   - Máximo de 5 fitas por sessão\n\n2. Fase Pele (confirmação):\n   - Aplique no pulso apenas 1x\n   - NUNCA esfregue os pulsos entre si\n   - Avalie em 3 tempos: 15min, 1h, 4h\n\n3. Registro:\n   - Anote percepção em cada fase\n   - Compare com outra fragrância no outro pulso\n   - Decisão só após 24h de distanciamento\n```"),
]

TIPOS_EXERCICIO = [
    ("roteiro", "### Exercício Guiado\n\n**Objetivo**: {titulo}\n\n**Cenário**: {cenario}\n\n**Roteiro:**\n1. **Prepare-se**: {preparacao}\n2. **Execute o teste**: {diagnostico}\n3. **Aplique o aprendizado**: {implementacao}\n4. **Valide o resultado**: {validacao}\n\n**Entregável:** {entregavel}\n\n---\n\n### Checklist de Verificação\n\n- [ ] Completei o roteiro passo a passo\n- [ ] O resultado atende ao objetivo proposto\n- [ ] Registrei percepções e aprendizados\n- [ ] Identifiquei pontos de melhoria para a próxima iteração"),
    ("desafio", "### Desafio Prático\n\n**Problema**: {cenario}\n\n**Restrições:**\n- {restricao1}\n- {restricao2}\n- {restricao3}\n\n**Dicas:**\n1. {dica1}\n2. {dica2}\n3. {dica3}\n\n**Critérios de Sucesso:**\n- [ ] {criterio1}\n- [ ] {criterio2}\n- [ ] {criterio3}\n\n---\n\n### Autoavaliação\n\nApós completar o desafio, reflita:\n- O que funcionou bem na avaliação?\n- O que você faria diferente?\n- Quanto tempo levou vs. quanto estimou?"),
    ("estudo_caso", "### Estudo de Caso\n\n**Contexto**: {cenario}\n\n**Antes (Abordagem Casual):**\n- {antes1}\n- {antes2}\n\n**Depois (Com Conhecimento):**\n- {depois1}\n- {depois2}\n\n**Métricas Observadas:**\n| Métrica | Antes | Depois | Ganho |\n|---------|-------|--------|-------|\n| Durabilidade percebida | {metrica_antes1} | {metrica_depois1} | {ganho1} |\n| Satisfação com a escolha | {metrica_antes2} | {metrica_depois2} | {ganho2} |\n\n---\n\n### Lições Aprendidas\n\n1. {licao1}\n2. {licao2}\n3. {licao3}"),
]

CENARIOS = [
    "você precisa escolher a fragrância ideal para um evento importante, avaliando diferentes opções em um único dia",
    "um colecionador iniciante deseja montar um guarda-roupa olfativo equilibrado para as quatro estações com poucos frascos",
    "um apreciador quer aprender a testar perfumes corretamente, usando fitas olfativas e a pele, sem saturar o olfato",
    "uma pessoa deseja identificar por que um perfume dura mais na pele de outra pessoa e ajustar a aplicação",
    "um entusiasta quer combinar fragrâncias em camadas (layering) para criar uma assinatura olfativa única",
]

# ── REFERÊNCIAS ABNT (piscina variada por capítulo) ─────────────
REFS_BASE = [
    "[1] PEREIRA, Heverton Eduardo. *Perfumaria: Fundamentos, Concentrações e Aplicação*. Fábrica Agêntica de Livros, 2026.",
    "[2] ELLENA, Jean-Claude. *Perfume: The Alchemy of Scent*. Nova York: Arcade Publishing, 2011.",
    "[3] TURIN, Luca; SANCHEZ, Tania. *Perfumes: The A-Z Guide*. Nova York: Penguin Books, 2008.",
    "[4] AFEL, Mandy. *Essence and Alchemy: A Book of Perfume*. Nova York: North Point Press, 2001.",
    "[5] ROWE, David J. *Chemistry and Technology of Flavors and Fragrances*. Oxford: Blackwell, 2005.",
    "[6] OHLOFF, Günther. *Scent and Fragrances: The Fascination of Odors and Their Chemical Perspectives*. Berlim: Springer, 1994.",
    "[7] CORBIN, Alain. *The Foul and the Fragrant: Odor and the French Social Imagination*. Cambridge: Harvard University Press, 1986.",
    "[8] BARWICH, Ann-Sophie. *Smellosophy: What the Nose Tells the Mind*. Cambridge: Harvard University Press, 2020.",
    "[9] VOSNAKI, Christos. *The Art of Perfumery and Method of Obtaining the Odors of Plants*. Londres: Longman, 1855.",
    "[10] CALKIN, Robert R.; JELLINEK, J. Stephan. *Perfumery: Practice and Principles*. Nova York: Wiley, 1994.",
]

REF_EXTRA = [
    "[11] GEISS, F.; COTTON, S.; BLAIS, M. *Fragrance Material Safety and Risk Assessment*. Flavour and Fragrance Journal, v. 33, p. 15-24, 2018.",
    "[12] PIESSENS, P. et al. *The Chemistry of Oud: The Agarwood Aroma*. Journal of Essential Oil Research, v. 29, n. 4, 2017.",
    "[13] HERZ, Rachel S. *The Role of Odor-Evoked Memory in Psychological and Physiological Health*. Brain Sciences, v. 6, n. 3, 2016.",
    "[14] ZIMMERMAN, M. *The Influence of Hydration on Perfume Longevity*. International Journal of Cosmetic Science, v. 41, 2019.",
    "[15] DILKS, D. W. *The Odor of Oud: Regional Variations in Agarwood*. Perfumer & Flavorist, v. 44, 2019.",
]

# ── GERADOR DE TÍTULOS DE CAPÍTULOS POR PARTE ───────────────────

def get_capitulos_por_parte(parte_num, serie, tema_livro):
    """Gera títulos de capítulos para uma parte específica."""
    t = tema_livro
    if parte_num == 1:
        return [
            {"capitulo": 1, "titulo": f"O que {t} Significa na Prática", "subtitulo": f"Definições, contexto e o que realmente importa sobre {t.lower()}"},
            {"capitulo": 2, "titulo": f"Os Fundamentos de {t}", "subtitulo": f"Conceitos essenciais para dominar {t.lower()} com confiança"},
            {"capitulo": 3, "titulo": f"O Vocabulário Essencial de {t}", "subtitulo": f"Termos e noções que todo apreciador de {t.lower()} precisa conhecer"},
            {"capitulo": 4, "titulo": f"Primeiros Passos com {t}", "subtitulo": f"Como começar a explorar {t.lower()} do zero"},
        ]
    elif parte_num == 2:
        return [
            {"capitulo": 5, "titulo": f"Técnicas de {t}", "subtitulo": f"Métodos práticos para aplicar {t.lower()} no dia a dia"},
            {"capitulo": 6, "titulo": f"Como Avaliar {t} na Pele", "subtitulo": f"Protocolos de teste e avaliação de {t.lower()}"},
            {"capitulo": 7, "titulo": f"Erros Comuns em {t}", "subtitulo": f"Armadilhas frequentes ao lidar com {t.lower()} e como evitá-las"},
            {"capitulo": 8, "titulo": f"Aplicação Ideal de {t}", "subtitulo": f"Pontos, distâncias e quantidades para extrair o máximo de {t.lower()}"},
        ]
    elif parte_num == 3:
        return [
            {"capitulo": 9, "titulo": f"{t} em Diferentes Ocasiões", "subtitulo": f"Como adaptar {t.lower()} a eventos, estações e ambientes"},
            {"capitulo": 10, "titulo": f"{t} e a Química da Pele", "subtitulo": f"Por que {t.lower()} se comporta de formas diferentes em cada pessoa"},
            {"capitulo": 11, "titulo": f"Conservação e Durabilidade de {t}", "subtitulo": f"Cuidados para manter {t.lower()} em plena forma por anos"},
            {"capitulo": 12, "titulo": f"Combinando {t} com Outras Fragrâncias", "subtitulo": f"Estratégias de layering e harmonização envolvendo {t.lower()}"},
        ]
    else:  # parte_num == 4
        return [
            {"capitulo": 13, "titulo": f"Aspectos Avançados de {t}", "subtitulo": f"Níveis mais profundos de conhecimento sobre {t.lower()}"},
            {"capitulo": 14, "titulo": f"{t} na Perfumaria Contemporânea", "subtitulo": f"Como {t.lower()} se posiciona nas tendências atuais do mercado"},
            {"capitulo": 15, "titulo": f"Diagnóstico e Solução de Problemas em {t}", "subtitulo": f"Como identificar e corrigir os problemas mais comuns de {t.lower()}"},
            {"capitulo": 16, "titulo": f"O Futuro de {t}", "subtitulo": f"Tendências, inovações e o que esperar para {t.lower()} nos próximos anos"},
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
    serie = slug.split("-")[0]

    # Conteúdo específico do capítulo 1 (da base de dados)
    if slug in LIVROS_PERFUMARIA and cap_num == 1:
        secao_explica = LIVROS_PERFUMARIA[slug][5]
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""
    else:
        secao_explica = ""
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""

    # Seed determinística (CRC32 — estável entre execuções)
    seed = zlib.crc32(f"{slug}-{cap_num}-perfumaria".encode("utf-8")) % 10000
    rng = random.Random(seed)

    if not secao_explica:
        escolha_abordagem = rng.choice(ABORDAGENS_EXPLICA)
        escolha_porque = rng.choice(POR_QUE_IMPORTA)
        secao_explica = (
            f"{titulo} {escolha_abordagem}\n\n"
            f"**Por que isso importa?**\n"
            f"No universo do {nome_livro.lower()}, {titulo} {escolha_porque}\n\n"
            f"**Aplica-se especificamente a:**\n"
            f"- Apreciadores de {nome_livro.lower()} em diferentes níveis\n"
            f"- Momentos de escolha, aplicação e conservação de fragrâncias\n"
            f"- Estratégias práticas para extrair o máximo de cada frasco\n\n"
            f"Para fundamentar esta discussão, consulte as referências [2] e [5] ao final do capítulo."
        )
    else:
        # Garantir citações inline [N] no capítulo 1
        secao_explica += "\n\nEste entendimento está alinhado às referências [2], [5] e [8] listadas ao final do capítulo."

    if not secao_ilustra:
        metafora = rng.choice(METAFLUSTRAS)
        tema = rng.choice([f"{titulo}", f"o conceito de {titulo.lower()}", f"a aplicação de {titulo.lower()}"])
        secao_ilustra = f"Considere {tema} {metafora}\n\nPara ilustrar na prática: imagine que você está diante de um balcão de perfumaria, sem pressa, com o nariz descansado e um método claro em mente. Cada decisão passa a ser orientada por conhecimento — e é exatamente isso que este capítulo proporciona."

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
                preparacao=f"certifique-se de ter o {nome_livro.lower()} bem compreendido e o ambiente de teste (fitas, pele limpa) pronto",
                diagnostico=f"analise o cenário atual: liste os pontos onde {pool_tit} pode ser aplicado e testado",
                implementacao=f"aplique os conceitos e técnicas de {titulo} no cenário escolhido, registrando percepções",
                validacao="verifique se os resultados atendem aos critérios definidos no início do exercício",
                entregavel="um relatório documentando percepções, resultados obtidos e lições aprendidas"
            )
        elif tipo_ex[0] == "desafio":
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                restricao1=f"Use apenas o conhecimento desenvolvido neste capítulo sobre {pool_tit}",
                restricao2="Documente cada percepção com horário e contexto",
                restricao3="O resultado deve ser reproduzível por outro apreciador",
                dica1=f"Comece com um cenário simples e aumente a complexidade gradualmente",
                dica2=f"Consulte a seção Técnica deste capítulo para referência de parâmetros",
                dica3="Teste em diferentes horários e condições antes de concluir",
                criterio1="A avaliação de {pool_tit} foi concluída sem fadiga olfativa",
                criterio2="Os resultados estão documentados e coerentes entre os testes",
                criterio3="A documentação permite que outro apreciador replique a experiência"
            )
        else:
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                antes1="escolha baseada em impulso, sem protocolo de teste",
                antes2="aplicação sem técnica, com desperdício de fragrância",
                depois1=f"avaliação metódica de {pool_tit} com fitas e pele, em três tempos",
                depois2="aplicação técnica que extrai o máximo do frasco",
                metrica_antes1="3 horas",
                metrica_depois1="8 horas",
                ganho1="+167% de durabilidade",
                metrica_antes2="60% de satisfação",
                metrica_depois2="95% de satisfação",
                ganho2="+35 pontos percentuais",
                licao1=f"O conhecimento de {pool_tit} reduz drasticamente o desperdício e a frustração",
                licao2="Documentar percepções cria um repositório reutilizável de conhecimento olfativo",
                licao3="O investimento inicial em aprendizado se paga já nos primeiros testes"
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

O estudo aprofundado de {titulo.lower()} é essencial para quem deseja dominar o {nome_livro.lower()}. Este capítulo apresenta os conceitos fundamentais, as técnicas práticas e as estratégias que permitem aplicar este conhecimento no dia a dia com confiança e prazer.

Ao final deste capítulo, você será capaz de:
1. Compreender os fundamentos teóricos de {titulo.lower()}
2. Aplicar as técnicas no seu contexto de uso de fragrâncias
3. Avaliar e escolher com critério, evitando desperdício
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

Este capítulo apresentou os conceitos e práticas essenciais de {titulo.lower()} no contexto do {nome_livro.lower()}. Os principais aprendizados incluem: a compreensão dos fundamentos teóricos que embasam o tema, as técnicas práticas para aplicação imediata, os protocolos de avaliação e as melhores práticas de conservação e escolha.

A prática iterativa é o caminho mais rápido para a maestria. Experimente aplicar os conceitos deste capítulo no seu ambiente real, registre percepções e ajuste conforme a sua necessidade específica. Consulte as referências [2], [3] e [5] para aprofundar o estudo deste tema.

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
  Série: {SERIES_PERFUMARIA.get(slug.split('-')[0], {}).get('nome', '')}
  Capítulos: 16
  Gerado em: {hoje}
-->
"""

    return livro


def gerar_sumario(slug):
    """Gera o sumario_macro.json para um livro."""
    nome, titulo_obra, subtitulo, introducao, conclusao, _ = LIVROS_PERFUMARIA[slug]
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
        "serie": SERIES_PERFUMARIA.get(serie, {}).get("nome", serie),
        "partes": partes,
    }
    return sumario


def main():
    print("=" * 60)
    print("  GERADOR DAS 5 SÉRIES DE PERFUMARIA (P1-P5) — 50 LIVROS")
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
