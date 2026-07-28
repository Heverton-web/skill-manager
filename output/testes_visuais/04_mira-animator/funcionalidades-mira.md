# MIRA Animator — Funcionalidades Exploradas

## 3 Artefatos Gerados

### 1. Deck de Apresentação (5 slides)
Navegação por teclado + dots, glassmorphism, Tailwind, animações fade-up.
Ideal para: pitch do livro, aulas, webinars.

### 2. Chart Race (SVG animado)
Barras horizontais animadas mostrando adoção de IDEs agênticas.
Ideal para: inserir no livro como figura estatística.

### 3. Metáfora Animada (SVG)
Partículas orbitando núcleo central com morphing de raio.
Ideal para: abertura de capítulo, transição visual.

## Pipeline MIRA Completo (39 agentes)
extract → planner → copywriter → builder → animator → 3D → SVG → chart

## Instalação
```bash
mkdir pasta- slides && cd pasta-slides
npx mira-animator install
npx mira-animator link /caminho/para/fonte --name=aidd
# No Claude: /mira-new "apresentação AIDD"
# Depois: fill the deck aidd with content from the aidd source
```