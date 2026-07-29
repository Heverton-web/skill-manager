import fs from 'fs';
import path from 'path';

const target = path.resolve('.claude/agents');
const link = path.resolve('agentic/agents');

if (!fs.existsSync(link)) {
  fs.symlinkSync(target, link, 'junction');
  console.log('Junction criada com sucesso:', link, '->', target);
} else {
  console.log('Junction ja existe.');
}
