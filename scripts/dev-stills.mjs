// Render PNG stills at the given times (seconds) in ONE browser session – handy for checking frames.
//   npm run stills -- 0.5 2.4 8.1        → out/stills/t_0.5.png …
// Optional env: REMOTION_BROWSER=/path/to/chrome   (otherwise Remotion's own Chrome is used)
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';

const times = process.argv.slice(2).map(Number).filter((n) => !Number.isNaN(n));
if (!times.length) {
  console.error('usage: npm run stills -- <seconds> [<seconds> ...]');
  process.exit(1);
}
const outDir = path.resolve('out/stills');
fs.mkdirSync(outDir, {recursive: true});

const browserExecutable = process.env.REMOTION_BROWSER || null;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const browser = await openBrowser('chrome', {browserExecutable, chromeMode: 'headless-shell'});
const composition = await selectComposition({serveUrl, id: 'WWCCPromo', puppeteerInstance: browser});

for (const s of times) {
  const frame = Math.min(composition.durationInFrames - 1, Math.round(s * composition.fps));
  const output = path.join(outDir, `t_${s}.png`);
  const t0 = Date.now();
  await renderStill({composition, serveUrl, output, frame, imageFormat: 'png', puppeteerInstance: browser});
  console.log(`t=${s}s (frame ${frame}) → ${output}  [${((Date.now() - t0) / 1000).toFixed(1)}s]`);
}
await browser.close({silent: true});
