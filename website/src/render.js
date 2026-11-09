/**
 * İçerikten (content.js) HTML üreten saf fonksiyonlar.
 * Hem build sırasında (Node — sayfayı önceden oluşturmak için)
 * hem de tarayıcıda (dil değiştirince) çalışır. DOM kullanmaz.
 */
import { profile, socials, content, ui } from './content.js';

export const LANGS = ['tr', 'en'];
export const DEFAULT_LANG = 'tr';

export const SECTIONS = [
  { key: 'hero', id: 'top' },
  { key: 'about', id: 'hakkimda' },
  { key: 'experience', id: 'deneyim' },
  { key: 'skills', id: 'yetkinlikler' },
  { key: 'projects', id: 'projeler' },
  { key: 'contact', id: 'iletisim' },
];

/* ───────────────────────── yardımcılar ───────────────────────── */

export const t = (value, lang) => {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    return value[lang] ?? value[DEFAULT_LANG] ?? '';
  }
  return value ?? '';
};

const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ESC[c]);

/** *vurgu* → <em>vurgu</em> */
const rich = (s) => esc(s).replace(/\*([^*]+)\*/g, '<em>$1</em>');
/** *vurgu* işaretlerini kaldır (düz metin) */
export const plain = (s) => String(s ?? '').replace(/\*/g, '');

/** Başlığı kelimelere böler (kayarak gelme animasyonu için), *vurgu* destekler. */
function splitWords(text) {
  let em = false;
  return String(text)
    .split(/\s+/)
    .filter(Boolean)
    .map((raw, i) => {
      let word = raw;
      let trail = '';
      if (word.startsWith('*')) {
        em = true;
        word = word.slice(1);
      }
      let closes = false;
      const m = word.match(/^(.*)\*([.,;:!?…)"'»]*)$/);
      if (m) {
        word = m[1];
        trail = m[2];
        closes = true;
      }
      const inner = em ? `<em>${esc(word)}</em>${esc(trail)}` : esc(word + trail);
      if (closes) em = false;
      return `<span class="w"><span style="--i:${i}">${inner}</span></span>`;
    })
    .join(' ');
}

const pad2 = (n) => String(n).padStart(2, '0');
const period = (item, lang) => {
  const end = item.end ? esc(item.end) : esc(t(ui.present, lang));
  const note = item.endNote ? ` (${esc(t(item.endNote, lang))})` : '';
  return `${esc(item.start)} — ${end}${note}`;
};
const activeSocials = () => socials.filter((s) => s.url);
const year = new Date().getFullYear();
const host = (url) => String(url).replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '');

const arrow = (dir = 'up-right') =>
  dir === 'right'
    ? '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M8.5 3.5 13 8l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
    : dir === 'up'
      ? '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 14V3M3.5 7.5 8 3l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
      : dir === 'left'
        ? '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M14 8H3M7.5 3.5 3 8l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
        : '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5l7-7M5.5 4.5h6v6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';

const assetUrl = (path, base) => (/^https?:\/\//.test(path) ? path : base + String(path).replace(/^\//, ''));

const langHref = (page, lang) => {
  const file = page === 'cv' ? './cv.html' : './';
  return lang === DEFAULT_LANG ? file : `${file}?lang=${lang}`;
};

/* ───────────────────────── <head> ───────────────────────── */

export function pageTitle(lang, page = 'home') {
  return page === 'cv' ? `${profile.name} — CV` : `${profile.name} — ${t(profile.role, lang)}`;
}

export function renderHead(lang, page = 'home') {
  const title = pageTitle(lang, page);
  const description = t(content.meta.description, lang);
  const site = profile.url.replace(/\/$/, '');
  const url = site + (page === 'cv' ? '/cv.html' : '/');
  const image = site + '/og-image.jpg';
  const person = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: profile.name,
    url: profile.url,
    description,
    email: profile.email ? `mailto:${profile.email}` : undefined,
    address: { '@type': 'PostalAddress', addressLocality: t(profile.location, 'en'), addressCountry: profile.country },
    affiliation: { '@type': 'CollegeOrUniversity', name: 'Kocaeli University' },
    knowsAbout: ['Energy efficiency', 'Energy audits', 'ISO 50001', 'Waste heat recovery', 'Organic Rankine Cycle', 'PV + BESS feasibility', 'LCOE', 'Electricity markets'],
    sameAs: activeSocials().map((s) => s.url),
  };
  const json = JSON.stringify(person).replace(/</g, '\\u003c');
  return `<title>${esc(title)}</title>
    <meta name="description" content="${esc(description)}" />
    <link rel="canonical" href="${url}" />
    <link rel="alternate" hreflang="tr" href="${url}" />
    <link rel="alternate" hreflang="en" href="${url}?lang=en" />
    <link rel="alternate" hreflang="x-default" href="${url}" />
    <meta property="og:type" content="profile" />
    <meta property="og:site_name" content="${esc(profile.name)}" />
    <meta property="og:title" content="${esc(title)}" />
    <meta property="og:description" content="${esc(description)}" />
    <meta property="og:url" content="${url}" />
    <meta property="og:image" content="${image}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="${lang === 'en' ? 'en_US' : 'tr_TR'}" />
    <meta property="profile:first_name" content="${esc(profile.firstName)}" />
    <meta property="profile:last_name" content="${esc(profile.lastName)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${esc(title)}" />
    <meta name="twitter:description" content="${esc(description)}" />
    <meta name="twitter:image" content="${image}" />
    <script type="application/ld+json">${json}</script>`;
}

/* ───────────────────────── ana sayfa ───────────────────────── */

function renderHeader(lang) {
  const navItems = SECTIONS.slice(1)
    .map(
      (s, i) =>
        `<li><a href="#${s.id}" data-nav="${i + 1}"><span class="site-nav__num">${pad2(i + 1)}</span>${esc(t(ui.nav[s.key], lang))}</a></li>`,
    )
    .join('');
  const other = lang === 'tr' ? 'en' : 'tr';
  return `
  <header class="site-header" data-header>
    <div class="site-header__inner">
      <a class="brand" href="#top" aria-label="${esc(profile.name)} — ${esc(t(ui.home, lang))}">
        <span class="brand__mark" aria-hidden="true">${esc(profile.initials)}</span>
        <span class="brand__name">${esc(profile.name)}</span>
      </a>
      <nav class="site-nav" aria-label="${esc(t(ui.mainMenu, lang))}">
        <ul>${navItems}</ul>
      </nav>
      <div class="site-header__actions">
        <button type="button" class="lang-toggle" data-action="lang" data-lang="${other}" aria-label="${esc(t(ui.langSwitch, lang))}">
          <span class="${lang === 'tr' ? 'is-active' : ''}">TR</span><span class="lang-toggle__sep" aria-hidden="true">/</span><span class="${lang === 'en' ? 'is-active' : ''}">EN</span>
        </button>
        <a class="btn btn--small" href="${langHref('cv', lang)}" title="${esc(t(ui.cvLong, lang))}">${esc(t(ui.cv, lang))} ${arrow()}</a>
        <button type="button" class="menu-toggle" data-action="menu" aria-expanded="false" aria-controls="mobile-menu">
          <span class="menu-toggle__label">${esc(t(ui.menu, lang))}</span>
          <span class="menu-toggle__icon" aria-hidden="true"><i></i><i></i></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu" data-mobile-menu hidden>
    <nav aria-label="${esc(t(ui.mainMenu, lang))}">
      <ol>
        ${SECTIONS.slice(1)
          .map(
            (s, i) =>
              `<li style="--i:${i}"><a href="#${s.id}" data-nav="${i + 1}"><span>${pad2(i + 1)}</span>${esc(t(ui.nav[s.key], lang))}</a></li>`,
          )
          .join('')}
      </ol>
    </nav>
    <div class="mobile-menu__foot">
      ${profile.email ? `<a href="mailto:${esc(profile.email)}">${esc(profile.email)}</a>` : ''}
      <a href="${langHref('cv', lang)}">${esc(t(ui.cvLong, lang))} ${arrow()}</a>
    </div>
  </div>

  <nav class="rail" aria-label="${esc(t(ui.sections, lang))}">
    <ol>
      ${SECTIONS.map((s, i) => {
        const label = i === 0 ? t(ui.home, lang) : t(ui.nav[s.key], lang);
        return `<li><a href="#${s.id}" data-nav="${i}"><span class="rail__label" aria-hidden="true">${esc(label)}</span><span class="rail__dot" aria-hidden="true"></span><span class="sr-only">${esc(label)}</span></a></li>`;
      }).join('')}
    </ol>
  </nav>`;
}

function renderHero(lang) {
  const letters = (word, offset) =>
    [...word].map((ch, i) => `<span class="ch" style="--i:${i + offset}">${esc(ch)}</span>`).join('');
  return `
  <section class="section hero" id="top" data-section data-playground aria-label="${esc(profile.name)}">
    <div class="stage" data-stage aria-hidden="true"></div>
    <div class="hero__inner container">
      ${
        profile.available
          ? `<p class="hero__status" data-intro style="--d:0"><span class="pulse" aria-hidden="true"></span>${esc(t(content.hero.status, lang))}</p>`
          : ''
      }
      <h1 class="hero__title">
        <span class="sr-only">${esc(profile.name)}</span>
        <span class="hero__name" aria-hidden="true" data-name>
          <span class="line">${letters(profile.firstName, 0)}</span>
          <span class="line">${letters(profile.lastName, profile.firstName.length)}</span>
        </span>
      </h1>
      <p class="hero__role" data-intro style="--d:350">${esc(t(profile.role, lang))}<span class="hero__sep" aria-hidden="true"></span>${esc(t(profile.location, lang))}</p>
      <p class="hero__lead" data-intro style="--d:450">${esc(t(content.hero.lead, lang))}</p>
      <div class="hero__cta" data-intro style="--d:550">
        <a class="btn btn--primary" href="#deneyim" data-magnetic>${esc(t(ui.viewWork, lang))} ${arrow('right')}</a>
        <a class="btn btn--ghost" href="${langHref('cv', lang)}" data-magnetic>${esc(t(ui.viewCv, lang))} ${arrow()}</a>
      </div>
    </div>
    <div class="hero__footer container" data-intro style="--d:700">
      <a class="scroll-cue" href="#hakkimda"><span class="scroll-cue__track" aria-hidden="true"><span></span></span>${esc(t(ui.scroll, lang))}</a>
      <p class="hero__hint"><span class="hero__hint-icon" aria-hidden="true"></span>${esc(t(ui.playHint, lang))}</p>
      <p class="hero__clock"><span class="sr-only">${esc(t(ui.localTime, lang))}: </span><span data-clock>--:--</span> · ${esc(t(profile.location, lang))}</p>
    </div>
  </section>`;
}

function eyebrow(index, key, lang) {
  return `<p class="eyebrow" data-reveal><span class="eyebrow__num">${pad2(index)}</span><span class="eyebrow__line" aria-hidden="true"></span>${esc(t(ui.nav[key], lang))}</p>`;
}

function renderAbout(lang, base) {
  const a = content.about;
  const portrait = profile.photo
    ? `<img src="${esc(assetUrl(profile.photo, base))}" alt="${esc(profile.name)}" width="480" height="600" loading="lazy" />`
    : `<div class="portrait__mono" aria-hidden="true"><span>${esc(profile.initials)}</span></div>`;
  return `
  <section class="section about" id="hakkimda" data-section aria-labelledby="about-title">
    <div class="stage" data-stage aria-hidden="true"></div>
    <div class="container about__grid">
      <div class="about__content">
        ${eyebrow(1, 'about', lang)}
        <h2 class="section-title split" id="about-title" data-reveal>${splitWords(t(a.title, lang))}</h2>
        <div class="about__body">
          <figure class="portrait" data-reveal style="--d:120">
            ${portrait}
            <figcaption><span class="pulse" aria-hidden="true"></span>${esc(t(profile.location, lang))}</figcaption>
          </figure>
          <div class="prose">
            ${a.paragraphs.map((p, i) => `<p data-reveal style="--d:${160 + i * 80}">${rich(t(p, lang))}</p>`).join('')}
          </div>
        </div>
        <ul class="stats">
          ${a.stats
            .map(
              (s, i) =>
                `<li class="stat" data-reveal style="--d:${i * 90}"><span class="stat__value"><span data-count="${esc(s.value)}">${esc(s.value)}</span>${s.unit ? `<small>${esc(s.unit)}</small>` : ''}</span><span class="stat__label">${esc(t(s.label, lang))}</span></li>`,
            )
            .join('')}
        </ul>
      </div>
    </div>
  </section>`;
}

function renderExperience(lang) {
  const e = content.experience;
  const job = (j, i) => `
          <li class="job" data-reveal style="--d:${i * 60}">
            <div class="job__meta">
              <span class="job__date">${period(j, lang)}</span>
              ${j.location ? `<span class="job__loc">${esc(t(j.location, lang))}</span>` : ''}
            </div>
            <h3 class="job__role">${esc(t(j.role, lang))}</h3>
            <p class="job__company">${esc(t(j.company, lang))}${j.note ? `<span>${esc(t(j.note, lang))}</span>` : ''}</p>
            ${
              j.bullets?.length
                ? `<ul class="job__bullets">${j.bullets.map((b) => `<li>${rich(t(b, lang))}</li>`).join('')}</ul>`
                : ''
            }
          </li>`;
  const edu = (d, i) => `
          <li class="job job--edu" data-reveal style="--d:${i * 60}">
            <div class="job__meta"><span class="job__date">${period(d, lang)}</span></div>
            <h3 class="job__role">${esc(t(d.degree, lang))}</h3>
            <p class="job__company">${esc(t(d.school, lang))}</p>
            ${
              d.details?.length
                ? `<ul class="job__bullets">${d.details.map((x) => `<li>${rich(t(x, lang))}</li>`).join('')}</ul>`
                : ''
            }
          </li>`;
  const certs = e.certifications?.length
    ? `<h3 class="timeline__subtitle" data-reveal><span aria-hidden="true"></span>${esc(t(e.certificationsTitle, lang))}</h3>
        <ul class="certs" data-reveal>
          ${e.certifications
            .map(
              (c) =>
                `<li><span class="certs__name">${esc(t(c.name, lang))}</span><span class="certs__meta">${esc(c.issuer)} · ${esc(c.date)}</span></li>`,
            )
            .join('')}
        </ul>`
    : '';
  return `
  <section class="section experience" id="deneyim" data-section aria-labelledby="exp-title">
    <div class="stage" data-stage aria-hidden="true"></div>
    <div class="container experience__grid">
      <header class="experience__head">
        <div class="sticky">
          ${eyebrow(2, 'experience', lang)}
          <h2 class="section-title split" id="exp-title" data-reveal>${splitWords(t(e.title, lang))}</h2>
          <p class="section-intro" data-reveal style="--d:120">${esc(t(e.intro, lang))}</p>
        </div>
      </header>
      <div class="timeline">
        <ol class="timeline__list">${e.jobs.map(job).join('')}
        </ol>
        ${
          e.education?.length
            ? `<h3 class="timeline__subtitle" data-reveal><span aria-hidden="true"></span>${esc(t(e.educationTitle, lang))}</h3>
        <ol class="timeline__list">${e.education.map(edu).join('')}
        </ol>`
            : ''
        }
        ${certs}
      </div>
    </div>
  </section>`;
}

function renderSkills(lang) {
  const s = content.skills;
  const track = s.marquee.map((m) => `<span>${esc(m)}</span><i aria-hidden="true">✦</i>`).join('');
  return `
  <section class="section skills" id="yetkinlikler" data-section aria-labelledby="skills-title">
    <div class="stage" data-stage aria-hidden="true"></div>
    <div class="container skills__grid">
      <div class="skills__content">
        ${eyebrow(3, 'skills', lang)}
        <h2 class="section-title split" id="skills-title" data-reveal>${splitWords(t(s.title, lang))}</h2>
        <p class="section-intro" data-reveal style="--d:120">${esc(t(s.intro, lang))}</p>
        <div class="skill-groups">
          ${s.groups
            .map(
              (g, i) => `
          <div class="skill-group" data-reveal style="--d:${i * 70}">
            <h3 class="skill-group__name"><span>${pad2(i + 1)}</span>${esc(t(g.name, lang))}</h3>
            <ul class="chips">${g.items.map((it) => `<li class="chip">${esc(t(it, lang))}</li>`).join('')}</ul>
          </div>`,
            )
            .join('')}
        </div>
        <div class="langs" data-reveal>
          <h3 class="skill-group__name"><span>${pad2(s.groups.length + 1)}</span>${esc(t(s.languagesTitle, lang))}</h3>
          <ul>
            ${s.languages
              .map(
                (l) =>
                  `<li><span class="langs__name">${esc(t(l.name, lang))}</span><span class="langs__line" aria-hidden="true"></span><span class="langs__level">${esc(t(l.level, lang))}</span></li>`,
              )
              .join('')}
          </ul>
        </div>
      </div>
    </div>
    <div class="marquee" aria-hidden="true"><div class="marquee__track"><div>${track}</div><div>${track}</div></div></div>
  </section>`;
}

/* proje kartlarındaki küçük, kod ile çizilmiş önizlemeler */
function projectVisual(p, lang, base) {
  const bar = (label) => `<div class="mock__bar"><i></i><i></i><i></i><span>${esc(label)}</span></div>`;
  const site = host(p.links?.[0]?.url || '');
  if (p.visual === 'ntherm') {
    const classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    return `
            <div class="mock mock--ntherm" aria-hidden="true">
              <div class="mock__window">
                ${bar(site)}
                <div class="mock__ntherm">
                  <div class="mock__wall">
                    <i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>
                    <span class="mock__heat"></span><span class="mock__heat"></span><span class="mock__heat"></span>
                    <b>U = 0,28 W/m²K</b>
                  </div>
                  <div class="mock__classes">
                    ${classes.map((c, i) => `<span style="--i:${i}"${c === 'B' ? ' class="is-on"' : ''}>${c}</span>`).join('')}
                  </div>
                </div>
              </div>
            </div>`;
  }
  if (p.visual === 'chart') {
    // temsili günlük fiyat eğrisi (gerçek veri değildir; sadece görsel)
    const actual = [52, 48, 45, 44, 45, 50, 60, 72, 78, 74, 66, 60, 56, 55, 58, 64, 74, 86, 92, 88, 80, 72, 64, 57];
    const forecast = [54, 49, 46, 45, 47, 52, 62, 70, 75, 73, 68, 62, 57, 56, 57, 62, 71, 83, 90, 89, 82, 74, 66, 59];
    const toPath = (arr) =>
      arr.map((v, i) => `${i === 0 ? 'M' : 'L'}${(i / 23) * 300},${110 - v}`).join(' ');
    return `
            <div class="mock mock--chart" aria-hidden="true">
              <div class="mock__window">
                ${bar(site)}
                <div class="mock__chart">
                  <div class="mock__legend"><span><i class="a"></i>${lang === 'tr' ? 'Gerçekleşen' : 'Actual'}</span><span><i class="f"></i>${lang === 'tr' ? 'Tahmin' : 'Forecast'}</span></div>
                  <svg viewBox="0 0 300 100" preserveAspectRatio="none">
                    <path class="mock__grid" d="M0,25H300M0,50H300M0,75H300" />
                    <path class="mock__area" d="${toPath(actual)} L300,100 L0,100 Z" />
                    <path class="mock__line mock__line--a" d="${toPath(actual)}" />
                    <path class="mock__line mock__line--f" d="${toPath(forecast)}" />
                  </svg>
                  <div class="mock__hours"><span>00</span><span>06</span><span>12</span><span>18</span><span>23</span></div>
                </div>
              </div>
            </div>`;
  }
  if (p.visual === 'web') {
    return `
            <div class="mock mock--web" aria-hidden="true">
              <div class="mock__window">
                ${bar(site)}
                <div class="mock__web">
                  <div class="mock__nav"><b></b><span></span><span></span><span></span><em>TR / EN</em></div>
                  <div class="mock__hero">
                    <div class="mock__copy"><b></b><b></b><span></span><span></span><u></u></div>
                    <div class="mock__gauge"><i></i><span>%25</span></div>
                  </div>
                  <div class="mock__tiles"><i></i><i></i><i></i></div>
                </div>
              </div>
            </div>`;
  }
  if (p.visual) {
    return `<img class="card__img" src="${esc(assetUrl(p.visual, base))}" alt="${esc(t(p.title, lang))}" loading="lazy" />`;
  }
  return `<div class="card__gradient" aria-hidden="true"></div>`;
}

function renderProjects(lang, base) {
  const pr = content.projects;
  const cards = pr.items
    .map(
      (p, i) => `
        <article class="card" data-reveal data-tilt style="--d:${i * 90}">
          <div class="card__visual">${projectVisual(p, lang, base)}</div>
          <div class="card__body">
            <p class="card__meta"><span>${pad2(i + 1)}</span><span>${period(p, lang)}</span></p>
            <h3 class="card__title">${esc(t(p.title, lang))}</h3>
            <p class="card__kind">${esc(t(p.kind, lang))}</p>
            <p class="card__desc">${rich(t(p.description, lang))}</p>
            <ul class="tags">${p.tags.map((tag) => `<li>${esc(tag)}</li>`).join('')}</ul>
            ${
              p.links?.some((l) => l.url)
                ? `<div class="card__links">${p.links
                    .filter((l) => l.url)
                    .map(
                      (l) =>
                        `<a href="${esc(l.url)}" target="_blank" rel="noopener noreferrer">${esc(t(l.label, lang))} ${arrow()}</a>`,
                    )
                    .join('')}</div>`
                : ''
            }
          </div>
        </article>`,
    )
    .join('');
  const wide = pr.items.length % 2 === 0 ? ' card--wide' : '';
  return `
  <section class="section projects" id="projeler" data-section aria-labelledby="projects-title">
    <div class="stage" data-stage aria-hidden="true"></div>
    <div class="container">
      <header class="projects__head">
        ${eyebrow(4, 'projects', lang)}
        <h2 class="section-title split" id="projects-title" data-reveal>${splitWords(t(pr.title, lang))}</h2>
        <p class="section-intro" data-reveal style="--d:120">${esc(t(pr.intro, lang))}</p>
      </header>
      <div class="cards">${cards}
        <a class="card card--next${wide}" href="#iletisim" data-reveal>
          <span class="card--next__plus" aria-hidden="true"></span>
          <span class="card--next__text">
            <span class="card--next__title">${rich(t(pr.next.title, lang))}</span>
            <span class="card--next__sub">${esc(t(pr.next.text, lang))}</span>
          </span>
          <span class="card--next__cta">${esc(t(ui.contactMe, lang))} ${arrow('right')}</span>
        </a>
      </div>
    </div>
  </section>`;
}

function renderContact(lang) {
  const c = content.contact;
  const links = activeSocials()
    .map(
      (s) =>
        `<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer me"><span>${esc(s.label)}</span>${arrow()}</a></li>`,
    )
    .join('');
  return `
  <section class="section contact" id="iletisim" data-section data-playground aria-labelledby="contact-title">
    <div class="container contact__inner">
      ${eyebrow(5, 'contact', lang)}
      <div class="contact__stage" data-stage aria-hidden="true"></div>
      <h2 class="contact__title split" id="contact-title" data-reveal>${splitWords(t(c.title, lang))}</h2>
      <p class="contact__text" data-reveal style="--d:120">${esc(t(c.text, lang))}</p>
      ${
        profile.email
          ? `<div class="contact__mail" data-reveal style="--d:200">
        <a class="mail-link" href="mailto:${esc(profile.email)}" data-magnetic aria-label="${esc(t(ui.sendMail, lang))}: ${esc(profile.email)}">${esc(profile.email)}</a>
        <button type="button" class="copy-btn" data-action="copy" data-copy="${esc(profile.email)}">${esc(t(ui.copy, lang))}</button>
      </div>`
          : ''
      }
      ${profile.phone ? `<p class="contact__phone" data-reveal><a href="tel:${esc(profile.phone.replace(/\s+/g, ''))}">${esc(profile.phone)}</a></p>` : ''}
      ${links ? `<ul class="socials" data-reveal style="--d:260">${links}</ul>` : ''}
    </div>
    <footer class="site-footer container">
      <p>© ${year} ${esc(profile.name)}</p>
      <p class="site-footer__built">${esc(t(ui.builtWith, lang))}</p>
      <a href="#top" class="site-footer__top">${esc(t(ui.backToTop, lang))} ${arrow('up')}</a>
    </footer>
  </section>`;
}

/** Ana sayfanın #app içeriği */
export function renderApp(lang, base = '/') {
  return `
  <a class="skip-link" href="#main">${esc(t(ui.skip, lang))}</a>
  ${renderHeader(lang)}
  <main id="main">
    ${renderHero(lang)}
    ${renderAbout(lang, base)}
    ${renderExperience(lang)}
    ${renderSkills(lang)}
    ${renderProjects(lang, base)}
    ${renderContact(lang)}
  </main>
  <div class="toast" data-toast role="status" aria-live="polite"></div>`;
}

/* ───────────────────────── klasik CV sayfası ───────────────────────── */

export function renderCv(lang) {
  const e = content.experience;
  const s = content.skills;
  const L = ui.cvSections;
  const other = lang === 'tr' ? 'en' : 'tr';
  const contactItems = [
    profile.email && `<li><span>${esc(t(L.email, lang))}</span><a href="mailto:${esc(profile.email)}">${esc(profile.email)}</a></li>`,
    profile.phone &&
      `<li><span>${esc(t(L.phone, lang))}</span><a href="tel:${esc(profile.phone.replace(/\s+/g, ''))}">${esc(profile.phone)}</a></li>`,
    `<li><span>${esc(t(L.web, lang))}</span><a href="${esc(profile.url)}">${esc(host(profile.url))}</a></li>`,
    `<li><span>${esc(t(L.location, lang))}</span>${esc(t(profile.location, lang))}, Türkiye</li>`,
  ]
    .filter(Boolean)
    .join('');
  const socialItems = activeSocials()
    .map((so) => `<li><span>${esc(so.label)}</span><a href="${esc(so.url)}">${esc(host(so.url))}</a></li>`)
    .join('');

  return `
  <div class="cv-toolbar" role="toolbar" aria-label="CV">
    <a class="cv-btn" href="${langHref('home', lang)}">${arrow('left')}<span>${esc(t(ui.backToSite, lang))}</span></a>
    <div class="cv-toolbar__right">
      <button type="button" class="cv-btn" data-action="lang" data-lang="${other}" aria-label="${esc(t(ui.langSwitch, lang))}">${other.toUpperCase()}</button>
      <button type="button" class="cv-btn cv-btn--primary" data-action="print">${esc(t(ui.print, lang))}</button>
    </div>
  </div>
  <main class="cv-page">
    <article class="cv">
      <header class="cv__header">
        <div>
          <h1 class="cv__name">${esc(profile.name)}</h1>
          <p class="cv__role">${esc(t(profile.role, lang))} · ${esc(t(content.hero.status, lang))}</p>
        </div>
        <div class="cv__mark" aria-hidden="true">${esc(profile.initials)}</div>
      </header>

      <div class="cv__grid">
        <aside class="cv__side">
          <section>
            <h2>${esc(t(L.contact, lang))}</h2>
            <ul class="cv__kv">${contactItems}</ul>
          </section>
          ${socialItems ? `<section><h2>${esc(t(L.links, lang))}</h2><ul class="cv__kv">${socialItems}</ul></section>` : ''}
          <section>
            <h2>${esc(t(L.skills, lang))}</h2>
            ${s.groups
              .map(
                (g) =>
                  `<div class="cv__skill"><h3>${esc(t(g.name, lang))}</h3><p>${g.items.map((it) => esc(t(it, lang))).join(' · ')}</p></div>`,
              )
              .join('')}
          </section>
          <section>
            <h2>${esc(t(L.languages, lang))}</h2>
            <ul class="cv__langs">${s.languages
              .map((l) => `<li><span>${esc(t(l.name, lang))}</span><span>${esc(t(l.level, lang))}</span></li>`)
              .join('')}${(s.extras || []).map((x) => `<li><span>${esc(t(x, lang))}</span></li>`).join('')}</ul>
          </section>
        </aside>

        <div class="cv__main">
          <section>
            <h2>${esc(t(L.summary, lang))}</h2>
            ${content.about.paragraphs.map((p) => `<p>${esc(plain(t(p, lang)))}</p>`).join('')}
          </section>
          <section>
            <h2>${esc(t(L.experience, lang))}</h2>
            ${e.jobs
              .map(
                (j) => `
            <div class="cv__item">
              <div class="cv__item-head">
                <h3>${esc(t(j.role, lang))}</h3>
                <p class="cv__date">${period(j, lang)}</p>
              </div>
              <p class="cv__org">${esc(t(j.company, lang))}${j.location ? ` · ${esc(t(j.location, lang))}` : ''}${j.note ? ` <span>(${esc(t(j.note, lang))})</span>` : ''}</p>
              ${j.bullets?.length ? `<ul>${j.bullets.map((b) => `<li>${esc(plain(t(b, lang)))}</li>`).join('')}</ul>` : ''}
            </div>`,
              )
              .join('')}
          </section>
          <section>
            <h2>${esc(t(L.projects, lang))}</h2>
            ${content.projects.items
              .map(
                (p) => `
            <div class="cv__item">
              <div class="cv__item-head">
                <h3>${esc(t(p.title, lang))} <span>· ${esc(t(p.kind, lang))}</span></h3>
                <p class="cv__date">${period(p, lang)}</p>
              </div>
              <p>${esc(plain(t(p.description, lang)))}</p>
              <p class="cv__tags">${p.tags.map(esc).join(' · ')}${
                p.links?.[0]?.url ? ` · <a href="${esc(p.links[0].url)}">${esc(host(p.links[0].url))}</a>` : ''
              }</p>
            </div>`,
              )
              .join('')}
          </section>
          ${
            e.education?.length
              ? `<section>
            <h2>${esc(t(L.education, lang))}</h2>
            ${e.education
              .map(
                (d) => `
            <div class="cv__item">
              <div class="cv__item-head">
                <h3>${esc(t(d.degree, lang))}</h3>
                <p class="cv__date">${period(d, lang)}</p>
              </div>
              <p class="cv__org">${esc(t(d.school, lang))}</p>
              ${d.details?.length ? `<ul>${d.details.map((x) => `<li>${esc(plain(t(x, lang)))}</li>`).join('')}</ul>` : ''}
            </div>`,
              )
              .join('')}
          </section>`
              : ''
          }
          ${
            e.certifications?.length
              ? `<section>
            <h2>${esc(t(L.certifications, lang))}</h2>
            <ul class="cv__certs">${e.certifications
              .map((c) => `<li><span>${esc(t(c.name, lang))}</span><span>${esc(c.issuer)} · ${esc(c.date)}</span></li>`)
              .join('')}</ul>
          </section>`
              : ''
          }
        </div>
      </div>
    </article>
  </main>`;
}
