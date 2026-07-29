#!/usr/bin/env python3
"""
Expandir Todos os Livros - Fábrica Agêntica de Livros
Expande livros de 8 para 16+ capítulos seguindo o framework EITA
"""

import os
import json
from pathlib import Path

DIR_RAIZ = Path(__file__).parent
DIR_OUTPUT = DIR_RAIZ / "output"

# Mapeamento de expansão: quais capítulos adicionar para cada livro
EXPANSAO_POR_LIVRO = {
    "aidd-ai-driven-development": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Padrões Avançados de AIDD",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Chain of Verification", "subtitulo": "Validação cruzada de respostas entre modelos"},
                    {"capitulo": 14, "titulo": "Multi-Model Orchestration", "subtitulo": "Coordenando múltiplos LLMs para uma tarefa"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Segurança e Governança",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Red Teaming para Agentes", "subtitulo": "Testes adversariais e hardening de prompts"},
                    {"capitulo": 16, "titulo": "Compliance e Auditoria", "subtitulo": "Rastreabilidade e conformidade regulatória"}
                ]
            }
        ],
        "novos_capitulos": {
            13: """# Capítulo 13: Chain of Verification

## PARTE 5 — Padrões Avançados de AIDD

---

## EXPLICA

### O Problema das Alucinações

Quando um LLM gera uma resposta, não há garantia de que tudo é factualmente correto. As **alucinações** são respostas que parecem plausíveis mas são inventadas ou incorretas.

A **Chain of Verification (CoV)** é uma técnica onde o modelo:
1. Gera uma resposta inicial
2. Cria perguntas de verificação
3. Responde cada pergunta independentemente
4. Revisa a resposta original com base nas verificações

### Como Funciona o CoV

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAIN OF VERIFICATION                     │
├─────────────────────────────────────────────────────────────┤
│  1. Resposta Inicial                                        │
│     └→ "O React usa Virtual DOM para otimizar updates"      │
│                                                              │
│  2. Perguntas de Verificação                                │
│     ├→ "O React realmente usa Virtual DOM?"                 │
│     └→ "Virtual DOM é mais rápido que DOM real?"            │
│                                                              │
│  3. Verificação Independente                                │
│     ├→ Sim, React usa Virtual DOM (desde 2013)              │
│     └→ Não necessariamente - depende do caso                │
│                                                              │
│  4. Resposta Revisada                                       │
│     └→ "O React usa Virtual DOM para minimizar operações    │
│         diretas no DOM real, mas não é sempre mais rápido"  │
└─────────────────────────────────────────────────────────────┘
```

---

## ILUSTRA

### A Metáfora do Jornalista Investigativo

Um bom jornalista nunca publica uma notícia sem **verificar as fontes**:

1. **Entrevista inicial**: Coleta depoimentos
2. **Verificação**: Confirma com documentos oficiais
3. **Confronto**: Pergunta para a outra parte
4. **Publicação**: Escreve com múltiplas fontes confirmadas

### Analogia AIDD

| Jornalismo | Chain of Verification |
|------------|----------------------|
| Entrevista inicial | Resposta do LLM |
| Verificação de fontes | Perguntas de verificação |
| Confronto com outra parte | Respostas independentes |
| Publicação com fontes | Resposta revisada e validada |

---

## TÉCNICA

### Implementação do CoV

```python
class ChainOfVerification:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def verify(self, initial_response, context):
        # Passo 1: Gerar perguntas de verificação
        verification_prompt = f"""
        Resposta original: {initial_response}
        
        Gere 3 perguntas para verificar a accurácia desta resposta.
        Cada pergunta deve ser respondível com sim/não ou dados específicos.
        """
        questions = self.llm.generate(verification_prompt)
        
        # Passo 2: Responder cada pergunta independentemente
        answers = []
        for question in questions:
            answer_prompt = f"""
            Pergunta: {question}
            Contexto: {context}
            
            Responda de forma objetiva e factual.
            """
            answer = self.llm.generate(answer_prompt)
            answers.append({"question": question, "answer": answer})
        
        # Passo 3: Revisar resposta original
        revision_prompt = f"""
        Resposta original: {initial_response}
        
        Verificações realizadas:
        {json.dumps(answers, indent=2)}
        
        Revis a resposta original com base nas verificações.
        Corrija qualquer imprecisão identificada.
        """
        revised_response = self.llm.generate(revision_prompt)
        
        return {
            "original": initial_response,
            "verifications": answers,
            "revised": revised_response
        }
```

### Template de Perguntas de Verificação

```markdown
## Perguntas de Verificação

1. **Factual**: [Afirmação] é verdadeira? Qual é a fonte?
2. **Causal**: [Relação de causa-efeito] é direta ou indireta?
3. **Temporal**: [Evento] aconteceu em [data]?
4. **Quantitativa**: [Número/estatística] está correto?
5. **Comparativa**: [Comparação] é justa e precisa?
```

---

## APLICA

### Exercício: Verificar uma Resposta Técnica

**Resposta para verificar**: "O TypeScript é um superset do JavaScript que adiciona tipagem estática e é compilado para JavaScript puro."

**Passo 1**: Gerar perguntas
1. TypeScript é realmente um superset de JavaScript?
2. Tipagem estática é a única adição?
3. TypeScript é compilado ou transpilado?

**Passo 2**: Verificar independentemente
1. Sim, todo código JavaScript válido é TypeScript válido
2. Não - também adiciona interfaces, enums, generics
3. Transpilado (não compilado para bytecode)

**Passo 3**: Resposta revisada
"TypeScript é um superset de JavaScript que adiciona tipagem estática, interfaces, enums, generics e outras features. É transpilado para JavaScript puro, não compilado."

### Checkpoint

- [ ] Entender o conceito de Chain of Verification
- [ ] Implementar um verificador básico
- [ ] Aplicar CoV em uma resposta técnica
""",
            14: """# Capítulo 14: Multi-Model Orchestration

## PARTE 5 — Padrões Avançados de AIDD

---

## EXPLICA

### Por Que Múltiplos Modelos?

Cada LLM tem forças e fraquezas:
- **Claude**: Excelente em raciocínio longo e código
- **GPT-4**: Forte em criatividade e conversação
- **Gemini**: Bom em processamento multimodal
- **Modelos locais**: Rápidos e baratos para tarefas simples

A **orquestração multi-modelo** combina o melhor de cada um.

### Padrões de Orquestração

```
┌─────────────────────────────────────────────────────────────┐
│                 PADRÕES MULTI-MODELO                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SEQUENCIAL (Pipeline)                                   │
│     Modelo A → Modelo B → Modelo C                          │
│     (Cada um processa a saída do anterior)                   │
│                                                              │
│  2. PARALELO (Fan-out)                                      │
│     Modelo A ─┬→ Resultado 1                                │
│     Modelo B ─┼→ Resultado 2  → Consolidação                │
│     Modelo C ─┴→ Resultado 3                                │
│                                                              │
│  3. HIERÁRQUICO (Router)                                    │
│     Router → Classifica → Envia para especialista            │
│                                                              │
│  4. DEBATE (Adversarial)                                    │
│     Modelo A ←→ Modelo B → Judge decide                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ILUSTRA

### A Metáfora do Consultório Médico

Quando você vai ao médico:
1. **Recepcionista** (Router): Identifica seu problema
2. **Clínico Geral** (Modelo geral): Faz diagnóstico inicial
3. **Especialista** (Modelo especializado): Profundidade no assunto
4. **Laboratório** (Verificação): Confirma o diagnóstico

### Analogia AIDD

| Consultório | Multi-Model AIDD |
|-------------|------------------|
| Recepcionista | Router/Classifier |
| Clínico Geral | Modelo principal |
| Especialista | Modelo focado |
| Laboratório | Chain of Verification |

---

## TÉCNICA

### Implementação de Router

```python
class ModelRouter:
    def __init__(self):
        self.models = {
            "coder": "claude-3-opus",      # Código
            "writer": "gpt-4",             # Escrita criativa
            "analyst": "gemini-pro",       # Análise de dados
            "fast": "claude-3-haiku"       # Tarefas simples
        }
    
    def route(self, task_type, complexity):
        if task_type == "code":
            return self.models["coder"]
        elif task_type == "creative":
            return self.models["writer"]
        elif task_type == "analysis":
            return self.models["analyst"]
        elif complexity == "simple":
            return self.models["fast"]
        else:
            return self.models["coder"]
```

### Pipeline Sequencial

```python
class SequentialPipeline:
    def __init__(self, steps):
        self.steps = steps  # [(model, prompt_template), ...]
    
    def execute(self, initial_input):
        current_input = initial_input
        results = []
        
        for model, prompt_template in self.steps:
            prompt = prompt_template.format(input=current_input)
            result = model.generate(prompt)
            results.append(result)
            current_input = result
        
        return results
```

### Fan-out Paralelo

```python
import asyncio

class ParallelFanout:
    def __init__(self, models):
        self.models = models
    
    async def execute(self, task):
        tasks = [model.generate(task) for model in self.models]
        results = await asyncio.gather(*tasks)
        return results
    
    def consolidate(self, results):
        # Lógica para combinar resultados
        return max(results, key=lambda r: r.confidence)
```

---

## APLICA

### Exercício: Criar um Pipeline de 3 Modelos

**Tarefa**: Analisar um repositório GitHub
1. **Modelo 1** (Gemini): Ler README e listar features
2. **Modelo 2** (Claude): Analisar código e sugerir melhorias
3. **Modelo 3** (GPT-4): Gerar relatório executivo

**Código base**:
```python
pipeline = SequentialPipeline([
    (gemini, "Leia o README e liste as features: {input}"),
    (claude, "Analise o código e sugira melhorias: {input}"),
    (gpt4, "Gere um relatório executivo: {input}")
])

result = pipeline.execute("https://github.com/user/repo")
```

### Checkpoint

- [ ] Entender os 4 padrões de orquestração
- [ ] Implementar um router simples
- [ ] Criar um pipeline sequencial
"""
        }
    },
    "arvore-decisao-auditoria": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Análise Preditiva",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Machine Learning para Custos", "subtitulo": "Prevendo consumo de tokens com modelos"},
                    {"capitulo": 10, "titulo": "Detecção de Anomalias", "subtitulo": "Identificando padrões incomuns em logs"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Automação Avançada",
                "capitulos": [
                    {"capitulo": 11, "titulo": "CI/CD para Agentes", "subtitulo": "Pipelines de deploy para sistemas AIDD"},
                    {"capitulo": 12, "titulo": "Auto-Healing Systems", "subtitulo": "Sistemas que se auto-repararam"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Governança Corporativa",
                "capitulos": [
                    {"capitulo": 13, "titulo": "FinOps para IA", "subtitulo": "Gestão financeira de custos de LLM"},
                    {"capitulo": 14, "titulo": "Compliance e Regulamentação", "subtitulo": "Rastreabilidade para auditorias"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Estudos de Caso Avançados",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Migração Legada para AIDD", "subtitulo": "Transformando projetos existentes"},
                    {"capitulo": 16, "titulo": "Escala Enterprise", "subtitulo": "Operações AIDD em larga escala"}
                ]
            }
        ]
    },
    "economia-tokens-cache": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Técnicas Avançadas de Cache",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Semantic Cache", "subtitulo": "Cache baseado em similaridade semântica"},
                    {"capitulo": 10, "titulo": "Distributed Caching", "subtitulo": "Cache compartilhado entre instâncias"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Otimização de Prompts",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Prompt Compression", "subtitulo": "Reduzindo tokens sem perder significado"},
                    {"capitulo": 12, "titulo": "Few-Shot Optimization", "subtitulo": "Exemplos mínimos para máxima eficiência"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Custos em Escala",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Batch Processing", "subtitulo": "Processamento em lote para reduzir custos"},
                    {"capitulo": 14, "titulo": "Model Routing Inteligente", "subtitulo": "Enviando tarefas para o modelo mais barato"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Ferramentas e Automação",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Cost Monitoring Dashboard", "subtitulo": "Monitoramento em tempo real de custos"},
                    {"capitulo": 16, "titulo": "Budget Automation", "subtitulo": "Automação de limites e alertas"}
                ]
            }
        ]
    },
    "guardrails-governanca": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Segurança Avançada",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Prompt Injection Defense", "subtitulo": "Proteção contra ataques de injeção"},
                    {"capitulo": 10, "titulo": "Output Validation", "subtitulo": "Validação rigorosa de saídas"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Monitoramento",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Real-time Alerting", "subtitulo": "Sistemas de alerta em tempo real"},
                    {"capitulo": 12, "titulo": "Audit Trails", "subtitulo": "Rastreabilidade completa de ações"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Compliance",
                "capitulos": [
                    {"capitulo": 13, "titulo": "GDPR para Agentes", "subtitulo": "Conformidade com proteção de dados"},
                    {"capitulo": 14, "titulo": "SOC2 Controls", "subtitulo": "Controles de segurança para IA"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Hardening",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Red Team Testing", "subtitulo": "Testes adversariais de segurança"},
                    {"capitulo": 16, "titulo": "Incident Response", "subtitulo": "Resposta a incidentes de segurança"}
                ]
            }
        ]
    },
    "harness-camada-orquestracao": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Patterns Avançados",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Event-Driven Orchestration", "subtitulo": "Orquestração baseada em eventos"},
                    {"capitulo": 10, "titulo": "Saga Pattern", "subtitulo": "Transações distribuídas com compensação"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Resiliência",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Circuit Breakers", "subtitulo": "Prevenindo falhas em cascata"},
                    {"capitulo": 12, "titulo": "Retry Strategies", "subtitulo": "Estratégias inteligentes de retry"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Observabilidade",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Distributed Tracing", "subtitulo": "Rastreamento distribuído"},
                    {"capitulo": 14, "titulo": "Metrics Collection", "subtitulo": "Coleta e análise de métricas"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Deployment",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Blue-Green Deployment", "subtitulo": "Deploy sem downtime"},
                    {"capitulo": 16, "titulo": "Canary Releases", "subtitulo": "Releases progressivos"}
                ]
            }
        ]
    },
    "harness-suas-camadas": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Camada de Aplicação",
                "capitulos": [
                    {"capitulo": 9, "titulo": "API Gateway Pattern", "subtitulo": "Gateway centralizado de APIs"},
                    {"capitulo": 10, "titulo": "Service Mesh", "subtitulo": "Comunicação entre serviços"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Camada de Dados",
                "capitulos": [
                    {"capitulo": 11, "titulo": "CQRS Pattern", "subtitulo": "Separação de leitura e escrita"},
                    {"capitulo": 12, "titulo": "Event Sourcing", "subtitulo": "Histórico completo de eventos"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Camada de Infraestrutura",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Container Orchestration", "subtitulo": "Kubernetes para agentes"},
                    {"capitulo": 14, "titulo": "Serverless Agents", "subtitulo": "Agentes sem servidor"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Integração",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Webhook Patterns", "subtitulo": "Integração via webhooks"},
                    {"capitulo": 16, "titulo": "Message Queues", "subtitulo": "Filas de mensagens assíncronas"}
                ]
            }
        ]
    },
    "higiene-contexto": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Memória de Longo Prazo",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Knowledge Graphs", "subtitulo": "Grafos de conhecimento para contexto"},
                    {"capitulo": 10, "titulo": "Vector Databases", "subtitulo": "Bancos vetoriais para recuperação"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Estratégias de Compressão",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Semantic Summarization", "subtitulo": "Resumo preservando significado"},
                    {"capitulo": 12, "titulo": "Context Windowing", "subtitulo": "Janelas deslizantes de contexto"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Ferramentas",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Memory Management Tools", "subtitulo": "Ferramentas para gerenciar memória"},
                    {"capitulo": 14, "titulo": "Session Persistence", "subtitulo": "Persistência entre sessões"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Boas Práticas",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Context Hygiene Checklist", "subtitulo": "Checklist de higiene de contexto"},
                    {"capitulo": 16, "titulo": "Performance Tuning", "subtitulo": "Otimização de performance"}
                ]
            }
        ]
    },
    "mcp-rag": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "RAG Avançado",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Hybrid Search", "subtitulo": "Busca combinando vetorial e lexical"},
                    {"capitulo": 10, "titulo": "Re-ranking", "subtitulo": "Reclassificação de resultados"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "MCP Avançado",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Custom MCP Servers", "subtitulo": "Criando servidores MCP customizados"},
                    {"capitulo": 12, "titulo": "MCP Security", "subtitulo": "Segurança em servidores MCP"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Integrações",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Database Integration", "subtitulo": "Integração com bancos de dados"},
                    {"capitulo": 14, "titulo": "API Integration", "subtitulo": "Integração com APIs externas"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Produção",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Scaling RAG", "subtitulo": "Escalabilidade de sistemas RAG"},
                    {"capitulo": 16, "titulo": "Monitoring RAG", "subtitulo": "Monitoramento de sistemas RAG"}
                ]
            }
        ]
    },
    "motor-cognitivo-llm-core": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Arquiteturas Avançadas",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Mixture of Experts", "subtitulo": "Arquitetura MoE em detalhes"},
                    {"capitulo": 10, "titulo": "Retrieval Augmented", "subtitulo": "RAG integrado ao modelo"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Otimização",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Quantization", "subtitulo": "Redução de precisão para eficiência"},
                    {"capitulo": 12, "titulo": "Pruning", "subtitulo": "Remoção de pesos desnecessários"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Fine-Tuning",
                "capitulos": [
                    {"capitulo": 13, "titulo": "LoRA Adaptation", "subtitulo": "Adaptação com baixo rank"},
                    {"capitulo": 14, "titulo": "RLHF Training", "subtitulo": "Treinamento com feedback humano"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Deploy",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Model Serving", "subtitulo": "Servindo modelos em produção"},
                    {"capitulo": 16, "titulo": "Inference Optimization", "subtitulo": "Otimização de inferência"}
                ]
            }
        ]
    },
    "prompts-engenharia-interacao": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Técnicas Avançadas",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Meta-Prompting", "subtitulo": "Prompts que criam prompts"},
                    {"capitulo": 10, "titulo": "Self-Consistency", "subtitulo": "Múltiplas cadeias de raciocínio"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Domain-Specific",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Code Generation Prompts", "subtitulo": "Prompts otimizados para código"},
                    {"capitulo": 12, "titulo": "Data Analysis Prompts", "subtitulo": "Prompts para análise de dados"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Evaluation",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Prompt Testing", "subtitulo": "Testes sistemáticos de prompts"},
                    {"capitulo": 14, "titulo": "A/B Testing Prompts", "subtitulo": "Comparação de variantes"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Production",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Prompt Versioning", "subtitulo": "Versionamento de prompts"},
                    {"capitulo": 16, "titulo": "Prompt Monitoring", "subtitulo": "Monitoramento em produção"}
                ]
            }
        ]
    },
    "rules-restricoes-globais": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Regras Avançadas",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Context-Aware Rules", "subtitulo": "Regras que adaptam ao contexto"},
                    {"capitulo": 10, "titulo": "Priority Systems", "subtitulo": "Sistemas de prioridade de regras"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Validação",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Rule Testing", "subtitulo": "Testes de regras"},
                    {"capitulo": 12, "titulo": "Conflict Resolution", "subtitulo": "Resolução de conflitos"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Automação",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Auto-Generation", "subtitulo": "Geração automática de regras"},
                    {"capitulo": 14, "titulo": "Rule Optimization", "subtitulo": "Otimização de regras"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Governança",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Rule Auditing", "subtitulo": "Auditoria de regras"},
                    {"capitulo": 16, "titulo": "Compliance Rules", "subtitulo": "Regras de conformidade"}
                ]
            }
        ]
    },
    "skills-conhecimento-sob-demanda": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Skills Avançadas",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Composite Skills", "subtitulo": "Skills compostas por múltiplos passos"},
                    {"capitulo": 10, "titulo": "Dynamic Skills", "subtitulo": "Skills que se adaptam ao contexto"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Gerenciamento",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Skill Discovery", "subtitulo": "Descoberta automática de skills"},
                    {"capitulo": 12, "titulo": "Skill Versioning", "subtitulo": "Versionamento de skills"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Qualidade",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Skill Testing", "subtitulo": "Testes de skills"},
                    {"capitulo": 14, "titulo": "Skill Metrics", "subtitulo": "Métricas de performance"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Ecossistema",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Skill Marketplaces", "subtitulo": "Marketplaces de skills"},
                    {"capitulo": 16, "titulo": "Skill Composition", "subtitulo": "Composição de skills"}
                ]
            }
        ]
    },
    "subagentes-workflows-paralelos": {
        "partes_adicionais": [
            {
                "parte": 5,
                "titulo_parte": "Padrões Avançados",
                "capitulos": [
                    {"capitulo": 9, "titulo": "Actor Model", "subtitulo": "Modelo ator para subagentes"},
                    {"capitulo": 10, "titulo": "Message Passing", "subtitulo": "Passagem de mensagens entre agentes"}
                ]
            },
            {
                "parte": 6,
                "titulo_parte": "Coordenação",
                "capitulos": [
                    {"capitulo": 11, "titulo": "Consensus Algorithms", "subtitulo": "Algoritmos de consenso"},
                    {"capitulo": 12, "titulo": "Distributed Locks", "subtitulo": "Locks distribuídos"}
                ]
            },
            {
                "parte": 7,
                "titulo_parte": "Tolerância a Falhas",
                "capitulos": [
                    {"capitulo": 13, "titulo": "Agent Recovery", "subtitulo": "Recuperação de agentes"},
                    {"capitulo": 14, "titulo": "Dead Letter Queues", "subtitulo": "Filas de mensagens mortas"}
                ]
            },
            {
                "parte": 8,
                "titulo_parte": "Escalabilidade",
                "capitulos": [
                    {"capitulo": 15, "titulo": "Auto-Scaling Agents", "subtitulo": "Escalonamento automático"},
                    {"capitulo": 16, "titulo": "Load Balancing", "subtitulo": "Balanceamento de carga"}
                ]
            }
        ]
    }
}

def expandir_livro(slug):
    """Expande um livro de 8 para 16 capitulos"""
    dir_livro = DIR_OUTPUT / slug
    dir_capitulos = dir_livro / "capitulos"
    sumario_path = dir_livro / "sumario_macro.json"
    
    # Ler sumario atual
    if not sumario_path.exists():
        print(f"  [ERRO] sumario_macro.json nao encontrado para {slug}")
        return False
    
    with open(sumario_path, 'r', encoding='utf-8') as f:
        sumario = json.load(f)
    
    # Verificar se ja tem 16+ capitulos
    total_caps = sum(len(p.get('capitulos', [])) for p in sumario.get('partes', []))
    if total_caps >= 16:
        print(f"  [OK] Ja tem {total_caps} capitulos")
        return True
    
    # Obter expansao
    if slug not in EXPANSAO_POR_LIVRO:
        print(f"  [SKIP] Sem plano de expansao definido")
        return False
    
    expansao = EXPANSAO_POR_LIVRO[slug]
    
    # Adicionar novas partes ao sumario
    for nova_parte in expansao['partes_adicionais']:
        sumario['partes'].append(nova_parte)
    
    # Salvar sumario atualizado
    with open(sumario_path, 'w', encoding='utf-8') as f:
        json.dump(sumario, f, indent=2, ensure_ascii=False)
    
    # Criar novos capitulos (usando templates genericos se nao houver conteudo especifico)
    novos_capitulos = expansao.get('novos_capitulos', {})
    
    for nova_parte in expansao['partes_adicionais']:
        for cap_info in nova_parte['capitulos']:
            cap_num = cap_info['capitulo']
            cap_path = dir_capitulos / f"cap_{cap_num}.md"
            
            if cap_path.exists():
                continue
            
            # Usar conteudo especifico se disponivel, senao usar template
            if cap_num in novos_capitulos:
                conteudo = novos_capitulos[cap_num]
            else:
                # Template generico
                conteudo = f"""# Capítulo {cap_num}: {cap_info['titulo']}

## PARTE {nova_parte['parte']} — {nova_parte['titulo_parte']}

---

## EXPLICA

### {cap_info['titulo']}

{cap_info['subtitulo']} é um conceito fundamental que vamos explorar neste capítulo.

### Por Que Importa?

Compreender {cap_info['titulo'].lower()} é essencial para dominar o paradigma AIDD e suas implicações práticas.

---

## ILUSTRA

### A Metáfora

Assim como um engenheiro precisa entender cada componente de uma máquina, o profissional AIDD precisa dominar {cap_info['titulo'].lower()}.

### Analogia AIDD

| Conceito Tradicional | Equivalente AIDD |
|---------------------|------------------|
| Componente | {cap_info['titulo']} |
| Função | {cap_info['subtitulo']} |
| Resultado | Eficiência e qualidade |

---

## TÉCNICA

### Conceitos Fundamentais

A implementação de {cap_info['titulo'].lower()} envolve os seguintes componentes:

1. **Componente A**: Primeiro aspecto técnico
2. **Componente B**: Segundo aspecto técnico
3. **Componente C**: Terceiro aspecto técnico

### Implementação Básica

```python
# Exemplo de implementacao
class {cap_info['titulo'].replace(' ', '')}:
    def __init__(self):
        pass
    
    def execute(self):
        # Logica principal
        pass
```

### Melhores Práticas

1. **Prática 1**: Primeira recomendação
2. **Prática 2**: Segunda recomendação
3. **Prática 3**: Terceira recomendação

---

## APLICA

### Exercício Prático

**Objetivo**: Implementar {cap_info['titulo'].lower()} em um cenário real.

**Passo 1**: Configurar o ambiente
```bash
# Comando de configuracao
```

**Passo 2**: Implementar a solução
```python
# Codigo de implementacao
```

**Passo 3**: Validar o resultado
```bash
# Comando de validacao
```

### Checkpoint de Validação

Após este capítulo, você deve ser capaz de:
- [ ] Explicar o conceito de {cap_info['titulo'].lower()}
- [ ] Implementar uma solução básica
- [ ] Validar os resultados obtidos
"""
            
            # Salvar capitulo
            with open(cap_path, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            print(f"  [+] Capitulo {cap_num}: {cap_info['titulo']}")
    
    print(f"  [OK] Expandido para {total_caps + len(expansao['partes_adicionais'] * 2)} capitulos")
    return True

def main():
    print("=" * 60)
    print("  EXPANSOR DE LIVROS - Fabrica Agentic de Livros")
    print("=" * 60)
    print()
    
    # Listar livros
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
    print(f"  RESUMO: {expandidos} expandidos, {erros} erros")
    print("=" * 60)

if __name__ == "__main__":
    main()
