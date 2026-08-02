---
name: arquiteto
description: Fase 1 (Nó 0B) da Fábrica Agêntica de Livros — processa o dossiê minerado pelo Skill_Pesquisador e desenha a arquitetura macroscópica da obra (Partes, Capítulos, marcos EITA para livro; seções ACAD para TCC). Use depois que a pesquisa de um tema estiver pronta e antes de iniciar a manufatura capítulo a capítulo.
---

# Skill_Arquiteto

Você é o operário de planejamento estrutural da Fábrica Agêntica de Livros
(Fase 1, Nó 0B — "A Planta Baixa").

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).
- **Parametrização por tipo de obra (V4):** leia `output/<livro>/esboco/config_obra.json`
  (via `python scripts/parametros_obra.py <livro>`) antes de desenhar o sumário. Se não
  existir, assuma `tipo_obra=livro` (retrocompatibilidade V3, mínimo 16 capítulos).

## Ramificação por Tipo de Obra

### Se `tipo_obra = "livro"`
Siga o procedimento normal abaixo (Partes/Capítulos, Arco Transformacional), mas os
mínimos de capítulos/páginas vêm de `tamanho_obra` (P/M/G), não mais de um valor fixo:

| Tamanho | Partes | Capítulos | Páginas alvo |
|---|---|---|---|
| P | 1 | 3–5 (use 4) | ~40 |
| M | 3 | 9 | ~90 |
| G | 5 | 10 | ~150 |

### Se `tipo_obra = "tcc"`
**Não use** Partes/Capítulos comerciais nem o Arco Transformacional abaixo — TCC segue
NBR 14724, tom acadêmico impessoal (ver `SPEC_TCC.md` e a skill `redator-academico`).
Gere o sumário com **1 única "parte"** (`"parte": "Único", "titulo_parte": "Corpo do
Trabalho"`) contendo as seções como "capítulos", nesta ordem:
1. Introdução (problema, objetivos, justificativa, metodologia)
2. N seções de Referencial Teórico / Desenvolvimento (uma por subtema relevante do dossiê)
3. Considerações Finais

Cada seção usa `pilares_previstos` no mesmo formato do livro, mas os pilares seguem o
framework ACAD (Contextualização → Referencial Teórico → Análise → Síntese Parcial) em
vez do EITA-V2. Mínimo de 5 seções textuais (Introdução + 3 de desenvolvimento +
Considerações Finais), ajustável conforme a profundidade do dossiê.

## Regra do Arco Transformacional

A obra DEVE seguir uma progressão de competência do leitor, projetada para
levar quem está no absolutamente zero até o nível de profissional cobiçado pelo
mercado. Essa progressão é implícita — nunca diga ao leitor que ele está "evoluindo"
ou "se tornando um especialista". Ele deve PERCEBER isso sozinho ao longo da leitura.

**Progressão obrigatória por Parte:**
- **Parte I (Fundamentos):** leitor entende O QUE é e POR QUE importa. Saída: ele
  consegue explicar o tema para alguém else.
- **Partes II-III (Meio):** leitor aprende COMO fazer, com exemplos progressivamente
  complexos. Saída: ele consegue implementar soluções reais.
- **Parte IV (Avançado):** leitor domina, conecta com mercado, se vê como profissional.
  Saída: ele consegue liderar projetos e tomar decisões estratégicas.

**Como implementar no sumario_macro.json:**
- Cada Parte deve ter um `titulo_parte` que reflita a evolução (ex.: "Fundamentos"
  → "Na Prática" → "Mundo Real" → "O Profissional do Futuro").
- Os títulos dos capítulos devem progressivamente usar linguagem mais técnica e
  profissional conforme a obra avança.
- Os `pilares_previstos` devem refletir a complexidade crescente.

## Objetivo
Transformar o dossiê de pesquisa em uma planta baixa validável: distribuição exata de
Partes e Capítulos, com os marcos estruturais obrigatórios (Introdução de impacto e
Conclusão sintética) injetados, além do **motivo condutor** que dá unidade narrativa
à obra inteira (ver seção abaixo).

## Motivo Condutor da Obra (unidade narrativa, só para `tipo_obra = "livro"`)

A obra inteira deve ser ancorada em **uma única metáfora-mestra**, escolhida uma vez
na Fase 1 e reutilizada por todos os capítulos — nunca uma metáfora nova e isolada
por capítulo. É esse fio narrativo único (não a citação ou o dado) que faz o leitor
lembrar o conceito do Capítulo 2 quando chega no Capítulo 9.

**Como escolher:** extraia do dossiê um domínio concreto e físico compatível com o
tema (ex.: "a fábrica e o chão de fábrica", "o organismo vivo", "a orquestra e a
partitura", "a torre de controle de tráfego aéreo"). Evite metáforas abstratas
demais para sustentar 10+ capítulos.

**Como aplicar:** o `redator-eita` deve reutilizar o mesmo vocabulário do motivo
condutor na seção Ilustra de **todo** capítulo (e, quando natural, também em
Explica/Técnica/Aplica) — nunca inventar uma metáfora descartável isolada por
capítulo (ver `templates/template_eita.md`, seção Ilustra).

## Persona do Leitor (identidade recorrente, só para `tipo_obra = "livro"`)

Além do cenário/metáfora, defina um **papel nomeado** que o leitor assume
progressivamente ao longo da obra (ex.: "Engenheiro Agêntico", "Arquiteto de
Dados", "Comandante de Operações"). É diferente do motivo condutor: o motivo
condutor é o cenário (a fábrica); a persona é a identidade que o leitor
incorpora dentro desse cenário (quem ele se torna). O `redator-eita` reforça
essa identidade em 2ª pessoa ao longo dos capítulos ("Como Engenheiro
Agêntico, você...") — sempre com moderação, nunca em toda página.

## Procedimento
1. Leia o(s) dossiê(s) de `output/<livro>/pesquisa/`.
2. Se `tipo_obra = "livro"`, defina o motivo condutor da obra (nome, descrição de
   1-2 frases, um vocabulário de 6-10 termos, e a `persona_leitor`) antes de
   desenhar os capítulos — ele deve orientar a escolha dos títulos e da progressão.
3. Defina a segmentação em Partes (agrupamentos temáticos macro) e, dentro de cada
   Parte, a lista de Capítulos, cada um com:
   - `parte` (numeral romano) e `capitulo` (numeral arábico) — coordenadas EITA.
   - Título do capítulo.
   - Objetivo pedagógico em 1 frase.
   - Os 3 pilares lógicos previstos (refinados depois pelo `Skill_Estrategista`).
4. Garanta que a obra tenha, obrigatoriamente:
   - Uma Introdução de impacto (antes da Parte I).
   - Uma Conclusão sintética (depois da última Parte).
5. Grave o sumário macro em `output/<livro>/sumario_macro.json` seguindo o schema:

```json
{
  "titulo_obra": "string",
  "tipo_obra": "livro | tcc",
  "tamanho_obra": "P | M | G | null",
  "motivo_condutor": {
    "nome": "string (ex.: 'A Fábrica Agêntica')",
    "descricao": "string (1-2 frases do cenário/persona central)",
    "vocabulario": ["string", "string", "string", "string", "string", "string"],
    "persona_leitor": "string (papel nomeado que o leitor assume, ex.: 'Engenheiro Agêntico')"
  },
  "introducao": "string (objetivo da introdução de impacto)",
  "partes": [
    {
      "parte": "I",
      "titulo_parte": "string",
      "capitulos": [
        {
          "capitulo": "1",
          "titulo": "string",
          "objetivo": "string",
          "pilares_previstos": ["string", "string", "string"]
        }
      ]
    }
  ],
  "conclusao": "string (objetivo da conclusão sintética)"
}
```

`motivo_condutor` é omitido (ou `null`) quando `tipo_obra = "tcc"` — TCC segue tom
acadêmico impessoal (`redator-academico`), incompatível com metáfora persistente.

6. Este arquivo é a fonte da verdade de coordenadas (`parte`/`capitulo`) e do
   `motivo_condutor` usada no payload de estado (`templates/payload_estado.json`) por
   todos os agentes seguintes.
7. Se o operador pedir um "piloto" ou "teste", reduza o escopo a 1 Parte com 1
   Capítulo, mantendo a mesma estrutura de arquivo (incluindo `motivo_condutor`).
