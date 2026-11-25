// Rendu image par image de index.html (fonction renderAt(t) déterministe) -> MP4 1080x1920 + voix.
// Usage : node render.mjs                -> build/treve-motion.mp4
//         node render.mjs --stills 1,5,9 -> build/still_<t>.jpg (contrôle visuel)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(dir); // sert le dépôt entier (assets partagés dans ../treve)
const FPS = 30, DUR = 69.5;
const args = process.argv.slice(2);
const ANNOT = args.includes('--annot');
mkdirSync(path.join(dir, 'build'), { recursive: true });

// petit serveur statique (fetch() ne marche pas en file://)
const types = { '.html': 'text/html', '.json': 'application/json', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.js': 'text/javascript' };
const server = http.createServer(async (req, res) => {
  try {
    const p = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(root)) throw 0;
    res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' });
    res.end(await readFile(p));
  } catch { res.writeHead(404); res.end(); }
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(`http://127.0.0.1:${port}/treve2/index.html${ANNOT ? '?annot' : ''}`);
await page.waitForFunction(() => window.READY === true);

if (args[0] === '--stills') {
  for (const t of args[1].split(',').map(Number)) {
    await page.evaluate(t => renderAt(t), t);
    await page.screenshot({ path: path.join(dir, 'build', `still_${t}.jpg`), type: 'jpeg', quality: 85 });
  }
} else {
  const out = path.join(dir, 'build', ANNOT ? 'treve-anime-annote.mp4' : 'treve-anime.mp4');
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(root, 'treve', 'assets', 'voix.wav'),
    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
    '-af', 'loudnorm=I=-14:TP=-1.5', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(DUR * FPS);
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => renderAt(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${N}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('ok ->', out);
}
await browser.close();
server.close();
