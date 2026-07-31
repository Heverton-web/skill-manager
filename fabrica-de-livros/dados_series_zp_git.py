#!/usr/bin/env python3
"""
Dados da Serie ZP4 — Git e Controle de Versão: Do Zero ao Profissional (20 livros)
Jornada progressiva: Livro 1 = absoluto zero, Livro 20 = pronto para o mercado.
Cada livro tem 4 Partes e 16 Capitulos (EITA-V2).
Usado por gerar-livros-zp.py e compilar-para-pdf.py
"""

LIVROS_ZP_GIT = {
    # ═══════════ NIVEL 0-1: ZERO ABSOLUTO E FUNDAMENTOS ═══════════
    "ZP4-01-o-que-e-controle-de-versao": (
        "Controle de Versão: Conceitos e Fundamentos",
        "Controle de Versão: O Conceito que Todo Profissional Precisa Dominar",
        "Do zero: o que é, por que usar, histórico de mudanças e os sistemas modernos",
        "Todo código profissional vive em um sistema de controle de versão — e entender o conceito é o primeiro passo. Este livro explica o que é controle de versão, por que ele é obrigatório, o que é um histórico de mudanças, e como Git e GitHub se tornaram o padrão universal da indústria.",
        "Controle de versão não é um detalhe técnico: é a base do trabalho em equipe moderno. Quem entende o conceito — registrar, comparar e restaurar versões do trabalho — entra em qualquer projeto sabendo como o time colabora. É a fundação da sua jornada profissional.",
        "Controle de versão registra o histórico de mudanças de arquivos, permitindo comparar versões, reverter erros e colaborar sem sobrescrever o trabalho de outros [1]. Sistemas modernos (Git) são distribuídos: cada cópia do projeto contém o histórico completo. Plataformas como GitHub centralizam a colaboração: repositórios, issues, pull requests [2].\n\n**Por que importa?** Sem controle de versão, o trabalho vive em pastas 'final_v2', 'final_final' — um desastre para equipes. Com Git, cada mudança é rastreável, reversível e comentada. A habilidade é pré-requisito para qualquer vaga de desenvolvimento.\n\n**O que muda na prática:** Instale o Git, crie seu primeiro repositório e faça seu primeiro commit. Entender o ciclo básico (modificar → commit) é o ponto de partida para tudo que vem depois [3]."
    ),
    "ZP4-02-instalacao-e-configuracao-do-git": (
        "Instalação e Configuração do Git",
        "Instalação e Configuração: Primeiros Passos, git config e Ambiente de Trabalho",
        "Instalação, git config, identidade, editor, aliases e ambiente",
        "Git instalado e configurado é o ambiente de trabalho de todo desenvolvedor. Este livro guia a instalação em Windows, macOS e Linux, a configuração de identidade (git config), o editor padrão, aliases e o ambiente de terminal que torna o Git confortável no dia a dia.",
        "A configuração inicial do Git define a experiência de todos os projetos futuros: identidade correta nos commits, editor confortável e aliases que aceleram comandos. Um ambiente bem configurado é o primeiro sinal de um profissional organizado.",
        "A instalação do Git difere por sistema: Windows (Git for Windows, incluindo Git Bash), macOS (Homebrew ou instalador) e Linux (apt/dnf) [1]. A configuração essencial é a identidade: git config --global user.name 'Seu Nome' e user.email — gravada em cada commit. Outras: editor padrão (core.editor), diff tool e aliases (git config --global alias.co checkout) [2].\n\n**Por que importa?** Commits com identidade errada são um problema em projetos compartilhados. Aliases reduzem digitação e erros: co para checkout, br para branch. O Git Bash no Windows oferece o ambiente Unix que o Git espera.\n\n**O que muda na prática:** Configure identidade e aliases no primeiro dia, e verifique com git config --list. Um ambiente pronto evita fricção em todos os projetos da carreira [3]."
    ),
    "ZP4-03-fundamentos-init-add-commit-status": (
        "Fundamentos: init, add, commit e status",
        "Fundamentos do Git: init, add, commit, status e o Ciclo de Trabalho",
        "git init, git add, git commit, git status, staging area e boas mensagens",
        "O ciclo básico do Git é simples — e dominá-lo bem é o que sustenta tudo o que vem depois. Este livro ensina git init, git add, git commit, git status, a staging area (área de preparação) e as boas práticas de mensagens de commit que times profissionais seguem.",
        "O ciclo modify → stage → commit é executado centenas de vezes por dia por todo desenvolvedor. Entender a staging area — a área intermediária entre o arquivo modificado e o histórico — é o conceito que dá controle total sobre o que entra em cada commit.",
        "O fluxo básico: git init cria o repositório; git add <arquivo> move mudanças para a staging area; git commit -m 'mensagem' grava o snapshot no histórico; git status mostra o estado do working directory [1]. A staging area permite preparar commits seletivos — só o que faz sentido junto. Mensagens de commit descrevem o porquê da mudança, não o quê [2].\n\n**Por que importa?** Commits são a memória do projeto: quem leu o histórico entende a evolução. Mensagens ruins ('correção', 'update') destroem esse valor. A staging area separa o trabalho em andamento do que está pronto para entrar no histórico.\n\n**O que muda na prática:** Crie o hábito de git status antes de tudo, prepare commits pequenos e coesos com mensagens descritivas. Esse ciclo bem executado é a assinatura do profissional [3]."
    ),
    "ZP4-04-historico-log-diff-e-show": (
        "Histórico: log, diff e show",
        "Histórico do Git: log, diff, show e a Leitura do Passado do Projeto",
        "git log, git diff, git show, navegação no histórico e comparação de mudanças",
        "O histórico do Git é um livro sobre o projeto — e saber lê-lo é essencial. Este livro ensina git log (o histórico de commits), git diff (comparação de mudanças), git show (detalhes de um commit) e as formas de navegar e interpretar o passado do código.",
        "O histórico é onde o desenvolvedor encontra respostas: o que mudou, quando, por quem e por quê. Dominar log, diff e show permite auditar mudanças, investigar bugs e entender decisões antigas — habilidades que diferenciam o profissional no dia a dia e nas entrevistas.",
        "git log mostra o histórico: commits com hash, autor, data e mensagem [1]. Opções poderosas: --oneline (resumido), --graph (grafo de branches), --author, --since. git diff compara: working directory vs staging (git diff), staging vs último commit (git diff --staged). git show <hash> exibe o commit completo com suas mudanças [2].\n\n**Por que importa?** Investigar um bug é ler o diff do commit que o introduziu. Revisar código é ler diffs. O git blame atribui cada linha ao autor — útil para entender o porquê de uma decisão. O histórico bem lido acelera o onboarding em qualquer projeto.\n\n**O que muda na prática:** Explore o histórico de um projeto real: git log --oneline --graph, examine diffs de mudanças antigas e use git blame para entender linhas críticas. Ler o passado do código é aprender de graça [3]."
    ),
    "ZP4-05-branches-criar-alternar-e-mesclar": (
        "Branches: Criar, Alternar e Mesclar",
        "Branches: Ramificações, Git Checkout/Switch, Merge e o Trabalho em Paralelo",
        "Branches, git branch, git checkout/switch, merge e trabalho paralelo",
        "Branches são o superpoder do Git: desenvolver em paralelo sem interferir na base principal. Este livro ensina a criar, alternar, listar e mesclar branches — e o fluxo de trabalho que permite várias funcionalidades evoluírem ao mesmo tempo com segurança.",
        "O trabalho profissional é feito em branches: cada funcionalidade, correção ou experimento vive em uma ramificação separada e só entra na main quando está pronta. Dominar branches é o pré-requisito para colaborar em qualquer equipe — e o conceito mais importante depois do commit.",
        "Branches são ponteiros para commits que divergem da linha principal [1]. git branch cria; git checkout (ou git switch, mais moderno) alterna; git merge integra uma branch na outra. O merge cria um novo commit de junção quando os históricos divergem. Branches são baratas — criar muitas é normal [2].\n\n**Por que importa?** Trabalhar direto na main é a marca do iniciante: um erro quebra a base de todos. Com branches, o código experimental não afeta ninguém até ser mesclado. Git Flow e trunk-based (capítulos futuros) são estratégias construídas sobre branches.\n\n**O que muda na prática:** Crie uma branch por tarefa (feature/nome), trabalhe nela e mescle quando pronta. O hábito de branch por funcionalidade é universal nos times profissionais [3]."
    ),
    "ZP4-06-resolucao-de-conflitos": (
        "Resolução de Conflitos",
        "Conflitos de Merge: Entender, Resolver e Prevenir",
        "Merge conflicts, marcas de conflito, resolução, abortar e prevenção",
        "Conflitos acontecem — e resolvê-los é uma habilidade profissional. Este livro ensina a entender por que os conflitos ocorrem, ler as marcas de conflito (<<<<<<<, =======, >>>>>>>), resolver com calma e método, e as práticas que previnem conflitos frequentes.",
        "O conflito não é um fracasso: é o Git pedindo uma decisão humana quando duas mudanças tocaram o mesmo código. Quem sabe resolver conflitos com calma — em vez de pânico — trabalha com confiança em qualquer time. É também um dos temas mais cobrados em entrevistas.",
        "Um conflito de merge ocorre quando duas branches modificam as mesmas linhas de forma incompatível [1]. O Git marca o arquivo: <<<<<<< HEAD (sua versão), ======= separador, >>>>>>> branch (a outra versão). Resolver é editar o arquivo escolhendo a combinação correta, depois git add e git commit. Para sair de um merge problemático: git merge --abort [2].\n\n**Por que importa?** Conflitos são inevitáveis em equipes — mas frequentes conflitos sinalizam problemas de comunicação ou de granularidade de mudanças. Resolver com método (entender os dois lados antes de editar) evita perda de trabalho. Ferramentas visuais (VS Code, meld) ajudam.\n\n**O que muda na prática:** Não resolva no susto: leia os dois lados, decida a versão correta e teste o resultado. Merges pequenos e frequentes geram menos conflitos que merges grandes e raros [3]."
    ),
    # ═══════════ NIVEL 2: TRABALHO REMOTO E GITHUB ═══════════
    "ZP4-07-trabalho-remoto-clone-push-pull": (
        "Trabalho Remoto: clone, push e pull",
        "Trabalho Remoto: Repositórios, clone, push, pull, fetch e Remotes",
        "Remote, clone, push, pull, fetch, origin e sincronização",
        "Git é distribuído: o código vive localmente e em remotos (GitHub, GitLab). Este livro ensina o trabalho remoto: git clone, git push, git pull, git fetch, a configuração de remotes (origin) e o fluxo de sincronização entre máquina local e servidor.",
        "O trabalho real acontece entre local e remoto: você baixa (pull/clone), desenvolve e envia (push). Dominar remotes e o fluxo de sincronização é o que conecta seu trabalho individual à colaboração em equipe — e é o dia a dia de todo desenvolvedor.",
        "Um remote é um repositório em outro lugar: git remote add origin <url> [1]. git clone baixa um repositório remoto completo (com histórico) e configura origin automaticamente. git push envia commits locais; git pull busca e mescla (fetch + merge); git fetch só baixa as referências sem mesclar. O fluxo: pull antes de começar, push depois de terminar [2].\n\n**Por que importa?** Entender a diferença entre fetch (baixar referências) e pull (baixar e mesclar) evita surpresas. Pull antes de push evita rejeições por divergência. GitHub, GitLab e Bitbucket são remotos com camadas de colaboração (issues, PRs).\n\n**O que muda na prática:** Clone um projeto, crie um branch, faça uma mudança, push e abra um pull request. O fluxo local ↔ remoto é a base de toda contribuição em equipe [3]."
    ),
    "ZP4-08-github-repositorios-e-issues": (
        "GitHub: Repositórios e Issues",
        "GitHub: Repositórios, Issues, Projects e a Plataforma de Colaboração",
        "Repositórios, issues, labels, milestones, projetos e documentação",
        "GitHub é a maior plataforma de desenvolvimento do mundo — o seu portfólio e o lugar onde o trabalho acontece. Este livro ensina a usar GitHub profissionalmente: repositórios (README, .gitignore), issues com labels e milestones, projects e a documentação que todo repo profissional tem.",
        "GitHub é o cartão de visita do desenvolvedor: recrutadores avaliam repositórios antes do currículo. Dominar a plataforma — repositórios organizados, issues bem descritas e documentação clara — é o que transforma código em trabalho profissional visível.",
        "Um repositório GitHub bem estruturado tem: README (o que é, como rodar, como contribuir), .gitignore (arquivos que não entram no versionamento), LICENSE e CONTRIBUTING [1]. Issues organizam trabalho com labels (bug, enhancement), milestones (metas) e assignees. Projects (kanban) planejam sprints. Wiki e GitHub Pages documentam [2].\n\n**Por que importa?** O README é a porta de entrada do seu projeto — e do seu perfil profissional. Issues bem descritas são a base da colaboração open source e do trabalho em equipe. Um perfil GitHub ativo com projetos documentados é o CV mais forte que um dev pode ter.\n\n**O que muda na prática:** Transforme um projeto seu em um repositório profissional: README completo, .gitignore correto e issues para as próximas melhorias. Seu GitHub é o seu portfólio público [3]."
    ),
    "ZP4-09-pull-requests-e-code-review": (
        "Pull Requests e Code Review",
        "Pull Requests e Code Review: Contribuição, Revisão e a Qualidade do Time",
        "Pull requests, descrição, revisão, comentários, aprovação e merge",
        "O pull request é a unidade de colaboração profissional: propor, revisar e integrar mudanças com qualidade. Este livro ensina a abrir pull requests bem descritos, revisar código com comentários construtivos e conduzir o fluxo de aprovação e merge em equipe.",
        "PRs são onde a qualidade do código nasce: cada mudança é revisada por pares antes de entrar na base. Quem domina o fluxo — descrever bem, revisar com critério e responder feedback — trabalha em qualquer equipe e produz software mais confiável.",
        "Um pull request propõe mudanças de uma branch para outra com descrição, testes e contexto [1]. A revisão (code review) avalia: correção, clareza, testes e boas práticas — com comentários inline no diff. O fluxo: abrir PR → revisores comentam → autor ajusta → aprovação → merge. Proteção de branch (branch protection) exige review para merge na main [2].\n\n**Por que importa?** Code review pega bugs, compartilha conhecimento e padroniza o código — 4 olhos veem mais que 2. PRs pequenos e focados são revisados mais rápido e com mais qualidade. A comunicação respeitosa no review define a cultura do time.\n\n**O que muda na prática:** Abra PRs pequenos com descrição clara, revise o diff com intenção (não só 'LGTM') e responda feedback com transparência. Esse fluxo é o coração do trabalho em equipe moderno [3]."
    ),
    "ZP4-10-estrategias-de-branching": (
        "Estratégias de Branching",
        "Estratégias de Branching: Git Flow, Trunk-Based e o Fluxo Certo para o Time",
        "Git Flow, trunk-based, GitHub Flow, feature branches e releases",
        "Nem todo time usa branches do mesmo jeito: as estratégias de branching organizam como as mudanças fluem até a produção. Este livro compara Git Flow, GitHub Flow e trunk-based development — e ensina a escolher a estratégia certa para cada tipo de projeto e equipe.",
        "A estratégia de branching é uma decisão de arquitetura de colaboração: define cadência de releases, disciplina de testes e a complexidade dos merges. Dominar as opções — e saber qual se encaixa em cada contexto — é o que diferencia um profissional que entende o fluxo do time.",
        "Git Flow usa branches especializadas: main (produção), develop (integração), feature/* (tarefas), release/* (preparação), hotfix/* (correções urgentes) [1]. GitHub Flow simplifica: tudo a partir da main, com feature branches e PRs — deploy contínuo. Trunk-based: todos integram na main diariamente com feature flags [2].\n\n**Por que importa?** Git Flow é robusto para releases versionadas (versões estáveis + hotfixes); GitHub Flow é ágil para deploy contínuo; trunk-based exige disciplina e testes fortes. Escolher a estratégia errada adiciona complexidade ou fragilidade desnecessárias.\n\n**O que muda na prática:** Entenda o contexto (frequência de release, tamanho do time, maturidade de testes) e mapeie a estratégia correspondente. Saber explicar essa escolha é diferencial em entrevistas e no time [3]."
    ),
    "ZP4-11-rebase-cherry-pick-e-amend": (
        "Rebase, Cherry-pick e Amend",
        "Reescrita de Histórico: rebase, cherry-pick, amend e interactive rebase",
        "Rebase, cherry-pick, amend, reword, squash e reescrita de histórico",
        "O Git permite reescrever o histórico — uma ferramenta poderosa que exige critério. Este livro ensina git rebase (linearização), cherry-pick (copiar commits), amend (corrigir o último commit) e o interactive rebase (reorder, squash, reword) — com as regras de ouro para usar sem causar dano.",
        "Reescrever o histórico com rebase e squash produz commits limpos e legíveis — o padrão de projetos profissionais. Mas reescrever commits já publicados e compartilhados é perigoso. Dominar essas ferramentas com as regras certas é uma marca de senioridade.",
        "git cherry-pick <hash> copia um commit de outra branch [1]. git commit --amend corrige a mensagem ou adiciona arquivos ao último commit. git rebase -i reescreve uma série de commits: reword (mudar mensagens), squash (juntar), drop (remover), reorder. Rebase sobre a main (git rebase main) lineariza o histórico antes do merge [2].\n\n**Por que importa?** A regra de ouro: nunca reescreva commits já publicados (push) e compartilhados — o histórico divergente quebra o repositório de todos. Rebase antes do PR (squash de WIP em commits coesos) é o uso profissional seguro.\n\n**O que muda na prática:** Use amend para corrigir erros imediatos, squash para limpar WIP antes do PR e cherry-pick para mover correções. Rebase com critério — nunca em commits publicados [3]."
    ),
    "ZP4-12-stash-e-trabalho-interrompido": (
        "Stash e Trabalho Interrompido",
        "Stash: Guardar, Recuperar e Gerenciar Trabalho em Andamento",
        "git stash, pop, apply, drop, stash list e trabalho interrompido",
        "O trabalho é interrompido toda hora — e o stash é a resposta. Este livro ensina git stash para guardar mudanças em andamento sem commit, recuperá-las depois (pop, apply) e gerenciar múltiplos stashes — a habilidade prática que mantém o fluxo de trabalho organizado.",
        "Precisa trocar de branch no meio do trabalho? O stash guarda suas mudanças, deixa o diretório limpo e devolve tudo depois. É uma das ferramentas mais usadas e menos ensinadas do Git — e dominá-la evita perder trabalho e misturar mudanças.",
        "git stash guarda mudanças não commitadas e limpa o diretório [1]. git stash pop recupera e remove o stash; git stash apply recupera sem remover; git stash list mostra todos; git stash drop descarta. Stashes nomeados (git stash push -m 'wip login') organizam múltiplos. git stash --include-untracked guarda também arquivos novos [2].\n\n**Por que importa?** Trocar de contexto sem stash mistura trabalhos e gera commits errados. Stash é também o primeiro passo de muitos fluxos (pull antes de continuar). Perder mudanças por não saber usar stash é um dos acidentes mais comuns de iniciantes.\n\n**O que muda na prática:** Crie o hábito: ao ser interrompido, git stash push -m 'descrição'; ao voltar, git stash pop. Nunca perca trabalho e mantenha o diretório sempre consistente [3]."
    ),
    # ═══════════ NIVEL 3: GIT AVANÇADO E AUTOMAÇÃO ═══════════
    "ZP4-13-tags-releases-e-versionamento": (
        "Tags, Releases e Versionamento Semântico",
        "Tags e Releases: Versionamento Semântico e Entregas Estáveis",
        "Tags, anotadas, semver, releases, changelog e versionamento",
        "Versões estáveis são marcadas, documentadas e publicadas — é o papel das tags e releases. Este livro ensina git tag (leves e anotadas), a publicação de releases no GitHub, o versionamento semântico (semver: major.minor.patch) e o changelog profissional.",
        "Tags marcam pontos importantes do histórico (versões, releases); o semver comunica o impacto de cada mudança; o changelog documenta o que mudou entre versões. Juntos, eles formam o ciclo de versionamento que usuários e times consomem — e que todo projeto profissional publica.",
        "git tag v1.0.0 marca um commit; tags anotadas (-a) incluem mensagem, autor e data [1]. O versionamento semântico (semver) define: MAJOR (quebra compatibilidade), MINOR (nova funcionalidade compatível), PATCH (correção) [2]. Releases no GitHub combinam tag + notas de versão + artefatos. O changelog (CHANGELOG.md) documenta cada versão.\n\n**Por que importa?** Usuários e dependências confiam no semver: MAJOR 0 significa pré-release; subir MAJOR errado quebra consumidores. Tags permitem voltar a qualquer versão publicada — essencial em produção. O changelog comunica o valor de cada release.\n\n**O que muda na prática:** Versione com semver, crie tags anotadas em cada release e publique releases no GitHub com notas claras. Versionamento profissional é a cara de um projeto maduro [3]."
    ),
    "ZP4-14-git-avancado-reflog-bisect-e-filtros": (
        "Git Avançado: reflog, bisect e filtros",
        "Git Avançado: reflog, bisect, filter-branch e o Histórico Profundo",
        "Reflog, bisect, grep, filter-branch e recuperação de trabalho",
        "Quando o Git parece ter perdido trabalho — ou um bug surgiu sem aviso — as ferramentas avançadas salvam o dia. Este livro ensina git reflog (recuperar commits 'perdidos'), git bisect (encontrar o commit que introduziu um bug) e as ferramentas de análise profunda do histórico.",
        "O reflog é a rede de segurança definitiva: registra todos os movimentos do HEAD, permitindo recuperar commits que pareciam perdidos. O bisect encontra automaticamente o commit que introduziu um bug — uma economia gigante de tempo. São as ferramentas dos profissionais experientes.",
        "git reflog mostra o histórico de movimentos do HEAD — cada commit por onde o HEAD passou, mesmo os 'perdidos' por reset [1]. git bisect encontra o commit culpado por busca binária: git bisect start, bad/good, e o Git testa os pontos médios até isolar o commit. git grep busca no histórico; git log -S 'texto' encontra quando um texto entrou no código [2].\n\n**Por que importa?** 'Perdi meu trabalho' quase sempre tem solução com reflog. Bugs antigos são encontrados em minutos com bisect em vez de dias de investigação manual. Essas ferramentas transformam o histórico em uma máquina de diagnóstico.\n\n**O que muda na prática:** Aprenda reflog para nunca temer reset, e bisect na primeira suspeita de regressão. Investigação de bugs com Git é a marca da senioridade [3]."
    ),
    "ZP4-15-hooks-do-git-e-automacao": (
        "Hooks do Git e Automação",
        "Hooks do Git: Gatilhos Automáticos para Qualidade e Padrões",
        "Hooks, pre-commit, pre-push, Husky, lint e automação de qualidade",
        "Hooks são gatilhos que o Git dispara em eventos (commit, push) — e a base da automação de qualidade. Este livro ensina os hooks do Git (pre-commit, pre-push), a configuração manual e com Husky, e como automatizar lint, testes e formatação antes de cada commit.",
        "Qualidade automatizada é a marca de equipes maduras: o lint e os testes rodam antes do commit entrar — não depois do bug chegar à produção. Hooks (e ferramentas como Husky) fazem isso automaticamente, garantindo que o padrão do time seja seguido por todos, sempre.",
        "Hooks são scripts em .git/hooks que o Git executa em eventos: pre-commit, commit-msg, pre-push, post-merge [1]. Um pre-commit roda lint e testes e bloqueia o commit se falharem. Husky facilita a configuração em projetos JavaScript/Node (npx husky init). Ferramentas como lint-staged rodam lint apenas nos arquivos alterados [2].\n\n**Por que importa?** Código que quebra lint ou testes não deveria entrar no histórico. Automatizar no hook (em vez de depender da disciplina individual) padroniza a qualidade do time inteiro. Hooks também automatizam formatação e geração de arquivos.\n\n**O que muda na prática:** Configure pre-commit com lint e testes no seu projeto. A automação de qualidade é um investimento que se paga no primeiro bug evitado [3]."
    ),
    "ZP4-16-fluxos-de-equipe-e-boas-praticas": (
        "Fluxos de Equipe e Boas Práticas",
        "Fluxos de Equipe: Commits Semânticos, Revisão e a Cultura do Time",
        "Commits semânticos, convenções, revisão, documentação e cultura",
        "O Git funciona sozinho; a colaboração é que precisa de convenções. Este livro ensina os fluxos de equipe profissionais: convenções de commits semânticos (Conventional Commits), padrões de mensagem, a disciplina de revisão, documentação e a cultura que faz times produtivos.",
        "Times profissionais não improvisam: convenções de commit, revisão e documentação criam um histórico legível e previsível que qualquer pessoa entende. Conventional Commits (feat, fix, breaking) geram até changelogs e versionamento automáticos. É a camada humana do Git.",
        "Conventional Commits padroniza mensagens: feat(scope): descrição, fix:, chore:, docs:, BREAKING CHANGE [1]. O padrão permite gerar changelog e versionamento automáticos (semantic-release). Outras boas práticas: commits atômicos (uma mudança lógica por commit), PRs pequenos, revisão construtiva e documentação viva (README atualizado) [2].\n\n**Por que importa?** Histórico padronizado é pesquisável e automatizável. Commits atômicos facilitam bisect, revert e revisão. A cultura de revisão respeitosa e documentação contínua é o que sustenta a velocidade do time no longo prazo.\n\n**O que muda na prática:** Adote Conventional Commits no seu próximo projeto e mantenha commits pequenos e coesos. A padronização do time começa no seu exemplo [3]."
    ),
    "ZP4-17-github-actions-e-ci-cd": (
        "GitHub Actions e CI/CD",
        "GitHub Actions: CI/CD Automatizado — Testes, Build e Deploy",
        "Workflows, actions, jobs, CI, CD, secrets e deploy automatizado",
        "A automação de integração e entrega contínuas (CI/CD) roda no GitHub Actions: cada push dispara testes, build e deploy automaticamente. Este livro ensina a criar workflows, usar actions, configurar jobs e secrets e automatizar da qualidade ao deploy.",
        "CI/CD é o padrão de entrega profissional: código que passa nos testes automáticos vai para produção com confiança. GitHub Actions torna isso acessível — e dominar workflows é uma habilidade valorizada em qualquer vaga de desenvolvimento moderno.",
        "Um workflow GitHub Actions é um YAML em .github/workflows: triggers (on: push, pull_request), jobs, steps e actions reutilizáveis [1]. Exemplo: rodar testes (actions/checkout, setup-node, npm test) a cada push. Secrets (settings → secrets) guardam tokens sem expor no código. O fluxo: testes no PR, build e deploy na main [2].\n\n**Por que importa?** CI pega regressões automaticamente antes do merge; CD entrega com repetibilidade, sem erros manuais. Matrizes (matrix) testam em múltiplas versões de Node/OS. Caches aceleram dependências. Um pipeline bem desenhado é a espinha dorsal da qualidade do projeto.\n\n**O que muda na prática:** Crie um workflow que roda lint + testes em todo push e um job de deploy na main. CI/CD profissional começa com um workflow simples e evolui [3]."
    ),
    # ═══════════ NIVEL 4-5: OPEN SOURCE, SEGURANÇA E CARREIRA ═══════════
    "ZP4-18-contribuicao-em-projetos-open-source": (
        "Contribuição em Projetos Open Source",
        "Open Source: Contribuir, Colaborar e Construir Reputação",
        "Fork, issues, contribuição, mantenedores, convenções e reputação",
        "Contribuir para projetos open source é o caminho mais rápido para aprender de verdade e construir reputação. Este livro ensina o fluxo completo de contribuição: escolher um projeto, entender as convenções (CONTRIBUTING), abrir issues e pull requests e colaborar com mantenedores.",
        "Open source é uma universidade gratuita com portfólio incluído: cada contribuição é pública, revisada e visível para recrutadores. Dominar o fluxo de contribuição — do fork ao merge — transforma seu GitHub em um histórico profissional real de colaboração.",
        "O fluxo de contribuição: escolha um projeto (issues com label 'good first issue'), faça fork e clone, crie uma branch, implemente, abra um PR seguindo o CONTRIBUTING [1]. Convenções: mensagens de commit do projeto, testes exigidos, discussão respeitosa. Mantenedores revisam e pedem ajustes — o ciclo de feedback é o aprendizado [2].\n\n**Por que importa?** Cada PR aceito é uma prova pública de habilidade: código revisado por mantenedores experientes em projetos usados por milhões. A contribuição ensina padrões reais (testes, CI, documentação) que tutoriais não ensinam. É o portfólio mais forte que existe.\n\n**O que muda na prática:** Encontre um projeto que você já usa, resolva um 'good first issue' e abra seu primeiro PR. A primeira contribuição abre as portas para as próximas [3]."
    ),
    "ZP4-19-seguranca-gpg-e-secrets": (
        "Segurança: GPG, Secrets e Boas Práticas",
        "Segurança no Git: GPG, Assinatura de Commits, Secrets e Proteção de Repositório",
        "GPG, assinatura de commits, .gitignore, secrets, branch protection e audit",
        "Segurança no Git vai além do código: commits assinados provam autoria, secrets não podem vazar para o histórico, e a proteção de branches guarda a base do projeto. Este livro ensina GPG, assinatura de commits, o .gitignore correto, a proteção de repositório e a auditoria de segurança.",
        "Um commit pode ser forjado, um secret pode vazar no histórico e uma branch desprotegida pode ser destruída. Segurança é responsabilidade de todo desenvolvedor: assinar commits com GPG, proteger secrets e configurar branch protection são práticas que times sérios exigem.",
        "GPG assina commits e tags, provando autoria: gpg --gen-key, depois git config user.signingkey e git commit -S [1]. O .gitignore impede arquivos sensíveis (chaves, .env) de entrar no histórico. Secrets no GitHub: nunca no código — use Actions secrets e variáveis de ambiente. Branch protection (settings) exige reviews e bloqueia push direto na main [2].\n\n**Por que importa?** Um secret vazado no histórico continua acessível mesmo depois de removido — o histórico é imutável (forçado com filter-branch/bfg). Commits assinados garantem integridade e autoria. Proteção de branch é a última linha de defesa contra erros e mal-intencionados.\n\n**O que muda na prática:** Ative o GPG no seu ambiente, use .gitignore desde o primeiro dia e configure branch protection no seu repositório. Segurança é um hábito desde o início [3]."
    ),
    "ZP4-20-carreira-e-colaboracao-profissional": (
        "Carreira e Colaboração Profissional",
        "Carreira em Git: Portfólio, Entrevistas e o Desenvolvedor Profissional",
        "Portfólio GitHub, entrevistas, colaboração, CV e mercado",
        "Você domina Git — agora mostre isso ao mundo. Este livro prepara você para o mercado: o portfólio GitHub como cartão de visita, as perguntas de Git em entrevistas técnicas, a colaboração profissional e como o seu perfil público constrói a carreira.",
        "O GitHub é o currículo do desenvolvedor moderno: recrutadores olham seu perfil antes do CV. Um portfólio com projetos documentados, commits limpos e contribuições abertas fala por você. Este livro fecha a jornada transformando o conhecimento em carreira.",
        "O portfólio profissional: repositórios com README completo, .gitignore correto, testes e CI rodando, e histórico de commits limpo e semântico [1]. Entrevistas técnicas cobram Git com frequência: diferença entre merge e rebase, como resolver conflitos, o que é o reflog, estratégias de branching. Exercícios práticos e simulações preparam [2].\n\n**Por que importa?** Um perfil GitHub ativo com projetos reais e contribuições demonstra prática contínua — o sinal mais forte para recrutadores. Saber explicar decisões de Git (por que trunk-based, por que squash) mostra senioridade. A colaboração registrada no histórico é prova de trabalho em equipe.\n\n**O que muda na prática:** Pola seu GitHub: READMEs, contribuições, commits semânticos. Pratique as perguntas clássicas de Git em voz alta. A jornada do zero ao profissional está completa — e seu GitHub conta essa história [3]."
    ),
}
