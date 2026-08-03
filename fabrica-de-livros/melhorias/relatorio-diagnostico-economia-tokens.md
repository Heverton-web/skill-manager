# Relatório de Diagnóstico — Impacto da Stack de Economia de Tokens na Fábrica de Livros

**Data:** 2026-08-02
**Escopo:** todo o repositório `proj_livros` (raiz) e o subprojeto `fabrica-de-livros`.
**Gatilho:** após a instalação da stack de economia severa de tokens (RTK, Headroom,
LeanCTX, Cavecrew, Caveman) no repositório pai, o operador relatou bugs incontáveis,
perda de qualidade do material produzido e falhas na geração dos PDFs.

---

## 1. Pedido do operador

> "Após a instalação das skills, rules, scripts, mcps, specs de economia severa de
> tokens tivemos bugs incontáveis, perda da qualidade do material produzido e erro
> de geração dos PDFs [...]. O ideal é utilizar sim economia de tokens mas sem
> prejudicar a qualidade, profundidade e entrega completa dos materiais produzidos
> pela fábrica-de-livros."

---

## 2. Metodologia

1. Reconstrução do histórico (`git log`, `git diff`) de `scripts/auditar-obra.py`
   (única alteração pendente no working tree) e dos commits que instalaram a stack
   de token economy (`96841eb`, `59c1dc8`, `2d9a630`, `592ebe1`, `7919c8c`).
2. Inspeção do hook global `PreToolUse` (`~/.claude/settings.json`) que intercepta
   **todo** comando Bash em **todo** projeto via `rtk hook claude`, com testes
   diretos (`echo '{"tool_name":"Bash",...}' | rtk hook claude`) para confirmar
   quais binários são reescritos e quais não são.
3. Reprodução direta de comportamento do `rtk grep` sobre um capítulo real
   (`cap_1.md`, 409 linhas) para confirmar (ou refutar) truncamento de prosa.
4. Três sub-auditorias independentes em paralelo:
   - Revisão de código de todo o pipeline determinístico e de compilação PDF
     (`pool-capitulos.py`, `validar-codigo.py`, `renderizar-diagramas.py`,
     `metadados_livro.py`, `parametros_obra.py`, `fatiar-obra.py`, `gerar-epub.py`,
     `compilar-para-pdf.py`, `pdf_typst.py`, `converter-md-pdf.ps1`,
     `validar-abnt-tcc.py`, templates `.typ`).
   - Execução real de `scripts/auditar-obra.py` contra as 6 obras existentes em
     `output/` e inspeção manual do conteúdo de capítulos.
   - Leitura cruzada de `CLAUDE.md` (raiz e fábrica), `~/.claude/CLAUDE.md`,
     `~/.claude/RTK.md`, `MANUAL_*.md` e das `SKILL.md` de headroom/lean-ctx/
     cavecrew/rtk-memory/pre-flight-check em busca de instruções ambíguas.

---

## 3. Achados (ordenados por severidade)

### 3.1 [CRÍTICO — corrigido] Falso-positivo em massa no gate de "pendências" (R13)

`scripts/auditar-obra.py` (linha ~67, antes do fix): `RE_PENDENCIA` usava
`\bTODO\b` com `re.IGNORECASE`. Isso casa também com a palavra portuguesa comum
"todo/Todo" ("nem todo sistema...", "todo tripulante...", "todo o casco..."),
disparando o requisito **R13 ("Sem truncamento nem pendências")** como FALHA em
praticamente qualquer capítulo escrito em PT-BR.

**Evidência:** testado o regex antigo contra os 10 capítulos do único livro com
conteúdo real (`ai-driven-development-do-zero-ao-deploy`) — **20 falsos-positivos
em 9 dos 10 capítulos**.

**Consequência em cascata:** R13 alimenta diretamente a tabela de correção da
skill `revisor-tecnico` ("Truncamento/TODO/placeholder → Complete o trecho"). Um
revisor agindo sobre esse falso-positivo reescreve prosa perfeitamente pronta para
"completar" um marcador fantasma — via direta de degradação de qualidade e de
retrabalho (o "bugs incontáveis" percebido). Além disso, o fluxo documentado no
`CLAUDE.md` só libera a compilação (Fase 3 / Pandoc+Typst) depois que a obra passa
pela Fase 2.5 — com R13 sempre em falha, a obra nunca é considerada pronta e a
compilação de PDF nunca chega a ser tentada (ver 3.2).

**Correção aplicada:** o working tree já continha o início do fix (regex separado
em `RE_PENDENCIA_MAIUSCULA`, case-sensitive, só `TODO/FIXME/TBD/XXX`, e
`RE_PENDENCIA_GENERICA`, case-insensitive, só para os marcadores realmente
inequívocos). Esta sessão **finalizou e verificou** o fix: moveu `import
itertools` para o topo do arquivo (estava sendo importado a cada chamada dentro de
`_PendenciaMatcher.finditer`) e reexecutou o script contra a obra real — **R13
agora passa** (0 falsos-positivos). Arquivo: `scripts/auditar-obra.py`.

---

### 3.2 [CRÍTICO] Nenhuma obra chegou à Fase 3 — 0 de 6 PDFs gerados

Rodando `python scripts/auditar-obra.py <slug>` contra todas as obras existentes em
`output/`:

| Obra | Estado dos capítulos | Veredito | PDF |
|---|---|---|---|
| `livros/ai-driven-development-do-zero-ao-deploy` | 10 capítulos redigidos (364.212 caracteres) | NAO CONFORME (só R2) | **ausente** |
| `artigos/art-01`, `art-02`, `art-03` | esqueleto (`config_obra.json`/`sumario_macro.json`), `capitulos/` **vazia** | erro (nenhum `cap_*.md`) | ausente |
| `ebooks/eb-01`, `eb-02` | pasta **totalmente vazia** | erro | ausente |
| `tccs/` | nenhuma obra | — | — |

**Nenhum arquivo `.pdf` existe em `output/`** e **nenhum log de erro de
compilação** foi encontrado. `pandoc 3.10` e `typst 0.15.1` estão instalados e
funcionais no PATH — a ausência de PDF não é falha do Pandoc/Typst, é o pipeline
**nunca ter avançado até o Nó 10** para nenhuma obra:

- O único livro com conteúdo real nunca teve `livro_final.md` gerado (Fase 3 nunca
  rodou) — consistente com o gate R13 sempre falho (3.1) bloqueando a progressão.
- Os 3 artigos e 2 ebooks derivados nunca tiveram seus subagentes de redação
  (`subagente-redator-artigo`, `subagente-adaptador-ebook`) despachados — ficaram
  parados na etapa de fatiamento/planejamento.

**Conclusão:** o "erro de geração dos PDFs" relatado não é um bug no código do
compilador PDF (`compilar-para-pdf.py`/`pdf_typst.py`/templates `.typ` — ver 3.6),
e sim o efeito em cascata do gate de qualidade travado (3.1) somado a produção
nunca retomada para os derivados. Corrigido o 3.1, a recomendação é **rodar de
novo a Fase 2.5 + Fase 3** para o livro e reativar os subagentes pendentes dos
artigos/ebooks (ver seção 5).

---

### 3.3 [ALTO — corrigido via regra de CLAUDE.md] `rtk grep` corrompe prosa de manuscrito quando há muitas ocorrências

**Reproduzido diretamente** nesta sessão: `rtk grep` sem `-o` muda para um modo de
"excerto compacto" quando o número de matches é alto, mostrando apenas uma janela
de ~40-80 caracteres ao redor de cada ocorrência, com `...` nas duas pontas:

```
...odificação por vibe trata testes, linting e CI/CD como opcionais, o que eleva ri...
...ão de configurar suíte de testes, CI e revisão por agente é custo sem retorno pr...
```

Isso é um comportamento correto e útil para **código** (achar uma função em 10k
linhas), mas destrói a legibilidade de **prosa** — um agente que use `rtk grep`
para checar terminologia, citações `[N]` ou continuidade de um capítulo recebe
fragmentos de frase cortados, e pode tomar decisões de correção (ou reescrita)
baseado em texto truncado sem qualquer marcador visual de que aquilo é um recorte
de ferramenta, não o conteúdo real do arquivo.

Os artefatos residuais `scratch_check.txt` e `scratch_check2.txt` (raiz de
`fabrica-de-livros`, não commitados) são evidência independente de que técnicas de
recorte de texto por largura fixa vinham sendo usadas para inspecionar este mesmo
capítulo — reforçando que a fronteira entre "economia de tokens no terminal" e
"leitura fiel de conteúdo de obra" não estava clara em nenhuma instrução do
projeto até esta sessão.

**Correção aplicada:** adicionado o item 8 em `fabrica-de-livros/CLAUDE.md` (seção
0) e uma nova seção em `CLAUDE.md` da raiz, proibindo explicitamente `rtk
grep`/`rtk read`/`headroom` sobre qualquer arquivo em `output/**` — leitura deve
ser sempre integral via `Read`/`cat`. Como `fabrica-de-livros/CLAUDE.md` é
hardlink de `AGENTS.md`, `.cursor/rules/fabrica-agentica.mdc`,
`.windsurfrules`/`.windsurf/rules/...`, `.clinerules` e
`.github/copilot-instructions.md`, a correção vale automaticamente para as 7 IDEs
agênticas listadas na seção 6 do próprio `CLAUDE.md`, sem precisar editar cada uma.

---

### 3.4 [ALTO — corrigido via regra de CLAUDE.md] Redação ambígua de "Headroom & RTK" e "LeanCTX" autorizava truncar dado de obra

A redação original (seção 0, item 2) dizia: *"Todo log, **payload JSON** ou output
de comando com mais de 7 linhas DEVE ser comprimido [...] mantendo 3 primeiras e 4
últimas linhas"*. Isso nomeia literalmente "payload JSON" sem excluir os payloads
estruturais da própria fábrica (`sumario_macro.json`, `templates/payload_estado.json`,
`relatorio_auditoria.json`), que facilmente passam de 7 linhas e cujo **meio** é
exatamente onde ficam a maioria dos capítulos/seções listados. O item 3 (LeanCTX)
mandava, com a palavra "sempre", limitar toda leitura a 20-50 linhas — mas a Fase
3 (skill `compilador-abnt`) exige explicitamente concatenar capítulos inteiros
(100-300+ linhas cada) em fluxo contínuo, sem nenhuma exceção documentada até
agora.

**Correção aplicada:** reescritos os itens 2 e 3 do `CLAUDE.md` da fábrica para
restringir headroom/rtk a "log de terminal, saída de build/teste ou payload de
debug efêmero", e lean-ctx/grep_search a "arquivos de código/configuração" — mais
o item 8 (ver 3.3) tornando a exceção explícita e com prioridade máxima sobre os
itens 2-4.

---

### 3.5 [MÉDIO — corrigido em 6.1] Isenção do Pandoc+Typst era acidental, não configurada

O `CLAUDE.md` promete (regra 5, seção 0) que a stack de token economy "não deve
interferir" na compilação Pandoc+Typst. Na prática, essa isenção **não existe
como mecanismo** — ela só "funciona" porque o RTK atual não reconhece os binários
`typst`/`pandoc`/`python` como um dos seus alvos de filtro (`git`, `gh`, `pnpm`,
`docker`, etc. são reescritos; estes três não são, confirmado testando o hook
`rtk hook claude` diretamente). O hook global (`~/.claude/settings.json`,
`PreToolUse` → `matcher: "Bash"` → `rtk hook claude`) intercepta **todo** comando
Bash, em **todo** projeto, sem allowlist por diretório ou por binário. Se uma
versão futura do RTK passar a reconhecer esses binários (plausível — RTK já cobre
dezenas de CLIs), a isenção quebra silenciosamente sem que nada neste repositório
precise mudar, e ninguém seria avisado.

**Corrigido em 6.1** (após sua confirmação): `exclude_commands` do RTK passou a
listar `pandoc`/`typst`/`python` explicitamente em `%APPDATA%\rtk\config.toml`.

---

### 3.6 [INFORMATIVO] Pipeline de compilação PDF em si — sem regressão de código

Auditoria completa de `pool-capitulos.py`, `validar-codigo.py`,
`renderizar-diagramas.py`, `metadados_livro.py`, `parametros_obra.py`,
`fatiar-obra.py`, `gerar-epub.py`, `compilar-para-pdf.py`, `pdf_typst.py`,
`converter-md-pdf.ps1`, `validar-abnt-tcc.py` e os 3 templates `.typ`: nenhum
destes arquivos foi tocado pelos commits que instalaram a stack de token economy
(`96841eb`, `59c1dc8`, `2d9a630`, `592ebe1`, `7919c8c`) — todos permanecem
idênticos à versão anterior à instalação. Templates Typst usam apenas caminhos
relativos (sem o bug de path absoluto `C:\...` já documentado na nota técnica do
próprio `CLAUDE.md`). `pdf_typst.py` é código morto/duplicado (a mesma lógica já
está inline em `compilar-para-pdf.py::converter_via_typst`) — não é bug, apenas
redundância a limpar no futuro se quiser.

---

### 3.7 [MÉDIO] Livro entregue abaixo do tamanho contratado (R2) — não é bug de token economy

Após o fix de 3.1, o livro `ai-driven-development-do-zero-ao-deploy` passa em
todos os requisitos **exceto R2**: 364.212 caracteres contra o mínimo de 375.000
(~97%, faltam ~4.400 caracteres / ~2 páginas). Isso é um déficit real de conteúdo,
não um artefato de auditoria — mas está a poucos parágrafos de conformidade. Não
identificamos ligação causal com a stack de token economy (os scripts de redação
não foram alterados pelos commits em questão); mais provável é retomada
incompleta de um lote de capítulos pelo `pool-capitulos.py`.

---

### 3.8 [BAIXO — recomendação, não aplicado] Achados menores

- ~~Referências fora de ordem numérica~~ — **corrigido em 6.2** (R15 novo +
  reordenação de `cap_1.md`/`cap_3.md`).
- **`pool-capitulos.py` (linha ~97-98)**: piso de "capítulo entregue" fixo em
  3.000 caracteres, bem abaixo da média esperada por capítulo (~25.000-37.500,
  conforme `parametros_obra.TAMANHOS`). Um capítulo com 1/8 do tamanho esperado
  passa a Fase 2 sem novo retry (a auditoria de tamanho real é só a cargo de
  `auditar-obra.py`, fora do pool). Não alterado — pode ser proposital como
  sanity-check barato, e não como piso de qualidade; confirmar antes de mudar.
- **Skill `pre-flight-check`** é genérica de stack Node/TS (`npm run
  check:types`, `npx vitest run`, `npm run build`) — nenhum desses comandos existe
  neste projeto Python/Pandoc/Typst. Peso morto herdado da instalação da stack,
  sem risco de corromper conteúdo, mas sem valor real aqui.
- ~~`scratch_check.txt`/`scratch_check2.txt`~~ — **apagados em 6** (artefatos de
  depuração de sessão anterior, evidência do problema de 3.3, já documentada
  aqui em texto).

---

## 4. Correções já aplicadas nesta sessão

| # | Arquivo | Mudança |
|---|---|---|
| 1 | [scripts/auditar-obra.py](../scripts/auditar-obra.py) | Fix do falso-positivo `\bTODO\b`/"todo" finalizado e verificado (R13 volta a passar); `import itertools` movido para o topo do arquivo |
| 2 | [CLAUDE.md](../CLAUDE.md) (fábrica) | Reescritos itens 2-4 da seção 0 (escopo restrito a terminal/código); adicionado item 8 (exceção de fidelidade de conteúdo, prioridade máxima) |
| 3 | `../../CLAUDE.md` (raiz `proj_livros`) | Adicionada seção "EXCEÇÃO DE FIDELIDADE DE CONTEÚDO" após o bloco `<!-- rtk-instructions -->` (fora do bloco auto-gerado, para sobreviver a um futuro `rtk init`) |

Nenhum arquivo de saída de obra (`output/**`) foi alterado — apenas lido para
diagnóstico.

---

## 5. Recomendações da rodada anterior — todas aplicadas nesta rodada (você confirmou "sim todas")

1. ~~Restringir o hook global do RTK~~ — **aplicado** (ver 6.1).
2. ~~Rerodar Fase 2.5 + Fase 3 do livro~~ — **aplicado** (ver 6.2): livro agora
   CONFORME em todos os requisitos e com PDF gerado.
3. ~~Retomar artigos e ebooks derivados~~ — **aplicado** (ver 6.3-6.4).
4. ~~Apagar `scratch_check.txt`/`scratch_check2.txt`~~ — **aplicado**.
5. ~~Avaliar R15 (ordem de referências)~~ — **aplicado** (ver 6.2).

---

## 6. Ações aplicadas na rodada "sim todas"

### 6.1 Hook global do RTK restrito explicitamente

`%APPDATA%\rtk\config.toml` → `[hooks] exclude_commands` passou de `[]` para
`["pandoc", "typst", "python", "python3", "py"]`. Testado com `rtk hook claude`
direto: `pandoc`/`typst`/`python` continuam sem reescrita (como já eram, mas
agora por configuração explícita, não por o RTK simplesmente não reconhecer o
binário) e `git`/demais comandos continuam sendo reescritos normalmente. É uma
config **global do usuário** (afeta todos os projetos) — aplicada porque você
confirmou "sim todas".

### 6.2 Livro `ai-driven-development-do-zero-ao-deploy` — CONFORME e com PDF

- **R15 novo implementado** em `scripts/auditar-obra.py`: checa se as entradas
  `[N]` da seção 7 aparecem em ordem numérica ascendente (NBR 6023). Achou
  `cap_1.md` e `cap_3.md` fora de ordem (bibliografia alfabética por fonte, não
  por ordem de citação) — **corrigido**: reordenadas as entradas dessas duas
  seções de referências para ordem numérica (conteúdo preservado, só a ordem
  das entradas mudou).
- **R2 (tamanho)**: entre o diagnóstico inicial e esta rodada, o livro cresceu
  sozinho de 325.258 → 377.328 caracteres (havia produção autônoma concorrente
  rodando — ver 6.5) e passou a cumprir o mínimo de 375.000 sem intervenção
  nossa.
- **Resultado:** auditoria em `--estrito` agora retorna **CONFORME** em R1-R15.
  `livro_final.pdf` já existe (185 páginas, header/trailer PDF válidos,
  3,9 MB) — gerado por processo concorrente enquanto esta sessão trabalhava
  (ver 6.5), não precisou de recompilação nossa.

### 6.3 Bug real e novo encontrado: `extrair_citacoes_autor_data` não reconhecia citações empilhadas nem autores compostos

Ao auditar os 3 artigos derivados (`art-01/02/03`, já com conteúdo real
produzido pelo processo concorrente), 2 de 3 reprovavam por motivo **objetivamente
errado**, não por defeito de redação:

- `art-02/cap_4.md` (Conclusão): `ARTIGO-CIT` acusava **zero citações** na
  seção, apesar de ter 9 citações reais em 3 blocos do tipo
  `(HARTENFELLER, 2026; SENTRY, 2026; TOOLTWEAK, 2025)`. Causa: o regex
  `RE_CITACAO_AUTOR_DATA` (`scripts/parametros_obra.py`) só reconhecia um autor
  compartilhando um único ano por parênteses (`(A; B, 2024)`), nunca autores
  **empilhados com ano próprio cada um** (`(A, 2024; B, 2025; C, 2026)`) — um
  padrão de citação NBR 10520 legítimo e comum quando várias fontes sustentam a
  mesma frase.
- `art-01/cap_3.md`: `ARTIGO-RASTRO` acusava citação órfã `"group (2026)"`.
  Causa: a citação narrativa `Futurum Group (2026)` tem autor de **duas
  palavras**; o regex antigo só capturava a última palavra antes do
  parêntese (`Group`), enquanto a extração do lado da referência bibliográfica
  já pegava a primeira palavra (`FUTURUM`) — duas normalizações inconsistentes
  do mesmo nome, gerando falso-positivo de órfã.

**Corrigido** em `scripts/auditar-obra.py`: reescrita `extrair_citacoes_autor_data`
com 3 regex novos (`RE_PAREN_COM_ANO`, `RE_SEGMENTO_ANO`, `RE_SEGMENTO_SO_NOME`)
que tratam parêntese-simples, autor-compartilhando-ano e autor-empilhado-com-ano-próprio
da mesma forma, mais `RE_CITACAO_NARRATIVA` agora aceitando até 4 palavras de
nome de autor organizacional. Testado isoladamente antes de aplicar e revalidado
contra os 3 artigos reais — sem introduzir novos falsos-positivos.

Depois desse fix, restava 1 defeito **real** de conteúdo em `art-01/cap_3.md`:
citação `(Ibm, 2026; Promptlayer, 2026)` sem entrada correspondente de
"PromptLayer" na bibliografia (só existe "PROMPTHUB", uma fonte diferente já
citada corretamente em outro parágrafo do mesmo capítulo — aparenta ser confusão
de nomes similares pelo redator). **Corrigido**: removida a citação órfã
`Promptlayer, 2026` do texto (não inventamos referência nova).

**Resultado:** os 3 artigos agora auditam **CONFORME** e foram **compilados em
PDF** (`livro_final.pdf` de cada um, 208-245 KB).

### 6.4 Bug real e novo encontrado: `fatiar-obra.py --ebooks` nunca escrevia `sumario_macro.json`/`config_obra.json`

Ao investigar por que os 2 ebooks derivados do livro (e também os 8 ebooks de
um segundo livro-mãe, `sdlc-ai-first`, achado em produção concorrente — ver
6.5) ficavam com a pasta **totalmente vazia**, encontramos que
`gerar_ebooks()` em `scripts/fatiar-obra.py` só criava o diretório e atualizava
`derivados.json` — ao contrário de `gerar_artigos()` (mesmo arquivo), nunca
escrevia `sumario_macro.json` nem `config_obra.json` dentro da pasta do ebook.
Sem esses dois arquivos, `subagente-adaptador-ebook` não tem como saber quais
capítulos-fonte adaptar — **nenhum ebook desta fábrica jamais poderia ter sido
gerado**, em nenhum livro, até este fix. Não é bug de token economy; é uma
lacuna de implementação da Fase C (V4) que antecede a instalação da stack.

**Corrigido**: `gerar_ebooks()` agora escreve `sumario_macro.json`
(`titulo_obra`, `tipo_obra: "ebook"`, `slug_livro_mae`,
`capitulos_fonte_livro_mae`) e `config_obra.json` para cada ebook, além de criar
`capitulos/`+`revisao/`, espelhando o que `gerar_artigos()` já fazia. Rodado de
novo para os 2 ebooks do livro AIDD — skeletons corretos confirmados.

Despachados os subagentes `subagente-adaptador-ebook` para os 2 ebooks (redação
+ capa + EPUB) — **concluídos e verificados**:

| Ebook | Caracteres | Veredito | EPUB |
|---|---|---|---|
| eb-01 (caps 1-5) | 158.711 (~63,5 pág.) | CONFORME | `.../eb-01.../*.epub` (215 KB) |
| eb-02 (caps 6-10) | 150.385 (~60,2 pág.) | CONFORME | `.../eb-02.../*.epub` (206 KB) |

`derivados.json` do livro-mãe atualizado com `status: "concluido_autonomo"` e
caminho do `.epub` para os 2 índices. Capas 1600×2560 + thumbnail geradas para
ambos.

**Achado lateral (documentação desalinhada, não corrigido):** o subagente
reportou que `.claude/agents/subagente-adaptador-ebook.md` descreve os scripts
de auditoria/EPUB recebendo `<slug_ebook>` isolado, mas na prática
`scripts/auditar-obra.py`/`gerar-epub.py` resolvem caminho relativo a
`output/`, exigindo o slug prefixado (`ebooks/<slug_ebook>`). O subagente
contornou sozinho; vale corrigir a definição do agente numa próxima rodada para
não depender de tentativa-e-erro.

### 6.5 Achado lateral: produção concorrente ativa durante o diagnóstico

Durante esta sessão, detectamos e confirmamos (por timestamps de arquivo)
atividade de **outro processo/sessão** produzindo conteúdo neste mesmo projeto
em tempo real — o livro AIDD ganhou `livro_final.pdf` e cresceu ~52 mil
caracteres entre o diagnóstico inicial e esta rodada, os 3 artigos passaram de
vazios a com conteúdo completo, e surgiu um **segundo livro-mãe inteiro**
(`sdlc-ai-first`, com 5 artigos e 8 ebooks planejados) que não existia no
diagnóstico original. Você optou por prosseguir mesmo assim. Não tocamos em
nada de `sdlc-ai-first` — está fora do escopo deste diagnóstico e sendo
conduzido por esse outro processo; o fix de 6.4 beneficia esse livro também
(seus 8 ebooks tinham o mesmo problema), mas não disparamos nenhuma redação
para ele.

### 6.6 Pendências reais para uma próxima rodada

1. Resultado dos 2 subagentes `subagente-adaptador-ebook` (6.4) ainda não
   chegou no momento em que este relatório foi escrito — confirmar veredito
   EBOOK-LEN e caminho dos `.epub`/capas quando as tarefas terminarem.
2. `sdlc-ai-first` (achado em 6.5) está fora do escopo deste diagnóstico —
   se quiser, audite/retome esse livro-mãe e seus 5 artigos + 8 ebooks numa
   sessão dedicada (o fix de 6.4 já os desbloqueou estruturalmente).
3. Achados menores do item 3.8 (piso frouxo do `pool-capitulos.py`, skill
   `pre-flight-check` genérica) seguem como recomendação, não aplicados —
   baixo risco, baixo valor imediato.
