import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
import { DEFAULT_LANG, renderApp, renderCv, renderHead } from './src/render.js';

const root = fileURLToPath(new URL('.', import.meta.url));

/**
 * Sayfaları build sırasında içerikle doldurur (SEO ve hızlı ilk görüntü için).
 * index.html ve cv.html içindeki <!--head--> ve <!--app--> yer tutucuları değiştirilir.
 */
function prerender(base) {
  return {
    name: 'nadirturkmen-prerender',
    transformIndexHtml: {
      order: 'pre',
      handler(html, ctx) {
        const isCv = /cv\.html$/.test(ctx.path || ctx.filename || '');
        return html
          .replace('<!--head-->', renderHead(DEFAULT_LANG, isCv ? 'cv' : 'home'))
          .replace('<!--app-->', isCv ? renderCv(DEFAULT_LANG) : renderApp(DEFAULT_LANG, base));
      },
    },
  };
}

export default defineConfig(() => {
  // GitHub Pages alt klasörde yayınlıyorsa (örn. /turkmens/) BASE_PATH ile ayarlanır.
  const base = process.env.BASE_PATH || '/';
  return {
    base,
    plugins: [prerender(base)],
    build: {
      target: 'es2020',
      chunkSizeWarningLimit: 800,
      rollupOptions: {
        input: {
          main: root + 'index.html',
          cv: root + 'cv.html',
        },
      },
    },
  };
});
