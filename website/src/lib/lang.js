import { DEFAULT_LANG, LANGS } from '../render.js';

const KEY = 'nt.lang';

/** Öncelik: ?lang= parametresi → kayıtlı tercih → varsayılan (tr) */
export function getInitialLang() {
  const param = new URLSearchParams(location.search).get('lang');
  if (param && LANGS.includes(param)) return param;
  try {
    const saved = localStorage.getItem(KEY);
    if (saved && LANGS.includes(saved)) return saved;
  } catch {
    /* depolama kapalı olabilir */
  }
  return DEFAULT_LANG;
}

export function hasSavedLang() {
  try {
    return !!localStorage.getItem(KEY);
  } catch {
    return true;
  }
}

export function saveLang(lang) {
  try {
    localStorage.setItem(KEY, lang);
  } catch {
    /* önemli değil */
  }
}

/** Adres çubuğunu dile göre günceller (sayfayı yenilemeden) */
export function syncUrl(lang) {
  try {
    const url = new URL(location.href);
    if (lang === DEFAULT_LANG) url.searchParams.delete('lang');
    else url.searchParams.set('lang', lang);
    history.replaceState(history.state, '', url);
  } catch {
    /* önemli değil */
  }
}

export function browserPrefersTurkish() {
  const list = navigator.languages?.length ? navigator.languages : [navigator.language || ''];
  return list.some((l) => /^tr\b/i.test(l || ''));
}
