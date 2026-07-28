# Capítulo 11 — Riscos, Dívida Técnica e o Lado Sombrio dos Agentes

Até agora, este livro focou no potencial transformador dos coding agents. Mas ignorar os riscos seria irresponsável. Assim como a terceirização de código para fornecedores de baixo custo nos anos 2000 gerou uma crise de qualidade, a terceirização para agentes de IA em 2026 está gerando uma nova forma de dívida técnica — mais insidiosa, mais rápida e mais difícil de detectar.

## Dívida técnica gerada por IA

### As 3 fontes de dívida técnica de agentes

**1. Código que funciona mas não é compreendido:** O agente gera código que passa nos testes, mas o desenvolvedor não entende completamente como ele funciona. Seis meses depois, ninguém sabe como manter ou estender aquele código. É a dívida técnica da **caixa-preta**.

**2. Código que funciona mas não é resiliente:** O agente otimiza para o caminho feliz (happy path). Casos de borda — concorrência, falhas de rede, dados malformados — são frequentemente ignorados. O sistema funciona até o momento em que algo inesperado acontece.

**3. Código que polui o design:** Agentes, por natureza, tendem a adicionar código em vez de refatorar. Cada nova feature adiciona mais acoplamento, mais arquivos, mais complexidade. Sem supervisão deliberada, a arquitetura se degrada mais rápido do que com desenvolvimento manual.

### O custo da falsa produtividade

O perception gap (Capítulo 3) tem um impacto concreto: desenvolvedores que acreditam estar sendo produtivos com coding agents, mas na verdade estão gerando dívida técnica, criam um ciclo vicioso:

1. Agente gera código rapidamente
2. Desenvolvedor aprova sem revisão profunda (viés de fluência)
3. Código vai para produção com bugs ou problemas arquiteturais
4. Tempo gasto depois para corrigir é maior que o tempo "economizado"
5. Desenvolvedor acha que o problema é o agente, não o processo

## Viés de automação e atrofia de julgamento crítico

### O viés de automação

O **viés de automação** é a tendência humana a confiar em sistemas automatizados mesmo quando eles cometem erros. Em coding agents, esse viés se manifesta de várias formas:

- **Aprovação sem leitura:** "O agente gerou, deve estar certo"
- **Falsa confiança:** "O código parece complexo, confio que o agente sabe o que fez"
- **Atrofia de habilidades:** "Não preciso mais aprender X, o agente faz"

### A atrofia do desenvolvedor

O risco mais existencial não é o agente substituir o desenvolvedor — é o desenvolvedor **se substituir** voluntariamente. Quando um engenheiro deixa de praticar habilidades fundamentais (debugging, análise de causa raiz, design de arquitetura) porque o agente "faz isso", ele está terceirizando não apenas o código, mas o julgamento.

Sinais de atrofia:
- Desenvolvedor não consegue identificar por que o código do agente está errado
- Desenvolvedor não sabe como consertar um bug sem pedir ajuda ao agente
- Desenvolvedor não consegue projetar uma arquitetura — só consegue iterar em sugestões do agente

### O antídoto: revisão adversarial deliberada

A prática que previne a atrofia é a **revisão adversarial deliberada**: o desenvolvedor assume que o código do agente pode estar errado e ativamente tenta provar isso. Não é "revisar para aprovar" — é "revisar para reprovar".

## Segurança, vazamento de dados e conformidade

### Riscos de segurança específicos de coding agents

Além dos riscos tradicionais de segurança de software, coding agents introduzem novos vetores:

- **Injeção indireta de prompt:** Um arquivo malicioso no repositório pode contaminar o contexto do agente
- **Vazamento de credenciais:** Agentes podem, inadvertidamente, commitar secrets em arquivos de configuração
- **Código com vulnerabilidades:** Agentes geram código funcional mas nem sempre seguem práticas seguras (OWASP Top 10)

### Dados e propriedade intelectual

O envio de código proprietário para APIs de modelos de linguagem (Claude, GPT, Gemini) levanta questões legais ainda não totalmente resolvidas:

- **Treinamento:** O código enviado pode ser usado para treinar futuras versões do modelo?
- **Confidencialidade:** A API provider pode reter e analisar o código enviado?
- **Jurisdição:** Onde os dados são processados? (GDPR, LGPD, CCPA)

![Riscos e controles no ecossistema AIDD](../imagens/cap_11_diagrama_1.svg)

### O EU AI Act e implicações regulatórias

A regulamentação europeia de IA (EU AI Act) classifica sistemas de IA por nível de risco. Coding agents usados em setores regulados (saúde, finanças) podem se enquadrar como **risco alto**, exigindo:
- Documentação de conformidade
- Supervisão humana
- Transparência e explicabilidade
- Precisão e robustez demonstráveis

![Riscos e controles no ecossistema AIDD](../imagens/cap_11_diagrama_1.svg)

---

Neste capítulo, examinamos os riscos que acompanham a adoção de coding agents — dívida técnica de caixa-preta, viés de automação com atrofia de julgamento, e riscos de segurança e conformidade. No capítulo final, projetaremos o perfil do profissional do futuro: o engenheiro de intenção.
