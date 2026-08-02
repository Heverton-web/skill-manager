# Relatório de Análise — Tom de Comunicação na Redação dos Livros

**Data:** 2026-08-02
**Escopo:** apenas a *forma de comunicação* do texto gerado pelo redator de capítulos
(`redator-eita` / `template_eita.md`). Nenhuma regra de ABNT, estrutura EITA-V2
(7 seções), citação numerada `[N]` ou requisito contratual (R1-R14) é questionada
ou alterada por este relatório.

---

## 1. Pedido do operador

> "Percebi que a CRIAÇÃO de um LIVRO utiliza linguagem extremamente técnica com
> pouca aplicabilidade prática e utilidade real ao leitor. O conteúdo produzido
> é técnico, mas impessoal, totalmente informacional e raso em explicações e
> voltado ao público técnico. O correto é: manter o conteúdo técnico embasado em
> referências bibliográficas reais e acessíveis [...], mas com linguagem simples
> em tom pessoal, transformacional, conduzindo o leitor, mesmo que absoluto
> iniciante ou PhD no assunto, a uma leitura prazerosa e que gere o efeito
> 'Uau!'. Percebi que os conceitos, termos técnicos não são definidos nem
> aprofundados o quanto deveriam [...]"

Material de referência (embrionário, mas no padrão desejado):
`Fabrica_Agentica-Da_Probabilidade_Matematica_ao_Determinismo_Operacional.md`

Material produzido pela esteira atual (para contraste):
`output/ai-driven-development/livro_compilado.md`

Regra do operador: **não alterar** ABNT, EITA ou regras do projeto — o ajuste é
exclusivamente na *forma de comunicação*.

---

## 2. Metodologia

Leitura comparativa dos dois arquivos (prefácio + capítulos 1-3 de cada um) e
verificação quantitativa de padrões objetivos:

| Métrica | Referência (348.091 caracteres) | Produzido (120.329 caracteres, 10 capítulos) |
|---|---|---|
| Citações `[N]` no corpo | 0 (usa lista de fontes comentada, sem marcador inline) | 620 |
| Trechos com citações **empilhadas** (`[N][N]...` sem prosa entre elas) | 0 | 115 |
| Ocorrências do motivo condutor central (ex.: "Engenheiro Agêntico", "esteira", "fábrica", "Motor", "Cérebro") só no trecho lido (prefácio + 2 capítulos) | 449 | — |
| Persistência das metáforas próprias do livro produzido pelo restante da obra (ex.: "cabine"/"guindaste" do Cap. 3, "oficina de produção" do Cap. 2) | — | confinadas ao próprio capítulo (1 a 6 ocorrências, 0 fora dele) |

Também foram lidos os arquivos-fonte da esteira que definem a regra de redação:
[.claude/skills/redator-eita/SKILL.md](.claude/skills/redator-eita/SKILL.md) e
[templates/template_eita.md](templates/template_eita.md).

---

## 3. Conclusões

### 3.1 A metáfora é descartável, não persistente
No material de referência, o motivo condutor (a fábrica, o Engenheiro Agêntico,
o Cérebro/Motor/Mãos) aparece **449 vezes só nos 2 primeiros capítulos** e é
reaproveitado inclusive na seção "Explica" e "Técnica" (não só na "Ilustra").
Ele constrói uma história única que atravessa o livro inteiro — o leitor nunca
perde o fio.

No material produzido, cada capítulo inventa uma metáfora nova e a **contém**
dentro da própria seção "Ilustra" (Cap. 2 usa "oficina de produção" 1 vez só;
Cap. 3 usa "cabine de guindaste" 3-6 vezes, mas nunca fora do próprio capítulo).
Fora da seção "Ilustra", o texto volta a um registro de relatório técnico. Não
há reforço, não há callback, e a metáfora não ajuda o leitor a **lembrar** o
conceito no capítulo seguinte.

**Causa raiz:** `template_eita.md` trata a seção 3 (Ilustra) como uma caixa
isolada por capítulo ("analogia ou metáfora que ancore o conceito... sempre
acompanhada de um diagrama"), sem exigir que o motivo condutor seja definido
**uma única vez para a obra inteira** e reutilizado como vocabulário nas demais
seções e capítulos.

### 3.2 Citações empilhadas transformam prosa em revisão de literatura
O produzido tem 620 marcadores `[N]` em 120 mil caracteres — quase o dobro da
densidade normalmente aceitável em texto de leitura contínua — e **115 trechos**
onde 2+ citações aparecem coladas sem uma frase de transição entre elas
(ex.: `"...ganho individual de produtividade [...] [10]"`, `"[8][9]"`). O efeito
é o de um artigo acadêmico stuffado de referências, não de um mentor contando
uma história embasada em dados.

O material de referência atinge o mesmo objetivo (embasamento real, fontes
verificáveis) com uma abordagem inteiramente diferente: cada fonte vira uma
**seção comentada** ao final do capítulo ("*Contexto na Fábrica:*..."), e o
corpo do texto flui sem interrupção de colchetes.

**Importante:** a regra do projeto (R10/R14) exige citação inline `[N]` — isso
**não muda**. O problema não é a existência da citação, é a *densidade e o
empilhamento* dela dentro da seção "Explica", que hoje é tratada como o lugar
de despejar estatísticas ("75% do código", "8x mais", "90% dos devs" — 5+
números seguidos, 1 por citação) em vez de contar uma ideia e ancorá-la em 1
fonte por vez.

**Causa raiz:** `redator-eita/SKILL.md` diz apenas "citações `[N]` obrigatórias
para afirmações factuais" e "mínimo de 3 por capítulo" — não há teto de
densidade nem orientação de que cada citação deve vir **depois** de uma frase
que já ensinou a ideia em linguagem própria, nunca substituindo a explicação
por uma sequência de dados creditados.

### 3.3 Termos técnicos são definidos uma vez, não aprofundados
No produzido, um termo como "harness" ganha uma definição de uma frase na
seção "Explica" (*"o software que dá ao LLM acesso ao terminal..."*) e segue
para citações. No material de referência, o termo equivalente ("Motor") é
definido **três vezes, de três ângulos diferentes**: (1) definição técnica
direta na "Explica"; (2) reforço através de uma metáfora industrial estendida
("braços robóticos que soldam o chassi") na "Ilustra"; e (3) uma segunda
metáfora complementar ("esteira trituradora → parede magnética → esteira
rolante") especificamente para o conceito mais difícil do capítulo (tokens/
janela de contexto). Essa redundância pedagógica é o que faz o iniciante
"grudar" no conceito sem cansar o especialista, que lê a definição técnica e
segue em frente.

**Causa raiz:** o template pede só **uma** analogia por seção "Ilustra". Não há
instrução para reforçar o mesmo conceito com uma segunda camada de explicação
quando o conceito é estruturalmente denso (ex.: física de tokens, arquitetura
de memória) — o que o material de referência faz e o produzido não.

### 3.4 Falta o "erro vs. acerto" dramatizado
O ponto mais forte do material de referência é o par narrativo **"Método do
Operário (Errado)" vs. "Método do Engenheiro Agêntico (a aplicação correta)"**,
com um cenário físico único (construir o login com Supabase), um erro real
(a IA usa Firebase por acidente), um diagnóstico passo a passo e uma correção
— tudo em 2ª pessoa, com tensão e resolução. É esse arco que gera o efeito
"Uau!": o leitor vive o erro antes de aprender a solução.

No produzido, a seção "Aplica" cumpre o requisito contratual ("cenário
corporativo, métricas de sucesso/fracasso, armadilhas comuns") mas como uma
**lista de bullets** ("1. Delegar sem critério de aceite... 2. Acreditar que
IA conserta arquitetura ruim..."). É informação correta, mas sem narrativa —
não há personagem, não há erro acontecendo em tempo real, não há a virada de
"ah, é isso que eu estava fazendo errado".

**Causa raiz:** `template_eita.md`, seção 5 (Aplica), pede "armadilhas comuns e
como evitá-las" — que o redator satisfaz, corretamente, com uma lista. O
template não pede uma **cena** (situação + erro + diagnóstico + correção)
como dispositivo narrativo obrigatório.

### 3.5 Voz de relatório vs. voz de mentor
Frases do produzido ("A Google anunciou que 75%...", "O relatório DORA 2025
mostrou que...") são no registro de notícia/whitepaper. Frases do material de
referência ("Neste exato segundo, a velha identidade de operário grita na sua
cabeça...", "Você agora compreende a planta baixa da fábrica...") são no
registro de mentor falando diretamente com o leitor, em 2ª pessoa, com
tensão dramática.

O `redator-eita/SKILL.md` já pede tom transformacional e construções como "Ao
dominar isso, você..." — a regra existe, mas é genérica demais para competir
com a pressão contrária de "citações obrigatórias" e "mínimo 60% em Técnica",
que empurram o redator para o registro informacional por segurança (é mais
fácil auditar/validar uma lista de estatísticas citadas do que uma cena
narrativa).

---

## 4. Sugestões de melhoria (sem alterar ABNT / EITA / regras do projeto)

Todas as sugestões abaixo **mantêm as 7 seções, a ordem, o mínimo de 3
citações `[N]`/capítulo, a rastreabilidade R14 e todos os requisitos R1-R14**.
O ajuste é em *regras adicionais de estilo* dentro do mesmo template/skill.

### 4.1 Motivo condutor único por obra (não por capítulo)
Adicionar ao Passo do `arquiteto` (Fase 1): ao desenhar o sumário macro, definir
**um único motivo condutor/metáfora-mestra** para a obra inteira (ex.: "a
fábrica", "o organismo vivo", "a orquestra") e gravá-lo em
`output/<slug>/esboco/motivo_condutor.json` (ou campo equivalente em
`sumario_macro.json`). O `redator-eita` passa a **consultar esse arquivo antes
de escrever a seção Ilustra** de qualquer capítulo, reaproveitando o mesmo
vocabulário/persona em vez de inventar uma metáfora nova a cada capítulo.

### 4.2 Teto de densidade de citação + regra de "citação após explicação"
Em `redator-eita/SKILL.md`, seção "Citações inline", adicionar:
- Nunca emendar 2+ citações consecutivas (`[N][N]`) sem uma frase de transição
  entre elas.
- Cada citação deve vir **depois** de uma frase que já expressa a ideia em
  linguagem própria — a citação reforça, nunca substitui, a explicação.
- Evitar parágrafos com mais de 2 citações na seção "Explica" (mover dados
  excedentes para a seção "Técnica" ou para uma nota de rodapé/tabela).

### 4.3 Definição em duas camadas para conceitos estruturalmente densos
Adicionar à seção "Ilustra" do template: quando o conceito do capítulo for
estruturalmente complexo (o `estrategista`, na Fase 2/Nó 1-2, sinaliza isso no
`payload_estrategico`), o redator deve produzir **duas analogias
complementares** (uma para a mecânica geral, outra para o ponto mais difícil),
em vez de uma única analogia genérica.

### 4.4 Cena obrigatória de contraste ("Erro Comum vs. Prática Correta")
Na seção "Técnica" ou "Aplica" (a critério do redator), exigir pelo menos
**uma cena narrativa em 2ª pessoa**: situação concreta → erro plausível que o
leitor cometeria → diagnóstico → correção. Isso substitui (ou antecede) a
lista de "armadilhas comuns" hoje puramente enumerativa — a lista pode
continuar existindo como síntese, mas precisa vir precedida de uma cena.

### 4.5 Reforçar a regra de voz com exemplos negativos e positivos
Em `redator-eita/SKILL.md` § "Tom Transformacional", incluir 2-3 pares de
frase (❌ registro de relatório / ✅ registro de mentor) extraídos deste
próprio comparativo, para calibrar o redator com exemplos concretos em vez de
só regras abstratas.

### 4.6 Evidência determinística para a Fase 2.5 (auditoria objetiva)
Seguindo o princípio de "evidência determinística, não impressão do agente" já
usado no projeto (`auditar-obra.py`), adicionar uma checagem opcional e
não bloqueante em `scripts/auditar-obra.py`:
- Detectar e reportar (não reprovar automaticamente) trechos com citações
  empilhadas (`(\[\d+\]){2,}` sem espaço/prosa entre colchetes).
- Contar ocorrências do motivo condutor da obra (`motivo_condutor.json`) por
  capítulo e sinalizar capítulos com 0 ocorrências fora da seção Ilustra.
Essas métricas entram no parecer de `revisao/parecer_revisao.md` como
recomendação de estilo, sem impedir a compilação — mantendo REGRA 4
(auto-correção) como decisão do `revisor-tecnico`, não do script.

---

## 5. O que este relatório **não** propõe
- Não altera a estrutura de 7 seções do EITA-V2.
- Não altera nenhum requisito contratual R1-R14 de `/criar-livro`.
- Não altera formato ABNT, numeração de citação `[N]` ou mínimo de referências.
- Não remove a exigência de diagrama Mermaid nem de código validado por CI.
- Não é uma implementação — é a análise e a lista de sugestões pedidas.
