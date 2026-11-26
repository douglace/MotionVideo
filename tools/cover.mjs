// Génère une image de couverture (Shorts 1080x1920) à partir du moteur d'un épisode.
// Usage : node tools/cover.mjs <dossier-episode> <script-de-couverture.js> <sortie.png>
// Le script de couverture est évalué dans la page : il dispose de toutes les fonctions
// de dessin de l'épisode (soldier, dunes, coin, checkpoint…) et doit dessiner sur #cv.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [ep, script, out] = process.argv.slice(2);
const types = { '.html': 'text/html', '.json': 'application/json', '.woff2': 'font/woff2' };
const server = http.createServer(async (req, res) => {
  try { const p = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname)); if (!p.startsWith(root)) throw 0;
    const b = await readFile(p); res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' }); res.end(b);
  } catch { if (!res.headersSent) res.writeHead(404); res.end(); }
}).listen(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/${ep}/index.html`);
await page.waitForFunction(() => window.READY === true);
const code = await readFile(path.resolve(script), 'utf8');
await page.evaluate(code);
await page.screenshot({ path: out, type: 'png' });
console.log('ok ->', out);
await browser.close(); server.close();
