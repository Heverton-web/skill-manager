# Relatório de Implementação (Rodada 2) — Sugestões Adicionais de Tom de Comunicação

**Data:** 2026-08-02
**Pedido do operador:** depois de perguntar "há mais sugestões que gostaria de
sugerir?", o operador pediu "implemente" para as 5 ideias adicionais propostas
e um novo relatório de implementação em `.md` e `.pdf`.

Este documento é a continuação de
[relatorio-implementacao.md](relatorio-implementacao.md) (rodada 1: motivo
condutor, densidade de citação, dupla analogia, cena de contraste, exemplos de
voz, alertas de estilo em `auditar-obra.py`). Todas as mudanças abaixo também
são **aditivas** — nenhuma altera ABNT, as 7 seções do EITA-V2 ou os
requisitos contratuais R1-R14.

---

## Resumo das 5 sugestões e o que foi feito com cada uma

| # | Sugestão | Status |
|---|---|---|
| 1 | Persona recorrente do leitor (além da metáfora) | **Implementada** |
| 2 | Callback explícito entre capítulos | **Implementada** |
| 3 | Variação de ritmo de frase | **Implementada** (checagem heurística) |
| 4 | Sub-títulos evocativos em seções longas | **Implementada** |
| 5 | Piloto com leitor real antes de escalar | **Não codificada** — ver justificativa abaixo |

---

## 1. Persona recorrente do leitor

**Arquivos:** `arquiteto/SKILL.md`, `redator-eita/SKILL.md`, `template_eita.md`

- `arquiteto` agora define, junto do motivo condutor, uma **persona do
  leitor** nomeada (`persona_leitor`, ex.: "Engenheiro Agêntico") — o papel que
  o leitor incorpora dentro do cenário do motivo condutor. Campo novo no
  schema de `sumario_macro.json`:
  ```json
  "motivo_condutor": {
    "nome": "...", "descricao": "...", "vocabulario": [...],
    "persona_leitor": "string (ex.: 'Engenheiro Agêntico')"
  }
  ```
- `redator-eita` reforça essa identidade em 2ª pessoa ("Como Engenheiro
  Agêntico, você já sabe que...") **com moderação**: 1-2 vezes por capítulo,
  nunca em toda página — regra explícita para não soar repetitivo.
- Diferença deliberada da metáfora já existente: o motivo condutor é o
  *cenário* (a fábrica); a persona é *quem o leitor se torna* dentro dele.

## 2. Callback explícito entre capítulos

**Arquivos:** `estrategista/SKILL.md`, `template_eita.md`, `redator-eita/SKILL.md`,
`scripts/auditar-obra.py`

- `estrategista` passa a identificar, para cada capítulo (exceto o 1º), **um
  conceito nomeado** de um capítulo anterior a retomar explicitamente — campo
  `callback_capitulo_anterior` no draft (nível de capítulo, fora da lista de
  pilares), ex.: `"Capítulo 3: o conceito de Janela de Contexto, agora
  aplicado a memória distribuída"`.
- A regra de "ponte com capítulo anterior" da seção Introdução (que já
  existia) foi reforçada: não pode mais ser uma transição genérica — precisa
  nomear o capítulo e o conceito.
- **Evidência determinística nova em `auditar-obra.py`:** função
  `tem_callback_capitulo_anterior()` com duas regex (`RE_CALLBACK_NUMERADO`
  para "Capítulo N" com N diferente do próprio, `RE_CALLBACK_GENERICO` para
  "capítulo(s) anterior(es)"). Resultado por capítulo em `callback_presente`,
  agregado em `alertas_estilo.capitulos_sem_callback_capitulo_anterior`. O
  Capítulo 1 é automaticamente isento (não há capítulo anterior).

## 3. Variação de ritmo de frase

**Arquivo:** `scripts/auditar-obra.py` (checagem nova, não bloqueante)

- Nova função `ritmo_de_frase()`: quebra o corpo do capítulo (sem código, sem
  headings) em frases por heurística de pontuação, mede a **média de
  palavras por frase** e o **coeficiente de variação** (desvio-padrão /
  média).
- Um capítulo é sinalizado em `alertas_estilo.capitulos_ritmo_monotono`
  apenas quando a variação é baixa (`coeficiente_variacao < 0.35`) **e** a
  frase média é longa (`>= 18 palavras`) — a combinação que caracteriza tom de
  relatório (frases uniformemente longas), não apenas frases longas
  ocasionais.
- É explicitamente documentado como **heurístico** (não um parser
  gramatical): serve de sinal de estilo, nunca de requisito bloqueante.

## 4. Sub-títulos evocativos em seções longas

**Arquivos:** `template_eita.md`, `redator-eita/SKILL.md`

- Quando a seção Técnica (ou Aplica) ultrapassar ~800 palavras, o redator deve
  quebrá-la em blocos com sub-títulos em `###` (nunca `##`, reservado às 7
  seções contratuais) — ex.: `### A Falha na Esteira e a Correção
  Estrutural`.
- **Verificação de segurança:** confirmado que a regex de detecção de seção
  usada por `dividir_secoes()` em `auditar-obra.py` (`^##\s*(\d)...`) exige
  um dígito logo após `##` — uma linha `### Texto` nunca é capturada como
  início de seção, então os sub-títulos não interferem na auditoria nem na
  compilação.
- Os sub-títulos podem reaproveitar o vocabulário do motivo condutor,
  reforçando a unidade narrativa também na estrutura visual do capítulo.

## 5. Piloto com leitor real antes de escalar — não codificada

Esta sugestão é uma **prática de processo manual**, não uma regra de
formatação ou de conteúdo: rodar 1 capítulo do próximo livro e coletar
feedback de um leitor humano antes de liberar a obra inteira em lote.

**Por que não virou código/skill:** transformar isso em um *gate* automático
(ex.: pausar a esteira depois do primeiro capítulo esperando aprovação humana)
contradiz diretamente a **REGRA 3** do projeto ("Autonomia Total Agêntica" —
depois que o tema é definido, a esteira roda 100% sem paradas). Adicionar uma
parada obrigatória mudaria o comportamento contratual do fluxo, o que não foi
pedido nem é compatível com o restante do sistema.

**Como fica disponível, então:** como recomendação de processo para o
operador, não como código — nada impede rodar manualmente `/criar-livro
<slug>` limitando o sumário a 1 capítulo (o próprio `arquiteto` já aceita isso
via "Se o operador pedir um piloto ou teste, reduza o escopo a 1 Parte com 1
Capítulo"), revisar o resultado, e só então rodar a obra completa.

---

## Validação técnica

```
python -m py_compile scripts/auditar-obra.py   # OK, sem erro de sintaxe
python scripts/auditar-obra.py ai-driven-development
```

Resultado do smoke-test (mesma obra-piloto usada na rodada 1):
- `[ESTILO] sem callback nomeado a capitulo anterior em: cap 03, cap 04, cap 06, cap 09`
  — funcionando (livro produzido antes desta mudança, comportamento esperado).
- `[OK] Ritmo de frase variado em todos os capitulos avaliados` — a checagem
  rodou sem erro e não acusou falso positivo nesta obra.
- Veredito R1-R14 permaneceu `NAO CONFORME` pelos mesmos dois motivos de
  sempre (contagem de capítulos/páginas) — **inalterado** pelas novas
  checagens de estilo, confirmando que elas continuam não bloqueantes.
- JSON de saída verificado em UTF-8 válido, com os novos campos
  `callback_presente`, `ritmo_frase`,
  `capitulos_sem_callback_capitulo_anterior` e `capitulos_ritmo_monotono`.

## Arquivos alterados nesta rodada

| Arquivo | Mudança |
|---|---|
| `.claude/skills/arquiteto/SKILL.md` | `persona_leitor` no schema + seção explicativa |
| `.claude/skills/estrategista/SKILL.md` | campo `callback_capitulo_anterior` |
| `templates/template_eita.md` | callback nomeado (Introdução), persona (Ilustra), sub-títulos evocativos (Técnica) |
| `.claude/skills/redator-eita/SKILL.md` | espelha as 3 regras acima + procedimento atualizado |
| `scripts/auditar-obra.py` | `tem_callback_capitulo_anterior()`, `ritmo_de_frase()`, 2 novos campos em `alertas_estilo` |
| `.claude/skills/revisor-tecnico/SKILL.md` | Passo 3.1 ganha os 2 novos alertas |
| `.claude/agents/subagente-redator-capitulo.md` | checklist ganha persona, callback e ritmo |

(Os arquivos correspondentes em `agentic/` são hardlinks/junctions e se
atualizam automaticamente — ver seção 6 do `CLAUDE.md`.)

## O que **não** foi alterado
- As 7 seções do EITA-V2, sua ordem e cabeçalhos literais.
- Nenhum requisito contratual R1-R14 de `/criar-livro`.
- REGRA 3 (autonomia total) — por isso a sugestão 5 ficou fora do código.
- Fluxo de TCC/Artigo/E-book, que usa tom deliberadamente diferente
  (acadêmico impessoal ou leve de mercado, sem motivo condutor/persona).
