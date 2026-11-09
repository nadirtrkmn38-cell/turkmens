/**
 * Sayfa içi küçük etkileşimler:
 * kayarak gelme animasyonları, isimdeki harflerin imlece tepkisi,
 * kartların eğilmesi, mıknatıs butonlar, sayaçlar ve yerel saat.
 * Her dil değişiminde yeniden kurulur; destroy() ile temizlenir.
 */
import { profile } from '../content.js';

export function initEffects(root, { reducedMotion = false, lang = 'tr' } = {}) {
  const cleanups = [];
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const on = (el, type, fn, opts) => {
    el.addEventListener(type, fn, opts);
    cleanups.push(() => el.removeEventListener(type, fn, opts));
  };

  /* ── kayarak gelme ── */
  const reveals = [...root.querySelectorAll('[data-reveal]')];
  if (reducedMotion || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
            if (entry.target.querySelector('[data-count]')) countUp(entry.target);
          }
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.1 },
    );
    reveals.forEach((el) => io.observe(el));
    cleanups.push(() => io.disconnect());
  }

  /* ── sayaçlar (3, 10, ~20, 4,3 …) ── */
  function countUp(el) {
    const node = el.querySelector('[data-count]');
    const m = String(node.dataset.count).match(/^([^\d]*)(\d+)(?:([.,])(\d+))?(.*)$/);
    if (!m || reducedMotion) return;
    const [, prefix, int, sep, dec = '', suffix] = m;
    const end = parseFloat(int + (dec ? '.' + dec : ''));
    const format = (v) => prefix + (sep ? v.toFixed(dec.length).replace('.', sep) : Math.round(v)) + suffix;
    const start = performance.now();
    const dur = 1500;
    const step = (now) => {
      const p = Math.min(1, (now - start) / dur);
      node.textContent = format(end * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(step);
    };
    node.textContent = format(0);
    requestAnimationFrame(step);
  }

  /* ── isim: harfler imlece yaklaştıkça kalınlaşır ── */
  const name = root.querySelector('[data-name]');
  if (name && finePointer && !reducedMotion) {
    const chars = [...name.querySelectorAll('.ch')];
    const BASE = 500;
    const weights = chars.map(() => BASE);
    const targets = chars.map(() => BASE);
    let centers = [];
    let raf = 0;
    let active = false;
    const measure = () => {
      centers = chars.map((c) => {
        const r = c.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 + window.scrollY };
      });
    };
    const tick = () => {
      let moving = false;
      chars.forEach((c, i) => {
        weights[i] += (targets[i] - weights[i]) * 0.14;
        if (Math.abs(targets[i] - weights[i]) > 0.5) moving = true;
        else weights[i] = targets[i];
        c.style.fontWeight = weights[i].toFixed(0);
      });
      raf = moving || active ? requestAnimationFrame(tick) : 0;
    };
    const wake = () => {
      if (!raf) raf = requestAnimationFrame(tick);
    };
    const onMove = (e) => {
      if (window.scrollY > window.innerHeight) return;
      if (!centers.length) measure();
      const radius = Math.max(160, window.innerWidth * 0.14);
      active = true;
      centers.forEach((c, i) => {
        const d = Math.hypot(e.clientX - c.x, e.clientY + window.scrollY - c.y);
        const k = Math.max(0, 1 - d / radius);
        targets[i] = 430 + 270 * k * k; // uzakta ince (430), imlecin yanında kalın (700)
      });
      wake();
    };
    const onLeave = () => {
      active = false;
      targets.fill(BASE);
      wake();
    };
    on(window, 'pointermove', onMove, { passive: true });
    on(document.documentElement, 'mouseleave', onLeave);
    on(window, 'resize', () => (centers = []));
    // harfler giriş animasyonundan sonra ölçülsün
    setTimeout(measure, 2200);
    cleanups.push(() => cancelAnimationFrame(raf));
  }

  /* ── proje kartları: hafif 3D eğilme + ışık ── */
  if (finePointer && !reducedMotion) {
    root.querySelectorAll('[data-tilt]').forEach((card) => {
      on(card, 'pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        card.style.setProperty('--mx', `${(x * 100).toFixed(1)}%`);
        card.style.setProperty('--my', `${(y * 100).toFixed(1)}%`);
        card.style.setProperty('--rx', `${((0.5 - y) * 5).toFixed(2)}deg`);
        card.style.setProperty('--ry', `${((x - 0.5) * 7).toFixed(2)}deg`);
      });
      on(card, 'pointerleave', () => {
        card.style.setProperty('--rx', '0deg');
        card.style.setProperty('--ry', '0deg');
      });
    });

    /* ── mıknatıs butonlar ── */
    root.querySelectorAll('[data-magnetic]').forEach((el) => {
      on(el, 'pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2);
        const dy = e.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${dx * 0.22}px, ${dy * 0.3}px)`;
      });
      on(el, 'pointerleave', () => {
        el.style.transform = '';
      });
    });
  }

  /* ── yerel saat ── */
  const clock = root.querySelector('[data-clock]');
  if (clock) {
    let fmt;
    try {
      fmt = new Intl.DateTimeFormat(lang === 'tr' ? 'tr-TR' : 'en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: profile.timeZone,
      });
    } catch {
      fmt = new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' });
    }
    const update = () => (clock.textContent = fmt.format(new Date()));
    update();
    const id = setInterval(update, 15000);
    cleanups.push(() => clearInterval(id));
  }

  return {
    destroy() {
      cleanups.forEach((fn) => fn());
    },
  };
}
