// Enerji Tedariği — Motion Reel: kare kare render + ffmpeg ile MP4.
//
// Kullanım:
//   node render.mjs                              -> cikti/enerjitedarigi_motion_reel.mp4 (1920x1080, 60 fps)
//   node render.mjs --sub 4                      -> alt kare örneklemeli hareket bulanıklığı (4x render)
//   node render.mjs --stills 2,6.5,12            -> yalnızca seçilen saniyelerin PNG kareleri
//   node render.mjs --sheet 0:45:0.5             -> kontrol paftası (küçük karelerden ızgara)
//   node render.mjs --format 9x16 --sub 4        -> dikey sürüm: cikti/enerjitedarigi_motion_reel_9x16.mp4 (1080x1920)
//
// Gerekenler: playwright (Chromium), ffmpeg (FFMPEG env / PATH / imageio-ffmpeg), music.wav (python3 music.py)
import { spawn, execSync } from 'node:child_process';
import { existsSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require_ = (await import('node:module')).createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require_('playwright')); } catch { ({ chromium } = await import('/opt/node22/lib/node_modules/playwright/index.mjs')); }

const dir = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const fps = Number(arg('--fps', 60));
const sub = Number(arg('--sub', 1));
const workers = Number(arg('--workers', Math.max(1, Math.min(4, os.cpus().length))));
const stills = arg('--stills', null);
const sheet = arg('--sheet', null);
const fmt = arg('--format', '16x9');
if (!['16x9', '9x16'].includes(fmt)) throw new Error('--format 16x9 ya da 9x16 olmalı');
const VERT = fmt === '9x16';
const [VW, VH] = VERT ? [1080, 1920] : [1920, 1080];
const sfx = VERT ? '_9x16' : '';
const outDir = path.join(dir, 'cikti');
const tmpDir = arg('--tmp', path.join(dir, '.tmp' + sfx));
mkdirSync(outDir, { recursive: true });

const ffmpeg = process.env.FFMPEG || (() => {
  try { return execSync('which ffmpeg', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch {}
  try { return execSync('python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"').toString().trim(); } catch {}
  return 'ffmpeg';
})();
const url = pathToFileURL(path.join(dir, 'index.html')).href + (VERT ? '?format=9x16' : '');

async function openPage() {
  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(() => window.ready);
  const cdp = await page.context().newCDPSession(page);
  const shot = async t => {
    await page.evaluate(tt => window.renderFrame(tt), t);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true, captureBeyondViewport: false });
    return Buffer.from(data, 'base64');
  };
  return { browser, page, shot };
}
const run = (args, opts = {}) => new Promise((res, rej) => {
  const p = spawn(ffmpeg, args, { stdio: ['pipe', 'inherit', 'inherit'], ...opts });
  p.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg çıkış kodu ' + c))));
  return p;
});

/* ---------- kontrol kareleri ---------- */
if (stills || sheet) {
  const kdir = path.join(outDir, 'kontrol'); mkdirSync(kdir, { recursive: true });
  let times;
  if (stills) times = stills.split(',').map(Number);
  else { const [a, e, s] = sheet.split(':').map(Number); times = []; for (let t = a; t <= e + 1e-9; t += s) times.push(+t.toFixed(4)); }
  // işçilere böl
  const chunks = Array.from({ length: Math.min(workers, times.length) }, () => []);
  times.forEach((t, i) => chunks[i % chunks.length].push([i, t]));
  const files = new Array(times.length);
  await Promise.all(chunks.map(async ch => {
    const { browser, shot } = await openPage();
    for (const [i, t] of ch) {
      const f = path.join(kdir, stills ? `kare${sfx}_${String(t).replace('.', '_')}.png` : `s${sfx}_${String(i).padStart(4, '0')}.png`);
      writeFileSync(f, await shot(t)); files[i] = f;
    }
    await browser.close();
  }));
  if (stills) { files.forEach(f => console.log('kare:', f)); process.exit(0); }
  const cols = Number(arg('--cols', 6)), tw = Number(arg('--tw', 320));
  const rows = Math.ceil(files.length / cols);
  const out = path.join(kdir, arg('--name', 'pafta' + sfx) + '.jpg');
  await run(['-y', '-hide_banner', '-loglevel', 'error', '-framerate', '1', '-i', path.join(kdir, `s${sfx}_%04d.png`),
    '-vf', `scale=${tw}:-1,tile=${cols}x${rows}:padding=4:color=black`, '-frames:v', '1', '-q:v', '3', out]);
  files.forEach(f => rmSync(f));
  console.log('pafta:', out);
  process.exit(0);
}

/* ---------- tam render ---------- */
const { browser: b0, page: p0 } = await openPage();
const duration = await p0.evaluate(() => window.DURATION);
await b0.close();
const rfps = fps * sub;
const total = Math.round(duration * rfps);
rmSync(tmpDir, { recursive: true, force: true }); mkdirSync(tmpDir, { recursive: true });
const per = Math.ceil(total / workers);
const t0 = Date.now();
let done = 0;
const segs = [];
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const a = w * per, e = Math.min(total, a + per);
  if (a >= e) return;
  const seg = path.join(tmpDir, `seg_${w}.mkv`); segs[w] = seg;
  const ff = spawn(ffmpeg, ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(rfps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264rgb', '-preset', 'ultrafast', '-qp', '0', seg], { stdio: ['pipe', 'inherit', 'inherit'] });
  const closed = new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg ' + c)))));
  const { browser, shot } = await openPage();
  for (let f = a; f < e; f++) {
    const buf = await shot(f / rfps);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    done++;
    if (done % 30 === 0) process.stdout.write(`\r${done}/${total} kare  (${((Date.now() - t0) / 1000).toFixed(0)} sn)`);
  }
  ff.stdin.end(); await closed; await browser.close();
}));
console.log(`\nrender bitti: ${((Date.now() - t0) / 1000).toFixed(0)} sn`);

const list = path.join(tmpDir, 'list.txt');
writeFileSync(list, segs.filter(Boolean).map(s => `file '${s}'`).join('\n'));
const music = path.join(dir, 'music.wav');
const out = path.join(outDir, arg('--out', `enerjitedarigi_motion_reel${sfx}.mp4`));
// alt kare -> hareket bulanıklığı (tmix), hafif film greni
let vf = '';
if (sub > 1) vf += `tmix=frames=${sub}:weights='${Array(sub).fill(1).join(' ')}',select='not(mod(n+1\\,${sub}))',setpts=N/(${fps}*TB),`;
vf += `format=yuv444p,noise=c0s=${arg('--grain', 3)}:c0f=t,format=yuv420p`;
const args = ['-y', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list];
if (existsSync(music)) args.push('-i', music);
args.push('-vf', vf, '-r', String(fps), '-c:v', 'libx264', '-preset', 'slow', '-crf', arg('--crf', '18'), '-profile:v', 'high',
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709');
if (existsSync(music)) args.push('-c:a', 'aac', '-b:a', '256k', '-shortest');
args.push(out);
await run(args);
if (!process.argv.includes('--keep')) rmSync(tmpDir, { recursive: true, force: true });
console.log('Hazır:', out);
