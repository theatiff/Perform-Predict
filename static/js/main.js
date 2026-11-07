// Theme toggle, mobile menu and page transitions.
const root = document.documentElement;
document.getElementById('themeToggle').addEventListener('click', () => {
  const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
  root.dataset.theme = next;
  try { localStorage.setItem('pp-theme', next); } catch (e) {}
  document.dispatchEvent(new Event('themechange'));
});
const links = document.getElementById('navLinks');
document.getElementById('menuBtn').addEventListener('click', () => links.classList.toggle('open'));
document.querySelectorAll('a[href]').forEach(a => {
  a.addEventListener('click', e => {
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || url.pathname === location.pathname || a.target || e.metaKey || e.ctrlKey) return;
    e.preventDefault();
    document.body.classList.add('leaving');
    setTimeout(() => (location.href = a.href), 220);
  });
});
window.addEventListener('pageshow', () => document.body.classList.remove('leaving'));

// Close the mobile menu after choosing a link.
links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
document.addEventListener('keydown', e => { if (e.key === 'Escape') links.classList.remove('open'); });

// On the home page, highlight the nav link of the section in view.
if (document.body.classList.contains('page-home')) {
  const navA = [...links.querySelectorAll('a[href*="#"]')];
  const home = links.querySelector('a[href="/"]');
  const mark = id => {
    navA.forEach(a => a.classList.toggle('active', id && a.getAttribute('href').endsWith('#' + id)));
    if (home) home.classList.toggle('active', !id);
  };
  const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) mark(e.target.id); }),
    { rootMargin: '-45% 0px -50% 0px' });
  ['about', 'features', 'contact'].forEach(id => { const el = document.getElementById(id); if (el) io2.observe(el); });
  window.addEventListener('scroll', () => {
    if (window.scrollY < 200) mark(null);
    else if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) mark('contact');
  }, { passive: true });
}
