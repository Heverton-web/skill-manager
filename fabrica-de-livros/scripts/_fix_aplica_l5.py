# -*- coding: utf-8 -*-
"""Insere a secao ## 5. Aplica nos caps 7-10 do Livro 5."""
from pathlib import Path

SLUG = "livros/claude-md-agents-md-e-rules-engenharia-da-memoria-e-das-regras-do-projeto"

APLICA = {
    "07": (
        "## 5. Aplica\n\n"
        "### 5.1 Onde Isso Vive no Mundo Real\n\n"
        "As regras condicionais estao em todo fluxo de desenvolvimento agentico em 2026 [6]. Cursor carrega `.cursor/rules/` por glob [6]. Claude Code usa regras por diretorio e subagente [1]. O padrao AGENTS.md usa aninhamento por diretorio [3][9]. O engenheiro que domina o principio da condicionalidade migra entre todas as implementacoes [6].\n\n"
        "### 5.2 O Erro Comum do Iniciante\n\n"
        "O erro mais comum e o glob generoso [6]: `**/*.{ts,tsx,js,jsx}` em uma regra de componentes dispara em modulos de infraestrutura e API [6]. O antídoto e o escopo estrito: `src/components/**`, alargado apenas com evidencia [6]. Outro erro classico e o alwaysApply descontrolado, que recria o problema do arquivo monolitico [6].\n\n"
        "### 5.3 O Padrao Profissional em 2026\n\n"
        "O padrao profissional trata as regras como codigo [6]: frontmatter valido, globs testados, auditoria trimestral e teste de adesao no CI (Secao 7.11) [6]. O resultado e um diretorio de regras enxuto, escopado e fiel a pratica [6]."
    ),
    "08": (
        "## 5. Aplica\n\n"
        "### 5.1 Onde Isso Vive no Mundo Real\n\n"
        "A cascata de instrucoes vive em todo monorepo maduro em 2026 [1][9]. O AGENTS.md aninhado governa por fronteira [3][9]. O CLAUDE.md por diretorio e o @import formam o grafo de memoria [1]. As regras condicionais escopam o detalhe [6]. A combinacao das camadas e a pratica diaria do engenheiro de memoria [1][9].\n\n"
        "### 5.2 O Erro Comum do Iniciante\n\n"
        "O erro mais comum e a constituicao detalhista [9]: o AGENTS.md raiz tenta cobrir cada territorio e incha [9]. O antidoto e a particao — cada territorio com suas leis locais e o detalhe fora da raiz (Secao 8.6) [1][9]. Outro erro classico e a duplicacao silenciosa entre camadas, que drift em direcoes opostas (Secao 8.7) [1][9].\n\n"
        "### 5.3 O Padrao Profissional em 2026\n\n"
        "O padrao profissional desenha a cascata como sistema [1][7][9]: constituicao curta, leis locais por territorio, dono unico por assunto e o teste da cascata no CI (Secao 8.8) [1][9]. O resultado e um monorepo onde qualquer agente recebe as instrucoes certas no momento certo [1][7][9]."
    ),
    "09": (
        "## 5. Aplica\n\n"
        "### 5.1 Onde Isso Vive no Mundo Real\n\n"
        "O combate ao drift vive no pipeline de qualidade de times maduros [1][7]. O linter de instrucoes valida a estrutura (Secao 9.8); o dashboard de frescor tria os arquivos obsoletos (Secao 9.6); e a revisao trimestral faz a auditoria profunda (Secao 9.15) [1][7]. A combinacao e o pipeline anti-drift em producao [1][7].\n\n"
        "### 5.2 O Erro Comum do Iniciante\n\n"
        "O erro mais comum e medir sem corrigir [1][7]: o dashboard acusa o drift, mas ninguem prioriza a correcao [1][7]. O antídoto e a fila de priorizacao por impacto (Secao 9.21) [1][7]. Outro erro classico e tratar o anti-drift como campanha periodica em vez de ciclo continuo (Secao 9.22) [1][7].\n\n"
        "### 5.3 O Padrao Profissional em 2026\n\n"
        "O padrao profissional trata o drift como divida tecnica de conhecimento [1][7]: medida, priorizada e paga no backlog (Secao 9.14) [1][7]. A cultura de transparencia (Secao 9.16) sustenta a pratica, e o pipeline (Secao 9.8) detecta antes que a regra morta contamine a confianca no contrato (Secao 9.3) [1][7]."
    ),
    "10": (
        "## 5. Aplica\n\n"
        "### 5.1 Onde Isso Vive no Mundo Real\n\n"
        "A engenharia da memoria de projeto vive na pratica de organizacoes maduras [1][7]. O engenheiro de memoria arquiteta a cascata, governa o padrao central e opera o pipeline anti-drift (Secao 10.15) [1][7]. A disciplina e a infraestrutura invisivel do desenvolvimento agentico (Secao 3.1) [1][7].\n\n"
        "### 5.2 O Erro Comum do Iniciante\n\n"
        "O erro mais comum e tentar construir tudo de uma vez [1][7]: a cascata completa, o padrao organizacional e a governanca na primeira semana [1][7]. O antídoto e o ciclo de quatro semanas por territorio (Secao 10.12): observe, escreva, neutralize e meca [1][7]. Outro erro classico e escrever a memoria a partir da imaginacao, nao da observacao (Secao 10.3) [1][7].\n\n"
        "### 5.3 O Padrao Profissional em 2026\n\n"
        "O padrao profissional trata a memoria como sistema sociotecnico [1][7][9]: arquivos mais cultura, contrato mais pratica, medicao mais revisao (Secao 10.1) [1][7][9]. O resultado e o entendimento compartilhado — o objetivo central da disciplina (Secao 10.14) [1][7][9]."
    ),
}

for cap, texto in APLICA.items():
    p = Path("output") / SLUG / "capitulos" / f"cap_{cap}.md"
    t = p.read_text(encoding="utf-8")
    conc = "## 6. Conclusao"
    if conc not in t:
        print(f"cap_{cap}: conclusao nao encontrada")
        continue
    t = t.replace(conc, texto + "\n\n" + conc, 1)
    p.write_text(t, encoding="utf-8")
    print(f"cap_{cap} OK - {len(t)} chars")
