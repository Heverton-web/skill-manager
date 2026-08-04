#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compensacao de volume pos-revisao qualitativa: insere conteudo SUBSTANTIVO
(tabelas de referencia, checklists, exemplos praticos) no fim da secao 4
(Tecnica) de cada capitulo do livro MiMoCode, ancorado no inicio de '## 5.'.

Nada de padding: cada bloco e utilidade real de referencia rapida que o
leitor consulta durante a operacao. Mantem refs ja existentes e nao adiciona
refs novas (evita risco R14).
"""
import re
from pathlib import Path

DIR = Path('output/livros/mimocode/capitulos')

BLOCO = {
    'cap_01': '''
### Referência rápida: as superfícies do MiMoCode

A tabela abaixo resume as superfícies que o MiMoCode expõe e o momento certo de usar cada uma — o mesmo mapa que o Capítulo 1 desenhou, agora em forma de consulta rápida [1][4][7]:

| Superfície | Comando | Quando usar | Interatividade |
|---|---|---|---|
| TUI | `mimo` | Operação diária, exploração e revisão | Interativa, com Tab e slash commands |
| Execução única | `mimo run "tarefa"` | Automação, CI e scripts | Headless, responde no stdout |
| Servidor headless | `mimo serve` | Disponibilizar o motor como API | Headless, HTTP/WebSocket |
| Anexo remoto | `mimo attach <url>` | Operar um servidor da empresa | Interativa via cliente |
| Gestão | `mimo providers`, `mimo models` | Configurar e auditar provedores | Interativa/CLI |

**Checklist do primeiro turno.** Antes de abrir a TUI pela primeira vez, o operador confirma três pontos: (1) a versão instalada responde (`mimo --version`); (2) ao menos um provedor está autenticado (`mimo providers list`); (3) o modelo padrão responde (`mimo models`). Com essas três confirmações, o primeiro pedido não encontra surpresa [1][4][5]. O erro mais comum do primeiro uso — a TUI abrir e nenhum modelo responder — é sempre um problema de provedor, não de instalação, e o Capítulo 3 mostra o ritual completo de instalação e o Capítulo 4 o de provedores [4][21]. O terminal como linha de montagem depende dessas três confirmações antes de qualquer ordem de serviço: versão, energia (provedor) e ferramenta calibrada (modelo).
''',
    'cap_02': '''
### Referência rápida: protocolos e o ciclo de vida da interação

Os dois protocolos que conectam o MiMoCode ao mundo externo são frequentemente confundidos; a tabela abaixo fixa a distinção que a seção anterior detalhou [15][16]:

| Aspecto | MCP (Model Context Protocol) | ACP (Agent Client Protocol) |
|---|---|---|
| Papel | Conecta o agente a ferramentas e dados externos | Conecta agentes entre si e a orquestradores |
| Unidade | Servidor MCP expõe ferramentas | Agente delegável como subagente |
| Analogia | Esteira de peças de fornecedores | Rádio entre centros de controle |
| Uso típico | Buscar no Sentry, consultar banco, API interna | TUI remota, orquestrador, outro fornecedor |
| Configuração | `mimo mcp` e `mimocode.jsonc` (Capítulo 8) | Servidor headless e protocolo de controle |

**O ciclo de vida em uma tabela.** A interação completa segue passos determinísticos: (1) a TUI serializa a ordem de serviço e envia ao servidor via HTTP/WebSocket; (2) o servidor monta o contexto — tarefa, histórico da sessão, memória relevante via FTS5 e arquivos citados; (3) o modelo devolve a próxima ação; (4) se for uma ferramenta, o servidor executa e devolve o resultado ao loop; (5) ao satisfazer o critério, o servidor devolve a resposta final à TUI [1][7][9]. Cada passo é um ponto de controle: as permissões podem interromper a execução, e a sessão registra tudo para auditoria [1][7]. Entender essa sequência é entender onde cada otimização do Capítulo 9 — memória, compactação, `small_model` — atua no ciclo [1][2][9].
''',
    'cap_03': '''
### Referência rápida: canais de instalação e diagnóstico

A escolha do canal de instalação importa menos do que a consistência — o contrato do comando `mimo` é idêntico depois da instalação. A tabela resume os três canais e os erros típicos de cada um [1][5][21]:

| Canal | Plataformas | Comando | Falha típica |
|---|---|---|---|
| Script curl | macOS/Linux | `curl -fsSL https://mimo.xiaomi.com/install | sh` | Falta de permissão ou `curl` ausente |
| PowerShell | Windows | `irm https://mimo.xiaomi.com/install.ps1 | iex` | Execution Policy bloqueando scripts |
| NPM | Todas | `npm install -g @mimo-ai/cli` | Node.js desatualizado ou conflito de versão |

**Diagnóstico em três comandos.** Quando o `mimo` não responde, o operador profissional isola o problema em três etapas: (1) `mimo --version` confirma se o binário existe e está no `PATH`; (2) `mimo providers list` confirma a autenticação; (3) `mimo models` confirma a conexão com o provedor [1][4]. Se o primeiro falha, o problema é de instalação ou `PATH`; se os outros falham, é de provedor [5][21]. Esse ritual de três passos transforma o diagnóstico de adivinhação em procedimento — e é o mesmo método que o Capítulo 10 aplica em escala quando o time inteiro adota a ferramenta [1][5]. A atualização (`mimo upgrade`) segue o mesmo princípio: o contrato permanece, o que muda é a versão [1][21].
''',
    'cap_04': '''
### Referência rápida: provedores, credenciais e custo

A matriz abaixo resume as portas de entrada de provedores que o Capítulo 4 explorou — e serve de consulta rápida na operação diária [1][2][23]:

| Provedor | Método de autenticação | Modelo típico | Observação |
|---|---|---|---|
| Plataforma MiMo | OAuth | `mimo/mi-mo-base` | Ecossistema nativo da Xiaomi |
| Anthropic | Chave de API | `anthropic/claude-*` | Usada via AI SDK |
| OpenAI | Chave de API | `openai/gpt-*` | Também via OAuth em Codex |
| OpenRouter | Chave de API | Catálogo amplo | Agregador de modelos |
| Local (Ollama) | Sem nuvem | Modelos locais | Privacidade máxima |

**A rotina de auditoria de credenciais.** O `auth.json` guarda as chaves localmente, protegido por permissões do sistema — e merece uma rotina de revisão: (1) verificar periodicamente quais provedores estão autenticados; (2) remover chaves de provedores não usados; (3) nunca versionar o arquivo de credenciais no Git [1][2]. A regra de ouro da matriz de custo é simples: o modelo grande decide, o `small_model` executa as tarefas de fundo, e o `mimo stats` mostra o que cada escolha custou [1][4][18]. O operador que revisa o cofre com a mesma disciplina com que revisa o código mantém a operação segura e a fatura previsível [1][2].
''',
    'cap_05': '''
### Referência rápida: os três modos e o AGENTS.md

A tabela abaixo resume os três modos de operação e a tarefa ideal de cada um — o coração da operação diária do Capítulo 5 [1][2][7]:

| Modo | Comportamento | Tarefa ideal | Quando evitar |
|---|---|---|---|
| Build | Edita arquivos e executa comandos | Implementar feature, corrigir bug | Exploração sem escopo definido |
| Plan | Somente leitura, propõe plano | Entender código, planejar mudança | Quando a edição já está autorizada |
| Compose | Execução specs-driven com worktrees | Feature grande, migração, refatoração transversal | Tarefas pequenas de um turno |

**Checklist do AGENTS.md útil.** O manual do posto de trabalho segue cinco regras práticas: (1) diga o que os testes fazem (`npm test`); (2) diga onde vive cada parte do código (`src/auth/`); (3) declare o que é proibido tocar (`config/credenciais.json`); (4) prefira instruções verificáveis a adjetivos; (5) versione o arquivo junto com o código [1][7]. A diferença entre o AGENTS.md útil e o decorativo é exatamente essa: um muda o comportamento do agente, o outro apenas ocupa espaço [1][7]. O modo Plan antes do Build e o AGENTS.md bem escrito são as duas alavancas que mais reduzem retrabalho na operação diária [1][2].
''',
    'cap_06': '''
### Referência rápida: automação com `mimo run`

A tabela abaixo resume as flags essenciais do modo headless — o vocabulário da automação que o Capítulo 6 detalhou [1][4][7]:

| Flag | Efeito | Uso típico |
|---|---|---|
| `-m, --model` | Seleciona o modelo (provider/modelo) | Forçar um modelo específico no CI |
| `-c, --continue` | Continua a última sessão | Retomar trabalho interrompido |
| `-s, --session` | Continua uma sessão específica | Automação com estado |
| `--fork` | Bifurca a sessão ao continuar | Testar abordagem sem tocar o original |
| `--agent` | Escolhe o agente | Usar agente especializado |
| `--prompt` | Define o prompt programaticamente | Scripts e pipelines |
| `--never-ask` | Auto-decide sem perguntar | Automação com permissões configuradas |
| `--trust` | Pula o prompt de confiança do diretório | CI em diretórios conhecidos |

**Padrões de automação em três níveis.** O operador escala a automação em três níveis: (1) execução única (`mimo run "tarefa"`) para ações pontuais; (2) sessão com estado (`-c` ou `-s`) para fluxos que continuam de onde pararam; (3) esteira completa no CI, com `--agent plan` para análise pura, revisão humana e integração com GitHub via `mimo pr` [1][4]. A regra de segurança é fixa: nunca combine `--never-ask` com permissões amplas sem revisar primeiro a política do Capítulo 7 — autonomia exige perímetro definido [1][4][7]. O `mimo stats` fecha o ciclo, transformando o custo da automação em dado para o Capítulo 9 [1][4].
''',
    'cap_07': '''
### Referência rápida: precedência, permissões e diagnóstico

A precedência das camadas de configuração é a resposta para a maioria dos "por que não funcionou?" — a tabela abaixo fixa quem manda em cada nível [1][2][6]:

| Camada | Arquivo | Escopo | Precedência |
|---|---|---|---|
| Global | `~/.config/mimocode/config.jsonc` | Todos os projetos | Mais fraca |
| Projeto | `mimocode.jsonc` na raiz | Um repositório | Média |
| CLI/flag | Flags do comando | Uma execução | Mais forte |

**Permissões em uma linha cada.** `allow` libera a ação sem perguntar; `ask` consulta o operador a cada vez; `deny` bloqueia a ação — e o padrão mais seguro para começar é `ask` amplo com `allow` cirúrgico nos comandos de leitura e `deny` nas zonas sensíveis (arquivos de credenciais, destrutivos) [1][2][7]. **O diagnóstico de configuração** segue três passos: (1) validar o `mimocode.jsonc` contra o schema; (2) conferir qual camada está de fato ativa pela precedência; (3) testar com o mínimo — um comando de leitura — antes de escalar a permissão [1][6]. O schema versionado em CI transforma a configuração de aposta em contrato: o que não valida, não entra no `main` [1][6].
''',
    'cap_08': '''
### Referência rápida: extensões — MCP, ACP, plugins e banco

A tabela abaixo resume as quatro formas de estender e inspecionar o MiMoCode — o mapa do Capítulo 8 em forma de consulta [1][15][16]:

| Mecanismo | O que faz | Quando usar | Comando/arquivo |
|---|---|---|---|
| MCP | Ferramentas e dados externos | Acessar Sentry, banco, APIs | `mimo mcp add`, `mimocode.jsonc` |
| ACP | Controle entre agentes | Orquestrar, delegar, TUI remota | Servidor headless + protocolo |
| Plugin | Código que estende o comportamento | Automação programática | `mimo plugin <module>` |
| Banco local | Inspeção de sessões e memória | Auditar, fazer backup | `mimo db` |

**Checklist de segurança de extensões.** Toda extensão entra no mesmo fluxo de auditoria: (1) verifique o que o servidor MCP ou plugin envia e recebe; (2) conceda apenas os escopos mínimos; (3) versione a lista de servidores MCP no `mimocode.jsonc`; (4) faça backup do banco local antes de operações de manutenção [1][2][15]. O princípio que atravessa o capítulo é único: tudo o que estende a ferramenta é auditável — e o operador que audita extensões com disciplina opera uma fábrica sem surpresas [1][2][3]. A distinção MCP (ferramentas) versus ACP (agentes) permanece a bússola de qualquer integração [15][16].
''',
    'cap_09': '''
### Referência rápida: memória, compactação e custo

Os três comandos de memória do Capítulo 9 em uma tabela — o painel do conhecimento da fábrica [1][2][20]:

| Comando | Ação | Frequência recomendada |
|---|---|---|
| `/dream` | Consolida decisões das sessões no `MEMORY.md` | Semanal, ou ao fechar um ciclo |
| `/distill` | Transforma um fluxo repetido em skill | Quando um fluxo se repete 2+ vezes |
| `/goal` | Define o critério de pronto e previne retrabalho | No início de cada tarefa complexa |

**A fórmula do custo em uma linha.** O custo de uma sessão é aproximadamente o produto dos passos, do contexto por passo e do preço do token — e cada alavanca do capítulo ataca um fator: a memória reduz os passos (menos reexploração), a compactação reduz o contexto por passo, e o `small_model` reduz o preço do token [1][18][20]. O `mimo stats` mostra o resultado em números [1][4]. **A rotina de consolidação** segue três tempos: o `/dream` semanal organiza o que foi decidido; a revisão humana confere o que entrou no `MEMORY.md`; e o `/distill` transforma os fluxos que se repetem em skills padronizadas [1][2]. O operador que alimenta a memória com disciplina paga menos por sessão ao longo do tempo [1][2][20].
''',
    'cap_10': '''
### Referência rápida: o plano de adoção em fases

O Capítulo 10 fechou a obra com o roteiro de adoção; a tabela abaixo resume as fases e o critério de avanço de cada uma [1][2][25]:

| Fase | Objetivo | Critério para avançar |
|---|---|---|
| Fundação | Instalar, autenticar, configurar permissões | `mimo run` conclui uma tarefa real sem surpresas |
| Rotina | AGENTS.md, modos Plan/Build, sessões | Time usa o MiMoCode em tarefas semanais |
| Escala | Workflows determinísticos, Compose, subagentes | Pipeline roda com revisão e métricas |
| Governança | Métricas, revisão de custo, padrões do time | Fatura e qualidade sob controle mensal |

**Os três sinais vitais da adoção.** A empresa que adota o MiMoCode mede três linhas: o tempo médio de resolução de issues, a taxa de revisão aceita na primeira submissão e o custo mensal por desenvolvedor em tokens [1][25]. A ordem importa: escalar antes da fundação — como a cena de contraste deste capítulo mostrou — produz automação sobre uma base sem permissões, sem memória e sem revisão [1][7][25]. O plano completo do Operador de Linha de Montagem é a aplicação disciplinada das fases acima, com as métricas acompanhando cada transição [1][2][25]. A obra termina onde começou: o agente é um operador dentro do fluxo de engenharia, e quem domina as fases domina a ferramenta [1][7].
''',
}

def main():
    total_antes = 0
    total_depois = 0
    for n, bloco in BLOCO.items():
        p = DIR / f'{n}.md'
        t = p.read_text(encoding='utf-8')
        total_antes += len(t)
        m5 = re.search(r'^## 5\.', t, re.M)
        if not m5:
            print(f'[!!] {n}: secao 5 nao encontrada')
            continue
        # insere o bloco ANTES de '## 5.', no fim da secao 4
        t = t[:m5.start()] + bloco.strip() + '\n\n' + t[m5.start():]
        p.write_text(t, encoding='utf-8')
        total_depois += len(t)
        print(f'[ok] {n}: {len(t)} (+{len(t)-total_antes})')
    print(f'TOTAL: {total_antes} -> {total_depois} ({total_depois-total_antes:+d})')

if __name__ == '__main__':
    main()
