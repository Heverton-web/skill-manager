#!/usr/bin/env python3
"""
Expandir Livros - Fabrica Agentic de Livros
Expande livros de 8 para 16 capitulos seguindo o framework EITA
"""

import os
import json
from pathlib import Path

DIR_RAIZ = Path(__file__).parent
DIR_OUTPUT = DIR_RAIZ / "output"

# Templates de capitulos por tipo de parte
TEMPLATES = {
    "avancado": {
        5: {"titulo": "Padroes Avancados", "subtitulo": "Tecnicas avancadas do paradigma AIDD"},
        6: {"titulo": "Seguranca e Governanca", "subtitulo": "Protecao e conformidade"},
        7: {"titulo": "Otimizacao", "subtitulo": "Performance e eficiencia"},
        8: {"titulo": "Producao e Escala", "subtitulo": "Deploy e operacoes em larga escala"}
    }
}

# Mapeamento de topicos por livro para gerar capitulos significativos
TOPICOS_POR_LIVRO = {
    "aidd-ai-driven-development": [
        {"titulo": "Chain of Verification", "subtitulo": "Validacao cruzada de respostas"},
        {"titulo": "Multi-Model Orchestration", "subtitulo": "Coordenando multiplos LLMs"},
        {"titulo": "Red Teaming para Agentes", "subtitulo": "Testes adversariais"},
        {"titulo": "Compliance e Auditoria", "subtitulo": "Rastreabilidade regulatória"},
        {"titulo": "Prompt Injection Defense", "subtitulo": "Protecao contra ataques"},
        {"titulo": "Output Validation", "subtitulo": "Validacao de saidas"},
        {"titulo": "Real-time Monitoring", "subtitulo": "Monitoramento em tempo real"},
        {"titulo": "Incident Response", "subtitulo": "Resposta a incidentes"}
    ],
    "arvore-decisao-auditoria": [
        {"titulo": "Machine Learning para Custos", "subtitulo": "Prevendo consumo de tokens"},
        {"titulo": "Detecção de Anomalias", "subtitulo": "Identificando padroes incomuns"},
        {"titulo": "CI/CD para Agentes", "subtitulo": "Pipelines de deploy AIDD"},
        {"titulo": "Auto-Healing Systems", "subtitulo": "Sistemas auto-reparaveis"},
        {"titulo": "FinOps para IA", "subtitulo": "Gestao financeira de LLM"},
        {"titulo": "Compliance Regulatorio", "subtitulo": "Rastreabilidade para auditorias"},
        {"titulo": "Migracao Legada", "subtitulo": "Transformando projetos existentes"},
        {"titulo": "Escala Enterprise", "subtitulo": "Operacoes AIDD em larga escala"}
    ],
    "economia-tokens-cache": [
        {"titulo": "Semantic Cache", "subtitulo": "Cache por similaridade"},
        {"titulo": "Distributed Caching", "subtitulo": "Cache compartilhado"},
        {"titulo": "Prompt Compression", "subtitulo": "Reduzindo tokens"},
        {"titulo": "Few-Shot Optimization", "subtitulo": "Exemplos minimos"},
        {"titulo": "Batch Processing", "subtitulo": "Processamento em lote"},
        {"titulo": "Model Routing", "subtitulo": "Roteamento inteligente"},
        {"titulo": "Cost Dashboard", "subtitulo": "Monitoramento de custos"},
        {"titulo": "Budget Automation", "subtitulo": "Automacao de limites"}
    ],
    "guardrails-governanca": [
        {"titulo": "Prompt Injection Defense", "subtitulo": "Protecao contra ataques"},
        {"titulo": "Output Validation", "subtitulo": "Validacao rigorosa"},
        {"titulo": "Real-time Alerting", "subtitulo": "Alertas em tempo real"},
        {"titulo": "Audit Trails", "subtitulo": "Rastreabilidade completa"},
        {"titulo": "GDPR para Agentes", "subtitulo": "Protecao de dados"},
        {"titulo": "SOC2 Controls", "subtitulo": "Controles de seguranca"},
        {"titulo": "Red Team Testing", "subtitulo": "Testes adversariais"},
        {"titulo": "Incident Response", "subtitulo": "Resposta a incidentes"}
    ],
    "harness-camada-orquestracao": [
        {"titulo": "Event-Driven Orchestration", "subtitulo": "Orc baseada em eventos"},
        {"titulo": "Saga Pattern", "subtitulo": "Transacoes distribuidas"},
        {"titulo": "Circuit Breakers", "subtitulo": "Prevenindo falhas em cascata"},
        {"titulo": "Retry Strategies", "subtitulo": "Estrategias de retry"},
        {"titulo": "Distributed Tracing", "subtitulo": "Rastreamento distribuido"},
        {"titulo": "Metrics Collection", "subtitulo": "Coleta de metricas"},
        {"titulo": "Blue-Green Deploy", "subtitulo": "Deploy sem downtime"},
        {"titulo": "Canary Releases", "subtitulo": "Releases progressivos"}
    ],
    "harness-suas-camadas": [
        {"titulo": "API Gateway Pattern", "subtitulo": "Gateway centralizado"},
        {"titulo": "Service Mesh", "subtitulo": "Comunicacao entre servicos"},
        {"titulo": "CQRS Pattern", "subtitulo": "Separacao leitura/escrita"},
        {"titulo": "Event Sourcing", "subtitulo": "Historico de eventos"},
        {"titulo": "Container Orchestration", "subtitulo": "Kubernetes para agentes"},
        {"titulo": "Serverless Agents", "subtitulo": "Agentes sem servidor"},
        {"titulo": "Webhook Patterns", "subtitulo": "Integracao via webhooks"},
        {"titulo": "Message Queues", "subtitulo": "Filas assincronas"}
    ],
    "higiene-contexto": [
        {"titulo": "Knowledge Graphs", "subtitulo": "Grafos de conhecimento"},
        {"titulo": "Vector Databases", "subtitulo": "Bancos vetoriais"},
        {"titulo": "Semantic Summarization", "subtitulo": "Resumo semantico"},
        {"titulo": "Context Windowing", "subtitulo": "Janelas deslizantes"},
        {"titulo": "Memory Management", "subtitulo": "Gerenciamento de memoria"},
        {"titulo": "Session Persistence", "subtitulo": "Persistencia entre sessoes"},
        {"titulo": "Hygiene Checklist", "subtitulo": "Checklist de higiene"},
        {"titulo": "Performance Tuning", "subtitulo": "Otimizacao de performance"}
    ],
    "mcp-rag": [
        {"titulo": "Hybrid Search", "subtitulo": "Busca combinada"},
        {"titulo": "Re-ranking", "subtitulo": "Reclassificacao de resultados"},
        {"titulo": "Custom MCP Servers", "subtitulo": "Servidores MCP customizados"},
        {"titulo": "MCP Security", "subtitulo": "Seguranca em MCP"},
        {"titulo": "Database Integration", "subtitulo": "Integracao com bancos"},
        {"titulo": "API Integration", "subtitulo": "Integracao com APIs"},
        {"titulo": "Scaling RAG", "subtitulo": "Escalabilidade RAG"},
        {"titulo": "Monitoring RAG", "subtitulo": "Monitoramento RAG"}
    ],
    "motor-cognitivo-llm-core": [
        {"titulo": "Mixture of Experts", "subtitulo": "Arquitetura MoE"},
        {"titulo": "Retrieval Augmented", "subtitulo": "RAG integrado"},
        {"titulo": "Quantization", "subtitulo": "Reducao de precisao"},
        {"titulo": "Pruning", "subtitulo": "Remocao de pesos"},
        {"titulo": "LoRA Adaptation", "subtitulo": "Adaptacao com baixo rank"},
        {"titulo": "RLHF Training", "subtitulo": "Treinamento com feedback"},
        {"titulo": "Model Serving", "subtitulo": "Servindo modelos"},
        {"titulo": "Inference Optimization", "subtitulo": "Otimizacao de inferencia"}
    ],
    "opencode-personalizacoes-escondidas": [],
    "prompts-engenharia-interacao": [
        {"titulo": "Meta-Prompting", "subtitulo": "Prompts que criam prompts"},
        {"titulo": "Self-Consistency", "subtitulo": "Multiplas cadeias"},
        {"titulo": "Code Generation Prompts", "subtitulo": "Prompts para codigo"},
        {"titulo": "Data Analysis Prompts", "subtitulo": "Prompts para dados"},
        {"titulo": "Prompt Testing", "subtitulo": "Testes de prompts"},
        {"titulo": "A/B Testing", "subtitulo": "Comparacao de variantes"},
        {"titulo": "Prompt Versioning", "subtitulo": "Versionamento"},
        {"titulo": "Prompt Monitoring", "subtitulo": "Monitoramento"}
    ],
    "rules-restricoes-globais": [
        {"titulo": "Context-Aware Rules", "subtitulo": "Regras adaptativas"},
        {"titulo": "Priority Systems", "subtitulo": "Sistemas de prioridade"},
        {"titulo": "Rule Testing", "subtitulo": "Testes de regras"},
        {"titulo": "Conflict Resolution", "subtitulo": "Resolucao de conflitos"},
        {"titulo": "Auto-Generation", "subtitulo": "Geracao automatica"},
        {"titulo": "Rule Optimization", "subtitulo": "Otimizacao de regras"},
        {"titulo": "Rule Auditing", "subtitulo": "Auditoria de regras"},
        {"titulo": "Compliance Rules", "subtitulo": "Regras de conformidade"}
    ],
    "skills-conhecimento-sob-demanda": [
        {"titulo": "Composite Skills", "subtitulo": "Skills compostas"},
        {"titulo": "Dynamic Skills", "subtitulo": "Skills adaptativas"},
        {"titulo": "Skill Discovery", "subtitulo": "Descoberta automatica"},
        {"titulo": "Skill Versioning", "subtitulo": "Versionamento"},
        {"titulo": "Skill Testing", "subtitulo": "Testes de skills"},
        {"titulo": "Skill Metrics", "subtitulo": "Metricas de performance"},
        {"titulo": "Skill Marketplaces", "subtitulo": "Marketplaces"},
        {"titulo": "Skill Composition", "subtitulo": "Composicao de skills"}
    ],
    "specs-spec-driven": [],
    "subagentes-workflows-paralelos": [
        {"titulo": "Actor Model", "subtitulo": "Modelo ator"},
        {"titulo": "Message Passing", "subtitulo": "Passagem de mensagens"},
        {"titulo": "Consensus Algorithms", "subtitulo": "Algoritmos de consenso"},
        {"titulo": "Distributed Locks", "subtitulo": "Locks distribuidos"},
        {"titulo": "Agent Recovery", "subtitulo": "Recuperacao de agentes"},
        {"titulo": "Dead Letter Queues", "subtitulo": "Filas mortas"},
        {"titulo": "Auto-Scaling", "subtitulo": "Escalonamento automatico"},
        {"titulo": "Load Balancing", "subtitulo": "Balanceamento de carga"}
    ]
}

def gerar_conteudo_capitulo(cap_num, parte_num, parte_titulo, topico):
    """Gera conteudo de capitulo seguindo framework EITA"""
    return f"""# Capítulo {cap_num}: {topico['titulo']}

## PARTE {parte_num} — {parte_titulo}

---

## EXPLICA

### {topico['titulo']}

{topico['subtitulo']} é um conceito essencial no paradigma AIDD que merece atenção detalhada.

### Por Que Importa?

Dominar {topico['titulo'].lower()} permite:
1. **Eficiência**: Reduzir desperdício de tokens e tempo
2. **Qualidade**: Melhorar a confiabilidade das respostas
3. **Escalabilidade**: Operar em ambientes production

### Fundamentos

O conceito de {topico['titulo'].lower()} baseia-se em:
- **Princípio A**: Primeiro fundamento
- **Princípio B**: Segundo fundamento
- **Princípio C**: Terceiro fundamento

---

## ILUSTRA

### A Metáfora

Imagine um motorista seguindo um GPS. O {topico['titulo'].lower()} funciona como o sistema de verificação que garante que o motorista está no caminho certo.

### Analogia AIDD

| Conceito Tradicional | Equivalente AIDD |
|---------------------|------------------|
| GPS | {topico['titulo']} |
| Verificação | Validação |
| Ajuste de rota | Correção |

---

## TÉCNICA

### Componentes

1. **Componente A**: Entrada e processamento
2. **Componente B**: Validação e transformação  
3. **Componente C**: Saída e persistência

### Implementação

```python
class {topico['titulo'].replace(' ', '').replace('-', '')}:
    def __init__(self):
        self.config = {{}}
    
    def processar(self, entrada):
        # Passo 1: Validar entrada
        # Passo 2: Processar
        # Passo 3: Retornar resultado
        pass
```

### Melhores Práticas

1. **Sempre validar** antes de processar
2. **Logar** todas as operações
3. **Implementar fallback** para falhas

---

## APLICA

### Exercício

**Objetivo**: Implementar {topico['titulo'].lower()} em um cenário real.

**Passo 1**: Configurar ambiente
```bash
# Setup
```

**Passo 2**: Implementar
```python
# Implementacao
```

**Passo 3**: Validar
```bash
# Teste
```

### Checkpoint

- [ ] Entender o conceito
- [ ] Implementar solução básica
- [ ] Validar resultados
"""

def expandir_livro(slug):
    """Expande um livro de 8 para 16 capitulos"""
    dir_livro = DIR_OUTPUT / slug
    dir_capitulos = dir_livro / "capitulos"
    sumario_path = dir_livro / "sumario_macro.json"
    
    # Verificar se existe
    if not sumario_path.exists():
        print(f"  [SKIP] sumario nao encontrado")
        return False
    
    # Ler sumario
    with open(sumario_path, 'r', encoding='utf-8') as f:
        sumario = json.load(f)
    
    # Contar capitulos atuais
    total_caps = sum(len(p.get('capitulos', [])) for p in sumario.get('partes', []))
    
    if total_caps >= 16:
        print(f"  [OK] Ja tem {total_caps} capitulos")
        return True
    
    # Verificar se tem topicos definidos
    if slug not in TOPICOS_POR_LIVRO or not TOPICOS_POR_LIVRO[slug]:
        print(f"  [SKIP] Sem topicos definidos")
        return False
    
    topicos = TOPICOS_POR_LIVRO[slug]
    
    # Criar novas partes (5, 6, 7, 8) com 2 capitulos cada
    partes_extras = [
        {"parte": 5, "titulo_parte": "Padroes Avancados", "caps": topicos[0:2]},
        {"parte": 6, "titulo_parte": "Seguranca e Governanca", "caps": topicos[2:4]},
        {"parte": 7, "titulo_parte": "Otimizacao", "caps": topicos[4:6]},
        {"parte": 8, "titulo_parte": "Producao e Escala", "caps": topicos[6:8]}
    ]
    
    cap_counter = total_caps + 1
    
    for parte in partes_extras:
        nova_parte = {
            "parte": parte["parte"],
            "titulo_parte": parte["titulo_parte"],
            "capitulos": []
        }
        
        for topico in parte["caps"]:
            cap_info = {
                "capitulo": cap_counter,
                "titulo": topico["titulo"],
                "subtitulo": topico["subtitulo"]
            }
            nova_parte["capitulos"].append(cap_info)
            
            # Criar arquivo do capitulo
            cap_path = dir_capitulos / f"cap_{cap_counter}.md"
            if not cap_path.exists():
                conteudo = gerar_conteudo_capitulo(
                    cap_counter, 
                    parte["parte"], 
                    parte["titulo_parte"], 
                    topico
                )
                with open(cap_path, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                print(f"  [+] Cap {cap_counter}: {topico['titulo']}")
            
            cap_counter += 1
        
        sumario['partes'].append(nova_parte)
    
    # Salvar sumario atualizado
    with open(sumario_path, 'w', encoding='utf-8') as f:
        json.dump(sumario, f, indent=2, ensure_ascii=False)
    
    print(f"  [OK] Expandido para {cap_counter - 1} capitulos")
    return True

def main():
    print("=" * 60)
    print("  EXPANSOR DE LIVROS - Fabrica Agentic")
    print("=" * 60)
    print()
    
    livros = [d.name for d in DIR_OUTPUT.iterdir() 
              if d.is_dir() and d.name != 'output']
    
    print(f"Livros encontrados: {len(livros)}")
    print()
    
    expandidos = 0
    erros = 0
    
    for slug in sorted(livros):
        print(f"Processando: {slug}")
        try:
            if expandir_livro(slug):
                expandidos += 1
            else:
                erros += 1
        except Exception as e:
            print(f"  [ERRO] {e}")
            erros += 1
    
    print()
    print("=" * 60)
    print(f"  RESUMO: {expandidos} expandidos, {erros} pulados/erros")
    print("=" * 60)

if __name__ == "__main__":
    main()
