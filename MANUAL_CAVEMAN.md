# Manual Completo: Caveman — Guia de Economia Severa de Tokens de Saída

> **Repositório:** [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman)  
> **Lema:** *"why use many token when few do trick"*  
> **Objetivo:** Reduzir os tokens de resposta (**output tokens**) do agente de IA em **~65%**, eliminando cortesia, preposições e enrolação, sem perder nenhuma precisão técnica de código ou comandos.

---

## 1. Visão Geral

O **Caveman** é um skill/plugin universal compatível com mais de 30 agentes e IAs de código (Claude Code, Cursor, Gemini CLI, Windsurf, Copilot, Antigravity, etc.).

### O que o Caveman faz:
* **Corta a "boca", mantém o "cérebro":** Mantém 100% da exatidão técnica, nomes de variáveis, stack traces, comandos de terminal e blocos de código.
* **Remove o ruído das respostas:** Elimina frases como *"Com certeza! Ficarei feliz em ajudar com isso..."*, *"O motivo pelo qual o seu componente..."* substituindo por respostas diretas e telegráficas.
* **Preserva o Idioma:** Escreve no idioma em que você fala (em português, responderá em português estilo caveman).

---

## 2. Instalação e Configuração

### 2.1 Instalação Global no Sistema

#### No Windows (PowerShell 5.1+):
```powershell
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex
```

#### No Linux / macOS / WSL / Git Bash:
```bash
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
```

#### Via NPX (Regra universal de agentes):
```bash
npx skills add JuliusBrussee/caveman
```

---

### 2.2 Instalação no Projeto Local (`proj_livros`)

Para garantir que todos os agentes que operam neste repositório apliquem o estilo Caveman de forma persistente, o método recomendado é adicionar a regra no arquivo de instruções de agentes (`.agents/AGENTS.md` ou `AGENTS.md`):

```markdown
## Regra Caveman (Economia Severa de Output Tokens)
- Respostas telegráficas, diretas e concisas.
- Cortar saudações, desculpas e enrolações.
- Preservar código, difs, comandos e erros byte a byte.
- Falar no idioma do usuário, mas em estilo caveman (poucas palavras, alto impacto).
```

Você também pode comprimir arquivos de instrução do projeto com o comando:
```bash
npx caveman-compress AGENTS.md
```
*(Reduz ~46% dos tokens de entrada de regras do projeto).*

---

## 3. Níveis de Compressão (`Níveis de Grunt`)

Você pode alternar o nível de compressão com o comando `/caveman <level>`:

| Nível | Exemplo de Resposta | Redução de Output |
| :--- | :--- | :---: |
| **Normal** | O motivo pelo qual o componente renderiza é porque um novo objeto é criado a cada render. Envolva-o em useMemo. | **0%** |
| **`lite`** | Envolva objeto em `useMemo`. Novo ref criado a cada render. | **~40%** |
| **`full`** *(padrão)* | Novo ref a cada render. Objeto prop inline = re-render. Usar `useMemo`. | **~65%** |
| **`ultra`** | Novo ref/render. `useMemo` nele. | **~80%** |
| **`wenyan`** | Chinês clássico denso (máxima densidade por token). | **~85%** |

---

## 4. Principais Comandos

| Comando | Função |
| :--- | :--- |
| `/caveman [lite\|full\|ultra]` | Ativa a compressão no nível desejado na sessão atual |
| `/caveman-commit` | Gera mensagens de commit no padrão Conventional Commits com assunto $\le$ 50 caracteres |
| `/caveman-review` | Comentários de code review em uma única linha (ex: `L42: 🔴 bug: user null. Add guard.`) |
| `/caveman-stats` | Exibe o total de tokens economizados e valor em USD na sessão e acumulado |
| `/caveman-compress <arquivo>` | Reescreve arquivos de instrução/memória no formato caveman |

---

## 5. Combinação Potencializada: LeanCTX + Caveman

Para atingir a **Máxima Economia Possível de Tokens**:

```
 ┌────────────────────────────────────────────────────────┐
 │ LeanCTX (Filtra Input Tokens: Arquivos AST + Shell)   │  → Economiza 60% a 90% dos INPUT tokens
 ├────────────────────────────────────────────────────────┤
 │ Caveman (Filtra Output Tokens: Respostas Telegráficas) │  → Economiza 65% dos OUTPUT tokens
 └────────────────────────────────────────────────────────┘
```

1. **LeanCTX** reduz o contexto que a IA lê de 2.000 tokens para ~13-100 tokens.
2. **Caveman** reduz o texto que a IA escreve de 200 tokens para ~35 tokens.
3. **Resultado:** Custo e tempo de resposta reduzidos drasticamente sem perda de qualidade no código.
