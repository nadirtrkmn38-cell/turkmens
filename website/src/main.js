import '@fontsource-variable/space-grotesk';
import '@fontsource-variable/inter';
import '@fontsource-variable/jetbrains-mono';
import '@fontsource/instrument-serif/400-italic.css';
import './styles/main.css';

import { content, ui } from './content.js';
import { pageTitle, renderApp, t } from './render.js';
import { browserPrefersTurkish, getInitialLang, hasSavedLang, saveLang, syncUrl } from './lib/lang.js';
import { initEffects } from './ui/effects.js';
import { initNav } from './ui/nav.js';

const html = document.documentElement;
const root = document.getElementById('app');
const BASE = import.meta.env.BASE_URL;
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

let lang = getInitialLang();
let world = null;
let effects = null;
let nav = null;

/* ───────────── içerik ───────────── */

function updateHead(next) {
  html.lang = next;
  document.title = pageTitle(next);
  document.querySelector('meta[name="description"]')?.setAttribute('content', t(content.meta.description, next));
}

function mount(next) {
  root.innerHTML = renderApp(next, BASE);
  updateHead(next);
}

function wire() {
  effects?.destroy();
  nav?.destroy();
  effects = initEffects(root, { reducedMotion, lang });
  nav = initNav(root);
  world?.setSections([...root.querySelectorAll('[data-section]')]);
}

// Sayfa build sırasında Türkçe olarak hazırlanır; farklı dil seçiliyse yeniden çizilir.
if (import.meta.env.DEV || html.lang !== lang || !root.querySelector('main')) mount(lang);
wire();

/* ───────────── dil değiştirme ───────────── */

function switchLang(next) {
  if (!next || next === lang) return;
  // okuma konumunu koru
  const sections = [...root.querySelectorAll('[data-section]')];
  const y = window.scrollY;
  let index = 0;
  let ratio = 0;
  sections.forEach((s, i) => {
    const top = s.getBoundingClientRect().top + y;
    if (top <= y + 1) {
      index = i;
      ratio = (y - top) / Math.max(1, s.offsetHeight);
    }
  });

  lang = next;
  saveLang(next);
  syncUrl(next);
  mount(next);
  wire();

  const target = root.querySelectorAll('[data-section]')[index];
  if (target) {
    const top = target.getBoundingClientRect().top + window.scrollY + ratio * target.offsetHeight;
    window.scrollTo({ top, behavior: 'instant' });
  }
  world?.setWord(t(content.contact.word, next), true);
  document.querySelector('.lang-prompt')?.remove();
}

/* ───────────── tıklamalar ───────────── */

const toastEl = () => root.querySelector('[data-toast]');
let toastTimer = 0;
function toast(message) {
  const el = toastEl();
  if (!el) return;
  el.textContent = message;
  el.classList.add('is-visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('is-visible'), 2400);
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.append(area);
    area.select();
    document.execCommand('copy');
    area.remove();
  }
  toast(t(ui.copied, lang));
}

document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-action]');
  if (!el) return;
  const action = el.dataset.action;
  if (action === 'lang') switchLang(el.dataset.lang);
  else if (action === 'menu') nav?.toggleMenu();
  else if (action === 'copy') copyText(el.dataset.copy);
});

/* ───────────── yükleme ekranı ───────────── */

const loader = document.getElementById('loader');
const loaderBar = loader?.querySelector('.loader__bar');
const loaderCount = loader?.querySelector('.loader__count');
let shown = 0;
let target = 0;
let loaderRaf = 0;

function setProgress(p) {
  target = Math.max(target, p);
  if (!loaderRaf) loaderRaf = requestAnimationFrame(tickLoader);
}

function tickLoader() {
  shown += (target - shown) * 0.16;
  if (target - shown < 0.4) shown = target;
  if (loaderBar) loaderBar.style.setProperty('--p', (shown / 100).toFixed(3));
  if (loaderCount) loaderCount.textContent = String(Math.round(shown)).padStart(3, '0');
  loaderRaf = shown < target ? requestAnimationFrame(tickLoader) : 0;
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function boot() {
  const started = performance.now();
  setProgress(12);

  const fonts = document.fonts?.ready ?? Promise.resolve();
  fonts.then(() => setProgress(45));

  world = await createWorld();
  setProgress(78);

  await Promise.race([fonts, wait(2500)]);
  if (world) {
    world.setSections([...root.querySelectorAll('[data-section]')]);
    try {
      await document.fonts?.load?.('700 100px "Space Grotesk Variable"', t(content.contact.word, lang));
    } catch {
      /* yedek yazı tipi kullanılır */
    }
    world.setWord(t(content.contact.word, lang));
    world.start();
  }
  setProgress(100);

  const elapsed = performance.now() - started;
  await wait(Math.max(0, (reducedMotion ? 200 : 1100) - elapsed));
  finish();
}

let finished = false;
function finish() {
  if (finished) return;
  finished = true;
  clearTimeout(window.__ntFailsafe);
  loader?.classList.add('is-done');
  html.classList.add('is-ready');
  world?.startIntro();
  setTimeout(maybePromptLanguage, 2600);
  greet();
}

async function createWorld() {
  const canvas = document.querySelector('canvas.webgl');
  if (!canvas) return null;
  try {
    const { World } = await import('./webgl/World.js');
    const small = Math.min(window.innerWidth, window.innerHeight) < 640 || matchMedia('(pointer: coarse)').matches;
    const cores = navigator.hardwareConcurrency || 4;
    let count = small ? 14000 : 30000;
    if (cores <= 4) count = Math.round(count * 0.7);
    return new World(canvas, { count, reducedMotion });
  } catch (err) {
    console.warn('[nadirturkmen.com] WebGL başlatılamadı, sade görünüme geçiliyor.', err);
    html.classList.add('no-webgl');
    return null;
  }
}

/* ───────────── parçacıklarla oyun: imleç, tıklama, basılı tutma ───────────── */

window.addEventListener(
  'pointermove',
  (e) => {
    world?.pointerMove(e.clientX, e.clientY);
  },
  { passive: true },
);

window.addEventListener('pointerup', (e) => {
  world?.release();
  if (e.pointerType !== 'mouse') world?.pointerLeave();
});
window.addEventListener('pointercancel', () => {
  world?.release();
  world?.pointerLeave();
});
window.addEventListener('blur', () => {
  world?.release();
  world?.pointerLeave();
});
html.addEventListener('mouseleave', () => world?.pointerLeave());

const NOT_PLAYABLE = 'a, button, input, textarea, select, label, p, li, .mail-link, .socials';
window.addEventListener('pointerdown', (e) => {
  if (!world || e.pointerType !== 'mouse' || e.button !== 0) return;
  if (!e.target.closest('[data-playground]') || e.target.closest(NOT_PLAYABLE)) return;
  e.preventDefault();
  world.press();
});

/* ───────────── İngilizce öneren küçük bildirim ───────────── */

function maybePromptLanguage() {
  if (hasSavedLang()) return;
  const suggested = browserPrefersTurkish() ? 'tr' : 'en';
  if (suggested === lang) return;
  const box = document.createElement('div');
  box.className = 'lang-prompt';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-label', t(ui.langPromptAction, suggested));
  box.lang = suggested;
  box.innerHTML = `<span>${t(ui.langPrompt, suggested)}</span>
    <button type="button" data-act="switch">${t(ui.langPromptAction, suggested)}</button>
    <button type="button" data-act="close" aria-label="${t(ui.dismiss, suggested)}">✕</button>`;
  box.addEventListener('click', (e) => {
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (act === 'switch') switchLang(suggested);
    if (act === 'close') saveLang(lang);
    if (act) box.remove();
  });
  document.body.append(box);
  requestAnimationFrame(() => box.classList.add('is-visible'));
}

/* ───────────── konsoldaki gizli not ───────────── */

function greet() {
  const style = 'font: 600 14px/1.6 system-ui; color: #ff7a45;';
  console.log('%cMerhaba meraklı geliştirici 👋', style);
  console.log('Bu site Three.js, GLSL ve biraz sabırla yapıldı. Parçacıklar: güneş → rüzgar → şebeke → atom → GES.');
}

boot();
