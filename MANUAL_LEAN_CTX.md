# Manual Completo: LeanCTX — Guia de Economia Severa de Tokens

> **Repositório:** [yvgude/lean-ctx](https://github.com/yvgude/lean-ctx)  
> **Objetivo:** Reduzir o consumo de tokens LLM em **60% a 90%+** em sessões de codificação e agentic AI, mantendo máxima precisão e contexto persistente.

---

## 1. Visão Geral e Arquitetura

O **LeanCTX** (Lean Context) é uma camada de engenharia de contexto (*Context Engineering Layer*) local escrita em Rust de alta performance. Ele atua como um intermediário (proxy / MCP server) entre as ferramentas de IA (Cursor, Claude Code, Antigravity, Copilot, VSCode, etc.) e o seu ambiente de desenvolvimento.

### Principais Pilares de Economia:
1. **Compressão AST & Leitura Seletiva (10 modos):** Em vez de enviar arquivos inteiros de milhares de linhas (~2.000 tokens cada), o LeanCTX extrai assinaturas de código, resumos estruturados ou recortes de alta entropia (ex: ~13 tokens por releitura em cache).
2. **Compressão de Shell/Terminal:** Filtra o ruído de +95 comandos de terminal (`git`, `npm`, `cargo`, `docker`, `pytest`), reduzindo resumos de terminal de 800-2000 tokens para ~120 tokens.
3. **Proxy HTTP Local (Cache de Histórico / Prompt-Cache-Safe):** Comprime requisições HTTP enviadas para LLMs sem quebrar a cache de prompt do provedor.
4. **Memória de Sessão Persistente (CCP):** Evita "cold start" e releitura de arquivos em novos chats salvando fatos, arquivos lidos e decisões no repositório local.
5. **Painel de Controle e Métricas (Dashboard / Ledger):** Acompanha a economia exata em tokens e dólares em tempo real.

---

## 2. Instalação e Configuração

### 2.1 Instalação Global

Existem 4 formas de instalar o binary do **LeanCTX** globalmente no seu sistema:

#### Opção A: Script Universal (Recomendado - Linux/macOS/Git Bash Windows)
```bash
curl -fsSL https://leanctx.com/install.sh | sh
```

#### Opção B: via Cargo (Rust package manager)
```bash
cargo install lean-ctx
```

#### Opção C: via NPM (Wrapper binário)
```bash
npm install -g lean-ctx-bin
```
*(Nota no Windows: Executar o PowerShell/Terminal como Administrador se houver restrição de permissão no diretório global).*

#### Opção D: via Homebrew (macOS/Linux)
```bash
brew tap yvgude/lean-ctx && brew install lean-ctx
```

---

### 2.2 Instalação no Projeto Local (`proj_livros`)

Para adicionar a dependência no seu projeto Node.js/Web local:

```bash
# Adicionar no package.json como devDependency
npm install --save-dev lean-ctx-bin
```

---

### 2.3 Inicialização e Integração com Agentes

Após a instalação, rode na raiz do projeto:

```bash
# 1. Configuração interativa inicial
lean-ctx setup

# 2. Inicializar ganchos para o seu agente/editor de preferência
lean-ctx init --agent claude
# ou
lean-ctx init --agent cursor
# ou
lean-ctx init --agent gemini

# 3. Diagnóstico de saúde do ambiente
lean-ctx doctor
```

---

## 3. Guia de Uso: Economia Severa de Tokens (Severe Token Economy)

Para alcançar uma **economia severa de 70% a 90%** em cada iteração com a IA, adote as seguintes práticas operacionais:

### 3.1 Utilização dos Modos de Leitura de Arquivo (10 Modos Seletivos)

Em vez de solicitar que o agente leia o arquivo inteiro, instrua-o ou configure as chamadas MCP para usar modos seletivos:

| Modo de Leitura | Descrição / Uso | Consumo Médio de Tokens | Economia |
| :--- | :--- | :---: | :---: |
| `signatures` | Retorna apenas declarações de classes, funções e tipos via Tree-sitter AST | ~50 - 150 tokens | **~85%** |
| `map` | Estrutura de tópicos do arquivo + numeração de linhas dos métodos | ~100 tokens | **~80%** |
| `density:0.4` | Filtro de entropia determinístico. Mantém 40% das linhas mais relevantes | 40% do original | **60%** |
| `lines:N-M` | Lê apenas o intervalo de linhas específico (ex: linhas 40 a 70) | ~30 - 100 tokens | **~90%** |
| `diff` | Mostra apenas as alterações recentes em relação ao git | ~50 - 200 tokens | **~80%** |
| `cached` | Leitura de arquivo idêntico já presente no cache local | **~13 tokens** | **99%** |

#### Regra de Ouro para Leitura de Arquivos:
1. **Primeiro:** Solicite a leitura no modo `signatures` ou `map`.
2. **Segundo:** Se precisar alterar uma função específica, solicite a leitura no modo `lines:N-M`.
3. **Nunca:** Leia arquivos inteiros com mais de 200 linhas no modo `full` a menos que seja estritamente necessário refatorar o arquivo inteiro.

---

### 3.2 Compressão Automática de Output de Shell

Ao rodar testes, compilações ou comandos `git`:
- Utilize `lean-ctx run <comando>` ou ative a interceptação automática do LeanCTX.
- Saídas de `git status`, `git diff`, `npm test`, `cargo build` e `pandoc` são sanitizadas, removendo logs repetitivos, mantendo apenas stack traces essenciais e sumários de erro.
- **Economia típica:** De 1.500 tokens de saída de console para ~100 tokens.

---

### 3.3 Memória Persistente de Sessão (CCP Protocol)

Para evitar que a IA esqueça o contexto ao trocar de chat ou após truncar o histórico:
- **Salvar Fatos/Decisões:** O LeanCTX mantém um gráfico de conhecimento local das decisões tomadas.
- Ao abrir uma nova sessão, execute:
  ```bash
  lean-ctx session recover
  ```
  Isso restaura o estado mental e o mapa de arquivos lidos sem recarregar todo o histórico de conversas antigas no prompt da IA.

---

### 3.4 Servidor MCP (Model Context Protocol)

O LeanCTX atua como um servidor MCP local que fornece **82 ferramentas otimizadas**. Para registrar no seu arquivo de configuração de MCP (ex: `claude_desktop_config.json` ou settings do editor):

```json
{
  "mcpServers": {
    "lean-ctx": {
      "command": "lean-ctx",
      "args": ["serve"]
    }
  }
}
```

Isso substitui ferramentas nativas de `read_file` e `execute_command` por versões com cache transparente e compressão AST.

---

## 4. Monitoramento da Economia

Você pode acompanhar os tokens economizados e a redução de custo em tempo real:

```bash
# Dashboard ao vivo
lean-ctx gain --live

# Relatório de economia e audit trail
lean-ctx savings

# Interface TUI no terminal
lean-ctx watch
```

---

## 5. Resumo das Regras de Atuação para IAs / Agentes

Quando você (ou outro agente de IA) estiver operando neste projeto sob o regime de **Economia Severa de Tokens**:
1. **Consultar o Cache / AST primeiro:** Em vez de abrir arquivos `.ts`, `.js`, `.py` ou `.bat` inteiros, use o modo de assinaturas (`signatures`).
2. **Limitar Saída de Execução:** Encapsule comandos longos pelo gerador de resumos do LeanCTX.
3. **Persistir Aprendizados:** Salve arquivos modificados e dependências no gráfico de contexto local.
4. **Respostas Concisas:** Manter respostas e explicações diretas ao ponto, sem re-sumarizar códigos gerados que já aparecem no diff.
