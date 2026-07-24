import { mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import { join, parse } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const sourceDir = join(root, 'mindmaps');
const outputDir = join(root, 'docs');

function runMarkmap(input, output) {
  return new Promise((resolve, reject) => {
    const command = process.platform === 'win32' ? 'npx.cmd' : 'npx';
    const child = spawn(command, ['markmap-cli', input, '-o', output, '--no-open'], { cwd: root, stdio: 'inherit', shell: process.platform === 'win32' });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`markmap-cli exited with code ${code}`)));
  });
}

await rm(outputDir, { recursive: true, force: true });
await mkdir(outputDir, { recursive: true });

const files = (await readdir(sourceDir)).filter(name => name.endsWith('.md') && name !== 'README.md');
if (!files.length) throw new Error('No Markdown files found in mindmaps/.');

for (const file of files) {
  const name = parse(file).name;
  await runMarkmap(join(sourceDir, file), join(outputDir, `${name}.html`));
}

const links = files.map(file => {
  const name = parse(file).name;
  return `    <li><a href="${name}.html">${name.replaceAll('-', ' ')}</a></li>`;
}).join('\n');

await writeFile(join(outputDir, 'index.html'), `<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter mind maps</title>
<style>body{font:16px system-ui,sans-serif;max-width: fiftyrem;max-width:50rem;margin:4rem auto;padding:0 1.25rem;line-height:1.5}a{color:#126b45}</style></head>
<body><h1>Chapter mind maps</h1><p>Interactive maps generated from Markdown sources in <code>mindmaps/</code>.</p><ul>
${links}
</ul></body></html>\n`);

console.log(`Built ${files.length} map(s) in docs/.`);
