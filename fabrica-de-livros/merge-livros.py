#!/usr/bin/env python3
"""
Merge de Todos os Livros - Fabrica Agentic
Combina todos os livros em 1 mega-livro com renumeracao de capitulos
"""

import os
import json
import re
from pathlib import Path

DIR_RAIZ = Path(__file__).parent
DIR_OUTPUT = DIR_RAIZ / "output"
MEGA_SLUG = "mega-livro-todos-aidd"

def obter_titulo_livro(slug):
    """Le o titulo do sumario_macro.json"""
    sumario_path = DIR_OUTPUT / slug / "sumario_macro.json"
    if sumario_path.exists():
        with open(sumario_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('titulo_obra', slug.replace('-', ' ').title())
    return slug.replace('-', ' ').title()

def renumerar_capitulo(conteudo, novo_numero):
    """Renumeria capitulos no conteudo markdown"""
    # Substitui "# Capitulo X:" por novo numero
    conteudo = re.sub(
        r'# Capítulo \d+:',
        f'# Capítulo {novo_numero}:',
        conteudo
    )
    # Substitui "## PARTE X" - mantem como esta (sera substituido pelo separador)
    return conteudo

def merge_todos_livros():
    """Faz merge de todos os livros em 1 mega-livro"""
    print("=" * 60)
    print("  MERGE DE LIVROS - Fabrica Agentic")
    print("=" * 60)
    print()
    
    # Listar livros (excluindo output e mega-livro se existir)
    livros = sorted([
        d.name for d in DIR_OUTPUT.iterdir()
        if d.is_dir() and d.name not in ['output', MEGA_SLUG]
    ])
    
    print(f"Livros encontrados: {len(livros)}")
    print()
    
    # Criar diretorio do mega-livro
    dir_mega = DIR_OUTPUT / MEGA_SLUG
    dir_mega.mkdir(exist_ok=True)
    dir_caps = dir_mega / "capitulos"
    dir_caps.mkdir(exist_ok=True)
    dir_pesq = dir_mega / "pesquisa"
    dir_pesq.mkdir(exist_ok=True)
    
    # Estrutura do mega sumario
    mega_sumario = {
        "titulo_obra": "Guia Completo de AI-Driven Development",
        "subtitulo": "Todos os Livros da Fabrica Agentic de Livros",
        "introducao": "Esta obra compila todos os livros produzidos pela Fabrica Agentic de Livros sobre AI-Driven Development, abrangendo desde fundamentos conceituais ate padroes avancados de orquestracao de agentes.",
        "conclusao": "Ao longo desta obra, exploramos os multiplos facetas do paradigma AI-Driven Development, desde a engenharia de prompts ate a governanca algoritmica. O conhecimento acumulado nestes 15 livros forma uma base solida para qualquer profissional que deseja dominar a arte de orquestrar agentes de IA.",
        "partes": []
    }
    
    cap_global = 1
    conteudo_mega = []
    
    for i, slug in enumerate(livros, 1):
        titulo = obter_titulo_livro(slug)
        dir_livro = DIR_OUTPUT / slug
        dir_caps_livro = dir_livro / "capitulos"
        
        print(f"[{i}/{len(livros)}] Processando: {slug}")
        
        # Adicionar separador do livro
        conteudo_mega.append(f"\n\n---\n\n# PARTE {i} — {titulo}\n\n")
        
        # Encontrar todos os capitulos deste livro
        caps_livro = sorted([
            f for f in os.listdir(dir_caps_livro)
            if f.startswith('cap_') and f.endswith('.md')
        ]) if dir_caps_livro.exists() else []
        
        # Criar entrada no sumario para este livro (como parte)
        parte = {
            "parte": i,
            "titulo_parte": titulo,
            "capitulos": []
        }
        
        for cap_file in caps_livro:
            cap_path = dir_caps_livro / cap_file
            with open(cap_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Renumerar capitulo
            conteudo_renumerado = renumerar_capitulo(conteudo, cap_global)
            conteudo_mega.append(conteudo_renumerado)
            conteudo_mega.append("\n\n")
            
            # Extrair titulo do capitulo
            titulo_match = re.search(r'# Capítulo \d+:\s*(.+)', conteudo)
            titulo_cap = titulo_match.group(1).strip() if titulo_match else f"Capítulo {cap_global}"
            
            parte["capitulos"].append({
                "capitulo": cap_global,
                "titulo": titulo_cap,
                "subtitulo": ""
            })
            
            # Salvar capitulo renumerado no mega-livro
            cap_mega_path = dir_caps / f"cap_{cap_global}.md"
            with open(cap_mega_path, 'w', encoding='utf-8') as f:
                f.write(conteudo_renumerado)
            
            cap_global += 1
        
        mega_sumario["partes"].append(parte)
        print(f"  -> {len(caps_livro)} capitulos (globais: {cap_global - len(caps_livro)}-{cap_global - 1})")
    
    # Salvar sumario do mega-livro
    sumario_path = dir_mega / "sumario_macro.json"
    with open(sumario_path, 'w', encoding='utf-8') as f:
        json.dump(mega_sumario, f, indent=2, ensure_ascii=False)
    
    # Salvar livro_final.md do mega-livro
    livro_final_path = dir_mega / "livro_final.md"
    with open(livro_final_path, 'w', encoding='utf-8') as f:
        f.write("![Capa do Livro](imagens/capa.svg)\n\n")
        f.write("# Guia Completo de AI-Driven Development\n\n")
        f.write("*Todos os Livros da Fabrica Agentic de Livros*\n\n")
        f.write("---\n\n")
        f.writelines(conteudo_mega)
        f.write("\n\n---\n\n![Contracapa do Livro](imagens/contracapa.svg)\n")
    
    # Relatorio
    print()
    print("=" * 60)
    print("  RELATORIO - MERGE CONCLUIDO")
    print("=" * 60)
    print(f"  Livros mergeados: {len(livros)}")
    print(f"  Total de capitulos: {cap_global - 1}")
    print(f"  MEGA SLUG: {MEGA_SLUG}")
    print(f"  Livro final: {livro_final_path}")
    print(f"  Sumario: {sumario_path}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    merge_todos_livros()
