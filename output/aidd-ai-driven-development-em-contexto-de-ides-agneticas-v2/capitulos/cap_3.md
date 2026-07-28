# Capítulo 3 — Spec-to-Code e Sub-Agentes Paralelos: Orquestração de Pipelines

O verdadeiro potencial do AIDD não está em gerar código isolado, mas em orquestrar pipelines inteiros de desenvolvimento onde múltiplos agentes colaboram paralelamente sob coordenação humana. Este capítulo explora os padrões de orquestração que transformaram a engenharia de software.

## Spec-to-Code: da Especificação Markdown ao Código Executável

O padrão Spec-to-Code é o fluxo fundamental do AIDD. Um desenvolvedor escreve uma especificação em Markdown — geralmente em um diretório `/specs` do repositório — e um agente a transforma em implementação completa. O fluxo típico tem quatro estágios:

1. **Parsing da Especificação**: O agente lê o arquivo Markdown e extrai requisitos, regras de negócio, critérios de aceitação e restrições técnicas. Arquivos de contexto como `CLAUDE.md` ou `.cursorrules` fornecem o contexto adicional do projeto — convenções, stack tecnológica, padrões arquiteturais.

2. **Geração do Plano**: O agente decompõe a especificação em tarefas atômicas ordenadas. Cada tarefa tem pré-condições, arquivos afetados, implementação esperada e critérios de validação. Este plano é apresentado ao desenvolvedor como um diff preview antes da execução.

3. **Execução Orquestrada**: O agente implementa cada tarefa na ordem definida, executando comandos de terminal, editando arquivos e rodando validações intermediárias. Erros são tratados pelo ciclo de auto-correção descrito no Capítulo 1.

4. **Validação Final**: O agente executa a suíte completa de testes, verifica lint e formatação, e apresenta o diff consolidado para revisão humana. O desenvolvedor pode aprovar, solicitar ajustes ou rejeitar o resultado.

Este padrão é particularmente eficaz para tarefas bem especificadas: adicionar uma rota de API, implementar um componente de UI com comportamento definido, ou refatorar um módulo com contrato conhecido.

![Pipeline Spec-to-Code](../imagens/cap_3_diagrama_1.svg)

## Delegação Paralela: Sub-Agentes para Schema, Testes e Documentação

Um dos diferenciais mais poderosos do AIDD é a capacidade de delegar tarefas simultâneas a sub-agentes especializados. Enquanto um agente principal coordena o fluxo geral, sub-agentes processam partes independentes em paralelo.

Considere uma tarefa de adicionar uma nova entidade ao sistema. O agente orquestrador pode delegar simultaneamente:

- **Sub-agente de banco de dados**: Gera a migração SQL, atualiza o schema do ORM e cria índices
- **Sub-agente de API**: Implementa os endpoints REST/GraphQL com validação e tratamento de erros
- **Sub-agente de testes**: Escreve testes unitários e de integração para a nova entidade
- **Sub-agente de documentação**: Atualiza a documentação da API e gera exemplos de uso

Cada sub-agente opera em contexto isolado, com acesso apenas aos arquivos relevantes para sua tarefa. O orquestrador coleta os resultados, resolve conflitos de merge, executa a validação integrada e apresenta o resultado consolidado.

Esta arquitetura reduz o tempo de implementação de horas para minutos em tarefas que envolvem múltiplas camadas do sistema, e é suportada nativamente por ferramentas como Claude Code (via sub-agents) e Antigravity (via agent graph).

![Orquestração com Sub-Agentes](../imagens/cap_3_diagrama_2.svg)

## Validação em Loop Fechado e Revisão Humana de Diff

O último estágio de qualquer pipeline AIDD é a validação integrada combinada com revisão humana. Após a execução autônoma, o agente:

1. Executa a suíte completa de testes (unitários, integração, e2e)
2. Verifica lint, formatação e tipos
3. Gera um diff consolidado de todas as alterações
4. Apresenta o diff para revisão humana com anotações sobre cada alteração

A revisão humana é o gate final — o desenvolvedor auditor inspeciona o diff em busca de problemas que agentes autônomos tipicamente ignoram: violações de convenções não documentadas, decisões arquiteturais que não se alinham com a visão de longo prazo do produto, e vulnerabilidades de segurança sutis.

Este modelo de "agente escreve, humano revisa" é dramaticamente mais produtivo que o ciclo tradicional "humano escreve, humano revisa, humano corrige". Estudos informais de times usando AIDD reportam reduções de 40-60% no tempo de implementação de funcionalidades, mantendo ou melhorando a qualidade do código graças à revisão humana focada.

![Fluxo de Validação](../imagens/cap_3_diagrama_3.svg)
