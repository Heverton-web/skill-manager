// test/teste_1_sem_stack.js
// SIMULAÇÃO: Execução de agente SEM a stack de economia de tokens.

const fs = require('fs');
const path = require('path');

const logPath = path.join(__dirname, 'sample_large_log.log');
let logContent = "";
if (fs.existsSync(logPath)) {
  logContent = fs.readFileSync(logPath, 'utf8');
} else {
  logContent = "[2026-08-02T13:00:00.000Z] INFO Server starting...\n" + "... (245 linhas de logs repetitivos e irrelevantes) ...\n" + "[2026-08-02T13:01:00.000Z] ERROR [AuthService] Failed login attempt for user 'admin_test' - Invalid Token Expiry at auth.js:142.";
}

// Simulador de Tokenizer aproximado (~4 caracteres por token)
function countTokens(text) {
  return Math.ceil(text.length / 4);
}

// Em um agente sem stack, o arquivo inteiro é injetado no contexto
const inputContext = `Prompt do Usuário: Por favor, analise os logs do sistema e me diga qual foi o erro que ocorreu e onde ele foi disparado.

Conteúdo do Arquivo de Log:
${logContent}`;

// Resposta Verbosa Padrão (Sem Caveman, Sem Headroom)
const outputResponse = `Olá! Tudo bem? Ficarei muito feliz em ajudar você com essa análise de logs.

Após examinar cuidadosamente todo o arquivo de log fornecido, identifiquei a seguinte ocorrência de erro relevante no sistema:

### Análise Detalhada do Erro:
- **Módulo Afetado:** AuthService (Serviço de Autenticação)
- **Tipo de Evento:** Falha na tentativa de login
- **Usuário:** admin_test
- **Endereço IP:** 192.168.1.50
- **Causa Raiz:** Ocorreu um erro de expiração de token inválido (Invalid Token Expiry).
- **Localização Exata no Código:** Arquivo \`auth.js\`, na linha 142.

### Recomendações:
Você deve verificar a função de validação de expiração de token dentro do arquivo \`auth.js\` na linha 142 para garantir que o cálculo da timestamp de expiração não esteja resultando em um valor passado ou nulo.

Se precisar de mais alguma ajuda ou esclarecimento adicional, por favor não hesite em me perguntar! Tenha um ótimo trabalho.`;

const inputTokens = countTokens(inputContext);
const outputTokens = countTokens(outputResponse);
const totalTokens = inputTokens + outputTokens;

console.log("=== TESTE 1: SEM A STACK DE ECONOMIA ===");
console.log(`Tokens de Entrada (Input Context): ${inputTokens}`);
console.log(`Tokens de Saída (Output Response): ${outputTokens}`);
console.log(`Total de Tokens Consumidos: ${totalTokens}`);
console.log("-----------------------------------------");

module.exports = { inputTokens, outputTokens, totalTokens, outputResponse };
