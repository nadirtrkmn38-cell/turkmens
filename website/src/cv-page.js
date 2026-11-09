import '@fontsource-variable/space-grotesk';
import '@fontsource-variable/inter';
import '@fontsource-variable/jetbrains-mono';
import './styles/cv.css';

import { content } from './content.js';
import { pageTitle, renderCv, t } from './render.js';
import { getInitialLang, saveLang, syncUrl } from './lib/lang.js';

const html = document.documentElement;
const root = document.getElementById('cv');
let lang = getInitialLang();

function mount(next) {
  root.innerHTML = renderCv(next);
  html.lang = next;
  document.title = pageTitle(next, 'cv');
  document.querySelector('meta[name="description"]')?.setAttribute('content', t(content.meta.description, next));
}

if (import.meta.env.DEV || html.lang !== lang || !root.querySelector('.cv')) mount(lang);

document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-action]');
  if (!el) return;
  if (el.dataset.action === 'print') window.print();
  if (el.dataset.action === 'lang') {
    lang = el.dataset.lang;
    saveLang(lang);
    syncUrl(lang);
    mount(lang);
  }
});

// cv.html?print → sayfa açılınca yazdırma penceresi
if (new URLSearchParams(location.search).has('print')) {
  window.addEventListener('load', () => setTimeout(() => window.print(), 400));
}
