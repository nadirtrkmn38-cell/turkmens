/**
 * Üst menü davranışı: kaydırınca arka plan, aşağı inerken gizlenme,
 * aktif bölüm vurgusu ve mobil menü.
 */
export function initNav(root) {
  const header = root.querySelector('[data-header]');
  const menu = root.querySelector('[data-mobile-menu]');
  const toggle = root.querySelector('[data-action="menu"]');
  const links = [...root.querySelectorAll('[data-nav]')];
  const sections = [...root.querySelectorAll('[data-section]')];
  let lastY = window.scrollY;
  let active = -1;
  let ticking = false;
  let open = false;

  const update = () => {
    ticking = false;
    const y = window.scrollY;
    header?.classList.toggle('is-scrolled', y > 24);
    const goingDown = y > lastY + 4;
    const goingUp = y < lastY - 4;
    if (!open) {
      if (goingDown && y > window.innerHeight * 0.6) header?.classList.add('is-hidden');
      else if (goingUp || y < 80) header?.classList.remove('is-hidden');
    }
    if (Math.abs(y - lastY) > 4) lastY = y;

    // ekranın ortasındaki bölüm
    const c = y + window.innerHeight * 0.45;
    let idx = 0;
    sections.forEach((s, i) => {
      if (s.getBoundingClientRect().top + y <= c) idx = i;
    });
    if (idx !== active) {
      active = idx;
      links.forEach((a) => {
        const on = Number(a.dataset.nav) === idx;
        a.classList.toggle('is-active', on);
        if (on) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }
  };

  const onScroll = () => {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(update);
    }
  };

  const setOpen = (value) => {
    if (!menu || !toggle) return;
    open = value;
    toggle.setAttribute('aria-expanded', String(value));
    document.documentElement.style.overflow = value ? 'hidden' : '';
    if (value) {
      menu.hidden = false;
      header?.classList.remove('is-hidden');
      requestAnimationFrame(() => menu.classList.add('is-open'));
    } else {
      menu.classList.remove('is-open');
      setTimeout(() => {
        if (!open) menu.hidden = true;
      }, 450);
    }
  };

  const onKey = (e) => {
    if (e.key === 'Escape' && open) {
      setOpen(false);
      toggle?.focus();
    }
  };

  const onMenuClick = (e) => {
    if (e.target.closest('a')) setOpen(false);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('keydown', onKey);
  menu?.addEventListener('click', onMenuClick);
  update();

  return {
    toggleMenu: () => setOpen(!open),
    closeMenu: () => setOpen(false),
    destroy() {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('keydown', onKey);
      menu?.removeEventListener('click', onMenuClick);
      document.documentElement.style.overflow = '';
    },
  };
}
