# Capítulo 4 — Context Engineering: A Nova Disciplina Fundamental

Em 2024, a habilidade mais valorizada de um desenvolvedor que usava IA era o *prompt engineering* — a arte de escrever a instrução perfeita para obter o resultado desejado de um modelo de linguagem. Em 2026, essa habilidade foi rebaixada a uma especialização menor. A disciplina que a substituiu é o **Context Engineering**: a arte de preencher a janela de contexto de um agente com exatamente a informação certa, no momento certo, na ordem certa.

Este capítulo explica por que essa transição ocorreu, detalha as seis camadas da arquitetura de contexto e expõe os anti-patterns que sabotam até mesmo os desenvolvedores mais experientes.

## A evolução: do Prompt Engineering ao Context Engineering

### A ilusão do prompt perfeito

Nos primeiros dias dos LLMs, o mantra era "o prompt certo resolve tudo". Desenvolvedores competiam para criar o prompt definitivo — a sequência mágica de palavras que faria o modelo gerar o código perfeito em toda tentativa.

Essa abordagem funciona bem em interações isoladas: uma pergunta, uma resposta. Mas coding agents não operam em interações isoladas. Uma sessão típica de um agente envolve dezenas de ações — ler arquivos, buscar símbolos, editar código, executar testes, corrigir erros, cada ação consumindo e adicionando ao contexto. Nesse cenário, a qualidade do *contexto acumulado* importa muito mais do que a qualidade do prompt inicial.

### Prompt Engineering (micro) vs. Context Engineering (macro)

| Dimensão | Prompt Engineering | Context Engineering |
|----------|-------------------|-------------------|
| **Alcance** | Mensagem única | Sessão inteira (20+ ações) |
| **Foco** | Escolha de palavras, framing | Arquitetura informacional |
| **Artefatos** | Prompt de sistema, instrução | Regras, RAG, memória, MCPs, histórico |
| **Erro típico** | Prompt ambíguo | Contexto poluído ou mal ordenado |
| **Impacto do erro** | Resposta errada em 1 interação | Degradação composta em toda a sessão |

![Prompt Engineering vs. Context Engineering](../imagens/cap_4_diagrama_1.svg)

### O efeito composto dos erros de contexto

Um erro no início de uma sessão longa não é corrigido naturalmente — ele se propaga e se amplifica. Se o agente começa uma sessão com uma compreensão errada da arquitetura do projeto, todas as decisões subsequentes serão contaminadas. É como dar uma direção errada para um motorista e esperar que ele encontre o caminho sozinho: quanto mais longe ele dirige, mais perdido fica.

Por isso, o Context Engineering não é opcional para quem usa coding agents em projetos reais. É a infraestrutura básica sobre a qual toda interação com o agente se apoia.

## As 6 camadas da arquitetura de Context Engineering

A indústria convergiu em uma arquitetura de contexto organizada em seis camadas. Cada camada resolve um problema específico e, juntas, formam um sistema que maximiza a eficiência e a precisão do agente.

### Camada 1: System Prompt Architecture

A base de tudo. O system prompt não é apenas "você é um assistente útil" — é um contrato detalhado que define:

- **Papéis:** O que o agente é (ex: "engenheiro de software sênior especializado em React e Node.js")
- **Restrições:** O que o agente NÃO deve fazer (ex: "nunca modifique o schema do banco de dados sem aprovação explícita")
- **Formato de saída:** Como as respostas devem ser estruturadas (ex: "sempre forneça uma explicação seguida do código")
- **Prioridades:** O que é mais importante (ex: "segurança acima de performance; testes acima de velocidade")

### Camada 2: RAG de Código

A recuperação de informação relevante do código-fonte não pode ser ingênua. Técnicas avançadas incluem:

- **Chunking estrutural:** Dividir o código em limites naturais (funções, classes, módulos) em vez de contar tokens cegamente
- **Hybrid search:** Combinar busca vetorial (similaridade semântica) com BM25 (correspondência exata de símbolos)
- **Dependency hydration:** Trazer automaticamente assinaturas e tipos das funções chamadas pelo trecho recuperado

### Camada 3: Tool Selection

Fornecer todas as ferramentas disponíveis o tempo todo é um erro. Ferramentas em excesso degradam o raciocínio do modelo. A prática recomendada é expor apenas as ferramentas necessárias para cada fase:

- **Fase de planejamento:** Apenas ferramentas de leitura (busca de arquivos, leitura de símbolos)
- **Fase de execução:** Ferramentas de edição e execução de comandos
- **Fase de validação:** Linters, type-checkers, test runners

### Camada 4: Memory Systems

Agentes precisam de memória que persiste entre sessões. Os sistemas de memória mais eficazes incluem:

- **Memória episódica:** Resumos estruturados de decisões passadas e descobertas arquiteturais
- **RTK Scratchpad:** Registro de erros resolvidos, padrões descobertos e decisões arquiteturais
- **CLAUDE.md / AGENTS.md:** Memória de longo prazo do projeto que o agente lê no início de cada sessão

### Camada 5: Context Compression

Sessões longas consomem tokens rapidamente. Para evitar o estouro de janela de contexto:

- **Rolling windows:** Manter apenas as N ações mais recentes no contexto ativo
- **Sumarização progressiva:** Comprimir histórico antigo em resumos estruturados
- **Bookending:** Colocar instruções críticas e escopo da tarefa no início e no final do contexto (combate ao efeito Lost in the Middle)

### Camada 6: Information Ordering (Bookending)

Pesquisas mostram que modelos de linguagem têm desempenho significativamente pior com informações no meio de contextos longos — o fenômeno **Lost in the Middle**. A técnica de *bookending* resolve isso:

- **Início do contexto:** Objetivo principal da sessão, restrições arquiteturais, instruções críticas
- **Meio do contexto:** Dados de referência, exemplos, contexto histórico comprimido
- **Final do contexto:** Escopo da tarefa imediata, critérios de verificação, instruções de formatação da saída

![As 6 camadas da arquitetura de Context Engineering](../imagens/cap_4_diagrama_2.svg)

![As 6 camadas da arquitetura de Context Engineering](../imagens/cap_4_diagrama_2.svg)

### Exemplo prático: contexto bem construído vs. mal construído

**Contexto mal construído (vai falhar):**
```
Escreva uma API REST para gerenciar usuários.
Use as melhores práticas.
```

O agente não sabe: qual framework, qual banco, quais regras de negócio, qual estilo de código do projeto, se existem usuários no sistema atual, se há autenticação, etc.

**Contexto bem construído (vai funcionar):**
```
Projeto: sistema de e-commerce (NestJS + PostgreSQL + Prisma)
Padrão: Clean Architecture (camadas: controller, use-case, repository)
Regras: 
1. Todo endpoint requer autenticação JWT via @Auth() decorator
2. Use DTOs com class-validator em todos os inputs
3. Escreva testes unitários para cada use-case

Tarefa: criar CRUD de usuários (admin cria, user edita próprio perfil)
Critérios de verificação:
- Testes unitários passando com coverage > 80%
- Todos os endpoints testados via Postman collection
- Lint passando sem warnings
```

## Anti-patterns e boas práticas

### Anti-pattern 1: Duplicação de Regras

O erro mais comum: manter o mesmo conjunto de regras copiado em `CLAUDE.md`, `.cursorrules`, `AGENTS.md` e arquivos customizados. Quando uma regra precisa ser atualizada (e sempre precisa), ela é atualizada em um arquivo mas esquecida nos outros.

**Solução:** Use uma única fonte da verdade com symlinks/hardlinks. O `AGENTS.md` é o padrão aberto que funciona em todas as ferramentas. Os demais arquivos apontam para ele via links do sistema de arquivos.

### Anti-pattern 2: Wishlists Abstratas

Instruções como "escreva código limpo" ou "evite bugs" são inúteis para o agente — ele não sabe o que "limpo" significa no contexto do seu projeto.

**Solução:** Prefira especificações executáveis e determinísticas:
- ❌ "Escreva código de qualidade"
- ✅ "Sempre execute `npm run lint --fix` antes de concluir"
- ✅ "Mantenha funções com menos de 30 linhas"
- ✅ "Use nomes de variáveis em inglês com padrão camelCase"

![Não faça vs. Faça: anti-patterns do Context Engineering](../imagens/cap_4_diagrama_3.svg)

### Anti-pattern 3: Poluição de Tokens

Inchar os arquivos de regras com documentações inteiras de bibliotecas, outputs de comandos ou exemplos extensos que nunca serão usados.

**Solução:** Mantenha os arquivos de regras entre 500 e 2000 tokens. Para documentações extensas:
- Use *Skills* (Claude Code) carregadas sob demanda
- Use MCP servers para consultas dinâmicas a documentações
- Use referências a arquivos de doc no próprio repositório

![Não faça vs. Faça: anti-patterns do Context Engineering](../imagens/cap_4_diagrama_3.svg)

---

Neste capítulo, vimos como o Context Engineering substituiu o Prompt Engineering como a disciplina central do desenvolvimento com IA, as seis camadas da arquitetura de contexto e os anti-patterns que mais sabotam sessões de agentes. No próximo capítulo, exploraremos o Spec-Driven Development, a metodologia que transforma especificações em contratos executáveis para governar agentes.
