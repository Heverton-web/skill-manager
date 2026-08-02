---
name: lean-ctx
description: Seleção cirúrgica e minificação de contexto antes de enviar para LLMs.
---

# lean-ctx — Context Engine Severo

## Diretrizes de Uso
1. **Injeção Mínima:** Nunca passe arquivos completos se apenas uma classe/função for necessária.
2. **Uso de Grep Prioritário:** Execute busca por padrão antes de abrir arquivos grandes.
3. **AST & Minificação:** Utilize o `lean-ctx` para extrair assinaturas e cabeçalhos de arquivo antes de editar.
