# Capítulo 3 — Métricas, SWE-bench e a Lacuna de Percepção

O entusiasmo em torno dos coding agents gerou uma enxurrada de alegações sobre produtividade. "Agentes escrevem código 10x mais rápido", "80% do código será gerado por IA", "a engenharia de software como conhecemos acabou". Mas quando os dados reais são examinados, o quadro é mais matizado — e, em alguns aspectos, preocupante.

Este capítulo examina o que os benchmarks realmente medem, o paradoxo entre atividade e entrega que emerge quando agentes aceleram a produção de código, e a surpreendente lacuna entre a percepção dos desenvolvedores e a realidade mensurada.

## SWE-bench e o panorama de benchmarks de coding agents

### O que é SWE-bench

Criado por pesquisadores de Princeton, o SWE-bench nasceu de uma necessidade simples: medir se modelos de linguagem conseguem resolver issues reais do GitHub. Diferente de benchmarks de programação competitiva (como HumanEval ou Codeforces), que testam trechos isolados, o SWE-bench apresenta ao modelo uma issue real de um repositório open-source — com descrição ambígua, contexto de código existente e múltiplos arquivos envolvidos.

O modelo precisa navegar pelo repositório, entender o problema, identificar a causa raiz, implementar a correção e garantir que todos os testes existentes continuem passando. É uma tarefa muito mais próxima do trabalho real de engenharia.

### A evolução: SWE-bench Verified e SWE-bench Pro

O SWE-bench original tinha problemas conhecidos: instâncias com bugs nos próprios testes, descrições ambíguas demais e casos onde a solução correta não era unívoca. Isso levou à criação de duas variações:

**SWE-bench Verified (2025):** Um subconjunto de 500 instâncias filtradas e validadas por humanos, retiradas de repositórios populares como Django, Flask, scikit-learn e SymPy. Cada instância foi verificada para garantir que o test suite é correto e que a solução esperada é inequívoca.

**SWE-bench Pro (2026):** Uma evolução desenhada para medir tarefas de engenharia de longa duração — aquelas que um desenvolvedor humano levaria horas ou dias para concluir. Contém 1.865 problemas de 41 repositórios ativamente mantidos, divididos em conjuntos públicos, hold-out e comerciais.

### Scores dos modelos frontier (2026)

Os resultados mais recentes mostram uma proximidade assustadora da saturação no SWE-bench Verified:

| Modelo | SWE-bench Verified | SWE-bench Pro |
|--------|-------------------|--------------|
| Claude Opus 5 | **96.0%** | — |
| Claude Mythos 5 | 95.5% | **80.3%** |
| GPT-5 | ~90% | ~72% |
| Gemini Ultra 2 | ~88% | ~70% |

![Evolução dos scores SWE-bench (2024-2026)](../imagens/cap_3_diagrama_1.svg)

### Limitações e o que os benchmarks não medem

Apesar dos números impressionantes, é crucial entender o que SWE-bench **não** mede:

- **Tarefas arquiteturais:** SWE-bench testa correção de bugs e implementação de features pequenas, não design de sistemas, refatoração de larga escala ou decisões arquiteturais.
- **Qualidade de código:** Um PR que resolve a issue mas introduz dívida técnica ou vulnerabilidades ainda conta como "correto" no benchmark.
- **Contexto empresarial:** Issues de repositórios open-source bem documentados são diferentes de tickets ambíguos em codebases corporativos legados.

Como apontam auditorias independentes (incluindo avaliações da OpenAI), os benchmarks de SWE-bench são indicadores direcionais, não instrumentos de procurement. Um score de 96% não significa que 96% das tarefas do mundo real serão resolvidas.

## O paradoxo da produtividade: atividade vs. entrega

### O aumento de atividade

Equipes que adotam coding agents registram aumentos dramáticos em métricas de atividade. Estudos da Faros AI e DORA mostram:

- **Aumento de ~100%** no volume de pull requests abertas por desenvolvedor
- **Aumento significativo** no tamanho médio das alterações (mais arquivos por PR)
- **Redução do tempo** para abrir o primeiro PR em tarefas greenfield

À primeira vista, esses números sugerem um salto de produtividade. Mas o quadro muda quando olhamos para o outro lado do funil.

### O gargalo da revisão

O dado mais crítico e menos divulgado: o tempo mediano de revisão de PRs cresceu até **90%** em equipes que adotaram coding agents intensivamente. A explicação é simples: quando agentes geram código mais rápido do que humanos conseguem revisar, o gargalo apenas se desloca — da implementação para a revisão.

![O funil invertido: descompasso entre geração e revisão de código](../imagens/cap_3_diagrama_2.svg)

![O funil invertido: descompasso entre geração e revisão de código](../imagens/cap_3_diagrama_2.svg)

As consequências são preocupantes:

1. **Acúmulo de PRs não revisados:** Desenvolvedores acumulam dezenas de PRs abertos, criando pressão para revisões superficiais.
2. **Aprovações sem leitura crítica:** A revisão vira uma cerimônia, não uma verificação real de qualidade.
3. **Instabilidade na entrega:** Relatórios DORA correlacionam adoção de IA não-governada com maior taxa de falhas em mudanças (change failure rate).

### Onde os ganhos reais acontecem

Quando bem aplicados em fluxos estruturados, os ganhos são reais e mensuráveis:

- **Tarefas rotineiras:** Redução de 25% a 50% no custo por tarefa em refatorações isoladas, geração de testes unitários e prototipação.
- **Horas economizadas:** Média de 7 a 9 horas semanais por engenheiro em tarefas repetitivas — escrita de código boilerplate, documentação inicial, geração de mocks.
- **Qualidade de código:** Equipes que usam agentes com revisão adversarial (como o Fable Method, coberto no Capítulo 9) reportam **menos** bugs em produção do que equipes sem agentes.

O paradoxo se resolve não com menos agentes, mas com melhor governança sobre como e quando eles atuam.

## O perception gap e métricas que importam

### O estudo METR

Um dos estudos mais reveladores sobre o impacto real de coding agents foi conduzido pelo METR (Measuring AI Agent Capabilities). Pesquisadores desenharam um experimento controlado onde desenvolvedores experientes usaram coding agents em codebases legadas reais para concluir tarefas complexas de manutenção e evolução.

Os resultados foram surpreendentes:

| Métrica | Percebido pelos devs | Real (medido) | Lacuna |
|---------|---------------------|---------------|--------|
| Velocidade em tarefas complexas | 20% mais rápidos | 19% **mais lentos** | **39 pontos** |
| Confiança na correção | 85% confiantes | 62% corretos | 23 pontos |
| Cobertura de testes | "Melhor que antes" | 12% menor | Significativa |

A lacuna de quase 40 pontos percentuais entre a percepção de ganho e a realidade medida é o que os pesquisadores chamam de **perception gap**. Desenvolvedores *acham* que estão mais produtivos, mais métricas objetivas mostram o oposto em tarefas complexas.

![Perception gap: percepção vs. realidade de produtividade](../imagens/cap_3_diagrama_3.svg)

### Por que isso acontece

O perception gap tem explicações cognitivas e ambientais:

1. **Viés de fluência:** Quando o agente gera código rapidamente, o desenvolvedor *sente* que está progredindo, mesmo que o código precise ser reescrito ou corrigido depois.
2. **Carga cognitiva da verificação:** Revisar código gerado por IA exige um tipo diferente de atenção — o revisor precisa imaginar *o que o agente poderia ter feito de errado*, não apenas verificar o que está ali.
3. **O paradoxo da escolha:** Com múltiplas abordagens sugeridas pelo agente, o desenvolvedor gasta mais tempo decidindo qual seguir do que gastaria implementando uma diretamente.

### Métricas que realmente importam

Para evitar o perception gap, equipes maduras estão migrando de métricas de atividade para métricas de entrega:

**Métricas de atividade (enganosas):**
- PRs abertos por desenvolvedor
- Linhas de código geradas
- Tempo até o primeiro commit

**Métricas de entrega (relevantes):**
- Throughput de features entregues (completas e testadas)
- Change failure rate (DORA)
- Tempo de revision (review time) por PR
- Taxa de rollback pós-deploy
- Dívida técnica identificada vs. paga (sonar/cobertura/estabilidade)
- Satisfação do desenvolvedor com o fluxo (qualitativa)

### A importância das evals automatizadas

O antídoto mais eficaz contra o perception gap são suítes de avaliação automatizada (evals) rodando a cada mudança de prompt ou configuração do agente. Empresas que implementaram evals rigorosas reportam taxas de rollback **4x menores** do que aquelas sem cobertura de avaliação.

Uma eval eficaz para coding agents inclui:
1. **Testes de regressão:** Todo o test suite existente deve passar antes e depois de cada alteração do agente.
2. **Property-based testing:** Testes que verificam propriedades invariantes do sistema, não apenas casos específicos.
3. **Análise de impacto:** Detecção automática de quais módulos foram alterados e se há dependências não testadas.
4. **Verificação adversarial:** Um segundo agente (ou um humano) que tenta ativamente encontrar falhas na solução proposta (ver Fable Method, Capítulo 9).

---

Neste capítulo, vimos que os benchmarks (SWE-bench) mostram progresso impressionante, mas com limitações importantes. O paradoxo da produtividade revela que atividade não é entrega, e o perception gap mostra que nossos instintos sobre produtividade podem estar errados. No próximo capítulo, mergulharemos na disciplina que está substituindo o prompt engineering como habilidade central: o Context Engineering.
