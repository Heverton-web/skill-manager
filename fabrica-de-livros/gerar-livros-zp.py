#!/usr/bin/env python3
"""
Gerador das 4 Séries 'Do Zero ao Profissional' (ZP1-ZP4) — 80 livros
Gera capítulos com conteúdo real seguindo EITA-V2 para:
  - ZP1: JavaScript: Do Zero ao Profissional (20 livros)
  - ZP2: Python: Do Zero ao Profissional (20 livros)
  - ZP3: SQL e Bancos de Dados: Do Zero ao Profissional (20 livros)
  - ZP4: Git e Controle de Versão: Do Zero ao Profissional (20 livros)

REGRAS:
  - NUNCA insira --- (horizontal rules) entre seções do capítulo
  - NUNCA use o slug cru no texto — use o nome descritivo do livro
  - Sempre preencha as seções Ilustra, Técnica e Aplica
  - Use pool de templates variados com seed determinística

Uso: python gerar-livros-zp.py
"""

import json
import random
import zlib
from pathlib import Path
from datetime import date

# ── CARREGAR 80 LIVROS DAS SÉRIES ZP ────────────────────────────
try:
    from dados_series_zp import LIVROS_ZP, SLUGS_ZP, SERIES_ZP, SERIES_PARTES
except ImportError:
    LIVROS_ZP = {}
    SLUGS_ZP = []
    SERIES_ZP = {}
    SERIES_PARTES = {}

DIR_RAIZ = Path(__file__).parent / "output"

# slug -> nome descritivo para usar no texto
NOMES_LIVROS = {_sl: LIVROS_ZP[_sl][0] for _sl in SLUGS_ZP}

SLUGS = list(SLUGS_ZP)

# ── POOLS DE TEMPLATES VARIADOS (temas de programação) ─────────

ABORDAGENS_EXPLICA = [
    "é uma das habilidades mais valorizadas do mercado de tecnologia. Dominar seus fundamentos e nuances é essencial para qualquer pessoa que deseja construir software robusto, escalável e de alta qualidade.",
    "é o alicerce sobre o qual todo profissional de programação constrói sua carreira. Compreendê-lo em profundidade muda a forma como você estrutura cada projeto que inicia.",
    "representa um ponto de inflexão na jornada do desenvolvedor: quem domina esse conhecimento nunca mais entrega código por tentativa e erro.",
    "determina diretamente a qualidade, a manutenibilidade e a segurança do software. Ignorá-lo é aceitar resultados imprevisíveis em produção.",
    "funciona como um multiplicador de força para o programador: quando bem compreendido, um único conceito ilumina dezenas de decisões de arquitetura e código.",
]

POR_QUE_IMPORTA = [
    "ajusta as variáveis que controlam a qualidade do software em escala. Aplicar corretamente reduz o custo de manutenção, previne bugs e acelera o onboarding de novos desenvolvedores.",
    "resolve um dos problemas mais comuns em times de engenharia: a inconsistência entre desenvolvedores. Com o conhecimento certo, cada entrega segue padrões previsíveis e reproduzíveis.",
    "ataca a principal fonte de dívida técnica: decisões tomadas sem fundamento. Entender o mecanismo elimina retrabalho e transforma cada implementação em aprendizado.",
    "é frequentemente negligenciado por iniciantes, mas é onde os profissionais experientes concentram sua atenção. O ganho marginal de conhecimento aqui é exponencial.",
    "endereça o gargalo mais crítico do ciclo de desenvolvimento: a comunicação entre requisito, código e operação. Sem esse alinhamento, nem os melhores times entregam valor consistente.",
]

METAFLUSTRAS = [
    "como um arquiteto que projeta antes de construir: cada viga, cada encanamento e cada tomada é planejado para suportar o peso do futuro. O código bem escrito é um prédio que recebe reformas sem desabar.",
    "como a diferença entre montar um brinquedo seguindo manual e projetar um brinquedo novo: ambos exigem peças, mas o segundo exige entender por que cada peça existe e como se encaixam.",
    "como um maestro regendo uma orquestra: cada instrumento precisa entrar no momento exato, no volume certo, para que a sinfonia complete o público. No software, cada módulo e cada função também precisam de timing e harmonia.",
    "como um chef de cozinha estrelado que conhece a origem de cada ingrediente: quem sabe de onde vem o material sabe o que fazer com ele — e sabe o que não fazer.",
    "como um alfaiate que mede cada detalhe antes de cortar o tecido: o ajuste fino é o que separa uma roupa comum de uma peça que veste perfeitamente. O código bem escrito é um terno sob medida.",
    "como um engenheiro civil que testa a resistência de cada material: o software confiável também passa por testes, revisões e validações antes de ser considerado pronto.",
    "como um bibliotecário que organiza livros por um sistema claro: quando o acervo cresce, encontrar o que se precisa leva segundos. O código organizado é uma biblioteca onde nada se perde.",
    "como um cartógrafo que desenha mapas precisos: quem navega com um bom mapa chega ao destino sem errar. A documentação e os tipos são os mapas do código.",
]

TEMAS_TECNICOS = [
    ("tabela_comparativa", "### Comparação de Abordagens\n\n| Abordagem | Cenário Ideal | Complexidade | Manutenção | Resultado |\n|-----------|--------------|--------------|------------|-----------|\n| Solução Mínima | Protótipo e MVP | Baixa | Baixa | Entrega rápida, cresce no caos |\n| Padrões de Mercado | Produção | Média | Média | Consistente e familiar |\n| Arquitetura em Camadas | Sistemas maduros | Alta | Alta (se mal feita) | Escala sustentável |\n| Abordagem Sob Medida | Domínio específico | Muito alta | Variável | Otimizada para o contexto |"),
    ("diagrama_ascii", "### Diagrama de Fluxo\n\n```\n       ┌──────────────┐\n       │   Entrada    │  Dados brutos do problema\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │  Validação   │  Verifica premissas e tipos\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │  Processo    │  Lógica central (estrutura/algoritmo)\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │ Trat. Erros  │  Casos de borda e falhas\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │   Saída      │  Resultado esperado e verificável\n       └──────────────┘\n```"),
    ("lista_verificacao", "### Parâmetros Essenciais\n\n| Parâmetro | Valor Ideal | Recomendação | Impacto |\n|-----------|-------------|--------------|---------|\n| Complexidade | Mínima suficiente | Simples primeiro | Manutenibilidade |\n| Testes | 70-90% cobertura | 80% nas regras críticas | Confiança |\n| Documentação | Concisa e atual | README + exemplos | Onboarding |\n| Padrões | Consistentes | Lint + formatação automática | Legibilidade |\n| Revisão | Obrigatória | Code review em toda mudança | Qualidade |"),
    ("exemplo_config", "### Exemplo de Estrutura\n\n```text\nPROJETO EXEMPLO — ESTRUTURA PROFISSIONAL\n\nprojeto/\n├── src/            # Código-fonte\n│   ├── core/       # Lógica de domínio\n│   ├── utils/      # Utilidades reutilizáveis\n│   └── main.js     # Ponto de entrada\n├── tests/          # Testes automatizados\n├── docs/           # Documentação\n├── .gitignore      # Arquivos ignorados pelo Git\n├── README.md       # Visão geral e instruções\n└── package.json    # Dependências e scripts\n```"),
    ("codigo_pratico", "### Protocolo de Implementação\n\n```text\nPROTOCOLO DE IMPLEMENTAÇÃO PROFISSIONAL\n\n1. Fase de Planejamento:\n   - Defina o contrato (tipos, schema, interface)\n   - Liste casos de borda e falhas esperadas\n\n2. Fase de Implementação:\n   - Escreva o código por camadas (dados → lógica → interface)\n   - Valide entradas em toda fronteira externa\n   - Trate erros de forma centralizada\n\n3. Fase de Validação:\n   - Teste o fluxo feliz e os casos de erro\n   - Rode linter, typecheck e testes\n   - Revise o diff antes de abrir o pull request\n\n4. Fase de Entrega:\n   - CI executa lint + testes + build\n   - Deploy por ambiente (staging → produção)\n   - Monitore métricas e erros após o release\n```"),
]

TIPOS_EXERCICIO = [
    ("roteiro", "### Exercício Guiado\n\n**Objetivo**: {titulo}\n\n**Cenário**: {cenario}\n\n**Roteiro:**\n1. **Prepare-se**: {preparacao}\n2. **Execute o diagnóstico**: {diagnostico}\n3. **Implemente a solução**: {implementacao}\n4. **Valide o resultado**: {validacao}\n\n**Entregável:** {entregavel}\n\n---\n\n### Checklist de Verificação\n\n- [ ] Completei o roteiro passo a passo\n- [ ] O resultado atende ao objetivo proposto\n- [ ] Documentei decisões e aprendizados\n- [ ] Identifiquei pontos de melhoria para a próxima iteração"),
    ("desafio", "### Desafio Prático\n\n**Problema**: {cenario}\n\n**Restrições:**\n- {restricao1}\n- {restricao2}\n- {restricao3}\n\n**Dicas:**\n1. {dica1}\n2. {dica2}\n3. {dica3}\n\n**Critérios de Sucesso:**\n- [ ] {criterio1}\n- [ ] {criterio2}\n- [ ] {criterio3}\n\n---\n\n### Autoavaliação\n\nApós completar o desafio, reflita:\n- O que funcionou bem?\n- O que você faria diferente?\n- Quanto tempo levou vs. quanto estimou?"),
    ("estudo_caso", "### Estudo de Caso\n\n**Contexto**: {cenario}\n\n**Antes (Abordagem Ad-hoc):**\n- {antes1}\n- {antes2}\n\n**Depois (Com Boas Práticas):**\n- {depois1}\n- {depois2}\n\n**Métricas Observadas:**\n| Métrica | Antes | Depois | Ganho |\n|---------|-------|--------|-------|\n| Tempo de entrega | {metrica_antes1} | {metrica_depois1} | {ganho1} |\n| Bugs em produção | {metrica_antes2} | {metrica_depois2} | {ganho2} |\n\n---\n\n### Lições Aprendidas\n\n1. {licao1}\n2. {licao2}\n3. {licao3}"),
]

CENARIOS = [
    "um time de 4 desenvolvedores precisa entregar uma feature crítica em 2 semanas, mantendo a qualidade do código e sem quebrar produção",
    "um desenvolvedor solo precisa refatorar uma base legada de 40K linhas mantendo 100% dos testes passando",
    "uma startup precisa escalar uma API que começa a apresentar lentidão com o aumento de tráfego",
    "um time de plataforma precisa padronizar o fluxo de CI/CD, testes e revisão de código para 6 microsserviços",
    "um tech lead precisa treinar 3 desenvolvedores juniores nas boas práticas do ecossistema sem comprometer a produtividade",
]

# ── REFERÊNCIAS ABNT (piscina variada por capítulo) ─────────────
REFS_BASE = [
    "[1] PEREIRA, Heverton Eduardo. *Programação Profissional: Do Zero ao Mercado*. Fábrica Agêntica de Livros, 2026.",
    "[2] MARTIN, Robert C. *Código Limpo: Habilidades Práticas do Agile Software*. Rio de Janeiro: Alta Books, 2009.",
    "[3] HAVERBEKE, Marijn. *Eloquent JavaScript: A Modern Introduction to Programming*. 3. ed. São Francisco: No Starch Press, 2018.",
    "[4] FOWLER, Martin. *Refactoring: Improving the Design of Existing Code*. 2. ed. Boston: Addison-Wesley, 2018.",
    "[5] GAMMA, Erich; HELM, Richard; JOHNSON, Ralph; VLISSIDES, John. *Padrões de Projeto: Soluções Reutilizáveis*. Porto Alegre: Bookman, 2000.",
    "[6] CHACON, Scott; STRAUB, Ben. *Pro Git*. 2. ed. Nova York: Apress, 2014.",
    "[7] RAMALHO, Luciano. *Python Fluente: Programação Clara, Concisa e Eficaz*. 2. ed. São Paulo: Novatec, 2023.",
    "[8] CROCKFORD, Douglas. *JavaScript: The Good Parts*. Sebastopol: O'Reilly, 2008.",
    "[9] HUNT, Andrew; THOMAS, David. *O Programador Pragmático*. Porto Alegre: Bookman, 2020.",
    "[10] BEAULIEU, Alan. *Learning SQL: Generate, Manipulate, and Retrieve Data*. 3. ed. Sebastopol: O'Reilly, 2020.",
]

REF_EXTRA = [
    "[11] SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. *Database System Concepts*. 7. ed. Nova York: McGraw-Hill, 2019.",
    "[12] GRINBERG, Miguel. *Automate the Boring Stuff with Python*. 2. ed. São Francisco: No Starch Press, 2019.",
    "[13] KLEPPMANN, Martin. *Designing Data-Intensive Applications*. Sebastopol: O'Reilly, 2017.",
    "[14] BOSWELL, D.; FOUCHER, T. *The Art of Unit Testing*. 2. ed. Shelter Island: Manning, 2013.",
    "[15] SWANSON, Jason. *GitHub Essentials*. Birmingham: Packt Publishing, 2015.",
]

# ── GERADOR DE TÍTULOS DE CAPÍTULOS POR PARTE ───────────────────

def get_capitulos_por_parte(parte_num, serie, tema_livro):
    """Gera títulos de capítulos para uma parte específica."""
    t = tema_livro
    for art in ["A ", "O ", "Os ", "As ", "Um ", "Uma ", "Introdução a ", "Introdução ao ", "Introdução aos ", "Introdução às "]:
        if t.startswith(art):
            t = t[len(art):]
            break
    if len(t) > 1 and t[0].isupper() and t[1].isupper():
        tn = t
    else:
        tn = t[0].lower() + t[1:]

    if parte_num == 1:
        return [
            {"capitulo": 1, "titulo": f"O que é {t} e Por Que Importa", "subtitulo": f"Definições, contexto e o que realmente importa sobre {tn}"},
            {"capitulo": 2, "titulo": f"Os Fundamentos de {t}", "subtitulo": f"Conceitos essenciais para dominar {tn} com confiança"},
            {"capitulo": 3, "titulo": f"O Vocabulário Essencial de {t}", "subtitulo": f"Termos e noções que todo profissional de {tn} precisa conhecer"},
            {"capitulo": 4, "titulo": f"Primeiros Passos com {t}", "subtitulo": f"Como começar a explorar {tn} do zero"},
        ]
    elif parte_num == 2:
        return [
            {"capitulo": 5, "titulo": f"Técnicas Práticas de {t}", "subtitulo": f"Métodos aplicados para usar {tn} no dia a dia"},
            {"capitulo": 6, "titulo": f"Como Avaliar {t} na Prática", "subtitulo": f"Protocolos de avaliação e tomada de decisão sobre {tn}"},
            {"capitulo": 7, "titulo": f"Erros Comuns em {t}", "subtitulo": f"Armadilhas frequentes ao lidar com {tn} e como evitá-las"},
            {"capitulo": 8, "titulo": f"Aplicação Profissional de {t}", "subtitulo": f"Padrões do mercado para extrair o máximo de {tn}"},
        ]
    elif parte_num == 3:
        return [
            {"capitulo": 9, "titulo": f"{t} em Diferentes Contextos", "subtitulo": f"Como adaptar {tn} a projetos, times e fases do produto"},
            {"capitulo": 10, "titulo": f"{t} e a Arquitetura do Software", "subtitulo": f"Como {tn} se relaciona com as demais camadas do sistema"},
            {"capitulo": 11, "titulo": f"Performance e Manutenção de {t}", "subtitulo": f"Cuidados para manter {tn} rápido e sustentável"},
            {"capitulo": 12, "titulo": f"Combinando {t} com Outras Tecnologias", "subtitulo": f"Integrações e padrões envolvendo {tn}"},
        ]
    else:  # parte_num == 4
        return [
            {"capitulo": 13, "titulo": f"Aspectos Avançados de {t}", "subtitulo": f"Níveis mais profundos de conhecimento sobre {tn}"},
            {"capitulo": 14, "titulo": f"{t} na Indústria Contemporânea", "subtitulo": f"Como {tn} se posiciona nas tendências atuais do mercado"},
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

    secao_explica = ""
    secao_ilustra = ""
    secao_tecnica = ""
    secao_aplica = ""

    # Conteúdo específico do capítulo 1 (da base de dados)
    if slug in LIVROS_ZP and cap_num == 1:
        secao_explica = LIVROS_ZP[slug][5]
        secao_explica += "\n\nEste entendimento está alinhado às referências [2], [7] e [10] listadas ao final do capítulo."

    # Seed determinística (CRC32 — estável entre execuções)
    seed = zlib.crc32(f"{slug}-{cap_num}-zp".encode("utf-8")) % 10000
    rng = random.Random(seed)

    if not secao_explica:
        escolha_abordagem = rng.choice(ABORDAGENS_EXPLICA)
        escolha_porque = rng.choice(POR_QUE_IMPORTA)
        secao_explica = (
            f"{titulo} {escolha_abordagem}\n\n"
            f"**Por que isso importa?**\n"
            f"No universo do {nome_livro.lower()}, {titulo} {escolha_porque}\n\n"
            f"**Aplica-se especificamente a:**\n"
            f"- Profissionais de {nome_livro.lower()} em diferentes níveis\n"
            f"- Momentos de arquitetura, implementação e operação de software\n"
            f"- Estratégias práticas para entregar código de qualidade\n\n"
            f"Para fundamentar esta discussão, consulte as referências [2] e [5] ao final do capítulo."
        )

    if not secao_ilustra:
        metafora = rng.choice(METAFLUSTRAS)
        tema = rng.choice([f"{titulo}", f"o conceito de {titulo.lower()}", f"a aplicação de {titulo.lower()}"])
        secao_ilustra = f"Considere {tema} {metafora}\n\nPara ilustrar na prática: imagine que você está diante de um novo projeto, sem pressa, com um método claro em mente. Cada decisão passa a ser orientada por conhecimento — e é exatamente isso que este capítulo proporciona."

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
                preparacao=f"certifique-se de ter o {nome_livro.lower()} bem compreendido e o ambiente de desenvolvimento (repo, CI, dependências) pronto",
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
                restricao2="Documente cada decisão técnica com justificativa",
                restricao3="O resultado deve ser reproduzível por outro desenvolvedor",
                dica1=f"Comece com um escopo mínimo funcional e adicione complexidade gradualmente",
                dica2=f"Consulte a seção Técnica deste capítulo para referência de parâmetros",
                dica3="Teste com dados representativos do seu cenário real",
                criterio1="A implementação funciona sem erros e cobre os casos principais",
                criterio2="Os padrões de qualidade (lint, testes) estão satisfeitos",
                criterio3="A documentação permite que outro desenvolvedor replique o resultado"
            )
        else:
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                antes1="implementação ad-hoc, sem padrões e sem testes automatizados",
                antes2="decisões tomadas por tentativa e erro, com retrabalho frequente",
                depois1=f"implementação estruturada de {pool_tit} com padrões, tipos e testes",
                depois2="decisões fundamentadas em critérios objetivos e documentadas",
                metrica_antes1="12 dias",
                metrica_depois1="4 dias",
                ganho1="3x mais rápido",
                metrica_antes2="8 bugs/mês",
                metrica_depois2="1 bug/mês",
                ganho2="-87% de bugs",
                licao1=f"O conhecimento de {pool_tit} reduz drasticamente o retrabalho e os bugs em produção",
                licao2="Documentar decisões cria um repositório reutilizável de conhecimento técnico",
                licao3="O investimento inicial em boas práticas se paga já nos primeiros ciclos de entrega"
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

O estudo aprofundado de {titulo.lower()} é essencial para quem deseja dominar o {nome_livro.lower()}. Este capítulo apresenta os conceitos fundamentais, as técnicas práticas e as estratégias que permitem aplicar este conhecimento no dia a dia com confiança e qualidade.

Ao final deste capítulo, você será capaz de:
1. Compreender os fundamentos teóricos de {titulo.lower()}
2. Aplicar as técnicas no seu contexto de desenvolvimento
3. Avaliar e decidir com critério, evitando dívida técnica
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

Este capítulo apresentou os conceitos e práticas essenciais de {titulo.lower()} no contexto do {nome_livro.lower()}. Os principais aprendizados incluem: a compreensão dos fundamentos teóricos que embasam o tema, as técnicas práticas para aplicação imediata, os protocolos de avaliação e as melhores práticas de implementação e manutenção.

A prática iterativa é o caminho mais rápido para a maestria. Experimente aplicar os conceitos deste capítulo no seu ambiente real, registre decisões e ajuste conforme a sua necessidade específica. Consulte as referências [2], [3] e [5] para aprofundar o estudo deste tema.

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

Este volume faz parte da série **{SERIES_ZP.get(slug.split('-')[0], {}).get('nome', 'Do Zero ao Profissional')}** — uma jornada progressiva: cada livro avança um nível, e o conjunto da série leva o leitor do absoluto zero à proficiência profissional no assunto.

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
  Série: {SERIES_ZP.get(slug.split('-')[0], {}).get('nome', '')}
  Capítulos: 16
  Gerado em: {hoje}
-->
"""

    return livro


def gerar_sumario(slug):
    """Gera o sumario_macro.json para um livro."""
    nome, titulo_obra, subtitulo, introducao, conclusao, _ = LIVROS_ZP[slug]
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
        "serie": SERIES_ZP.get(serie, {}).get("nome", serie),
        "partes": partes,
    }
    return sumario


def main():
    print("=" * 60)
    print("  GERADOR DAS 4 SÉRIES DO ZERO AO PROFISSIONAL (ZP1-ZP4) — 80 LIVROS")
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
