// test/run_benchmark.js
// Executa os dois testes e exibe os resultados estatísticos comparativos.

const teste1 = require('./teste_1_sem_stack.js');
const teste2 = require('./teste_2_com_stack.js');

const economiaInput = ((1 - (teste2.inputTokens / teste1.inputTokens)) * 100).toFixed(2);
const economiaOutput = ((1 - (teste2.outputTokens / teste1.outputTokens)) * 100).toFixed(2);
const economiaTotal = ((1 - (teste2.totalTokens / teste1.totalTokens)) * 100).toFixed(2);

console.log("\n=======================================================");
console.log("🔥 RESULTADO COMPARATIVO DE ECONOMIA SEVERA DE TOKENS 🔥");
console.log("=======================================================");
console.log(`Métrica                 | Sem Stack | Com Stack | Economia (%)`);
console.log(`------------------------|-----------|-----------|-------------`);
console.log(`Tokens de Entrada       | ${String(teste1.inputTokens).padEnd(9)} | ${String(teste2.inputTokens).padEnd(9)} | -${economiaInput}%`);
console.log(`Tokens de Saída         | ${String(teste1.outputTokens).padEnd(9)} | ${String(teste2.outputTokens).padEnd(9)} | -${economiaOutput}%`);
console.log(`TOTAL DE TOKENS         | ${String(teste1.totalTokens).padEnd(9)} | ${String(teste2.totalTokens).padEnd(9)} | -${economiaTotal}%`);
console.log("=======================================================\n");
