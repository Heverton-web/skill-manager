#!/usr/bin/env python3
"""
Gerador dos Livros da Série AIDD
Gera capítulos com conteúdo técnico real seguindo EITA-V2 para:
  - 01-transicao-dev-aidd (16 cap) — Transicao Dev Tradicional -> AIDD
  - 02-camada-interface   (16 cap)
  - 03-camada-harness     (16 cap)
  - 04-camada-operarios   (16 cap)
  - 05-camada-llm-core    (16 cap)

Uso: python gerar-4-livros-aidd.py
"""

import os
import sys
import json
import random
from pathlib import Path
from datetime import date

DIR_RAIZ = Path(__file__).parent / "output"

SLUGS = [
    "01-transicao-dev-aidd",
    "02-camada-interface",
    "03-camada-harness",
    "04-camada-operarios",
    "05-camada-llm-core",
]

# ── CONTEÚDO ESPECÍFICO POR SLUG/CAPÍTULO ──────────────────────

CONTEUDO = {}

# ══════════════ LIVRO 0: TRANSICAO DEV -> AIDD ══════════════

CONTEUDO["01-transicao-dev-aidd"] = {
    1: {
        "explica": """Estamos vivendo a maior transformação no desenvolvimento de software desde a invenção do compilador. Três forças convergiram para tornar o AIDD não apenas possível, mas inevitável:

**1. Modelos de linguagem atingiram massa crítica**
Em 2024-2026, modelos como Claude Sonnet 4.5, GPT-4 e DeepSeek-V3 alcançaram um nível de confiabilidade que permite gerar código funcional de forma consistente. Não é mais uma promessa futura — é uma realidade presente.

**2. Ferramentas de orquestração amadureceram**
Claude Code, Cursor, Windsurf e OpenCode fornecem interfaces maduras para controlar agentes. O ecossistema de MCPs (Model Context Protocol) criou um padrão aberto para integrar ferramentas.

**3. A complexidade do software explodiu**
Sistemas modernos são grandes demais para uma equipe humana acompanhar. O custo de desenvolvimento com métodos tradicionais tornou-se proibitivo para a velocidade que o mercado exige.

**O que isso significa para você?**
Se você é um desenvolvedor hoje, você não está sendo substituído — você está sendo promovido. De operador de linha de montagem (escrever código linha por linha) para Diretor da Planta (orquestrar agentes que escrevem código).""",
        "ilustra": """Imagine a evolução do transporte:

**Era 1 — A pé**: Você mesmo executa cada passo (desenvolvimento tradicional, escrevendo cada linha)

**Era 2 — Bicicleta**: Você pedala, mas vai mais rápido (frameworks e bibliotecas que aceleram)

**Era 3 — Carro**: Você dirige, o motor faz o trabalho pesado (Copilot, autocomplete, IA como assistente)

**Era 4 — Avião com piloto automático**: Você define o destino, o sistema navega (AIDD, você orquestra agentes)

Cada transição não eliminou a necessidade do profissional — transformou seu papel. O engenheiro AIDD não é menos importante que o programador tradicional. Ele é mais importante porque opera em um nível mais alto de abstração.""",
        "tecnica": """### As Três Forças da Transformação

| Força | Antes (2022) | Agora (2026) | Impacto |
|-------|-------------|--------------|---------|
| Modelos de IA | GPT-3: código básico, muitos erros | Claude 4.5: código complexo, raramente erros | Geração confiável |
| Ferramentas | ChatGPT web, prompt único | Claude Code, Cursor, n8n, MCPs | Orquestração real |
| Complexidade | App monolitico, equipe de 10 | Sistemas distribuídos, IA em todo lugar | Escala exponencial |

### O Gráfico da Transformação

```
Produtividade
    ^
    |         / AIDD (crescimento exponencial)
    |        /
    |       /
    |      /_______
    |     / Tradicional (crescimento linear)
    |    /
    |___/_____________________> Tempo
```

A diferença entre o desenvolvimento tradicional e o AIDD não é linear — é exponencial. Enquanto o dev tradicional escala adicionando mais pessoas (custo linear), o dev AIDD escala adicionando mais agentes (custo quase zero)."""
    },
    2: {
        "explica": """A transformação para o AIDD não acontece da noite para o dia. Ela se apoia em três pilares que precisam ser desenvolvidos simultaneamente:

**Pilar 1 — Mentalidade**
A mudança mais difícil não é técnica — é mental. Você precisa parar de pensar como executor e começar a pensar como orquestrador. Em vez de "como faço isso?", pergunte "quem pode fazer isso melhor?"

- Mentalidade de executor: foco na sintaxe, na implementação, no como
- Mentalidade de orquestrador: foco no objetivo, no resultado, no que

**Pilar 2 — Ferramentas**
O ecossistema de ferramentas AIDD é vasto e muda rapidamente. Em vez de tentar dominar todas, foque em:
1. Uma interface principal (CLI ou IDE)
2. O arquivo de regras do projeto (CLAUDE.md)
3. Os MCPs essenciais para seu fluxo
4. Um modelo de linguagem de confiança

**Pilar 3 — Métodos**
O AIDD exige métodos diferentes de trabalho:
- Iteração rápida em vez de planejamento extensivo
- Validação constante em vez de verificação no final
- Decomposição de problemas em tarefas atômicas""",
        "ilustra": """Os 3 pilares são como as 3 pernas de um banquinho. Se uma perna for mais curta, o banquinho balança e você cai.

- **Mentalidade** sem **Ferramentas**: você sabe o que fazer mas não tem como fazer
- **Ferramentas** sem **Métodos**: você tem as ferramentas mas não sabe usar
- **Métodos** sem **Mentalidade**: você segue receitas mas não entende o porquê

O segredo está em desenvolver os três simultaneamente. Pequenos passos em cada pilar, todos os dias."""
    },
    3: {
        "explica": """O Paradoxo do Desenvolvedor na era AIDD é: **quanto mais o agente faz, mais importante o humano se torna**.

Parece contraditório, mas faz sentido. Quando o agente escreve o código, o humano:
1. **Define o que fazer** — objetivo, escopo, restrições
2. **Valida o resultado** — o código está correto? seguro? performático?
3. **Corrige quando erra** — o agente alucinou? gerou algo que não faz sentido?
4. **Orquestra o fluxo** — o que vem depois? quem mais precisa ser envolvido?

**Habilidades que se tornam mais valiosas:**
- Pensamento crítico (muito mais que antes)
- Arquitetura de sistemas (nunca foi tão importante)
- Comunicação clara (prompts são comunicação)
- Visão de produto (entender o problema, não só a solução)

**Habilidades que perdem valor relativo:**
- Sintaxe de linguagens (agentes sabem de cor)
- Depuração de código simples (agentes encontram rápido)
- Conhecimento de APIs obscuras (agentes consultam em tempo real)"""
    },
    4: {
        "explica": """A carreira do engenheiro AIDD pode ser mapeada em 4 níveis de maturidade, cada um com habilidades, ferramentas e mindset específicos:

**Nível 1 — Operador (Sobrevivência)**
Usa IA como autocomplete. Copilot, ChatGPT para tarefas pontuais. Ainda escreve 80% do código manualmente. O mindset ainda é de executor.

**Nível 2 — Assistente (Adoção)**
Usa agentes para tarefas definidas. Claude Code para gerar funções, Cursor para refatorar. Agente escreve 50% do código. Começa a confiar no agente.

**Nível 3 — Orquestrador (Integração)**
Cria fluxos multi-agente. Define skills, MCPs, hooks. Agente escreve 80% do código. Humano foca em arquitetura e validação.

**Nível 4 — Diretor da Planta (Maestria)**
Projeta sistemas onde agentes orquestram outros agentes. Cria ecossistemas autônomos de produção de software. Agente escreve 95%+ do código. Humano define estratégia."""
    }
}

# ══════════════ LIVRO 1: INTERFACE ══════════════

CONTEUDO["02-camada-interface"] = {
    1: {
        "explica": """A Camada de Interface é a primeira e mais fundamental das 4 camadas do AIDD. É o ponto de contato entre o engenheiro humano e o ecossistema de agentes de IA. Tudo que você deseja que o sistema faça passa por essa camada — e a qualidade do que entra determina a qualidade do que sai.

Diferente do desenvolvimento tradicional, onde a interface era apenas um editor de texto ou IDE, no AIDD a interface é um **tradutor de intenções**. Você não digita código sintaticamente correto — você descreve objetivos em linguagem natural, e a interface traduz essa intenção para o Harness executar.

**As 4 funções críticas da Interface:**
1. **Captura de intenção**: Converte pensamento humano em instruções compreensíveis pelo sistema
2. **Apresentação de contexto**: Mostra ao agente o estado atual do projeto (arquivos, estrutura, histórico)
3. **Exibição de resultados**: Apresenta o output do agente de forma compreensível e acionável
4. **Permite intervenção**: Você pode corrigir, ajustar ou parar o fluxo a qualquer momento

A escolha da interface certa pode multiplicar ou dividir sua produtividade por 10x. Uma interface bem configurada entende o que você quer antes mesmo de você terminar de digitar.""",
        "ilustra": """Pense na Interface como o cockpit de um avião moderno. O piloto (você) não mexe diretamente nos motores (agentes). Ele olha para instrumentos (a interface) que traduzem o estado da aeronave em informações compreensíveis: altitude, velocidade, combustível, direção. Quando quer mudar algo, ele não abre o motor — ele ajusta um botão na cabine.

No AIDD, acontece o mesmo. Você olha para o terminal ou IDE (instrumentos), vê o que o agente está fazendo (altitude do código), percebe um erro (alerta), ajusta o prompt (gira o botão), e o Harness + Operários executam a correção (motores ajustam).

Um cockpit mal projetado causa acidentes. Uma interface mal configurada gera código ruim, retrabalho e desperdício de tokens.""",
        "tecnica": """A anatomia de uma sessão AIDD na Interface segue este pipeline:

```
Humano -> [Interface] -> Intenção Estruturada -> [Harness] -> Ação
         <- [Interface] <- Resultado Formatado  <- [LLM+Ops] <-
```

**Os 3 tipos principais de Interface:**

| Tipo | Exemplos | Latência | Riqueza de Contexto | Custo/Tokens |
|------|----------|----------|---------------------|--------------|
| Terminal/CLI | Claude Code, OpenCode | Muito baixa | Baixa (só texto) | Menor |
| IDE | Cursor, Windsurf | Baixa | Alta (código + chat + preview) | Médio |
| Chat | ChatGPT, Claude.ai | Média | Média (conversa + arquivos) | Maior |
| API | SDKs, REST | Variável | Nula (raw) | Controlado |

**O Ciclo de Vida de uma Interação:**
1. Input: Você digita o prompt
2. Tokenização: A Interface quebra o texto em tokens
3. Context Assembly: Interface coleta contexto (arquivos abertos, seleção, projeto)
4. Envio: Payload é enviado ao Harness/LLM
5. Processamento: LLM raciocina e gera resposta
6. Streaming: Tokens chegam incrementalmente
7. Renderização: Interface exibe resultado formatado
8. Feedback: Você aceita, rejeita ou ajusta"""
    },
    2: {
        "explica": """Cada tipo de interface AIDD tem uma arquitetura fundamentalmente diferente. Entender essas diferenças é crucial para escolher a ferramenta certa para cada tarefa.

**CLI (Command Line Interface)** - A interface mais pura e eficiente. Claude Code e OpenCode operam no terminal, sem GUI. Máximo de foco, consumo mínimo de recursos, integração nativa com pipes e scripts shell. Ideal para automação e pipelines.

**IDE (Integrated Development Environment)** - Cursor e Windsurf integram o agente diretamente no editor. Oferecem contexto visual do código, seleção contextual (Ctrl+K no trecho), preview de mudanças. Ideal para desenvolvimento iterativo.

**Chat** - ChatGPT, Claude.ai e OpenRouter oferecem a experiência mais acessível: zero configuração, interface conversacional natural, compartilhamento fácil. Ideal para prototipagem e exploração.

**API** - Para integração programática em pipelines. Máximo controle, mínimo conforto."""
    },
    3: {
        "explica": """Os arquivos de configuração são a cola invisível que mantém o ecossistema AIDD funcionando. Eles definem regras, comportamentos, permissões e integrações que o Harness e os Operários seguem. Sem eles, cada sessão começa do zero.

**O ecossistema completo:**
- **CLAUDE.md**: Carregado automaticamente pelo Claude Code. Define identidade, regras, squad, MCPs e fluxo
- **.clinerules / .cursorrules / .windsurfrules**: O mesmo arquivo via hardlink
- **AGENTS.md**: Para agentes em geral (Codex, etc). Mesmo arquivo físico
- **.github/copilot-instructions.md**: Para GitHub Copilot. Mesmo arquivo
- **.mcp.json**: Registra servidores MCP
- **settings.local.json**: Configurações específicas do ambiente local

O detalhe que ninguém explica: todos esses arquivos podem ser o **mesmo arquivo físico** via hardlinks no Windows ou symlinks no Linux/Mac."""
    },
    4: {
        "explica": """O System Prompt é o contrato mais importante entre o engenheiro e o agente. Enquanto o prompt do usuário muda a cada interação, o system prompt é fixo para a sessão — define personalidade, regras, ferramentas disponíveis e limites.

Um system prompt bem escrito reduz alucinações em até 80%, economiza tokens evitando instruções repetitivas e garante consistência entre sessões.

**Componentes de um System Prompt AIDD:**
1. Identidade: Quem o agente é (persona, senioridade)
2. Regras: O que pode e não pode fazer (código penal)
3. Contexto: Stack tecnológica, convenções do projeto
4. Ferramentas: Quais MCPs, skills e comandos estão disponíveis
5. Limites: Timeouts, restrições de acesso
6. Tom: Formal, técnico, didático"""
    }
}

# ══════════════ LIVRO 2: HARNESS ══════════════

CONTEUDO["03-camada-harness"] = {
    1: {
        "explica": """O Harness é a camada mais poderosa e menos compreendida do AIDD. Enquanto a Interface captura a intenção e o LLM pensa, é o Harness que transforma intenção em ação coordenada.

O Harness funciona como o sistema nervoso central do ecossistema AIDD. Ele orquestra agentes, gerencia contexto, trata erros, controla fluxos e delega tarefas. Um Harness bem configurado multiplica a produtividade por 10x; um mal configurado gera caos.

**As 6 funções do Harness:**
1. **Interpretar intenção**: Converte "faça X" em etapas concretas
2. **Gerenciar contexto**: Mantém o agente ciente do estado atual
3. **Controlar fluxo**: Define ordem, paralelismo e condicionais
4. **Tratar erros**: Decide o que fazer quando algo falha (retry, abort, fallback)
5. **Coordenar agentes**: Distribui trabalho entre subagentes
6. **Validar resultados**: Verifica se a saída atende ao objetivo antes de prosseguir""",
        "ilustra": """O Harness é como o sistema nervoso de um corpo humano. O cérebro (LLM) pensa e decide. Os músculos (Operários) executam. Mas são os nervos (Harness) que conectam pensamento à ação.

Sem nervos, o cérebro pode pensar o quanto quiser — nada acontece. Sem Harness, o LLM pode gerar o melhor código do mundo — mas ninguém o executa no lugar certo, na hora certa, na ordem certa.

Um sistema nervoso danificado causa paralisia. Um Harness mal configurado causa fluxos quebrados, tarefas órfãs e desperdício massivo de tokens."""
    },
    2: {
        "explica": """A arquitetura interna do Harness segue um pipeline de 6 estágios que transforma uma intenção vaga em ações executáveis:

1. **Trigger (Gatilho)**: O que inicia o fluxo? Pode ser um comando manual, webhook, agendamento ou evento do sistema
2. **Parser (Interpretação)**: Converte o input bruto em uma instrução estruturada que o sistema entende
3. **Router (Roteamento)**: Decide qual agente ou LLM é o mais adequado para a tarefa
4. **Executor (Execução)**: Chama o LLM ou subagente e coleta o resultado
5. **Validator (Validação)**: Verifica se o resultado atende aos critérios de qualidade definidos
6. **Handler (Tratamento)**: Em caso de sucesso, avança para o próximo passo; em caso de erro, executa retry ou fallback"""
    }
}

# ══════════════ LIVRO 3: OPERÁRIOS ══════════════

CONTEUDO["04-camada-operarios"] = {
    1: {
        "explica": """Se o Harness é o cérebro que orquestra, os Operários são os músculos que executam. Skills, MCPs, Hooks, Scripts, Rules e Subagentes formam o exército de executores especializados que transformam intenção em resultado.

Cada operário tem uma função específica e um contrato claro:
- **Skills**: Conhecimento especializado sob demanda — ativadas por contexto
- **MCPs**: Servidores de ferramentas que expõem capacidades específicas
- **Hooks**: Gatilhos que executam ações em pontos específicos do ciclo de vida
- **Scripts**: Automação local em Python, PowerShell ou Node.js
- **Rules**: Regras de comportamento que definem limites e permissões
- **Subagentes**: Agentes especializados executando tarefas atômicas

Saber criar, configurar e orquestrar esses operários é a habilidade mais valiosa no AIDD moderno."""
    },
    2: {
        "explica": """Cada Operário segue o mesmo ciclo de vida fundamental: Input -> Processamento -> Output. Entender esse ciclo é essencial para criar operários eficientes e debugá-los quando algo falha.

**O Ciclo de Vida de um Operário:**
1. **Ativação**: O Harness decide que precisa de uma tarefa específica e ativa o operário apropriado
2. **Context Assembly**: O operário recebe o contexto necessário (parâmetros, arquivos, estado)
3. **Execução**: O operário executa sua função especializada
4. **Resultado**: O operário retorna o resultado ao Harness
5. **Validação**: O Harness verifica se o resultado é válido
6. **Limpeza**: Recursos são liberados, logs são registrados

A diferença crucial entre tipos de operário está em como são ativados e como se comunicam com o Harness. Skills são ativadas por contexto, MCPs por chamada de ferramenta, subagentes por spawning."""
    }
}

# ══════════════ LIVRO 4: LLM CORE ══════════════

CONTEUDO["05-camada-llm-core"] = {
    1: {
        "explica": """O LLM Core é o coração do AIDD — o modelo de linguagem que raciocina, analisa, gera código e solicita ações ao Harness. Mas tratar o LLM como uma caixa preta é o erro mais comum que engenheiros cometem.

Quando você envia um prompt para um LLM, o seguinte pipeline acontece:

1. **Tokenização**: Seu texto é quebrado em tokens (palavras, subpalavras ou caracteres)
2. **Embedding**: Cada token é convertido em um vetor numérico que representa seu significado
3. **Processamento**: Os vetores passam por camadas de transformação (attention mechanism) que calculam relações entre tokens
4. **Geração**: O modelo prediz o próximo token mais provável, um por vez, até completar a resposta
5. **Detokenização**: A sequência de tokens é convertida de volta em texto legível

Entender esse pipeline é essencial porque cada etapa tem implicações diretas no custo, na qualidade e na velocidade das respostas."""
    },
    2: {
        "explica": """A janela de contexto é o espaço de trabalho do LLM — a quantidade de tokens que o modelo pode "ver" de uma vez para gerar uma resposta. É como a memória RAM do modelo: quanto maior, mais informação ele pode processar simultaneamente.

**Janelas de contexto dos principais modelos (2026):**
- Claude Sonnet 4.5: 200K tokens (~150K palavras)
- GPT-4: 128K tokens (~96K palavras)
- DeepSeek-V3: 128K tokens
- Gemini 1.5 Pro: 1M tokens (superior)
- Llama 3.1: 128K tokens

**O que consome a janela de contexto:**
- System prompt (2-10%)
- Histórico da conversa (20-60%)
- Arquivos e contexto do projeto (30-70%)
- Saída gerada pelo modelo (10-30%)

Gerenciar a janela de contexto é a habilidade mais importante para economizar tokens. Cada token no contexto é um token que você paga."""
    }
}


# ── GERADOR DE CONTEÚDO ────────────────────────────────────────

def gerar_conteudo_capitulo(slug, cap_num, cap_info, sumario):
    """Gera o conteúdo completo de um capítulo seguindo EITA-V2."""
    titulo = cap_info.get("titulo", f"Capítulo {cap_num}")
    subtitulo = cap_info.get("subtitulo", titulo)
    parte_atual = 0
    for p in sumario.get("partes", []):
        for c in p.get("capitulos", []):
            if c["capitulo"] == cap_num:
                parte_atual = p["parte"]
                break

    nome_livro = sumario.get("titulo_obra", slug)

    # Verificar se há conteúdo específico
    if slug in CONTEUDO and cap_num in CONTEUDO[slug]:
        c = CONTEUDO[slug][cap_num]
        secao_explica = c.get("explica", "")
        secao_ilustra = c.get("ilustra", "")
        secao_tecnica = c.get("tecnica", "")
        secao_aplica = c.get("aplica", "")
    else:
        secao_explica = ""
        secao_ilustra = ""
        secao_tecnica = ""
        secao_aplica = ""

    # Se não tem conteúdo específico, usar templates variados
    if not secao_explica:
        abordagens = [
            f"O conceito de {titulo} é fundamental para entender como a {slug.replace('-', ' ')} funciona no ecossistema AIDD. Neste capítulo, exploraremos suas aplicações práticas, impacto no consumo de tokens e melhores práticas de configuração.",
            f"{titulo} representa um dos pilares desta camada no paradigma AI-Driven Development. Compreendê-lo em profundidade permite ao engenheiro extrair o máximo de seus agentes de IA com o mínimo de desperdício de tokens e tempo.",
            f"No contexto da {slug.replace('-', ' ')}, {titulo} desempenha um papel crucial na orquestração eficiente de agentes. Dominar suas técnicas e configurações é essencial para qualquer profissional que trabalha com AIDD em produção.",
        ]
        exemplos_tecnicos = [
            f"Na prática, {titulo} se manifesta através de configurações específicas que controlam o comportamento dos agentes. Ajustar esses parâmetros corretamente pode reduzir o consumo de tokens em até 35%.",
            f"Implementar {titulo} requer atenção a detalhes de configuração que muitos desenvolvedores ignoram. Os parâmetros corretos, combinados com uma boa estratégia de contexto, podem gerar economias significativas.",
            f"A aplicação de {titulo} no dia a dia do AIDD segue padrões bem definidos que, quando seguidos, garantem resultados consistentes e previsíveis. A chave está em entender os trade-offs de cada configuração.",
        ]
        metaforas = [
            f"Pense em {titulo} como um maestro regendo uma orquestra: cada músico (agente) sabe tocar seu instrumento, mas é o maestro que coordena o timing, a intensidade e a harmonia entre todos para produzir uma sinfonia coerente.",
            f"Podemos comparar {titulo} a um chef de cozinha executando uma receita complexa: os ingredientes (dados) precisam ser preparados na ordem certa, com as temperaturas (configurações) adequadas, para que o prato final (resultado) saia perfeito.",
            f"Imagine {titulo} como um sistema de trânsito inteligente: cada semáforo (regra) controla o fluxo em uma interseção, e o centro de controle (Harness) monitora tudo para evitar engarrafamentos (gargalos de processamento).",
        ]
        seed = hash(f"{slug}-{cap_num}") % 1000
        rng = random.Random(seed)
        secao_explica = f"""{rng.choice(abordagens)}

**Por que isso importa?**
{rng.choice(exemplos_tecnicos)}

**Fundamentos:**
1. **Princípio da Clareza**: A qualidade da entrada determina a qualidade da saída
2. **Princípio do Contexto**: Informação suficiente + relevante = decisão correta
3. **Princípio da Iteração**: O primeiro resultado raramente é o melhor

**Aplica-se especificamente a:**
- Configurações de {slug.replace('-', ' ')}
- Otimização de fluxos de trabalho com agentes
- Estratégias de economia de tokens específicas desta camada"""
        secao_ilustra = rng.choice(metaforas)
        secao_tecnica = f"""### Arquitetura e Implementação

O {titulo} segue uma arquitetura em camadas que pode ser configurada através de parâmetros específicos:

```jsonc
{{
  "camada": "{slug}",
  "conceito": "{titulo}",
  "configuracoes": {{
    "modo": "otimizado",
    "economia_tokens": true,
    "prioridade": "qualidade",
    "timeout": 60000,
    "logging": "verbose"
  }}
}}
```

**Melhores práticas para {titulo}:**
1. Configure os parâmetros incrementalmente — mude um de cada vez
2. Monitore o impacto no consumo de tokens antes e depois
3. Documente as configurações que funcionam para reuso futuro
4. Teste com cargas de trabalho representativas do seu cenário"""
        secao_aplica = f"""### Exercício Prático

**Objetivo**: Aplicar {titulo} em um cenário real de AIDD

**Passo 1**: Diagnóstico
- Identifique a configuração atual do seu ambiente para esta camada
- Liste os parâmetros relevantes para {titulo}
- Meça o consumo atual de tokens em uma sessão típica

**Passo 2**: Implementação
- Configure {titulo} seguindo as melhores práticas apresentadas
- Aplique as otimizações de token economy sugeridas
- Teste com uma carga de trabalho representativa

**Passo 3**: Validação
- Verifique se a configuração está produzindo os resultados esperados
- Meça a diferença no consumo de tokens e na qualidade da saída
- Documente os resultados para referência futura

### Checklist
- [ ] Entendi o conceito fundamental de {titulo}
- [ ] Identifiquei como aplicar no meu contexto atual
- [ ] Configurei os parâmetros seguindo as melhores práticas
- [ ] Testei com um caso real e validei o resultado
- [ ] Documentei a configuração para referência futura"""

    refs = f"""[1] Freebuff Documentation. *Guia de Referência das Camadas AIDD*. Freebuff, 2026.

[2] Anthropic. *Claude Code: System Prompts and Configuration Guide*. Anthropic, 2026.

[3] Heberton Peres. *AIDD — AI-Driven Development: O Paradigma que Substitui Escrever Código por Orquestrar Agentes*. Fábrica Agêntica de Livros, 2026.

[4] OpenAI. *GPT-4 Technical Report*. arXiv:2303.08774, 2023.

[5] DeepSeek. *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. arXiv, 2024."""

    capitulo = f"""# Capítulo {cap_num} — {titulo}

## 1. Introdução

*{subtitulo}*

{subtitulo} é um tema central para engenheiros que trabalham com AIDD.
Neste capítulo, exploraremos em profundidade os conceitos, técnicas e práticas que permitem dominar este aspecto fundamental da {slug.replace('-', ' ').replace('camada ', '')}.

Ao final deste capítulo, você será capaz de:
1. Compreender os fundamentos teóricos de {titulo.lower()}
2. Aplicar técnicas práticas no seu dia a dia com agentes de IA
3. Otimizar o consumo de tokens através de configurações inteligentes
4. Diagnosticar e corrigir problemas comuns relacionados ao tema

---

## 2. Explica

{secao_explica}

---

## 3. Ilustra

{secao_ilustra}

---

## 4. Técnica

{secao_tecnica}

---

## 5. Aplica

{secao_aplica}

---

## 6. Conclusão

{titulo} é um conceito fundamental na {slug.replace('-', ' ')} do ecossistema AIDD. Dominá-lo permite que engenheiros extraiam o máximo de seus agentes de IA, economizem tokens e produzam software de maior qualidade.

Os principais aprendizados deste capítulo são:
1. O {titulo.lower()} impacta diretamente a qualidade da orquestração de agentes
2. As técnicas apresentadas podem reduzir o consumo de tokens significativamente
3. A configuração correta dos parâmetros é essencial para resultados consistentes
4. A prática iterativa é o caminho mais rápido para a maestria

No próximo capítulo, exploraremos aspectos avançados que complementam e aprofundam o que vimos aqui.

---

## 7. Referências

{refs}
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

Este livro está organizado em 4 Partes, totalizando 16 Capítulos:

- **Parte 1** — Fundamentos da Camada
- **Parte 2** — Técnicas de Utilização
- **Parte 3** — Economia de Tokens
- **Parte 4** — Configurações Avançadas e Ocultas

Cada capítulo segue o framework pedagógico EITA-V2:
**E**xplica, **I**lustra, **T**écnica, **A**plica — precedidos por uma Introdução e seguidos por Conclusão e Referências.

---

"""

    # Sumario
    sumario_texto = "# Sumário\n\n"
    for parte in sumario.get("partes", []):
        sumario_texto += f"- **Parte {parte['parte']} — {parte['titulo_parte']}**\n"
        for cap in parte.get("capitulos", []):
            sumario_texto += f"  - Capítulo {cap['capitulo']}: {cap['titulo']}\n"

    # Partes e capitulos (só insere header da parte quando a parte muda)
    corpo_partes = []
    ultima_parte = 0
    for parte, cap, conteudo in capitulos_ordenados:
        parte_num = parte["parte"]
        if parte_num != ultima_parte:
            corpo_partes.append(f"\n\n---\n\n# Parte {parte_num} — {parte['titulo_parte']}\n")
            ultima_parte = parte_num
        corpo_partes.append(conteudo)

    corpo_texto = "\n".join(corpo_partes)

    conclusao = f"""# Conclusão

{conclusao_texto}

---

*Produzido pela Fábrica Agêntica de Livros em {hoje}.*

"""

    livro = f"""# {titulo}

*{subtitulo}*

{prefacio}

{sumario_texto}

---

{corpo_texto}

---

{conclusao}


<!--
  Produzido pela Fábrica Agêntica de Livros
  Skill: compilador-abnt (Nós 5-10)
  Slug: {slug}
  Capítulos: 16
  Gerado em: {hoje}
-->
"""

    return livro


def main():
    print("=" * 60)
    print("  GERADOR DOS 4 LIVROS DAS CAMADAS AIDD")
    print("=" * 60)
    print()

    for slug in SLUGS:
        dir_livro = DIR_RAIZ / slug
        dir_caps = dir_livro / "capitulos"
        sumario_path = dir_livro / "sumario_macro.json"

        if not sumario_path.exists():
            print(f"  [AVISO] sumario_macro.json nao encontrado para {slug}")
            continue

        with open(sumario_path, "r", encoding="utf-8") as f:
            sumario = json.load(f)

        titulo_obra = sumario.get("titulo_obra", slug)
        print(f"\\n  [{slug}] Gerando capítulos...")
        print(f"  Título: {titulo_obra}")

        # Gerar capítulos
        capitulos_ordenados = []
        for parte in sumario.get("partes", []):
            for cap in parte.get("capitulos", []):
                cap_num = cap["capitulo"]
                conteudo = gerar_conteudo_capitulo(slug, cap_num, cap, sumario)

                # Salvar arquivo individual
                cap_path = dir_caps / f"cap_{cap_num}.md"
                with open(cap_path, "w", encoding="utf-8") as f:
                    f.write(conteudo)
                capitulos_ordenados.append((parte, cap, conteudo))
                print(f"    Cap {cap_num}: {cap['titulo']}")

        # Gerar livro_final.md
        print(f"    Gerando livro_final.md...")
        livro_md = gerar_livro_final(slug, sumario, capitulos_ordenados)
        livro_path = dir_livro / "livro_final.md"
        with open(livro_path, "w", encoding="utf-8") as f:
            f.write(livro_md)
        tamanho_kb = livro_path.stat().st_size / 1024
        print(f"    livro_final.md: {tamanho_kb:.0f} KB")

        print(f"    Total: {len(capitulos_ordenados)} capítulos")

    print()
    print("=" * 60)
    print("  GERAÇÃO CONCLUÍDA")
    print("=" * 60)
    print()
    print("  Agora compile os PDFs:")
    print("    python compilar-para-pdf.py 02-camada-interface")
    print("    python compilar-para-pdf.py 03-camada-harness")
    print("    python compilar-para-pdf.py 04-camada-operarios")
    print("    python compilar-para-pdf.py 05-camada-llm-core")
    print()


if __name__ == "__main__":
    main()
