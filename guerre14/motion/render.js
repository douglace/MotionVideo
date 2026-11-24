// Rasterise les scènes SVG de scenes.html image par image (Chromium / Playwright).
// Usage : node render.js                      -> toutes les scènes, dans ../build/motion/<scène>/NNNNN.jpg
//         node render.js --still i14 4.2 ...  -> aperçus ../build/motion/still_<scène>_<t>.png
// L'image n°k d'une scène correspond à τ = k/30 - 0.5 s (τ = temps depuis le début du plan).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FPS = 30, PRE = 0.5;
// durée de chaque plan (doit suivre SHOTS dans build.py)
const SCENES = { i14: 5.9, i17: 3.0, i18: 2.25, i19: 4.5, i20: 2.5, i21: 3.75, i22: 3.25, i23: 8.39 };
const OUT = path.join(__dirname, '..', 'build', 'motion');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'scenes.html'));
  await page.evaluate(() => document.fonts.ready);
  const clip = { x: 0, y: 0, width: 1080, height: 1920 };
  const args = process.argv.slice(2);
  fs.mkdirSync(OUT, { recursive: true });
  if (args[0] === '--still') {
    for (let i = 1; i < args.length; i += 2) {
      const [name, t] = [args[i], parseFloat(args[i + 1])];
      await page.evaluate(([n, tt]) => window.render(n, tt), [name, t]);
      await page.screenshot({ path: path.join(OUT, `still_${name}_${t}.png`), clip });
    }
  } else {
    const only = args.length ? args : Object.keys(SCENES);
    for (const name of only) {
      const dir = path.join(OUT, name);
      fs.mkdirSync(dir, { recursive: true });
      const n = Math.ceil((SCENES[name] + PRE + 0.2) * FPS);
      for (let k = 0; k < n; k++) {
        await page.evaluate(([nm, tt]) => window.render(nm, tt), [name, k / FPS - PRE]);
        await page.screenshot({ path: path.join(dir, String(k).padStart(5, '0') + '.jpg'), clip, type: 'jpeg', quality: 93 });
      }
      console.log(name, n, 'images');
    }
  }
  await browser.close();
})();
