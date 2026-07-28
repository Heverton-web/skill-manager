# Guia de Estilo Visual Premium — Livro AIDD

## Filosofia Visual
Dark tech premium com acentos dourados. O visual deve comunicar:
- **Inovação** — tecnologia de ponta, AI, futuro
- **Credibilidade** — conteúdo técnico profundo, pesquisa rigorosa
- **Prêmio** — qualidade de conteúdo digna de uma publicação O'Reilly

## Paleta de Cores

```
Fundo Principal:  #0a0a0f (preto rico)
Fundo Secundário: #111116 (preto elevado)
Superfície Card:  #1a1a2e (azul meia-noite)
Borda:           #1a1a1a → #2a2a2a (gradiente sutil)

Texto Principal:  #eaeaea (branco quente)
Texto Secundário: #888 (cinza médio)
Texto Terciário:  #555 (cinza escuro)

Acento Primário:  #d4af37 (dourado)
Acento Secundário:#f0d060 (dourado claro)
Destaque:        #ff6b6b (vermelho vinho para dados críticos)
```

## Tipografia

| Elemento | Fonte | Tamanho | Peso |
|----------|-------|---------|------|
| Título Capa | Georgia | 3.5em | Bold |
| Título Seção | Georgia | 2.2em | Bold |
| Corpo | Inter | 1.05em | Regular |
| Código | JetBrains Mono | 0.9em | Regular |
| Eyebrow | Inter Mono | 11px | Uppercase |

## Espaçamento
- Margens de página: 2.4cm (laterais), 2.6cm (topo), 2.8cm (base)
- Espaçamento entre seções: 3em
- Padding de cards: 2em
- Gap de grid: 1.5em

## Elementos Visuais

### Capa
- Gradiente radial: #0a0a0f → #1a1a2e
- Título centralizado em Georgia dourado
- Linha divisória dourada de 80px
- Elemento decorativo: circuito estilizado em opacidade 5%

### Diagramas
- Fundo escuro (#111116)
- Linhas em dourado (#d4af37) com opacidade 80%
- Nós com glow sutil (filter: drop-shadow)
- Animações SMIL para fluxo de dados

### Ícones
- Phosphor Icons (família única)
- strokeWidth: 1.5
- Cor: dourado ou branco conforme contexto

## Micro-Interações
- Hover em cards: border-color → dourado, translateY -2px
- Botões: scale 0.98 no active
- Scroll reveals: opacity 0→1, y 24→0, duração 0.6s

## O que EVITAR
- ❌ Gradientes roxo/azul de AI (lila rule)
- ❌ Gaussian blur excessivo
- ❌ Mais de 1 acento de cor
- ❌ Inter como fonte padrão (usar Geist ou alternativa)
- ❌ Cards em fundo branco puro (#ffffff → usar off-white)
