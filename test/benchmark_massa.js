// test/benchmark_massa.js
// Gera uma massa de dados de log e payload JSON com 250 linhas para o benchmark.

const fs = require('fs');
const path = require('path');

const testDir = __dirname;
if (!fs.existsSync(testDir)) {
  fs.mkdirSync(testDir, { recursive: true });
}

const sampleLogPath = path.join(testDir, 'sample_large_log.log');

let logLines = [];
logLines.push("[2026-08-02T13:00:00.000Z] INFO [Server] Starting application server v2.4.1...");
logLines.push("[2026-08-02T13:00:00.100Z] INFO [Database] Connecting to PostgreSQL at localhost:5432/db_livros...");
logLines.push("[2026-08-02T13:00:00.250Z] INFO [Database] Connection established (pool size: 10).");

for (let i = 1; i <= 240; i++) {
  logLines.push(`[2026-08-02T13:00:${String(Math.floor(i / 10)).padStart(2, '0')}.${String((i % 10) * 100).padStart(3, '0')}Z] DEBUG [Worker-${i % 4}] Executing background task #${i} - Processing book chunk ID_${1000 + i}... Status: OK.`);
}

logLines.push("[2026-08-02T13:01:00.000Z] ERROR [AuthService] Failed login attempt for user 'admin_test' from IP 192.168.1.50 - Invalid Token Expiry at auth.js:142.");
logLines.push("[2026-08-02T13:01:00.150Z] INFO [Server] Graceful shutdown signal received.");
logLines.push("[2026-08-02T13:01:00.300Z] INFO [Server] Server stopped successfully.");

fs.writeFileSync(sampleLogPath, logLines.join('\n'), 'utf8');
console.log(`Massa de dados gerada com sucesso em: ${sampleLogPath} (${logLines.length} linhas)`);
