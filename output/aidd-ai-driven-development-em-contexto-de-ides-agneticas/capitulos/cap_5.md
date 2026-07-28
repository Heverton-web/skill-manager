# Capítulo 5 — Spec-Driven Development na Prática

Se o Context Engineering é a infraestrutura, o Spec-Driven Development (SDD) é a metodologia. Enquanto o primeiro garante que o agente tenha o contexto certo, o segundo garante que o agente faça a coisa certa — e somente ela.

Este capítulo apresenta os seis elementos de uma especificação executável, os três níveis de rigor do SDD e as ferramentas que viabilizam essa abordagem no dia a dia.

## Os 6 elementos de uma especificação executável

Uma especificação para agentes de IA não é um documento de requisitos tradicional. Ela não precisa ser longa — precisa ser **precisa**, **inequívoca** e **verificável**. Seis elementos são essenciais.

### 1. Outcomes (Resultados Esperados)

O que significa "pronto"? Cada especificação deve definir critérios de sucesso observáveis. Não "a feature deve funcionar bem", mas "o endpoint GET /users retorna 200 com array de usuários; o POST /users retorna 201 com o usuário criado; todas as validações retornam 400 com mensagem de erro".

### 2. Scope Boundaries (Limites de Escopo)

O que está dentro e o que está **fora** do escopo. Este é o elemento mais negligenciado e o que mais previne desvios. Exemplo: "Dentro: CRUD de usuários com campos nome, email, senha. Fora: autenticação (já existe), recovery de senha (será feito depois), roles e permissões (escopo separado)."

### 3. Constraints & Assumptions (Restrições e Premissas)

O agente precisa saber o que não pode mudar. Stack tecnológica, APIs disponíveis, limites de performance, convenções do projeto. Exemplo: "Banco PostgreSQL via Prisma ORM. Autenticação via JWT com middleware @Auth(). UI em React com Tailwind. Não usar bibliotecas externas sem aprovação."

### 4. Prior Decisions (Decisões Prévias)

O que já foi decidido para não ser reinventado. Decisões arquiteturais, padrões de design, escolhas de bibliotecas. Exemplo: "Usar repository pattern. Toda query complexa vai em um service. Testes com Vitest. Nomes em inglês."

### 5. Task Breakdown (Decomposição em Tarefas)

A especificação não deve ser um bloco monolítico. Decompor em tarefas granulares que o agente pode executar sequencialmente, cada uma com seu próprio critério de verificação.

### 6. Verification Criteria (Critérios de Verificação)

Como saber se a implementação está correta? Testes que devem passar, linters que devem rodar sem erros, checks de segurança, validação de tipos. Exemplo: "Testes unitários com coverage > 80%. Lint sem warnings. TypeScript sem erros. Postman collection validando todos os endpoints."

![Template visual dos 6 elementos do SDD](../imagens/cap_5_diagrama_1.svg)

![Template visual dos 6 elementos do SDD](../imagens/cap_5_diagrama_1.svg)

![Espectro de rigor do SDD: Spec-First, Spec-Anchored, Spec-As-Source](../imagens/cap_5_diagrama_2.svg)

### Exemplo: spec vaga vs. spec executável

**Spec vaga (vai gerar retrabalho):**
```
Criar uma tela de login com email e senha.
```

**Spec executável (vai gerar código pronto):**
```
Outcomes: Tela de login funcional com autenticação JWT.
Scope: Dentro - formulário email/senha, validação client-side, chamada API /auth/login, redirect pós-login, mensagem de erro. Fora - recovery de senha, OAuth social, registro.
Constraints: React + Tailwind + React Hook Form + Zod. API em /auth/login (já existe). Tokens em httpOnly cookie via response.
Prior Decisions: Usar padrão do projeto: componente em src/components/, hook em src/hooks/, página em src/pages/.
Tasks: (1) Criar LoginPage com formulário; (2) Criar hook useAuth; (3) Conectar à API; (4) Adicionar validação; (5) Testar fluxo completo.
Verification: Testes do formulário passando. Lint sem erros. Fluxo manual validado via navegador.
```

## Níveis de rigor do SDD

O SDD não é uma abordagem binária — existe um espectro de rigor que as equipes adotam conforme a maturidade e a criticidade do projeto.

### Nível 1: Spec-First (Guiado Inicial)

A especificação é escrita antes do código para guiar o agente, mas não é mantida como documentação viva. Após o código gerado, a spec pode ser arquivada ou descartada.

**Quando usar:** Prototipação rápida, tarefas bem compreendidas, desenvolvedores experientes que sabem o que querem.

**Risco:** Sem sincronia entre spec e código, a especificação fica desatualizada rapidamente.

### Nível 2: Spec-Anchored (Documentação Viva)

A especificação é mantida em sincronia contínua com o código por meio de testes e contratos automatizados. Mudanças no código que violam a spec são detectadas em CI. É o equivalente funcional do Behavior-Driven Development (BDD), mas adaptado para agentes.

**Quando usar:** Features em produção, equipes médias, projetos que exigem rastreabilidade.

**Risco:** Requer disciplina para manter specs atualizadas; pode gerar *Markdown overload*.

### Nível 3: Spec-As-Source (A Especificação é o Código-Fonte)

O desenvolvedor edita estritamente a especificação em linguagem estruturada. O código é inteiramente gerado e regenerado por agentes a partir da spec. Edição manual do código é proibida.

**Quando usar:** Sistemas críticos, conformidade regulatória, equipes que querem máximo controle sobre o que o agente produz.

**Risco:** Maior custo de setup, requer ferramentas especializadas (Tessl), pode ser excessivo para projetos simples.

![Espectro de rigor do SDD: Spec-First, Spec-Anchored, Spec-As-Source](../imagens/cap_5_diagrama_2.svg)

## Ferramentas e integração no fluxo de trabalho

### GitHub Spec Kit

Toolkit open-source baseado em CLI que estrutura o ciclo de vida SDD. Comandos principais:
- `/speckit.constitution` — Estabelecer princípios do projeto
- `/speckit.specify` — Capturar requisitos em especificações
- `/speckit.plan` — Definir plano de implementação técnica
- `/speckit.tasks` — Decompor em tarefas
- `/speckit.implement` — Executar implementação via agente

### Tessl

Plataforma focada nos níveis mais rigorosos de SDD (Spec-Anchored e Spec-As-Source). Trata especificações como componentes gerenciáveis que geram código via MCP servers.

### Amazon Kiro & Q Developer

Oferecem suporte a fluxos adaptativos com *steering files*, guiando o desenvolvedor pelas fases de requisitos, design e tarefas, similar ao SDD mas integrado ao ecossistema AWS.

![Fluxo de integração SDD no pipeline de desenvolvimento](../imagens/cap_5_diagrama_3.svg)

### Integração com Git e CI/CD

O SDD funciona melhor quando as especificações são versionadas como código:
- **PRs de spec:** Antes do PR de código, um PR de especificação é aberto e revisado
- **Validação em CI:** O pipeline verifica se a implementação está aderente à spec
- **Spec drift detection:** Mudanças no código que desviam da spec são sinalizadas automaticamente

![Fluxo de integração SDD no pipeline de desenvolvimento](../imagens/cap_5_diagrama_3.svg)

---

Neste capítulo, vimos os seis elementos que transformam uma especificação vaga em um contrato executável para agentes, os três níveis de rigor do SDD e as ferramentas que integram essa abordagem no fluxo de trabalho. No próximo capítulo, exploraremos o AGENTS.md como padrão aberto para portabilidade de instruções entre ferramentas.
