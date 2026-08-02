# SPEC: Especificação Autônoma de Economia Severa de Tokens para Projetos Agênticos

Esta especificação define o padrão universal de **Economia Severa de Tokens** reutilizável em qualquer repositório. Ao aplicar esta SPEC em um novo projeto, ele passa a contar com compressão de linguagem (Caveman), compressão de logs/JSONs (Headroom), filtro de comandos CLI (RTK), motor de contexto cirúrgico (LeanCTX) e delegação comprimida por subagentes (Cavecrew).

---

## 🚀 Instalação Rápida Autônoma (1-Click Setup)

Para instalar a infraestrutura completa de Economia Severa de Tokens na raiz de **qualquer projeto**, copie e execute o script PowerShell abaixo no terminal do projeto:

```powershell
# Script Autônomo de Instalação de Economia Severa de Tokens
param([string]$ProjectPath = ".")

Set-Location $ProjectPath
Write-Host "⚡ Instalando ecossistema de economia de tokens..." -ForegroundColor Cyan

# 1. Instalar dependências CLI via uv / npm (se disponível)
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv tool install --python 3.13 "headroom-ai[all]"
}
if (Get-Command npm -ErrorAction SilentlyContinue) {
    npm install --save-dev headroom-ai 2>$null
}

# 2. Criar diretórios de skills multi-IDE
$dirs = @(".agents/skills", ".claude/skills", "agentic/skills")
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}

# 3. Criar arquivo CLAUDE.md e AGENTS.md com diretrizes de economia
$rulesHeader = @"
# ⚡ DIRETRIZES DE ECONOMIA SEVERA DE TOKENS (PRIORIDADE MÁXIMA)

1. **Estilo Caveman Ativo:** Pensamento em formato telegráfico (máx. 3-5 linhas). Comunicação sem preâmbulos, saudações ou palavras vazias. Preservar termos técnicos e idioma PT-BR.
2. **Compressão com Headroom & RTK:** Todo log, payload JSON ou output de comando com mais de 7 linhas DEVE ser comprimido via ``headroom`` (manter 3 primeiras e 4 últimas linhas) e filtrado via ``rtk``.
3. **Seleção Cirúrgica (LeanCTX):** Injetar no contexto APENAS o estritamente necessário. Sempre utilizar ``grep_search`` antes de ler arquivos e limitar a leitura por linha (``StartLine``/``EndLine``).
4. **Delegação Cavecrew:** Utilizar a skill ``cavecrew`` para delegar subagentes comprimidos em buscas ou edições extensas.
"@

$files = @("CLAUDE.md", "AGENTS.md")
foreach ($f in $files) {
    if (-not (Test-Path $f)) {
        Set-Content -Path $f -Value $rulesHeader -Encoding UTF8
    } else {
        $content = Get-Content -Path $f -Raw
        if ($content -notlike "*DIRETRIZES DE ECONOMIA SEVERA DE TOKENS*") {
            $newContent = $rulesHeader + "`n`n" + $content
            Set-Content -Path $f -Value $newContent -Encoding UTF8
        }
    }
}

# 4. Provisionar skills essenciais de economia severa
$skills = @("caveman", "cavecrew", "caveman-commit", "caveman-compress", "caveman-help", "caveman-review", "caveman-stats", "headroom", "lean-ctx", "rtk")

foreach ($sk in $skills) {
    # .agents/skills
    $agentSkDir = ".agents/skills/$sk"
    if (-not (Test-Path $agentSkDir)) { New-Item -ItemType Directory -Force -Path $agentSkDir | Out-Null }
    $agentSkFile = "$agentSkDir/SKILL.md"
    if (-not (Test-Path $agentSkFile)) {
        Set-Content -Path $agentSkFile -Value "---`nname: $sk`ndescription: Skill de Economia Severa de Tokens ($sk)`n---`n`n# $sk`nAtivo para economia severa." -Encoding UTF8
    }

    # agentic/skills
    $agenticSkDir = "agentic/skills/$sk"
    if (-not (Test-Path $agenticSkDir)) { New-Item -ItemType Directory -Force -Path $agenticSkDir | Out-Null }
    $agenticSkFile = "$agenticSkDir/SKILL.md"
    if (-not (Test-Path $agenticSkFile)) {
        Set-Content -Path $agenticSkFile -Value "---`nname: $sk`ndescription: Skill de Economia Severa de Tokens ($sk)`n---`n`n# $sk`nAtivo para economia severa." -Encoding UTF8
    }

    # .claude/skills
    $claudeSkFile = ".claude/skills/$sk"
    if (-not (Test-Path $claudeSkFile)) {
        Set-Content -Path $claudeSkFile -Value "---`nname: $sk`ndescription: Skill de Economia Severa de Tokens ($sk)`n---`n`n# $sk`nAtivo para economia severa." -Encoding UTF8
    }
}

Write-Host "✅ Economia Severa de Tokens instalada com sucesso!" -ForegroundColor Green
```

---

## 🛠️ As 4 Camadas de Economia Severa de Tokens

### Camada 1: Lógica e Comunicação (Caveman Mode)
- **O que faz:** Remove artigos, preposições, saudações, desculpas e palavras irrelevantes.
- **Redução:** ~65% de economia nos tokens de saída.
- **Ativação:** Automática via instrução inicial ou comando `/caveman`.

### Camada 2: Logs e Payloads JSON (Headroom)
- **O que faz:** Intercepta respostas de ferramentas e compressores de dados. Se o log tiver mais de 7 linhas, mantém apenas as 3 primeiras e as 4 últimas linhas.
- **Redução:** 60% a 95% em saídas ruidosas.
- **Comando CLI:** `headroom proxy --port 8787` ou `headroom wrap <comando>`.

### Camada 3: Leitura e Filtro de CLI (RTK - Rust Token Killer)
- **O que faz:** Intercepta comandos de terminal (`git status`, `npm test`, `pytest`, `eslint`) e trunca boilerplates.
- **Uso:** Adicionar o prefixo `rtk` antes de comandos de build/teste.

### Camada 4: Context Engine Cirúrgico (LeanCTX)
- **O que faz:** Injeta no prompt somente declarações de AST e blocos de código necessários.
- **Uso:** Preferir `grep_search` e limitar leituras via `StartLine`/`EndLine`.

---

## 📁 Estrutura de Diretórios de Skills Gerada

```
.
├── CLAUDE.md                # Diretrizes de economia para Claude Code e Antigravity
├── AGENTS.md                # Diretrizes universais de agentes (OpenCode, Cursor, Windsurf)
├── .agents/skills/          # Skills padrão para Antigravity / OpenCode
│   ├── caveman/
│   ├── cavecrew/
│   ├── headroom/
│   ├── lean-ctx/
│   └── rtk/
├── agentic/skills/          # Skills para Frameworks Agentic
└── .claude/skills/          # Skills para Claude Code
```

---

## 📋 Checklist de Verificação

- [x] O repositório possui `CLAUDE.md` e `AGENTS.md` com a seção `⚡ DIRETRIZES DE ECONOMIA SEVERA DE TOKENS`.
- [x] As pastas `.agents/skills`, `.claude/skills` e `agentic/skills` estão criadas e provisionadas.
- [x] O pacote `headroom-ai` está acessível no ambiente local.
- [x] Agentes realizam chamadas de leitura cirúrgicas via `grep_search` e leem arquivos parcialmente.
