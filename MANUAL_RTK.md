# Manual Completo: RTK (Rust Token Killer) — Guia de Instalação no Windows & Economia Severa

> **Repositório:** [rtk-ai/rtk](https://github.com/rtk-ai/rtk)  
> **Objetivo:** Interceptar e comprimir saídas verbose de comandos CLI (`git`, `npm`, `cargo`, `docker`, `pytest`) antes que cheguem à janela de contexto da IA, reduzindo o consumo de tokens de terminal em **60% a 90%** com latência $<10\text{ms}$.

---

## 1. Solução de Instalação para Windows (Git Bash / PowerShell / CMD)

O script `install.sh` padrão não suporta o ambiente `MINGW64` do Git Bash e o `cargo` exige a instalação prévia do compilador Rust.

Para o **Windows**, a instalação rápida e direta é via **Download do Executável Pré-compilado (`rtk.exe`)**.

### Método 1: Instalação Automática no Windows (Via PowerShell - Recomendado)

Abra o **PowerShell** e cole os comandos abaixo:

```powershell
# 1. Baixar o arquivo zip da última release do RTK
Invoke-WebRequest -Uri "https://github.com/rtk-ai/rtk/releases/latest/download/rtk-x86_64-pc-windows-msvc.zip" -OutFile "$env:TEMP\rtk.zip"

# 2. Extrair o rtk.exe
Expand-Archive -Path "$env:TEMP\rtk.zip" -DestinationPath "$env:TEMP\rtk_extracted" -Force

# 3. Mover o rtk.exe para uma pasta no PATH do usuário (ex: C:\Users\<usuario>\.local\bin)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.local\bin"
Move-Item -Force "$env:TEMP\rtk_extracted\rtk.exe" "$env:USERPROFILE\.local\bin\rtk.exe"

# 4. Adicionar a pasta .local\bin ao PATH (se ainda não estiver)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.local\bin", [EnvironmentVariableTarget]::User)
```

> **Nota para Git Bash (MINGW64):** Após executar o script acima no PowerShell, feche e reabra o seu terminal Git Bash para recarregar a variável `$PATH`.

---

### Método 2: Instalação Manual (Download Direto)

1. Acesse a página de releases: [https://github.com/rtk-ai/rtk/releases](https://github.com/rtk-ai/rtk/releases)
2. Baixe o arquivo **`rtk-x86_64-pc-windows-msvc.zip`**.
3. Extraia o executável `rtk.exe`.
4. Cole o `rtk.exe` dentro de qualquer pasta cadastrada no seu PATH (ou na própria pasta do projeto `c:\Users\trcnologia\Desktop\proj_livros\`).

---

### Método 3: via Rust / Cargo (Se tiver o Rust instalado)

Se você preferir instalar o Rust no Windows primeiro:
```powershell
winget install Rustup.Rustup
```
Depois de reiniciar o terminal:
```bash
cargo install --git https://github.com/rtk-ai/rtk
```

---

## 2. Inicialização dos Ganchos (Após Instalar o `rtk.exe`)

No **Git Bash**, **PowerShell** ou **Terminal**:

```bash
# 1. Verificar se o RTK foi reconhecido
rtk --version

# 2. Ativar ganchos no projeto atual
rtk init

# 3. Ativar ganchos globais para todos os agentes de IA da máquina
rtk init -g
```

---

## 3. Uso Prático no Contexto de Economia Severa

### Uso Direto (Opcional):
```bash
rtk git status
rtk npm test
rtk cargo build
```

### Uso Automático (Recomendado):
Após rodar `rtk init -g`, o RTK intercepta automaticamente os comandos disparados pelos seus agentes de IA (Cursor, Claude Code, Gemini, Antigravity) no terminal e devolve o output 60-90% mais curto.

---

## 4. O Ecossistema Definitivo de Economia Severa de Tokens

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. LeanCTX  : Comprime leituras AST de arquivos e gerencia o cache     │
├────────────────────────────────────────────────────────────────────────┤
│ 2. RTK      : Comprime a saída dos comandos do terminal (CLI Proxy)   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Caveman  : Comprime o texto das respostas geradas pela IA          │
└────────────────────────────────────────────────────────────────────────┘
```
