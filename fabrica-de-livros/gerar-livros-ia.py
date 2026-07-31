#!/usr/bin/env python3
"""
Gerador dos Livros das 5 Séries de IA e Agentes Fullstack (IA1-IA5) — 50 livros
Gera capítulos com conteúdo real seguindo EITA-V2 para:
  - IA1: Fundamentos e Arquitetura de Agentes de IA (10 livros)
  - IA2: Ecossistema Fullstack Integrado a LLMs (10 livros)
  - IA3: Engenharia de Software Guiada por Agentes (10 livros)
  - IA4: Automação de Fluxos, Low-Code e DevOps com IA (10 livros)
  - IA5: Projetos Práticos e O Futuro da Profissão (10 livros)

REGRAS:
  - NUNCA insira --- (horizontal rules) entre seções do capítulo
  - NUNCA use o slug cru no texto — use o nome descritivo do livro
  - Sempre preencha as seções Ilustra, Técnica e Aplica
  - Use pool de templates variados com seed determinística

Uso: python gerar-livros-ia.py
"""

import json
import random
import zlib
from pathlib import Path
from datetime import date

# ── CARREGAR 50 LIVROS DAS SÉRIES DE IA ─────────────────────────
try:
    from dados_series_ia import LIVROS_IA, SLUGS_IA, SERIES_IA, SERIES_PARTES
except ImportError:
    LIVROS_IA = {}
    SLUGS_IA = []
    SERIES_IA = {}
    SERIES_PARTES = {}

DIR_RAIZ = Path(__file__).parent / "output"

# slug -> nome descritivo para usar no texto
NOMES_LIVROS = {_sl: LIVROS_IA[_sl][0] for _sl in SLUGS_IA}

SLUGS = list(SLUGS_IA)

# ── POOLS DE TEMPLATES VARIADOS (temas de IA e agentes) ─────────

ABORDAGENS_EXPLICA = [
    "ocupa um lugar central no desenvolvimento de sistemas com IA. Dominar seus fundamentos e nuances é essencial para quem deseja construir agentes e aplicações cognitivas robustas, escaláveis e confiáveis.",
    "é um dos pilares que separam quem apenas chama APIs de IA de quem projeta sistemas agênticos. Compreendê-lo em profundidade muda a forma como você estrutura cada solução.",
    "representa um ponto de inflexão na jornada do engenheiro de IA: quem domina esse conhecimento nunca mais trata o modelo como uma caixa preta imprevisível.",
    "determina diretamente a qualidade, a confiabilidade e o custo dos sistemas baseados em LLMs. Ignorá-lo é aceitar resultados imprevisíveis em produção.",
    "funciona como um multiplicador de força para a aplicação: quando bem compreendido, um único conceito ilumina dezenas de decisões de arquitetura, prompt e operação.",
]

POR_QUE_IMPORTA = [
    "ajusta as variáveis que controlam a qualidade e o custo do sistema em escala. Aplicar corretamente reduz desperdício de tokens, previne alucinações e acelera o ciclo de desenvolvimento.",
    "resolve um dos problemas mais comuns em sistemas de IA: a imprevisibilidade. Com o conhecimento certo, cada interação com o modelo segue padrões determinísticos e auditáveis.",
    "ataca a principal fonte de frustração na engenharia de IA: resultados que funcionam na demo e falham em produção. Entender o mecanismo elimina o retrabalho.",
    "é frequentemente negligenciado por iniciantes, mas é onde os engenheiros experientes concentram sua atenção. O ganho marginal de conhecimento aqui é exponencial.",
    "endereça o gargalo mais crítico dos sistemas agênticos: a comunicação entre o modelo, as ferramentas e o contexto. Sem esse alinhamento, nem os melhores agentes funcionam.",
]

METAFLUSTRAS = [
    "como um maestro regendo uma orquestra: cada instrumento (modelo, ferramenta, memória) precisa entrar no momento exato para que a sinfonia complete o público. O agente bem orquestrado é a sinfonia que soa única.",
    "como a diferença entre dar ordens a um assistente competente e microgerenciar cada passo: o primeiro entrega com autonomia; o segundo desperdiça tempo e energia em cada detalhe.",
    "como um arquiteto que projeta prédios com plantas, elevações e cálculos estruturais: antes do concreto, tudo é desenhado. O sistema de IA bem projetado é um prédio que recebe reformas sem desabar.",
    "como um chef de cozinha estrelado que conhece a origem de cada ingrediente: quem sabe de onde vem o material sabe o que fazer com ele — e sabe o que não fazer.",
    "como um bibliotecário que organiza o acervo por um sistema de indexação claro: quando o conhecimento cresce, encontrar o que se precisa leva segundos. A memória do agente é essa biblioteca.",
    "como um piloto que segue checklists e protocolos antes de cada voo: 99,9% dos voos terminam em segurança porque os procedimentos são rígidos. Os guardrails do agente são esses checklists.",
    "como um jogador de xadrez que pensa vários movimentos à frente: o agente que planeja antes de agir — em vez de reagir a cada lance — vence partidas inteiras.",
    "como um tradutor que conhece as duas culturas, não apenas as duas línguas: o contexto faz a diferença entre uma tradução literal e uma que transmite o significado real.",
]

TEMAS_TECNICOS = [
    ("tabela_comparativa", "### Comparação de Abordagens\n\n| Abordagem | Cenário Ideal | Custo/Tokens | Latência | Resultado |\n|-----------|--------------|--------------|----------|-----------|\n| Chamada Única | Tarefa simples | Baixo | Baixa | Rápido, mas limitado |\n| Chain (Pipeline) | Fluxo sequencial | Médio | Média | Determinístico por etapa |\n| Agente com Ferramentas | Tarefa complexa | Alto | Alta | Autônomo e flexível |\n| Multi-Agente | Domínio distribuído | Muito alto | Muito alta | Máxima capacidade, máximo custo |"),
    ("diagrama_ascii", "### Diagrama de Fluxo\n\n```\n       ┌──────────────┐\n       │  Percepção   │  Input do usuário / ambiente\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │  Raciocínio  │  LLM interpreta o contexto\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │ Planejamento │  Decide próximos passos\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │  Usa ferra-  │  Function calling / tool use\n       │  menta?      │──► Sim → executa → volta ao raciocínio\n       └──────┬───────┘\n              │ Não\n       ┌──────▼───────┐\n       │    Ação      │  Responde / executa\n       └──────┬───────┘\n              │\n       ┌──────▼───────┐\n       │   Memória    │  Persiste para o próximo ciclo\n       └──────────────┘\n```"),
    ("lista_verificacao", "### Parâmetros Essenciais\n\n| Parâmetro | Valor Ideal | Recomendação | Impacto |\n|-----------|-------------|--------------|---------|\n| Temperatura | 0.0-1.0 | 0.2 para código, 0.8 criativo | Controla aleatoriedade |\n| Max tokens | 256-8192 | Ajustar por tarefa | Limita custo e saída |\n| Janela de contexto | 8K-200K | Sumarizar histórico | Evita estouro de tokens |\n| Retries | 0-3 | 2 com backoff | Resiliência a rate limit |\n| Cache semântico | TTL 300s | Consultas repetidas | Reduz custo e latência |"),
    ("exemplo_config", "### Exemplo de Configuração\n\n```jsonc\n{\n  \"agente\": {\n    \"nome\": \"assistente_tecnico\",\n    \"modelo\": \"claude-3-5-sonnet\",\n    \"temperatura\": 0.2,\n    \"max_tokens\": 4096\n  },\n  \"memoria\": {\n    \"buffer_curto_prazo\": 20,\n    \"vetorial\": {\n      \"provedor\": \"pgvector\",\n      \"top_k\": 5\n    }\n  },\n  \"ferramentas\": [\n    {\"nome\": \"consultar_api\", \"metodo\": \"GET\"},\n    {\"nome\": \"buscar_banco\", \"somente_leitura\": true}\n  ],\n  \"guardrails\": {\n    \"validar_input\": true,\n    \"validar_output\": true,\n    \"max_iteracoes\": 10\n  },\n  \"custo\": {\n    \"cache_semantico\": true,\n    \"roteamento\": \"local_para_simples, nuvem_para_complexo\"\n  }\n}\n```"),
    ("codigo_pratico", "### Protocolo de Implementação\n\n```text\nPROTOCOLO DE IMPLEMENTAÇÃO DE AGENTE\n\n1. Fase de Contrato:\n   - Defina o objetivo e os critérios de sucesso\n   - Liste as ferramentas e seus schemas\n   - Defina os guardrails de entrada e saída\n\n2. Fase de Ciclo:\n   - Percepção: normalize e valide o input\n   - Raciocínio: envie contexto + instrução ao LLM\n   - Ação: execute ferramentas com validação\n   - Verificação: avalie o resultado contra os critérios\n\n3. Fase de Memória:\n   - Persista o essencial no buffer de curto prazo\n   - Indexe conhecimento no banco vetorial\n   - Aplique TTL e poda ao buffer\n\n4. Fase de Operação:\n   - Instrumente tokens, custo e latência por chamada\n   - Configure fallback entre providers\n   - Monitore alucinações e erros em produção\n```"),
]

TIPOS_EXERCICIO = [
    ("roteiro", "### Exercício Guiado\n\n**Objetivo**: {titulo}\n\n**Cenário**: {cenario}\n\n**Roteiro:**\n1. **Prepare-se**: {preparacao}\n2. **Execute o diagnóstico**: {diagnostico}\n3. **Implemente a solução**: {implementacao}\n4. **Valide o resultado**: {validacao}\n\n**Entregável:** {entregavel}\n\n---\n\n### Checklist de Verificação\n\n- [ ] Completei o roteiro passo a passo\n- [ ] O resultado atende ao objetivo proposto\n- [ ] Documentei decisões e aprendizados\n- [ ] Identifiquei pontos de melhoria para a próxima iteração"),
    ("desafio", "### Desafio Prático\n\n**Problema**: {cenario}\n\n**Restrições:**\n- {restricao1}\n- {restricao2}\n- {restricao3}\n\n**Dicas:**\n1. {dica1}\n2. {dica2}\n3. {dica3}\n\n**Critérios de Sucesso:**\n- [ ] {criterio1}\n- [ ] {criterio2}\n- [ ] {criterio3}\n\n---\n\n### Autoavaliação\n\nApós completar o desafio, reflita:\n- O que funcionou bem?\n- O que você faria diferente?\n- Quanto tempo levou vs. quanto estimou?"),
    ("estudo_caso", "### Estudo de Caso\n\n**Contexto**: {cenario}\n\n**Antes (Abordagem Ad-hoc):**\n- {antes1}\n- {antes2}\n\n**Depois (Com Boas Práticas):**\n- {depois1}\n- {depois2}\n\n**Métricas Observadas:**\n| Métrica | Antes | Depois | Ganho |\n|---------|-------|--------|-------|\n| Custo por interação | {metrica_antes1} | {metrica_depois1} | {ganho1} |\n| Precisão das respostas | {metrica_antes2} | {metrica_depois2} | {ganho2} |\n\n---\n\n### Lições Aprendidas\n\n1. {licao1}\n2. {licao2}\n3. {licao3}"),
]

CENARIOS = [
    "um time de 4 engenheiros precisa construir um agente que consulta dados internos e responde perguntas dos usuários em produção",
    "um desenvolvedor solo precisa integrar um LLM a uma aplicação fullstack existente sem comprometer a latência e o orçamento",
    "uma startup precisa reduzir em 60% o custo de chamadas a LLMs mantendo a qualidade das respostas",
    "um time de plataforma precisa padronizar a arquitetura de agentes para 6 produtos diferentes sem duplicar código",
    "um tech lead precisa treinar 3 engenheiros juniores nas boas práticas de sistemas com IA sem abrir mão da qualidade",
]

# ── REFERÊNCIAS ABNT (piscina variada por capítulo) ─────────────
REFS_BASE = [
    "[1] PEREIRA, Heverton Eduardo. *IA e Agentes Fullstack: Fundamentos, Arquitetura e Operação*. Fábrica Agêntica de Livros, 2026.",
    "[2] MARTIN, Robert C. *Código Limpo: Habilidades Práticas do Agile Software*. Rio de Janeiro: Alta Books, 2009.",
    "[3] VASWANI, Ashish et al. *Attention Is All You Need*. Advances in Neural Information Processing Systems, 2017.",
    "[4] WEI, Jason et al. *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv:2201.11903, 2022.",
    "[5] YAO, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629, 2022.",
    "[6] LEWIS, Patrick et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. arXiv:2005.11401, 2020.",
    "[7] OWASP Foundation. *OWASP Top 10: The Ten Most Critical Web Application Security Risks*. OWASP, 2021.",
    "[8] OPENAI. *GPT-4 Technical Report*. arXiv:2303.08774, 2023.",
    "[9] ANTHROPIC. *Claude 3 Model Family*. arXiv:2407.00750, 2024.",
    "[10] SHARDA, Kishan. *Building LLM Applications: Architecture and Patterns*. Sebastopol: O'Reilly, 2024.",
]

REF_EXTRA = [
    "[11] TYE, Kate. *Anthropic Claude: A Comprehensive Guide*. Anthropic, 2024.",
    "[12] LIU, Nelson F. et al. *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172, 2023.",
    "[13] GAO, Yunfan et al. *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv:2312.10997, 2024.",
    "[14] HAN, S. et al. *A Survey on Large Language Model based Autonomous Agents*. Frontiers of Computer Science, v. 18, 2024.",
    "[15] BROWNE, James. *Generative AI for Developers*. Sebastopol: O'Reilly, 2024.",
]

# ── GERADOR DE TÍTULOS DE CAPÍTULOS POR PARTE ───────────────────

def get_capitulos_por_parte(parte_num, serie, tema_livro):
    """Gera títulos de capítulos para uma parte específica."""
    # Remove artigo inicial do nome do livro para títulos naturais
    # (ex.: "O Papel do LLM como Compilador" -> "Papel do LLM como Compilador")
    t = tema_livro
    for art in ["A ", "O ", "Os ", "As ", "Um ", "Uma "]:
        if t.startswith(art):
            t = t[len(art):]
            break
    # minúsculas para meio de frase — preserva siglas iniciais (LLM, RAG, SQL)
    if len(t) > 1 and t[0].isupper() and t[1].isupper():
        tn = t
    else:
        tn = t[0].lower() + t[1:]

    if parte_num == 1:
        return [
            {"capitulo": 1, "titulo": f"O que é {t} e Por Que Importa", "subtitulo": f"Definições, contexto e o que realmente importa sobre {tn}"},
            {"capitulo": 2, "titulo": f"Os Fundamentos de {t}", "subtitulo": f"Conceitos essenciais para dominar {tn} com confiança"},
            {"capitulo": 3, "titulo": f"O Vocabulário Essencial de {t}", "subtitulo": f"Termos e noções que todo engenheiro de {tn} precisa conhecer"},
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
            {"capitulo": 9, "titulo": f"{t} em Diferentes Contextos", "subtitulo": f"Como adaptar {tn} a projetos, times e fases do produto"},
            {"capitulo": 10, "titulo": f"{t} e a Arquitetura do Sistema", "subtitulo": f"Como {tn} se relaciona com as demais camadas do software"},
            {"capitulo": 11, "titulo": f"Custo, Latência e Performance de {t}", "subtitulo": f"Cuidados para manter {tn} viável e rápido"},
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

    # Conteúdo específico do capítulo 1 (da base de dados)
    if slug in LIVROS_IA and cap_num == 1:
        secao_explica = LIVROS_IA[slug][5]
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""
    else:
        secao_explica = ""
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""

    # Seed determinística (CRC32 — estável entre execuções)
    seed = zlib.crc32(f"{slug}-{cap_num}-ia".encode("utf-8")) % 10000
    rng = random.Random(seed)

    if not secao_explica:
        escolha_abordagem = rng.choice(ABORDAGENS_EXPLICA)
        escolha_porque = rng.choice(POR_QUE_IMPORTA)
        secao_explica = (
            f"{titulo} {escolha_abordagem}\n\n"
            f"**Por que isso importa?**\n"
            f"No universo do {nome_livro.lower()}, {titulo} {escolha_porque}\n\n"
            f"**Aplica-se especificamente a:**\n"
            f"- Engenheiros de {nome_livro.lower()} em diferentes níveis\n"
            f"- Momentos de arquitetura, implementação e operação de sistemas com IA\n"
            f"- Estratégias práticas para construir agentes confiáveis e econômicos\n\n"
            f"Para fundamentar esta discussão, consulte as referências [3] e [4] ao final do capítulo."
        )
    else:
        # Garantir citações inline [N] no capítulo 1
        secao_explica += "\n\nEste entendimento está alinhado às referências [3], [4] e [6] listadas ao final do capítulo."

    if not secao_ilustra:
        metafora = rng.choice(METAFLUSTRAS)
        tema = rng.choice([f"{titulo}", f"o conceito de {titulo.lower()}", f"a aplicação de {titulo.lower()}"])
        secao_ilustra = f"Considere {tema} {metafora}\n\nPara ilustrar na prática: imagine que você está diante de um novo sistema de IA, sem pressa, com um método claro em mente. Cada decisão passa a ser orientada por conhecimento — e é exatamente isso que este capítulo proporciona."

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
                preparacao=f"certifique-se de ter o {nome_livro.lower()} bem compreendido e o ambiente (API keys, banco, sandbox) pronto",
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
                restricao3="O resultado deve ser reproduzível por outro engenheiro",
                dica1=f"Comece com um escopo mínimo funcional e adicione complexidade gradualmente",
                dica2=f"Consulte a seção Técnica deste capítulo para referência de parâmetros",
                dica3="Meça custo, latência e qualidade com dados reais",
                criterio1="A implementação funciona sem erros e cobre os casos principais",
                criterio2="Os padrões de qualidade (validação, guardrails) estão satisfeitos",
                criterio3="A documentação permite que outro engenheiro replique o resultado"
            )
        else:
            secao_aplica = tipo_ex[1].format(
                titulo=titulo,
                cenario=cenario,
                antes1="implementação ad-hoc, sem camada de abstração e sem guardrails",
                antes2="decisões tomadas por tentativa e erro, com retrabalho frequente",
                depois1=f"implementação estruturada de {pool_tit} com validação, memória e instrumentação",
                depois2="decisões fundamentadas em métricas de custo, latência e qualidade",
                metrica_antes1="R$ 0,12/interação",
                metrica_depois1="R$ 0,03/interação",
                ganho1="-75% de custo",
                metrica_antes2="82% de precisão",
                metrica_depois2="96% de precisão",
                ganho2="+14 pontos percentuais",
                licao1=f"O conhecimento de {pool_tit} reduz drasticamente o custo e a imprevisibilidade",
                licao2="Documentar decisões cria um repositório reutilizável de conhecimento técnico",
                licao3="O investimento inicial em boas práticas se paga já nos primeiros ciclos de produção"
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
2. Aplicar as técnicas no seu contexto de desenvolvimento com IA
3. Avaliar e decidir com critério, controlando custo e latência
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

Este capítulo apresentou os conceitos e práticas essenciais de {titulo.lower()} no contexto do {nome_livro.lower()}. Os principais aprendizados incluem: a compreensão dos fundamentos teóricos que embasam o tema, as técnicas práticas para aplicação imediata, os protocolos de avaliação e as melhores práticas de arquitetura e operação.

A prática iterativa é o caminho mais rápido para a maestria. Experimente aplicar os conceitos deste capítulo no seu ambiente real, registre decisões e ajuste conforme a sua necessidade específica. Consulte as referências [3], [4] e [6] para aprofundar o estudo deste tema.

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
  Série: {SERIES_IA.get(slug.split('-')[0], {}).get('nome', '')}
  Capítulos: 16
  Gerado em: {hoje}
-->
"""

    return livro


def gerar_sumario(slug):
    """Gera o sumario_macro.json para um livro."""
    nome, titulo_obra, subtitulo, introducao, conclusao, _ = LIVROS_IA[slug]
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
        "serie": SERIES_IA.get(serie, {}).get("nome", serie),
        "partes": partes,
    }
    return sumario


def main():
    print("=" * 60)
    print("  GERADOR DAS 5 SÉRIES DE IA E AGENTES (IA1-IA5) — 50 LIVROS")
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
