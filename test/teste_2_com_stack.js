// test/teste_2_com_stack.js
// SIMULAÇÃO: Execução de agente COM A STACK de economia severa de tokens (Caveman + Headroom + LeanCTX + RTK).

const fs = require('fs');
const path = require('path');

// Simulador de Tokenizer aproximado (~4 caracteres por token)
function countTokens(text) {
  return Math.ceil(text.length / 4);
}

// Em um agente COM a stack:
// 1. LeanCTX + Grep localiza a linha exata de erro sem carregar o log inteiro.
// 2. Headroom comprime saídas extensas (Head + Tail).
const compressedContext = `Prompt: Analisar erro em log.

Contexto Cirúrgico (LeanCTX / Grep ERROR):
[2026-08-02T13:01:00.000Z] ERROR [AuthService] Failed login attempt for user 'admin_test' from IP 192.168.1.50 - Invalid Token Expiry at auth.js:142.`;

// Resposta Estilo Caveman Mode (Com a Stack)
const cavemanResponse = `Erro no AuthService. Tentativa login 'admin_test' falhou. Token expirado.
Loc: auth.js:142.
Fix: verificar timestamp expiração em auth.js:142.`;

const inputTokens = countTokens(compressedContext);
const outputTokens = countTokens(cavemanResponse);
const totalTokens = inputTokens + outputTokens;

console.log("=== TESTE 2: COM A STACK DE ECONOMIA (CAVEMAN + HEADROOM + LEAN-CTX + RTK) ===");
console.log(`Tokens de Entrada (Input Context): ${inputTokens}`);
console.log(`Tokens de Saída (Output Response): ${outputTokens}`);
console.log(`Total de Tokens Consumidos: ${totalTokens}`);
console.log("-----------------------------------------");

module.exports = { inputTokens, outputTokens, totalTokens, cavemanResponse };
