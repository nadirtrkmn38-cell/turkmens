// Enerji Tedariği reklam filmi — kare kare render + ffmpeg ile MP4 kodlama.
//
// Kullanım:
//   node render.mjs                         -> 16:9 (1920x1080) video
//   node render.mjs --format 9x16           -> 9:16 (1080x1920) dikey video
//   node render.mjs --stills 2,6.5,12       -> sadece seçilen saniyelerin PNG kareleri
//
// Gerekenler: playwright (Chromium), ffmpeg (FFMPEG env ya da PATH), music.wav (python3 music.py)
import { spawn, execSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require_ = (await import('node:module')).createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require_('playwright')); } catch { ({ chromium } = await import('/opt/node22/lib/node_modules/playwright/index.mjs')); }

const dir = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const format = arg('--format', '16x9');
const fps = Number(arg('--fps', 30));
const stills = arg('--stills', null);
const outDir = path.join(dir, 'cikti');
mkdirSync(outDir, { recursive: true });

const [W, H] = format === '9x16' ? [1080, 1920] : [1920, 1080];
const ffmpeg = process.env.FFMPEG || (() => { try { return execSync('which ffmpeg').toString().trim(); } catch { return 'ffmpeg'; } })();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(dir, 'index.html')).href + `?format=${format}`);
await page.evaluate(() => window.ready);
const duration = await page.evaluate(() => window.DURATION);

if (stills) {
  for (const s of stills.split(',').map(Number)) {
    await page.evaluate(t => window.renderFrame(t), s);
    const f = path.join(outDir, `kare_${format}_${String(s).replace('.', '_')}.png`);
    await page.screenshot({ path: f });
    console.log('kare:', f);
  }
  await browser.close();
  process.exit(0);
}

const music = path.join(dir, 'music.wav');
const out = path.join(outDir, `enerjitedarigi_reklam_${format}.mp4`);
const args = ['-y', '-hide_banner', '-loglevel', 'error',
  '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-'];
if (existsSync(music)) args.push('-i', music);
args.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
  '-r', String(fps), '-movflags', '+faststart');
if (existsSync(music)) args.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
args.push(out);

const ff = spawn(ffmpeg, args, { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round(duration * fps);
const t0 = Date.now();
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.renderFrame(t), f / fps);
  const buf = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 60 === 0) process.stdout.write(`\r${format}: ${f}/${total} kare (${((Date.now() - t0) / 1000).toFixed(0)} sn)`);
}
ff.stdin.end();
await new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg çıkış kodu ' + c)))));
await browser.close();
console.log(`\nHazır: ${out}`);
