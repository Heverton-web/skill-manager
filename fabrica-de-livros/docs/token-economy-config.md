# Token Economy Configuration

> Adaptado de [drona23/claude-token-efficient](https://github.com/drona23/claude-token-efficient)
> Integrado com skills próprias: `lean-ctx`, `caveman`, `headroom`, `calcular-gastos-sessao`

---

## Regras de Economia de Tokens

### 1. Leitura Inteligente de Arquivos
- Leia arquivos existentes antes de escrever. Não releia a menos que tenham mudado.
- Pule arquivos >100KB a menos que seja estritamente necessário.
- Use `grep`/`ripgrep` para localizar seções específicas em vez de ler arquivos inteiros.

### 2. Saída Concisa
- Seja minucioso no raciocínio, conciso na saída.
- Sem aberturas ou fechamentos bajuladores (syconphantic openers/closing fluff).
- Sem emojis ou travessões (em-dashes) desnecessários.
- Respostas diretas e telegráficas — estilo **caveman**.

### 3. Precisão Técnica
- Nunca adivinhe APIs, versões, flags, commit SHAs ou nomes de pacotes.
- Verifique lendo código ou documentação antes de afirmar.

### 4. Compressão de Logs/Outputs (headroom)
- Outputs de comando com >7 linhas: manter apenas as primeiras 3 + últimas 4 linhas.
- Priorizar `grep_search` antes de `view_file` — ler assinaturas antes de corpos completos.

### 5. Cálculo de Gastos (calcular-gastos-sessao)
- Ao final de cada sessão, calcule tokens consumidos e estimativa financeira.
- Registre no RTK SCRATCHPAD para memória entre sessões.

### 6. Gerenciamento de Contexto (lean-ctx)
- Contexto é recurso finito. Cada skill carregada consome tokens de input.
- Remova skills não utilizadas do fluxo ativo.
- Use `rtk-memory` para persistir aprendizados e evitar repetição de análise.

---

## Integração com Skills Instaladas

| Skill | Função | Ativada |
|-------|--------|---------|
| `lean-ctx` | Economia de contexto: grep antes de read | ✅ |
| `caveman` | Respostas telegráficas, diffs cirúrgicos | ✅ |
| `caveman-compress` | Comprimir arquivos de memória p/ caveman format | ✅ (global) |
| `headroom` | Comprimir logs >7 linhas | ✅ |
| `calcular-gastos-sessao` | Calcular tokens + custo por sessão | ✅ |
| `token-coach` | Coach de economia de tokens | ✅ (universal) |
| `token-dashboard` | Dashboard de consumo de tokens | ✅ (universal) |
| `token-optimizer` | Otimizador multi-superfície de tokens | ✅ (universal) |
| `fleet-auditor` | Auditor de frota de agentes | ✅ (universal) |
| `llm-cost-optimizer` | Otimizador de custo LLM | ✅ |
| `context-engine` | Gerenciamento de contexto | ✅ |

---

## Modos de Economia

### Modo Agressivo (M-drona23-v8)
```
## Approach
- Read existing files before writing. Don't re-read unless changed.
- Thorough in reasoning, concise in output.
- Skip files over 100KB unless required.
- No sycophantic openers or closing fluff.
- No emojis or em-dashes.
- Do not guess APIs, versions, flags, commit SHAs, or package names.
```

### Modo Normal
- Mantém abertura e fechamento educados mas sem bajulação.
- Emojis permitidos apenas quando comunicam informação (❌, ✅, ⚠️).
- Sempre priorizar concisão sobre formalidade.

### Modo Caveman (máxima economia)
- Apenas diffs cirúrgicos.
- Sem preâmbulos ou fechamentos.
- Frases telegráficas.
- Números crus em vez de explicações.
