import fs from 'fs';

function compressLog(input) {
  const lines = input.split(/\r?\n/);
  if (lines.length <= 7) {
    return input;
  }
  const head = lines.slice(0, 3);
  const tail = lines.slice(-4);
  const omittedCount = lines.length - 7;
  return [...head, `\n[... ${omittedCount} linhas omitidas por headroom ...]\n`, ...tail].join('\n');
}

const input = process.argv[2] ? fs.readFileSync(process.argv[2], 'utf8') : '';
if (input) {
  console.log(compressLog(input));
} else {
  console.log('Uso: node scripts/headroom.mjs <caminho-do-arquivo-de-log>');
}
