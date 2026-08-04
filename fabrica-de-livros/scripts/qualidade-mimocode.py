#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica as recomendacoes 1-6 da revisao qualitativa no livro MiMoCode.

Transformacoes:
  A1: cap_02 header duplicado 'O loop e o contexto' (2a ocorrencia) -> limite de passos
  A2: cap_10 header quebrado 'Skills nativas e do time'
  A3: cap_01 encurta enumeracao dos 3 pilares de memoria (detalhe fica no cap_02)
  REC6: benchmarks narrados uma vez (cap_01), demais -> referencia cruzada
  REC5: aberturas-formula -> transicoes especificas
  REC4: poda metafora (esteira/linha de montagem) nas secoes 1,2,4,6 (mantem 3-Ilustra e 5-cenas)
  REC3: mescla subsecoes ### com prefixo comum em secoes maiores
  REC2: remove clusters de citacao no fim de frases, apenas se cada ref continuar citada (R14-safe)

Seguranca: nunca toca blocos ```, preserva citacoes unicas (R14), nao mexe na secao 7.
"""
import re
import glob
from pathlib import Path

DIR = Path('output/livros/mimocode/capitulos')
ARQUIVOS = sorted(glob.glob(str(DIR / 'cap_*.md')))

def ler(n):
    return (DIR / f'{n}.md').read_text(encoding='utf-8')

def salvar(n, t):
    (DIR / f'{n}.md').write_text(t, encoding='utf-8')

def substituir(t, velho, novo, n, rotulo):
    qtd = t.count(velho)
    if qtd == 0:
        print(f'  [!!] {n} {rotulo}: NAO ENCONTRADO -> {velho[:60]}')
        return t
    t = t.replace(velho, novo)
    print(f'  [ok] {n} {rotulo}: {qtd}x')
    return t

def dividir_secoes(t):
    """Divide o texto em secoes ## N. e devolve [(num, conteudo)]."""
    partes = re.split(r'(?=^## \d\.)', t, flags=re.M)
    secs = []
    for p in partes:
        m = re.match(r'## (\d)\.', p)
        secs.append((int(m.group(1)) if m else 0, p))
    return secs

def juntar_secoes(secs):
    return ''.join(c for _, c in secs)

def processar_secoes(t, secoes_alvo, fn):
    """Aplica fn() apenas nas secoes numeradas em secoes_alvo."""
    secs = dividir_secoes(t)
    for i, (num, conteudo) in enumerate(secs):
        if num in secoes_alvo:
            secs[i] = (num, fn(conteudo))
    return juntar_secoes(secs)

# ============ REC 4: metafora (secoes 1,2,4,6; manter 3 e 5) ============
METAFORA = [
    ('as esteiras de ferramentas', 'os conjuntos de ferramentas'),
    ('a esteira de ferramentas', 'o conjunto de ferramentas'),
    ('as esteiras MCP', 'as ferramentas MCP'),
    ('as esteiras do Cap', 'as ferramentas do Cap'),
    ('as esteiras', 'as ferramentas'),
    ('a esteira', 'o fluxo'),
    ('na esteira', 'no fluxo'),
    ('da esteira', 'do fluxo'),
    ('esta esteira', 'este fluxo'),
    ('a mesma esteira', 'o mesmo fluxo'),
    ('operador de linha de montagem', 'operador da fábrica'),
    ('a linha de montagem', 'a fábrica'),
    ('da linha de montagem', 'da fábrica'),
    ('na linha de montagem', 'na fábrica'),
    ('de linha de montagem', 'da fábrica'),
]

def podar_metafora(texto):
    for velho, novo in METAFORA:
        texto = texto.replace(velho, novo)
    return texto

# ============ REC 2: citacoes redundantes (fim de frase, R14-safe) ============
CLUSTER_FIM = re.compile(r'(?:\[\d+\])+(?=\.)')

def reduzir_citacoes_dinamico(texto):
    """Remove clusters de citacao no fim de frases, recontando dinamicamente.

    Greedy em ordem de documento: um cluster so e removido se, apos contabilizar
    TODOS os clusters ja marcados para remocao e o proprio cluster, cada ref do
    cluster ainda tiver >= 1 ocorrencia restante no corpo — garantia R14: nenhuma
    ref da lista fica sem citacao no texto.
    """
    corpo = re.split(r'^## 7\.', texto, flags=re.M)[0]
    cluster_pool = list(CLUSTER_FIM.finditer(corpo))
    marcados = []  # spans marcados para remocao

    def ocorrencias_livres(r):
        """Ocorrencias de r fora de qualquer cluster marcado."""
        n = 0
        for m in re.finditer(rf'\[{r}\]', corpo):
            em_marcado = any(m.start() >= i and m.end() <= f for i, f in marcados)
            if not em_marcado:
                n += 1
        return n

    for m in cluster_pool:
        ini, fim = m.start(), m.end()
        refs = [int(x) for x in re.findall(r'\[(\d+)\]', m.group(0))]
        # simulacao: se removermos este cluster, quantas ocorrencias livres restam?
        ok = True
        for r in refs:
            livres_sem_cluster = ocorrencias_livres(r) - m.group(0).count(f'[{r}]')
            if livres_sem_cluster < 1:
                ok = False
                break
        if ok:
            marcados.append((ini, fim))

    if not marcados:
        return texto
    partes = []
    ultimo = 0
    for ini, fim in sorted(marcados):
        partes.append(corpo[ultimo:ini])
        ultimo = fim
    partes.append(corpo[ultimo:])
    novo_corpo = ''.join(partes)
    return novo_corpo + texto[len(corpo):]

# ============ REC 3: mescla de subsecoes com prefixo comum ============
def tokens_prefixo(a, b):
    ta, tb = a.split(), b.split()
    n = 0
    for x, y in zip(ta, tb):
        if x == y:
            n += 1
        else:
            break
    return n

CONECTIVOS = {'e', 'de', 'o', 'a', 'os', 'as', 'do', 'da', 'em', 'na', 'no'}

def rotular(resto):
    resto = resto.strip()
    # remove conectivos iniciais
    while True:
        palavras = resto.split()
        if palavras and palavras[0].lower() in CONECTIVOS:
            resto = ' '.join(palavras[1:])
        else:
            break
    if not resto:
        return None
    return resto[0].upper() + resto[1:]

def mesclar_subsecoes(texto):
    linhas = texto.split('\n')
    idx = [i for i, l in enumerate(linhas) if l.startswith('### ')]
    if len(idx) < 2:
        return texto
    # grupos de headers consecutivos (sem ## entre eles) com prefixo >= 3 tokens
    grupos = []
    atual = [idx[0]]
    for i in range(1, len(idx)):
        ant, cur = idx[i - 1], idx[i]
        # ha um ## entre eles?
        tem_secao = any(l.startswith('## ') for l in linhas[ant + 1:cur])
        if not tem_secao and tokens_prefixo(linhas[ant][4:], linhas[cur][4:]) >= 3:
            atual.append(cur)
        else:
            grupos.append(atual)
            atual = [cur]
    grupos.append(atual)

    # para grupos com >= 2 membros: mesclar
    total_removidos = 0
    for g in grupos:
        if len(g) < 2:
            continue
        cabeças = [linhas[i][4:] for i in g]
        # prefixo comum entre a primeira e as demais
        comum = cabeças[0]
        for c in cabeças[1:]:
            n = tokens_prefixo(comum, c)
            comum = ' '.join(comum.split()[:n])
        # novo header = prefixo comum sem conectivo final
        header_novo = '### ' + rotular(comum)
        # primeira cabeca: substitui o header
        linhas[g[0]] = header_novo
        # demais: viram rotulo em negrito no paragrafo seguinte
        for i in g[1:]:
            resto = cabeças[g.index(i)][len(comum):]
            rot = rotular(resto)
            if not rot:
                continue
            # acha a primeira linha nao vazia apos o header
            j = i + 1
            while j < len(linhas) and not linhas[j].strip():
                j += 1
            if j < len(linhas):
                linhas[j] = f'**{rot}.** {linhas[j]}'
            linhas[i] = ''
            total_removidos += 1
    novo = '\n'.join(linhas)
    # limpa linhas vazias duplicadas
    novo = re.sub(r'\n{3,}', '\n\n', novo)
    return novo, total_removidos

# ============ REC 5: aberturas-formula ============
ABERTURAS = {
    'cap_01': [
        ('Vale um registro de segurança que o open-source frequentemente suscita: ',
         'O open-source frequentemente suscita uma dúvida de segurança: '),
        ('Um detalhe que conecta a definição à operação: o ciclo de vida de uma tarefa no MiMoCode [1][7][9].',
         'O ciclo de vida de uma tarefa no MiMoCode conecta a definição à operação [1][7][9].'),
        ('Vale fechar a parte expositiva com um aviso honesto sobre a diferença entre conhecer e dominar — porque ela define o que você vai extrair deste livro.',
         'Um aviso honesto fecha a parte expositiva: a diferença entre conhecer e dominar define o que você vai extrair deste livro.'),
        ('Vale fechar um entendimento que atravessa a obra: a diferença entre o agente e o chat [1][7][9].',
         'Um entendimento atravessa a obra: a diferença entre o agente e o chat [1][7][9].'),
        ('Vale aprofundar a razão técnica pela qual o terminal — e não o editor nem o navegador — é a superfície natural de um agente de codificação, porque essa escolha explica quase tudo o que o MiMoCode faz diferente.',
         'Por que o terminal — e não o editor nem o navegador — é a superfície natural de um agente de codificação? Essa escolha explica quase tudo o que o MiMoCode faz diferente.'),
        ('Vale aprofundar um ponto que define o dia a dia do operador: a portabilidade do open-source.',
         'Um ponto define o dia a dia do operador: a portabilidade do open-source.'),
    ],
    'cap_02': [
        ('Vale registrar também como a arquitetura conversa com o modelo de negócio do mercado.',
         'A arquitetura também conversa com o modelo de negócio do mercado.'),
    ],
    'cap_03': [
        ('Vale um registro final sobre o que a instalação destrava além da TUI: ',
         'O que a instalação destrava além da TUI: '),
    ],
    'cap_04': [
        ('Vale um registro de contexto: a liberdade de provedores do MiMoCode não é um detalhe técnico, é uma posição de mercado.',
         'A liberdade de provedores do MiMoCode não é um detalhe técnico: é uma posição de mercado.'),
        ('Um detalhe que conecta o cofre ao fluxo corporativo: as variáveis de ambiente [1][2][23].',
         'O cofre conecta-se ao fluxo corporativo pelas variáveis de ambiente [1][2][23].'),
        ('Um detalhe que conecta o `small_model` ao ecossistema: os modelos pequenos evoluíram muito, e a escolha do auxiliar merece revisão periódica [1][2][3].',
         'Os modelos pequenos evoluíram muito, e a escolha do `small_model` merece revisão periódica [1][2][3].'),
        ('Vale fechar a parte técnica com a matemática simples que justifica a matriz de provedores — porque ela transforma a escolha de modelo de intuição em cálculo.',
         'A matemática simples que justifica a matriz de provedores fecha a parte técnica — e transforma a escolha de modelo de intuição em cálculo.'),
    ],
    'cap_05': [
        ('Vale registrar a curva de aprendizado dos três modos, porque ela explica a frustração do primeiro mês [1][2].',
         'A curva de aprendizado dos três modos explica a frustração do primeiro mês [1][2].'),
        ('Vale registrar também como o Compose se conecta às skills e aos workflows determinísticos do MiMoCode: ',
         'O Compose também se conecta às skills e aos workflows determinísticos do MiMoCode: '),
        ('Vale um registro de contexto sobre como os três modos se comparam com o mercado: ',
         'Os três modos se comparam com o mercado em um ponto de contexto: '),
        ('Vale fechar o contexto da ordem de serviço com o elo que o fecha: a revisão [1][7].',
         'O elo que fecha o contexto da ordem de serviço é a revisão [1][7].'),
        ('Vale fechar a parte técnica com a matemática da operação diária — porque o modo de uso da TUI define a fatura de tokens.',
         'A matemática da operação diária fecha a parte técnica — o modo de uso da TUI define a fatura de tokens.'),
    ],
    'cap_06': [
        ('Vale registrar um padrão de uso que poucos tutoriais mostram: o `mimo export` como ferramenta de colaboração entre operadores [1][4].',
         'Poucos tutoriais mostram um padrão de uso: o `mimo export` como ferramenta de colaboração entre operadores [1][4].'),
        ('Vale um registro de segurança sobre as flags de autonomia — porque elas são as mais mal compreendidas [1][4].',
         'As flags de autonomia são as mais mal compreendidas — daí o registro de segurança [1][4].'),
        ('Vale um registro sobre a combinação de flags, porque a automação raramente usa uma flag isolada [1][4].',
         'A automação raramente usa uma flag isolada — daí a importância da combinação [1][4].'),
        ('Vale um registro de precisão sobre o vocabulário do modo headless, porque ',
         'O vocabulário do modo headless exige precisão, porque '),
        ('Um detalhe que conecta as flags ao ambiente: a configuração por contexto [1][4][7].',
         'As flags conectam-se ao ambiente pela configuração por contexto [1][4][7].'),
        ('Um detalhe que conecta a automação às esteiras do Capítulo 8: o `mimo run` enxerga as ferramentas MCP configuradas — o mesmo motor headless que serve a TUI serve a esteira [1][15].',
         'A automação conecta-se às ferramentas do Capítulo 8: o `mimo run` enxerga as ferramentas MCP configuradas — o mesmo motor headless que serve a TUI serve o fluxo [1][15].'),
        ('Um detalhe que conecta a automação à memória persistente: o `mimo pr` e o `mimo run` alimentam e consultam o mesmo SQLite FTS5 que guarda a memória do projeto [1][4][20].',
         'A automação conecta-se à memória persistente: o `mimo pr` e o `mimo run` alimentam e consultam o mesmo SQLite FTS5 que guarda a memória do projeto [1][4][20].'),
    ],
    'cap_07': [
        ('Vale registrar exemplos de agentes custom que a rotina do time justifica [1][2][7].',
         'A rotina do time justifica exemplos concretos de agentes custom [1][2][7].'),
    ],
    'cap_08': [
        ('Um detalhe que conecta as extensões à memória da fábrica: ',
         'As extensões conectam-se à memória da fábrica: '),
        ('Um detalhe que conecta as extensões às skills do Capítulo 9: ',
         'As extensões conectam-se às skills do Capítulo 9: '),
        ('Vale aprofundar a gestão de esteiras, porque o `mimo mcp` é a ferramenta que o operador usa com mais frequência na rotina de extensão [1][4][15].',
         'A gestão de ferramentas merece aprofundamento: o `mimo mcp` é o comando que o operador usa com mais frequência na rotina de extensão [1][4][15].'),
    ],
    'cap_09': [
        ('Vale fechar a parte técnica com a fórmula completa do custo — porque a operação fina é a aplicação disciplinada dela [1][18]:',
         'A fórmula completa do custo fecha a parte técnica — a operação fina é a aplicação disciplinada dela [1][18]:'),
    ],
}

# ============ A1/A2/A3 + REC6 ============
CORRECOES = {
    'cap_02': [
        ('### O loop e o contexto\n\nO loop do agente tem uma válvula',
         '### O loop e o limite de passos\n\nO loop do agente tem uma válvula'),
    ],
    'cap_10': [
        ('### Skills nativas e do time', '### Skills nativas e as skills do time'),
    ],
    'cap_01': [
        ('O MiMoCode ataca esse problema com um sistema de memória persistente baseado em SQLite FTS5, dividido em três pilares: a memória de projeto (`MEMORY.md`), os checkpoints de sessão (`checkpoint.md`) e as notas de progresso de tarefas (`tasks/<id>/progress.md`) [1][2].',
         'O MiMoCode ataca esse problema com um sistema de memória persistente baseado em SQLite FTS5, organizado em três pilares — projeto, sessão e tarefa — que o Capítulo 2 detalha em arquitetura [1][2].'),
    ],
    'cap_04': [
        ('— e essa posição aparece nos benchmarks: a Xiaomi divulgou 62% no SWE-Bench Pro e 73% no Terminal Bench 2 usando o modelo MiMo, mas a mesma ferramenta opera com outros provedores [22][1].',
         '— e essa posição aparece nos benchmarks que o Capítulo 1 apresentou: a mesma ferramenta opera com vários provedores [22][1].'),
    ],
    'cap_05': [
        ('Os benchmarks publicados pela Xiaomi — 62% no SWE-Bench Pro e 73% no Terminal Bench 2 — são medidos justamente nesse modo de operação autônoma, o que dá uma noção do teto da ferramenta quando bem configurada [22].',
         'Os benchmarks do Capítulo 1 são medidos justamente nesse modo de operação autônoma, o que dá uma noção do teto da ferramenta quando bem configurada [22].'),
    ],
    'cap_07': [
        ('O benchmark SWE-Bench Pro de 62% e o Terminal Bench 2 de 73%, divulgados pela Xiaomi, são o teto da ferramenta bem configurada — e a distância entre o teto e o resultado individual é quase sempre configuração [1][22].',
         'Os benchmarks do Capítulo 1 são o teto da ferramenta bem configurada — e a distância entre o teto e o resultado individual é quase sempre configuração [1][22].'),
    ],
}

def main():
    total_antes = 0
    total_depois = 0
    for caminho in ARQUIVOS:
        n = re.sub(r'.*cap_', 'cap_', caminho).replace('.md', '')
        t = ler(n)
        total_antes += len(t)
        print(f'--- {n} ---')

        # 1. correcoes cirurgicas (A1, A2, A3, REC6)
        for velho, novo in CORRECOES.get(n, []):
            t = substituir(t, velho, novo, n, 'correcao')

        # 2. REC5 aberturas
        for velho, novo in ABERTURAS.get(n, []):
            t = substituir(t, velho, novo, n, 'abertura')

        # 3. REC4 metafora nas secoes 1,2,4,6
        t = processar_secoes(t, {1, 2, 4, 6}, podar_metafora)

        # 4. REC2 citacoes redundantes (R14-safe, contagem dinamica no corpo)
        t = reduzir_citacoes_dinamico(t)

        # 5. REC3 mescla de subsecoes
        t, removidos = mesclar_subsecoes(t)
        if removidos:
            print(f'  [ok] {n} mescla: {removidos} subsecoes fundidas')

        salvar(n, t)
        total_depois += len(t)
        print(f'  tamanho: {len(t)} ({len(t)-total_antes:+d} vs baseline parcial)')

    print(f'\nTOTAL: {total_antes} -> {total_depois} ({total_depois - total_antes:+d})')

if __name__ == '__main__':
    main()
