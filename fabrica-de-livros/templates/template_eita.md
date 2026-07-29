# Template Pedagógico EITA-V2 — Estrutura Obrigatória de 7 Seções por Capítulo

**Este template é CONTRATUAL.** Todo capítulo de toda obra produzida pela Fábrica
Agêntica de Livros DEVE seguir esta estrutura exata de 7 seções, nesta ordem,
com os cabeçalhos literais abaixo. Nenhuma seção pode ser omitida.

---

## Seções obrigatórias do capítulo

### 1. INTRODUÇÃO
**Objetivo:** Contextualizar o leitor no tema do capítulo. Explicar o que será
abordado, por que é relevante, e o que o leitor será capaz de fazer ao final.

**Regras:**
- Tom acessível para iniciantes, sem jargão desnecessário.
- Deve conter uma "ponte" com o capítulo anterior (se houver).
- Máximo de 2 parágrafos.
- Única seção que pode usar "você vai aprender" ou equivalente.

### 2. EXPLICA
**Objetivo:** Desconstrução teórica fundamental do conceito: causa raiz, mecânica
subjacente, definições precisas.

**Regras:**
- Posicione o leitor como agente ativo: "você vai perceber que...", "note como...".
- Inclua definições formais quando aplicável.
- Profundidade suficiente para que um PhD no assunto encontre valor, mas linguagem
  acessível para um iniciante.
- Citações obrigatórias `[N]` para afirmações factuais.

**Transformação implícita:** o leitor passa de "não sei o que é" para "sei definir
e explicar".

### 3. ILUSTRA
**Objetivo:** Analogia física, metáfora industrial ou exemplo concreto que ancore
o conceito na intuição do leitor.

**Regras:**
- Deve ser concreta e verificável, não decorativa.
- A analogia deve ser tão clara que o leitor pense "agora entendi".
- Use exemplos do cotidiano do desenvolvedor (mercado, código, equipes).
- Se a analogia for de outra área (física, biologia, etc.), explique a conexão.

**Transformação implícita:** o leitor passa de "parece abstrato" para "faz total
sentido".

### 4. TÉCNICA
**Objetivo:** Entrega prática de alto valor: código, arquitetura, esquema de dados,
diagrama, passo a passo de implementação. É o núcleo de valor do capítulo.

**Regras:**
- Código real, executável (não pseudocódigo, a menos que justificado).
- Arquiteturas e esquemas de dados reais.
- Passos numerados ou sequenciais.
- Mínimo de 60% do conteúdo do capítulo deve estar nesta seção.
- Citações `[N]` obrigatórias para técnicas, benchmarks e estatísticas.

**Transformação implícita:** o leitor passa de "não sei fazer" para "consigo
implementar".

### 5. APLICA
**Objetivo:** Contextualização em cenário corporativo real, de alta performance ou
produção industrial. Conecta a técnica ao resultado de negócio.

**Regras:**
- Cenário realista (startup, scale-up, enterprise).
- Métricas de sucesso e fracasso.
- Armadilhas comuns e como evitá-las.
- O leitor deve se enxergar aplicando aquilo no trabalho dele.

**Transformação implícita:** o leitor passa de "isso é teórico" para "vou usar no
mercado".

### 6. CONCLUSÃO
**Objetivo:** Síntese do que foi aprendido, conexão com o próximo capítulo (se
houver) e desafio final para o leitor.

**Regras:**
- Recapitule os 3 pontos principais em 1 parágrafo.
- Desafio ou exercício opcional.
- Ponte para o próximo capítulo (se houver).
- Tom de encerramento que reforça a transformação do leitor.

### 7. REFERÊNCIAS BIBLIOGRÁFICAS
**Objetivo:** Listar todas as fontes citadas no capítulo no formato ABNT numerado.

**Regras:**
- Use o formato ABNT: `[N] SOBRENOME, Nome. *Título*. Disponível em: URL. Acesso em: DD mês. AAAA.`
- Apenas fontes EFETIVAMENTE citadas no capítulo (com `[N]` no texto).
- Não incluir fontes do dossiê que não foram citadas neste capítulo.
- Mínimo de 3 referências por capítulo.
- Ordem alfabética por título.

---

## Estrutura visual no Markdown

```markdown
# Capítulo <N>: <Título>

## 1. Introdução
...

## 2. Explica
...

## 3. Ilustra
...

## 4. Técnica
...

## 5. Aplica
...

## 6. Conclusão
...

## 7. Referências Bibliográficas
[1] ...
[2] ...
```
