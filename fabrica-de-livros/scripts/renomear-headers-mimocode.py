#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renomeia os headers ### que ficaram truncados apos a mescla de subsecoes,
usando titulos limpos e descritivos baseados no conteudo fundido de cada secao."""
import re
from pathlib import Path

DIR = Path('output/livros/mimocode/capitulos')

RENOMEAR = {
    'cap_01': [
        ('### MiMoCode e', '### O MiMoCode em três registros'),
        ('### Decisão open-source e a', '### A decisão open-source'),
        ('### Custo e a', '### O custo e a transparência'),
    ],
    'cap_02': [
        ('### Papel das', '### O papel das ferramentas e das permissões'),
        ('### Cliente-servidor e o', '### Cliente-servidor e suas consequências'),
        ('### Memória persistente e', '### Memória persistente e suas consequências'),
        ('### Loop e', '### O loop: contexto, limite e modos'),
        ('### Arquitetura e', '### A arquitetura e o modelo de negócio'),
    ],
    'cap_03': [
        ('### Escolha do canal e', '### A escolha do canal de instalação'),
        ('### Onboarding e', '### O onboarding e a curva de aprendizado'),
        ('### Estrutura de', '### A estrutura de pastas'),
        ('### Primeiro turno e', '### O primeiro turno'),
        ('### Instalação e o', '### A instalação e o ecossistema'),
    ],
    'cap_04': [
        ('### Sistema de', '### O sistema de credenciais'),
        ('### Sintaxe provider/model e', '### A sintaxe provider/model'),
        ('### Small_model e', '### O small_model'),
    ],
    'cap_05': [
        ('### Três modos e', '### Os três modos de operação'),
        ('### Modo Compose e', '### O modo Compose'),
        ('### AGENTS.md e o', '### AGENTS.md e o versionamento'),
        ('### Contexto da ordem de', '### O contexto da ordem de serviço'),
        ('### Operação em', '### A operação em equipe'),
    ],
    'cap_06': [
        ('### Modo não-interativo e', '### O modo não-interativo'),
        ('### Flags essenciais e', '### As flags essenciais'),
        ('### Sessões pela CLI e', '### Sessões pela CLI'),
        ('### Integração com', '### A integração com GitHub'),
        ('### Mimo run', '### O mimo run na prática'),
        ('### Mimo run e', '### O mimo run e a operação fina'),
    ],
    'cap_07': [
        ('### Modelo de', '### O modelo de precedência'),
        ('### Schema e', '### O schema da configuração'),
        ('### Permissões e', '### As permissões'),
        ('### Agentes custom e', '### Agentes custom'),
        ('### Small_model e a', '### O small_model na configuração'),
        ('### Configuração e o', '### A configuração e o ambiente do time'),
    ],
    'cap_08': [
        ('### MCP e', '### O MCP'),
        ('### ACP e', '### O ACP'),
        ('### Plugins e', '### Os plugins'),
        ('### Mimo db e', '### O mimo db'),
        ('### Gestão de', '### A gestão de contexto'),
    ],
    'cap_09': [
        ('### Memória persistente', '### A memória persistente'),
        ('### /dream e', '### O comando /dream'),
        ('### /distill e', '### O comando /distill'),
        ('### Compactação e', '### A compactação de contexto'),
        ('### /goal e', '### O comando /goal'),
        ('### Compactação e a', '### A compactação e o custo'),
    ],
    'cap_10': [
        ('### Workflows determinísticos e', '### Os workflows determinísticos'),
        ('### Modo Compose e', '### O modo Compose'),
        ('### Subagentes em paralelo e', '### Subagentes em paralelo'),
        ('### Skills nativas e', '### Skills nativas'),
        ('### Ecossistema e', '### O ecossistema'),
        ('### Plano de', '### O plano de adoção'),
    ],
}

def main():
    for n, pares in RENOMEAR.items():
        p = DIR / f'{n}.md'
        t = p.read_text(encoding='utf-8')
        for velho, novo in pares:
            qtd = t.count(velho)
            if qtd:
                t = t.replace(velho, novo)
                print(f'[ok] {n}: {velho.strip()} -> {novo.strip()} ({qtd}x)')
            else:
                print(f'[!!] {n}: NAO ENCONTRADO: {velho}')
        p.write_text(t, encoding='utf-8')

if __name__ == '__main__':
    main()
