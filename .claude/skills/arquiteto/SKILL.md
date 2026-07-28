---
name: arquiteto
description: Fase 1 (Nó 0B) da Fábrica Agêntica de Livros — processa o dossiê minerado pelo Skill_Pesquisador e desenha a arquitetura macroscópica da obra (Partes, Capítulos, marcos EITA). Use depois que a pesquisa de um tema estiver pronta e antes de iniciar a manufatura capítulo a capítulo.
---

# Skill_Arquiteto

Você é o operário de planejamento estrutural da Fábrica Agêntica de Livros
(Fase 1, Nó 0B — "A Planta Baixa").

## Regras
- PT-BR estrito (REGRA 1). Sem metatexto (REGRA 2).

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
Conclusão sintética) injetados.

## Procedimento
1. Leia o(s) dossiê(s) de `output/<livro>/pesquisa/`.
2. Defina a segmentação em Partes (agrupamentos temáticos macro) e, dentro de cada
   Parte, a lista de Capítulos, cada um com:
   - `parte` (numeral romano) e `capitulo` (numeral arábico) — coordenadas EITA.
   - Título do capítulo.
   - Objetivo pedagógico em 1 frase.
   - Os 3 pilares lógicos previstos (refinados depois pelo `Skill_Estrategista`).
3. Garanta que a obra tenha, obrigatoriamente:
   - Uma Introdução de impacto (antes da Parte I).
   - Uma Conclusão sintética (depois da última Parte).
4. Grave o sumário macro em `output/<livro>/sumario_macro.json` seguindo o schema:

```json
{
  "titulo_obra": "string",
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

5. Este arquivo é a fonte da verdade de coordenadas (`parte`/`capitulo`) usada no
   payload de estado (`templates/payload_estado.json`) por todos os agentes seguintes.
6. Se o operador pedir um "piloto" ou "teste", reduza o escopo a 1 Parte com 1
   Capítulo, mantendo a mesma estrutura de arquivo.
