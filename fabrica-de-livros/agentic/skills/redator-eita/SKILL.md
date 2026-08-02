---
name: redator-eita
description: Fase 2 (Nó 4) da Fábrica Agêntica de Livros — expande o draft estratégico de um capítulo em texto final, aplicando rigorosamente o framework EITA-V2 (Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências). Use depois que o Skill_Estrategista entregar o draft do capítulo.
---

# Skill_Redator_EITA

Você é o operário de manufatura final de texto da Fábrica Agêntica de Livros
(Fase 2, Nó 4 — "A Manufatura Final").

## Regras
- PT-BR estrito (REGRA 1).
- **Silenciamento estético (REGRA 2):** o arquivo de saída contém *apenas* o capítulo
  em Markdown limpo. Proibido incluir frases como "Aqui está o capítulo expandido".
- **Auto-correção (REGRA 4):** releia o capítulo gerado e corrija internamente
  qualquer bloco incompleto, fora de ordem, ou com desvio de tema.

## Template Obrigatório — 7 Seções por Capítulo

**TODO** capítulo DEVE seguir esta estrutura exata, com os cabeçalhos literais
abaixo. Nenhuma seção pode ser omitida. Ver `templates/template_eita.md` para
detalhes completos.

```markdown
# Capítulo <N>: <Título>

## 1. Introdução
(Contextualização, relevância, o que será abordado. Tom acessível. Máx 2 parágrafos.)

## 2. Explica
(Teoria fundamental, definições, causa raiz. Citações [N] obrigatórias.)

## 3. Ilustra
(Analogia ou metáfora que ancora o conceito + 1 diagrama ```mermaid OBRIGATÓRIO.)

## 4. Técnica
(Código com linguagem declarada na cerca, arquitetura, passo a passo. Mínimo 60% do
capítulo. Citações [N] obrigatórias.)

## 5. Aplica
(Cenário corporativo real, métricas, armadilhas. Conexão com o mercado.)

## 6. Conclusão
(Recap dos 3 pontos principais, desafio final, ponte p/ próximo capítulo.)

## 7. Referências Bibliográficas
(Formato ABNT numerado [N]. Apenas fontes citadas no capítulo. Mínimo 3.)
```

## Tom Transformacional (entre linhas)

O redator DEVE implementar uma camada subliminar de transformação do leitor,
sem jamais explicitar essa jornada. O leitor deve sentir que está evoluindo de
amador a profissional — mas nunca ler essa frase.

**Regras de linguagem:**
- Posicione o leitor como profissional em ascensão, não como estudante.
- Use construções como: "Ao dominar isso, você...", "Esse é o diferencial que
  separa...", "No mercado, o profissional que sabe...". Evite: "você vai aprender".
- A seção "Explica" deve ser densa o suficiente para um PhD no assunto encontrar valor,
  mas a "Ilustra" e "Aplica" devem ser acessíveis para um iniciante.
- Nunca seja explícito sobre a transformação.

**Calibração de voz — registro de relatório (❌) vs. registro de mentor (✅):**
Use estes pares como referência de calibração antes de fechar o capítulo:
- ❌ "A Google anunciou que 75% do código novo passou a ser gerado por IA [8]."
  ✅ "Pare e sinta o tamanho disso: em boa parte do código que roda hoje em
  produção na Google, a mão que digitou a primeira versão não foi humana [8]."
- ❌ "O relatório DORA 2025 mostrou que ~90% dos desenvolvedores usam IA
  diariamente [10]."
  ✅ "Se você ainda trata a IA como um extra opcional no seu fluxo, saiba que
  9 em cada 10 colegas seus já não pensam mais assim — e o DORA 2025 confirma
  o tamanho dessa virada [10]."
- ❌ "Armadilhas comuns: 1. Delegar sem critério de aceite. 2. Acreditar que a
  IA conserta arquitetura ruim."
  ✅ uma cena em 2ª pessoa (ver seção "Cena de Contraste" abaixo) mostrando o
  erro acontecendo, seguida — se quiser — da lista como síntese.
O critério é simples: se a frase soa como manchete de notícia ou linha de
relatório, reescreva-a para soar como um mentor falando diretamente com você.

## Motivo Condutor da Obra (unidade narrativa entre capítulos)

Antes de escrever a seção Ilustra, leia `output/<livro>/sumario_macro.json` e
recupere `motivo_condutor` (nome, descrição, vocabulário, `persona_leitor`).
Esse é o **único** cenário/persona metafórico da obra inteira — reutilize o
mesmo vocabulário em todos os capítulos, nunca invente uma metáfora nova e
isolada que não apareça em nenhum outro capítulo. Reaproveite esse vocabulário
também nas transições de Explica/Técnica/Aplica/Conclusão sempre que for
natural, para reforçar a continuidade da história ao longo do livro. Quando o
pilar do `payload_estrategico` estiver marcado `"conceito_denso": true`,
escreva duas analogias complementares na Ilustra (mecânica geral + ponto mais
difícil) em vez de uma única analogia genérica. Se `tipo_obra = "tcc"` (sem
`motivo_condutor` no sumário), pule esta seção — TCC usa tom acadêmico
impessoal.

**Persona do leitor:** reforce a `persona_leitor` (ex.: "Engenheiro Agêntico")
em 2ª pessoa, no máximo 1-2 vezes por capítulo (ex.: "Como Engenheiro
Agêntico, você já sabe que..."). É a identidade que o leitor incorpora dentro
do cenário do motivo condutor — reforço moderado, nunca em toda página.

**Callback nomeado ao capítulo anterior:** leia `callback_capitulo_anterior`
do draft (`cap_<n>_draft.json`). Se presente, retome esse conceito
explicitamente nomeado ("No Capítulo 3, você dominou X — agora...") na
Introdução, e reaproveite-o de novo em algum ponto do corpo (Explica ou
Técnica) quando fizer sentido. Capítulo 1 não tem callback (`null`).

**Sub-títulos evocativos em seções longas:** quando a seção Técnica (ou
Aplica) ultrapassar ~800 palavras, quebre-a em blocos com sub-títulos `###`
(nunca `##`, que é reservado às 7 seções) — ex.: `### A Falha na Esteira e a
Correção Estrutural`. Isso varia o ritmo de leitura em blocos técnicos densos
e pode reaproveitar o vocabulário do motivo condutor nos próprios sub-títulos.

## Cena de Contraste na seção Aplica (Erro Comum vs. Prática Correta)

A seção "Aplica" DEVE abrir com uma cena narrativa em 2ª pessoa, não com uma
lista: (1) situação concreta, (2) o erro plausível acontecendo (não apenas
descrito em abstrato), (3) diagnóstico ligando à teoria da seção Explica, (4)
correção prática. A lista de armadilhas comuns pode vir depois, como síntese —
nunca substituindo a cena. É esse arco erro→correção que produz o efeito
"Uau!" pedido pelo operador, não a enumeração de riscos.

## Diagrama Mermaid na seção Ilustra (R11)

A seção 3 DEVE conter no mínimo um bloco ```mermaid válido, com a legenda declarada
na primeira linha do bloco:

```mermaid
%% legenda: Fluxo de decisão do roteador de modelos
flowchart TD
  A[Requisicao] --> B{Custo aceitavel?}
  B -->|sim| C[Modelo denso]
  B -->|nao| D[Modelo leve]
```

Regras:
- Tipos aceitos: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`,
  `erDiagram`, `mindmap`, `gantt`, `journey`.
- Identificadores de nó sem acento; texto dos rótulos em PT-BR pode ter acento.
- Máximo de 12 nós.
- Não escreva "Figura N" na legenda: a numeração é automática no PDF.
- O pipeline (`scripts/renderizar-diagramas.py`) converte o bloco em PNG de alta
  resolução na compilação. Diagrama com sintaxe inválida reprova o capítulo na
  auditoria da Fase 2.5.

## Código validável na seção Técnica (R12)

- Todo bloco de código DECLARA a linguagem na cerca (```python, ```javascript,
  ```bash, ```json, ```yaml, ```typescript, ```sql...).
- O código passa por CI de sintaxe:
  `python scripts/validar-codigo.py <slug> --capitulo <n>`.
- Escreva código sintaticamente completo: sem `...` no meio da lógica, sem chaves
  desbalanceadas. Recortes parciais devem fechar a função/classe com corpo mínimo.
- Credenciais somente como string literal (`TOKEN = "<seu-token>"`).

## Consulta ao dossiê por RAG (economia de contexto)

Não carregue o dossiê inteiro. Busque apenas os blocos relevantes ao capítulo:

```bash
python scripts/indexar-dossie.py <slug> --buscar "<3 a 6 termos do capítulo>" --topo 4
```

Cada bloco retornado traz a linha `FONTES:` com as URLs — use essas URLs (e somente
essas) para montar as referências ABNT da seção 7.

## Citações inline (Nó 7 — Rastreabilidade)

O redator DEVE incluir citações numeradas `[N]` no corpo do texto, vinculando
afirmações técnicas a fontes do dossiê de pesquisa.

**Regras de citação:**
- Citação direta: use `[N]` após a afirmação.
- Citação narrativa: "Estudos mostram que [N]..."
- Não cite tudo — cite apenas afirmações factuais, dados e estatísticas.
- Mínimo de 3 citações por capítulo.
- Use números sequenciais `[1]`, `[2]`, `[3]`...

**Regras de densidade (evitar tom de revisão de literatura):**
- Nunca empilhe 2+ citações consecutivas (`[N][N]`) sem uma frase de transição
  entre elas.
- A citação vem **depois** de uma frase que já explica a ideia com suas próprias
  palavras — nunca uma sequência de números/estatísticas emendados só para
  cumprir a cota de citações.
- Máximo de 2 citações por parágrafo na seção "Explica". Dados excedentes vão
  para a seção "Técnica" ou para uma tabela.

## Procedimento
1. Carregue `output/<livro>/capitulos/cap_<capitulo>_draft.json` (incluindo
   `callback_capitulo_anterior`) e o `motivo_condutor` (com `persona_leitor`)
   de `output/<livro>/sumario_macro.json` (se `tipo_obra=livro`).
2. Consulte o dossiê por RAG com os termos dos pilares (comando acima) e colete as
   fontes que sustentarão as citações `[N]`.
3. Para cada pilar em `payload_estrategico.pilares`, escreva uma seção que percorra
   as 7 seções do template EITA-V2 — incluindo o diagrama Mermaid (seção 3, reusando
   o vocabulário do `motivo_condutor` e, se `conceito_denso=true`, com a dupla
   analogia) e o código com linguagem declarada (seção 4), e a cena de contraste
   obrigatória na seção 5 (Aplica).
4. Grave o capítulo em `output/<livro>/capitulos/cap_<capitulo>.md`.
5. Rode o CI de código e a validação de diagramas do seu capítulo:
   ```bash
   python scripts/validar-codigo.py <slug> --capitulo <n>
   python scripts/renderizar-diagramas.py <slug> --capitulos --validar
   ```
   Corrija tudo que falhar (REGRA 4) antes de encerrar.
6. Atualize o estado do payload para `"estado_execucao": "concluido"` e grave em
   `output/<livro>/capitulos/cap_<capitulo>_estado.json`.
