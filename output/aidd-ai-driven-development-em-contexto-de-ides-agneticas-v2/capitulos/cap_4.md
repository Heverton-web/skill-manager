# Capítulo 4 — Desafios, Limitações e o Futuro do Desenvolvimento com Agentes

Nenhuma tecnologia emerge sem desafios. O AIDD, apesar de seu potencial transformador, enfrenta limitações significativas que precisam ser compreendidas e mitigadas para adoção responsável em ambientes de produção.

## Alucinação de Contexto e Deriva Arquitetural em Codebases Grandes

O problema mais comum em execuções longas de agentes é a **alucinação de contexto**. Diferente da alucinação de fatos em chatbots, aqui o agente "esquece" ou "distorce" o contexto do projeto ao longo de múltiplas iterações, introduzindo código que viola padrões não escritos da equipe.

Em codebases acima de 100 mil linhas, com múltiplos módulos e convenções históricas, agentes tendem a:

- **Ignorar padrões existentes**: Usar uma biblioteca diferente da que o resto do time usa para resolver o mesmo problema
- **Duplicar funcionalidades**: Criar novas funções que já existem em módulos que o agente não examinou
- **Violar convenções de naming**: Misturar camelCase com snake_case, ou usar padrões de diretório diferentes do estabelecido
- **Propagar erros**: Repetir o mesmo padrão incorreto em múltiplos arquivos porque o agente "aprendeu" o padrão errado do contexto

A mitigação mais eficaz é a manutenção rigorosa de arquivos de contexto como `CLAUDE.md`, `.cursorrules` e especificações em `SPEC.md` — quanto mais explícitas as convenções, menor a probabilidade de deriva.

## Segurança: Permissões de Terminal, Sandboxing e Confused Deputy

Agentes com capacidade de execução de comandos de terminal representam um vetor de risco significativo. O cenário mais preocupante é o ataque **Confused Deputy**: um prompt malicioso engana o agente para executar comandos destrutivos, usando a confiança que o desenvolvedor depositou no agente.

As principais camadas de segurança incluem:

- **Listas de permissão de comandos**: Restringir quais comandos o agente pode executar (ex: permitir `npm test` mas bloquear `rm -rf`)
- **Sandboxing por container**: Executar agentes em containers Docker com volumes montados apenas para leitura em diretórios críticos
- **Aprovação granular**: Exigir confirmação humana para comandos que alteram o sistema de arquivos fora do diretório do projeto
- **Detecção de padrões suspeitos**: Alertar sobre comandos que combinam operações de leitura com chamadas de rede externa

Ferramentas como Claude Code implementam um modelo de permissões onde o desenvolvedor pode configurar níveis de autonomia — desde "aprovar tudo" até "bloquear comandos de rede e instalação de pacotes".

![Zonas de Confiança](../imagens/cap_4_diagrama_1.svg)

## Futuro: Agentes Especialistas, MCP como Padrão Industrial

O AIDD está em seus estágios iniciais. As tendências que definem sua evolução incluem:

**Agentes Especialistas por Domínio**: Em vez de um agente genérico que tenta fazer tudo, veremos ecossistemas de agentes especializados — um para segurança, outro para banco de dados, outro para frontend — cada um com profundo conhecimento de seu domínio e capaz de colaborar com os demais via protocolos padronizados.

**MCP como Padrão Industrial**: O Model Context Protocol tem potencial para se tornar o padrão universal de integração agente-ferramenta, assim como HTTP/HTML se tornaram o padrão da web. Seu modelo aberto, a adoção por múltiplas plataformas e a facilidade de criação de servidores MCP criam um círculo virtuoso de expansão do ecossistema.

**Evolução do Papel do Desenvolvedor**: O desenvolvedor do futuro será cada vez mais um **especificador-orquestrador**: alguém que entende profundamente o domínio do problema, sabe traduzir necessidades de negócio em especificações precisas, e coordena times de agentes para executar a implementação. Habilidades de comunicação, pensamento sistêmico e curadoria serão mais valorizadas que conhecimento de sintaxe.

O AIDD não elimina a necessidade de desenvolvedores experientes — pelo contrário, amplifica seu impacto. Um desenvolvedor que entende arquitetura, segurança e domínio do negócio pode, com agentes, produzir o trabalho de um time inteiro. O desafio não é tecnológico, mas cultural: abraçar um novo paradigma onde o código é apenas o resultado final, não o processo.

![Roadmap do AIDD](../imagens/cap_4_diagrama_3.svg)
