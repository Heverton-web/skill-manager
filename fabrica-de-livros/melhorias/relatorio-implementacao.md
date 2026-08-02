# Relatório de Implementação — Sugestões de `relatorio-tom-de-comunicacao.md`

**Data:** 2026-08-02
**Pedido do operador:** "Implemente as sugestões de
`melhorias/relatorio-tom-de-comunicacao.md` ao projeto."

Este documento registra exatamente o que foi alterado na esteira, arquivo por
arquivo, mapeado às 6 sugestões do relatório anterior
([relatorio-tom-de-comunicacao.md](relatorio-tom-de-comunicacao.md)). Nenhuma
regra de ABNT, nenhuma das 7 seções do EITA-V2 e nenhum requisito contratual
R1-R14 foi alterado — todas as mudanças são aditivas, dentro da mesma estrutura.

---

## Resumo das mudanças

| # | Arquivo | O que mudou |
|---|---|---|
| 1 | [.claude/skills/arquiteto/SKILL.md](.claude/skills/arquiteto/SKILL.md) | Nova seção "Motivo Condutor da Obra" + campo `motivo_condutor` no schema de `sumario_macro.json` |
| 2 | [.claude/skills/estrategista/SKILL.md](.claude/skills/estrategista/SKILL.md) | Novo campo `conceito_denso` (bool) por pilar em `payload_estrategico` |
| 3 | [templates/template_eita.md](templates/template_eita.md) | Seção Explica: teto de densidade de citação. Seção Ilustra: regra do motivo condutor + dupla analogia. Seção Aplica: cena de contraste obrigatória |
| 4 | [.claude/skills/redator-eita/SKILL.md](.claude/skills/redator-eita/SKILL.md) | Espelha as 3 regras acima + exemplos ❌/✅ de calibração de voz + procedimento atualizado |
| 5 | [scripts/auditar-obra.py](scripts/auditar-obra.py) | Nova checagem não bloqueante: citações empilhadas e recorrência do motivo condutor fora da Ilustra (`alertas_estilo`) |
| 6 | [.claude/skills/revisor-tecnico/SKILL.md](.claude/skills/revisor-tecnico/SKILL.md) | Novo Passo 3.1 (leitura de `alertas_estilo`) + nova seção no template do parecer |
| 7 | [.claude/agents/subagente-redator-capitulo.md](.claude/agents/subagente-redator-capitulo.md) | Checklist de auto-validação ganha 3 itens de estilo |

`git diff --stat`: 12 arquivos alterados (6 fontes + suas 6 réplicas via
hardlink/junction em `agentic/`, que se atualizam automaticamente — ver seção 6
do `CLAUDE.md`), 413 inserções, 41 remoções.

---

## Detalhe por sugestão do relatório original

### 4.1 — Motivo condutor único por obra
**Arquivo:** `arquiteto/SKILL.md`
- Nova seção "Motivo Condutor da Obra": instrui o `arquiteto` a escolher, uma
  única vez na Fase 1, uma metáfora-mestra para a obra inteira (ex.: "a fábrica",
  "o organismo vivo") com nome, descrição e vocabulário de 6-10 termos.
- Schema de `sumario_macro.json` ganhou o campo:
  ```json
  "motivo_condutor": {
    "nome": "string",
    "descricao": "string",
    "vocabulario": ["string", ...]
  }
  ```
- Omitido (`null`) quando `tipo_obra = "tcc"` — preserva o tom acadêmico
  impessoal do TCC, que não deve ganhar metáfora persistente.

### 4.2 — Teto de densidade de citação + "citação após explicação"
**Arquivos:** `template_eita.md` (seção Explica) e `redator-eita/SKILL.md`
(seção "Citações inline")
- Regra nova: citação nunca substitui a explicação, sempre vem depois de uma
  frase que já expressa a ideia.
- Proibido empilhar 2+ citações consecutivas (`[N][N]`) sem prosa entre elas.
- Máximo de 2 citações por parágrafo na seção Explica; excedente vai para
  Técnica ou tabela.

### 4.3 — Definição em duas camadas para conceitos densos
**Arquivos:** `estrategista/SKILL.md`, `template_eita.md` (seção Ilustra),
`redator-eita/SKILL.md`
- `estrategista` agora marca `"conceito_denso": true/false` por pilar (só 1 dos
  3 pilares do capítulo normalmente justifica a marcação).
- Quando `conceito_denso=true`, o `redator-eita` escreve 2 analogias
  complementares na seção Ilustra (mecânica geral + ponto mais difícil), em vez
  de 1 única analogia genérica.

### 4.4 — Cena obrigatória de contraste (Erro Comum vs. Prática Correta)
**Arquivos:** `template_eita.md` (seção Aplica) e `redator-eita/SKILL.md`
- A seção Aplica deve abrir com uma cena narrativa em 2ª pessoa: situação
  concreta → erro plausível acontecendo → diagnóstico → correção.
- A lista de "armadilhas comuns" continua existindo, mas só como síntese
  posterior à cena — nunca a substituindo.

### 4.5 — Exemplos ❌/✅ na regra de tom
**Arquivo:** `redator-eita/SKILL.md` (seção "Tom Transformacional")
- Adicionados 3 pares de frase (❌ registro de relatório / ✅ registro de
  mentor), extraídos do comparativo original, para calibrar o redator com
  exemplos concretos.

### 4.6 — Evidência determinística (script)
**Arquivo:** `scripts/auditar-obra.py`
- Nova regex `RE_CITACAO_EMPILHADA` detecta sequências de 2+ citações `[N]`
  sem prosa entre elas.
- Nova função `montar_alertas_estilo()` calcula, por capítulo:
  - `capitulos_com_citacao_empilhada` (lista de ocorrências).
  - `capitulos_sem_recorrencia_motivo_condutor` (capítulos onde o vocabulário
    do `motivo_condutor` de `sumario_macro.json` não aparece fora da seção
    Ilustra).
- Os dois entram em `relatorio_auditoria.json.alertas_estilo` — **não afetam
  o veredito CONFORME/NÃO CONFORME** nem os requisitos R1-R14, são só
  recomendação de estilo.
- Saída humana do script ganhou as linhas `[ESTILO] ...` / `[OK] ...` /
  `[INFO] ...` correspondentes.
- `revisor-tecnico/SKILL.md` ganhou o Passo 3.1 (lê `alertas_estilo` e corrige
  oportunisticamente, sem travar a esteira) e uma nova seção no parecer:
  "Recomendações de estilo (não bloqueantes)".

---

## Validação técnica

- `python -m py_compile scripts/auditar-obra.py` → **OK**, sem erro de sintaxe.
- Smoke-test contra a obra já produzida `output/ai-driven-development/`:
  ```
  python scripts/auditar-obra.py ai-driven-development
  ```
  Resultado: o novo alerta `[ESTILO]` detectou corretamente **115 citações
  empilhadas** (o mesmo número apurado manualmente via `grep` no relatório
  anterior) e sinalizou, via `[INFO]`, que este livro-piloto não tem
  `motivo_condutor` em `sumario_macro.json` — comportamento esperado, pois foi
  produzido antes desta mudança. O veredito R1-R14 (`NAO CONFORME` por
  contagem de capítulos/páginas, não relacionado a este ajuste) permaneceu
  intacto, confirmando que o alerta de estilo não interfere na auditoria
  contratual.
- JSON de saída (`relatorio_auditoria.json`) verificado em UTF-8 válido.

## O que isso muda na prática, na próxima obra gerada
1. `/esbocar` → `arquiteto` grava o motivo condutor da obra junto com o sumário.
2. `estrategista` sinaliza qual pilar de cada capítulo é conceitualmente denso.
3. `redator-eita` reaproveita o motivo condutor em vez de inventar metáfora por
   capítulo, evita empilhar citações, reforça conceitos densos com 2 analogias,
   e abre a seção Aplica com uma cena de erro→correção.
4. `auditar-obra.py` reporta (sem bloquear) onde a obra ainda usa citação
   empilhada ou perdeu o fio do motivo condutor.
5. `revisor-tecnico` lê esses alertas e corrige o que for barato de corrigir,
   documentando o restante no parecer.

## O que **não** foi alterado
- As 7 seções do EITA-V2, sua ordem e cabeçalhos literais.
- Nenhum requisito contratual R1-R14 de `/criar-livro`.
- Formato ABNT, numeração `[N]`, mínimo de referências por capítulo.
- Fluxo de TCC/Artigo/E-book (`redator-academico`, `redator-ebook`) — o pedido
  do operador e o relatório de origem tratavam especificamente do tom do
  livro comercial (EITA), não do tom acadêmico impessoal do TCC.
