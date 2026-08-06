# -*- coding: utf-8 -*-
"""Reestrutura caps 7-10 do Livro 5 para o padrao EITA-V2."""
import re
from pathlib import Path

SLUG = "livros/claude-md-agents-md-e-rules-engenharia-da-memoria-e-das-regras-do-projeto"

REFERENCIAS = (
    "[1] ANTHROPIC. **Memory: how Claude remembers your project**. Claude Code Documentation, 2025-2026. Disponivel em: https://docs.anthropic.com/en/docs/claude-code/memory. Acesso em: 5 ago. 2026.\n"
    "[2] ANTHROPIC. **Overview: Claude Code**. Claude Code Documentation, 2025-2026. Disponivel em: https://docs.anthropic.com/en/docs/claude-code/overview. Acesso em: 5 ago. 2026.\n"
    "[3] AGENTS.MD. **AGENTS.md: the standard for AI agent instructions**. Agentic AI Foundation / OpenAI, ago. 2025. Disponivel em: https://agents.md/. Acesso em: 5 ago. 2026.\n"
    "[4] LINUX FOUNDATION. **Linux Foundation announces the formation of the Agentic AI Foundation**. Linux Foundation Press Release, 9 dez. 2025. Disponivel em: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation. Acesso em: 5 ago. 2026.\n"
    "[5] AGENTIC AI FOUNDATION. **Agentic AI Foundation official portal**. AAIF, 2025-2026. Disponivel em: https://aaif.io/. Acesso em: 5 ago. 2026.\n"
    "[6] OSMANI, Addy. **15 AGENTS.md - engineering guide to AGENTS.md**. Addy Osmani, 2025-2026. Disponivel em: https://addyosmani.com/agents/15-agents-md/. Acesso em: 5 ago. 2026.\n"
    "[7] AUGMENT CODE. **How to build AGENTS.md: construction guide**. Augment Code Guides, 2025-2026. Disponivel em: https://www.augmentcode.com/guides/how-to-build-agents-md. Acesso em: 5 ago. 2026.\n"
    "[8] CURSOR. **Rules: Cursor Documentation**. Cursor / Anysphere, 2025-2026. Disponivel em: https://cursor.com/docs/rules. Acesso em: 5 ago. 2026.\n"
    "[9] AGYN. **AGENTS.md vs CLAUDE.md: does Claude Code or Codex read both?**. Agyn Blog, jun. 2026. Disponivel em: https://agyn.io/blog/claude-md-agents-md-compatibility. Acesso em: 5 ago. 2026.\n"
    "[10] OPENAI. **Codex: AGENTS.md and coding agents**. OpenAI Documentation, 2025-2026. Disponivel em: https://openai.com/index/introducing-codex/. Acesso em: 5 ago. 2026.\n"
    "[11] GITHUB. **GitHub Copilot: repository instructions and AGENTS.md support**. GitHub Documentation, 2025-2026. Disponivel em: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions. Acesso em: 5 ago. 2026.\n"
    "[12] GITHUB. **GitHub Copilot Coding Agent: reading repository instructions**. GitHub Changelog, 2025-2026. Disponivel em: https://github.blog/. Acesso em: 5 ago. 2026.\n"
    "[13] ANTHROPIC. **Writing tools for AI agents - using AI agents**. Anthropic Engineering Blog, set. 2025. Disponivel em: https://www.anthropic.com/engineering/writing-tools-for-agents. Acesso em: 5 ago. 2026.\n"
    "[14] ANTHROPIC. **Effective context engineering for AI agents**. Anthropic Engineering Blog, set. 2025. Disponivel em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 5 ago. 2026.\n"
    "[15] ANTHROPIC. **Introducing the Model Context Protocol**. Anthropic News, 25 nov. 2024. Disponivel em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 5 ago. 2026.\n"
    "[16] MODEL CONTEXT PROTOCOL. **Architecture**. MCP Specification 2025-11-25, 25 nov. 2025. Disponivel em: https://modelcontextprotocol.io/specification/2025-11-25/architecture. Acesso em: 5 ago. 2026.\n"
    "[17] LINUX FOUNDATION. **Agentic AI Foundation: governance of foundational agentic infrastructure**. Linux Foundation Blog, dez. 2025. Disponivel em: https://www.linuxfoundation.org/blog/. Acesso em: 5 ago. 2026.\n"
    "[18] CURSOR. **Best practices for rules and context**. Cursor Documentation, 2025-2026. Disponivel em: https://cursor.com/docs/context/rules. Acesso em: 5 ago. 2026.\n"
    "[19] AIDER. **AGENTS.md support and multi-tool interoperability**. Aider Documentation, 2025-2026. Disponivel em: https://aider.chat/docs/repomap.html. Acesso em: 5 ago. 2026.\n"
    "[20] ANTHROPIC. **Claude Code best practices: memory and configuration**. Anthropic Engineering Blog, 2025-2026. Disponivel em: https://www.anthropic.com/engineering/claude-code-best-practices. Acesso em: 5 ago. 2026."
)

DADOS = {
    "07": {
        "ilustra": (
            "### 3.1 A Analogia do Mapa do Bairro\n\n"
            "A analogia do mapa do bairro ilumina as regras condicionais [6]. Um mapa da cidade inteira (o AGENTS.md global) e grande demais para carregar em todo passeio; o mapa do bairro (a regra condicional) e pequeno e cobre exatamente onde o viajante esta [6]. As regras condicionais sao os mapas de bairro: precisas, locais e carregadas apenas quando necessarias [6].\n\n"
            "```mermaid\nflowchart TD\n"
            "    A[Arquivo em edicao] --> B{Glob casa?}\n"
            "    B -- Sim --> C[Regra condicional carregada]\n"
            "    B -- Nao --> D[Regra fora do contexto]\n"
            "    C --> E[Agente segue a regra local]\n"
            "    D --> F[Contexto enxuto]\n"
            "    E --> G[Convencao obedecida]\n"
            "    F --> G\n```\n\n"
            "O diagrama mostra o mecanismo de selecao: o glob e o guardiao da fronteira [6]."
        ),
        "tecnica": (
            "### 4.1 Modelando o Escopo de uma Regra Condicional\n\n"
            "O primeiro instrumento do engenheiro de regras e modelar o escopo [6]. O codigo abaixo demonstra o parse do frontmatter e a avaliacao do glob [6]:\n\n"
            "```python\n"
            "from dataclasses import dataclass, field\n"
            "from fnmatch import fnmatch\n\n\n"
            "@dataclass\n"
            "class RegraCondicional:\n"
            "    descricao: str\n"
            "    globs: list = field(default_factory=list)\n"
            "    always_apply: bool = False\n"
            "    conteudo: str = \"\"\n\n"
            "    def aplica_a(self, caminho: str) -> bool:\n"
            "        if self.always_apply:\n"
            "            return True\n"
            "        return any(fnmatch(caminho, g) for g in self.globs)\n\n\n"
            "REGRA_EXEMPLO = RegraCondicional(\n"
            "    descricao=\"Regras de componentes do design system\",\n"
            "    globs=[\"src/components/ui/**/*.{ts,tsx}\"],\n"
            "    conteudo=\"Usar shadcn/ui como base; props mescladas com tailwind-merge.\",\n"
            ")\n\n\n"
            "def regras_para_arquivo(regras: list, caminho: str) -> list:\n"
            "    return [r for r in regras if r.aplica_a(caminho)]\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    print(REGRA_EXEMPLO.aplica_a(\"src/components/ui/Button.tsx\"))\n"
            "    print(REGRA_EXEMPLO.aplica_a(\"src/api/routes.ts\"))\n"
            "```\n\n"
            "O modelo demonstra o coracao do capitulo: o par (condicao, acao) [6]."
        ),
    },
    "08": {
        "ilustra": (
            "### 3.1 A Analogia do Sistema Juridico em Camadas\n\n"
            "A analogia do sistema juridico ilumina a cascata [1][9]. A constituicao (AGENTS.md raiz) define os principios; as leis federais (CLAUDE.md raiz) definem as politicas; as leis estaduais (AGENTS.md de um diretorio) definem as convencoes locais; e as leis municipais (regras condicionais) definem o detalhe [1][9].\n\n"
            "```mermaid\nflowchart TD\n"
            "    A[AGENTS.md raiz: constituicao] --> B[CLAUDE.md raiz: politicas]\n"
            "    B --> C[AGENTS.md do diretorio: leis locais]\n"
            "    C --> D[Regras condicionais: detalhe]\n"
            "    D --> E[Instrucao efetiva para o arquivo]\n"
            "    F[Teste da cascata no CI] --> G[Valida completude, duplicacao, contradicao]\n"
            "    G --> E\n```\n\n"
            "O diagrama mostra a soma ordenada das camadas e o teste que a valida [1][9]."
        ),
        "tecnica": (
            "### 4.1 Modelando a Cascata de Instrucoes\n\n"
            "O primeiro instrumento do engenheiro de cascata e modelar a soma das camadas [1][9]:\n\n"
            "```python\n"
            "from pathlib import Path\n\n\n"
            "class Cascata:\n"
            "    def __init__(self, raiz: Path):\n"
            "        self.raiz = raiz\n\n"
            "    def camadas_para(self, caminho: Path) -> list:\n"
            "        camadas = []\n"
            "        for pasta in list(caminho.parents)[::-1] + [self.raiz]:\n"
            "            try:\n"
            "                pasta.relative_to(self.raiz)\n"
            "            except ValueError:\n"
            "                continue\n"
            "            agents = pasta / \"AGENTS.md\"\n"
            "            claude = pasta / \"CLAUDE.md\"\n"
            "            if agents.exists():\n"
            "                camadas.append(agents)\n"
            "            if claude.exists():\n"
            "                camadas.append(claude)\n"
            "        return camadas\n\n"
            "    def instrucao_efetiva(self, caminho: Path) -> str:\n"
            "        partes = []\n"
            "        for arquivo in self.camadas_para(caminho):\n"
            "            partes.append(f\"# {arquivo}\\n{arquivo.read_text(encoding='utf-8')}\")\n"
            "        return \"\\n\\n\".join(partes)\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    c = Cascata(Path(\".\"))\n"
            "    print(len(c.camadas_para(Path(\"packages/api/src/routes/users.ts\"))))\n"
            "```\n\n"
            "O modelo demonstra a localidade e a aditividade da cascata [1][9]."
        ),
    },
    "09": {
        "ilustra": (
            "### 3.1 A Analogia da Fotografia e da Pratica\n\n"
            "A analogia da fotografia ilumina o drift [1][7]. A pratica e a realidade; o documento e a fotografia da realidade [1][7]. Toda fotografia envelhece: a paisagem muda, e a foto mostra o passado [1][7]. O drift e a diferenca entre a paisagem atual e a fotografia [1][7].\n\n"
            "```mermaid\nflowchart TD\n"
            "    A[Pratica real: a paisagem] --> B{Comparacao com o contrato}\n"
            "    B -- Convergem --> C[Contrato verdadeiro]\n"
            "    B -- Divergem --> D[Drift detectado]\n"
            "    D --> E[Auditoria: qual esta certo?]\n"
            "    E --> F[Corrigir o contrato]\n"
            "    F --> C\n"
            "    D --> G[Reescrever a partir da pratica]\n"
            "    G --> C\n```\n\n"
            "O diagrama mostra o ciclo anti-drift: comparar, detectar, decidir e corrigir [1][7]."
        ),
        "tecnica": (
            "### 4.1 Modelando o Indice de Drift\n\n"
            "O primeiro instrumento do engenheiro anti-drift e medir [1][7]:\n\n"
            "```python\n"
            "from dataclasses import dataclass\n\n\n"
            "@dataclass\n"
            "class Declaracao:\n"
            "    texto: str\n"
            "    verificavel: bool\n"
            "    confirmada: bool = False\n\n\n"
            "def indice_drift(declaracoes: list) -> dict:\n"
            "    verificaveis = [d for d in declaracoes if d.verificavel]\n"
            "    contraditas = [d for d in verificaveis if not d.confirmada]\n"
            "    taxa = round(100 * len(contraditas) / max(len(verificaveis), 1), 1)\n"
            "    return {\n"
            "        \"verificaveis\": len(verificaveis),\n"
            "        \"contraditas\": len(contraditas),\n"
            "        \"taxa_drift_pct\": taxa,\n"
            "        \"saudavel\": taxa <= 10,\n"
            "    }\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    decls = [\n"
            "        Declaracao(\"Usamos TypeScript\", True, True),\n"
            "        Declaracao(\"Testes com Vitest\", True, False),\n"
            "        Declaracao(\"Sem any implicito\", True, True),\n"
            "    ]\n"
            "    print(indice_drift(decls))\n"
            "```\n\n"
            "O modelo demonstra a medicao da Secao 9.4 [1][7]."
        ),
    },
    "10": {
        "ilustra": (
            "### 3.1 A Analogia da Infraestrutura Invisivel\n\n"
            "A analogia da infraestrutura invisivel ilumina a memoria de projeto [1][7]. O entendimento compartilhado e como a fundacao de um predio: ninguem a ve, mas tudo depende dela [1][7]. Sem fundacao, o predio racha; sem memoria, o trabalho agentico racha [1][7].\n\n"
            "```mermaid\nflowchart TD\n"
            "    A[Contrato: o que sabemos] --> B[Cascata: onde vive]\n"
            "    B --> C[Regras: com que limite]\n"
            "    C --> D[Drift: com que verdade]\n"
            "    D --> E[Operacao: o ciclo continuo]\n"
            "    E --> A\n"
            "    F[Entendimento compartilhado] --> E\n"
            "    E --> G[Agente opera com o entendimento do time]\n```\n\n"
            "O diagrama mostra a disciplina como sistema em ciclo [1][7][9]."
        ),
        "tecnica": (
            "### 4.1 Modelando o Sistema de Memoria de Projeto\n\n"
            "O primeiro instrumento do engenheiro de memoria e modelar o sistema [1][7]:\n\n"
            "```python\n"
            "from dataclasses import dataclass, field\n"
            "from datetime import date\n\n\n"
            "@dataclass\n"
            "class MemoriaProjeto:\n"
            "    contrato: str = \"\"\n"
            "    camadas: list = field(default_factory=list)\n"
            "    ultima_revisao: date = date.today()\n\n"
            "    def adicionar_camada(self, nome: str, caminho: str):\n"
            "        self.camadas.append({\"nome\": nome, \"caminho\": caminho})\n\n"
            "    def saudavel(self, indice_drift_pct: float, cobertura_pct: float) -> dict:\n"
            "        return {\n"
            "            \"drift_ok\": indice_drift_pct <= 10,\n"
            "            \"cobertura_ok\": cobertura_pct >= 80,\n"
            "            \"revisao_recente\": (date.today() - self.ultima_revisao).days <= 90,\n"
            "        }\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    m = MemoriaProjeto(contrato=\"AGENTS.md\")\n"
            "    m.adicionar_camada(\"api\", \"packages/api/AGENTS.md\")\n"
            "    print(m.saudavel(5.0, 90.0))\n"
            "```\n\n"
            "O modelo demonstra a sintese do Capitulo 10: o sistema com metricas de saude [1][7]."
        ),
    },
}

for cap, dados in DADOS.items():
    n = int(cap)
    p = Path("output") / SLUG / "capitulos" / f"cap_{cap}.md"
    t = p.read_text(encoding="utf-8")
    # 1. Converter subsecoes ## N.x para ### N.x
    t = re.sub(rf"^##\s*{n}\.(\d+)\s+(.+)$", rf"### {n}.\1 \2", t, flags=re.M)
    # 2. Converter conclusao (agora ###) para ## 6. Conclusao
    t = re.sub(rf"^###\s*{n}\.11\s+Conclus.*$", "## 6. Conclusao", t, flags=re.M)
    # 3. Remover secao de referencias antiga
    t = re.sub(r"##\s*Refer[êe]ncias.*$", "", t, flags=re.S)
    t = t.rstrip()
    # 4. Inserir ## 1. Introducao apos o titulo
    linhas = t.split("\n")
    for idx, linha in enumerate(linhas):
        if linha.startswith("# "):
            linhas.insert(idx + 1, "")
            linhas.insert(idx + 2, "## 1. Introducao")
            break
    t = "\n".join(linhas)
    # 5. Inserir ## 2. Explica antes do primeiro ###
    idx = t.find("### ")
    t = t[:idx] + "## 2. Explica\n\n" + t[idx:]
    # 6. Inserir Ilustra e Tecnica antes da Conclusao
    conc = "## 6. Conclusao"
    bloco = "## 3. Ilustra\n\n" + dados["ilustra"] + "\n\n## 4. Tecnica\n\n" + dados["tecnica"] + "\n\n## 6. Conclusao"
    if conc in t:
        t = t.replace(conc, bloco, 1)
    # 7. Anexar Referencias
    t = t.rstrip() + "\n\n## 7. Referencias\n\n" + REFERENCIAS + "\n"
    p.write_text(t, encoding="utf-8")
    print(f"cap_{cap} OK - {len(t)} chars")
