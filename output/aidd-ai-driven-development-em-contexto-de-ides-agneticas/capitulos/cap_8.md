# Capítulo 8 — Orquestração Multi-Agente e Fluxos de Trabalho

Nem toda tarefa pode ou deve ser executada por um único agente. Tarefas complexas — como o desenvolvimento de uma feature completa em um sistema de microserviços — envolvem múltiplas competências: análise de impacto, implementação, testes de integração, revisão de segurança, validação de performance.

O padrão emergente para esses cenários é a **orquestração multi-agente**: múltiplos agentes especializados colaborando sob a supervisão de um orquestrador, com cada agente fazendo o que faz de melhor.

## Padrões de orquestração

### Padrão Sequencial

O mais simples: uma cadeia de agentes onde a saída de um alimenta a entrada do próximo. Útil para pipelines bem definidos como "analisar → planejar → implementar → revisar → deploy".

**Vantagem:** Simplicidade, rastreabilidade clara, cada agente tem escopo definido.
**Desvantagem:** Qualquer gargalo na cadeia paralisa o fluxo inteiro.

### Padrão Supervisor

Um agente orquestrador (supervisor) coordena agentes subordinados, delegando tarefas, consolidando resultados e tomando decisões sobre o fluxo. O padrão mais comum em 2026.

**Vantagem:** Coordenação centralizada, decisões arquiteturais consistentes.
**Desvantagem:** O supervisor pode ser um gargalo cognitivo e consumir muitos tokens.

### Padrão Debate

Múltiplos agentes recebem o mesmo problema e discutem soluções concorrentes. Um agente moderador (ou voto) escolhe a melhor abordagem. Inspirado em ensaios clínicos e júris.

**Vantagem:** Qualidade superior em decisões complexas, múltiplas perspectivas.
**Desvantagem:** Custo computacional alto, consenso pode ser difícil para problemas abertos.

![Padrões de orquestração multi-agente](../imagens/cap_8_diagrama_1.svg)

### Padrão Swarm

Múltiplos agentes atuam em paralelo sem um coordenador central, cada um em seu escopo, com comunicação peer-to-peer via eventos. Inspirado em colônias de formigas ou abelhas.

**Vantagem:** Escalabilidade horizontal, resiliência a falhas individuais.
**Desvantagem:** Difícil de debugar, comportamento emergente imprevisível.

![Padrões de orquestração multi-agente](../imagens/cap_8_diagrama_1.svg)

## Frameworks de orquestração

### CrewAI

Framework Python para orquestração multi-agente baseado em papéis. Cada agente tem um papel, objetivo e conjunto de ferramentas. Um processo (sequencial ou hierárquico) define como eles colaboram.

```python
from crewai import Agent, Task, Crew

analista = Agent(role="Analyst", goal="Analisar requisitos", ...)
dev = Agent(role="Developer", goal="Implementar solução", ...)
tester = Agent(role="Tester", goal="Validar implementação", ...)

task = Task(description="Implementar feature X", agent=analista)
crew = Crew(agents=[analista, dev, tester], process="hierarchical")
```

### LangGraph

Framework da LangChain para definir fluxos de agentes como grafos de estados. Cada nó é um passo do agente, cada aresta é uma transição condicional. Suporta loops, branching e paralelismo.

**Diferencial:** Controle fino sobre o fluxo de execução, ideal para workflows com múltiplos caminhos condicionais (ex: se teste falha, volta para implementação).

### AutoGen (Microsoft)

Framework focado em conversação multi-agente com suporte a código. Agentes conversam entre si para resolver problemas, com um agente "assistant" gerando código e um "user proxy" executando e retornando resultados.

## Ciclos autônomos e fluxos de qualidade

### Plan-Act-Observe

O ciclo fundamental dos coding agents:
1. **Plan:** Agente analisa o problema e cria um plano
2. **Act:** Agente executa o plano (edita código, roda comandos)
3. **Observe:** Agente observa o resultado (testes passaram? erros?)
4. **Iterate:** Se necessário, ajusta o plano e repete

### Test-Driven Repair

Variação onde os testes são escritos PRIMEIRO, e o agente implementa até que os testes passem:
1. Escrever teste (humano ou agente especifica)
2. Agente implementa código
3. Rodar teste
4. Se falha: agente corrige e volta ao passo 3
5. Se passa: feature concluída

![Fluxo de verificação adversarial multi-agente](../imagens/cap_8_diagrama_2.svg)

### Adversarial Verification

Um segundo agente (ou o mesmo em modo adversarial) tenta ativamente quebrar a solução proposta — encontrar bugs, vulnerabilidades, casos de borda não cobertos. Inspirado no Fable Method (Capítulo 9).

![Fluxo de verificação adversarial multi-agente](../imagens/cap_8_diagrama_2.svg)

---

Neste capítulo, exploramos os principais padrões de orquestração multi-agente, os frameworks que os implementam e os ciclos de qualidade que garantem resultados confiáveis. No próximo capítulo, mergulharemos no Fable Method — uma metodologia completa para loops de agentes confiáveis com verificação adversarial.
