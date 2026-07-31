#!/usr/bin/env python3
"""
Dados das 4 Séries 'Do Zero ao Profissional' (ZP1-ZP4) — 80 livros
Jornada progressiva por série: Livro 1 = absoluto zero, Livro 20 = profissional.

  - ZP1: JavaScript: Do Zero ao Profissional (20 livros)
  - ZP2: Python: Do Zero ao Profissional (20 livros)
  - ZP3: SQL e Bancos de Dados: Do Zero ao Profissional (20 livros)
  - ZP4: Git e Controle de Versão: Do Zero ao Profissional (20 livros)

Cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-zp.py e compilar-para-pdf.py

NOTA: os livros vivem nos arquivos companheiros dados_series_zp_js.py,
dados_series_zp_python.py, dados_series_zp_sql.py e dados_series_zp_git.py,
mesclados abaixo. Ao copiar/clonar, leve os 5 arquivos juntos.
"""

from dados_series_zp_js import LIVROS_ZP_JS
from dados_series_zp_python import LIVROS_ZP_PYTHON
from dados_series_zp_sql import LIVROS_ZP_SQL
from dados_series_zp_git import LIVROS_ZP_GIT

SERIES_ZP = {
    "ZP1": {"nome": "JavaScript: Do Zero ao Profissional", "prefixo": "ZP1"},
    "ZP2": {"nome": "Python: Do Zero ao Profissional", "prefixo": "ZP2"},
    "ZP3": {"nome": "SQL e Bancos de Dados: Do Zero ao Profissional", "prefixo": "ZP3"},
    "ZP4": {"nome": "Git e Controle de Versão: Do Zero ao Profissional", "prefixo": "ZP4"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
# Estruturadas como jornada: Fundamentos -> Prática -> Aprofundamento -> Mercado
SERIES_PARTES = {
    "ZP1": ["Fundamentos da Linguagem", "DOM, Interatividade e APIs", "TypeScript, Algoritmos e Testes", "Backend, Projeto e Carreira"],
    "ZP2": ["Fundamentos da Linguagem", "Dados, Automação e Análise", "Web, Bancos e Testes", "IA, Projeto e Carreira"],
    "ZP3": ["Fundamentos e Modelagem", "Otimização e Transações", "Bancos na Prática e NoSQL", "Analítica, Big Data e Carreira"],
    "ZP4": ["Fundamentos do Git", "Trabalho Remoto e GitHub", "Git Avançado e Automação", "Open Source, Segurança e Carreira"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_ZP = {}
LIVROS_ZP.update(LIVROS_ZP_JS)
LIVROS_ZP.update(LIVROS_ZP_PYTHON)
LIVROS_ZP.update(LIVROS_ZP_SQL)
LIVROS_ZP.update(LIVROS_ZP_GIT)

SLUGS_ZP = list(LIVROS_ZP.keys())
