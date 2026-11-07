// Charts use only numbers passed from Flask (window.DASH).
const D = window.DASH;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
let charts = [];

function bar(id, labels, values, opts = {}) {
  const ctx = document.getElementById(id);
  const colors = values.map((v, i) => opts.signed ? (v >= 0 ? css('--accent') : css('--accent2')) : [css('--accent'), css('--accent2'), css('--muted')][i % 3]);
  charts.push(new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ data: values, backgroundColor: colors, borderRadius: 8, maxBarThickness: 38 }] },
    options: {
      indexAxis: opts.horizontal ? 'y' : 'x', responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { min: opts.xmin, max: opts.xmax, ticks: { color: css('--muted') }, grid: { color: css('--line') } },
        y: { min: opts.ymin, max: opts.ymax, ticks: { color: css('--muted') }, grid: { color: css('--line') } }
      }
    }
  }));
}

function draw() {
  charts.forEach(c => c.destroy()); charts = [];
  const s = D.school_metrics, c = D.college_metrics;
  bar('schoolPerf', ['Cross-validation R²', 'Test R²'], [s.cv_r2, s.test_r2], { ymin: 0, ymax: 1 });
  bar('collegePerf', ['Cross-validation accuracy', 'Random guess (1 of 8)'], [c.cv_acc, 12.5], { ymin: 0, ymax: 100 });
  bar('schoolImp', D.school_coef.labels, D.school_coef.values, { horizontal: true, signed: true });
  bar('collegeImp', D.college_imp.labels, D.college_imp.values, { horizontal: true, xmin: 0 });
}
draw();
document.addEventListener('themechange', draw);

// highlight the sidebar link of the section in view
const side = [...document.querySelectorAll('.side a')];
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) side.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id));
}), { rootMargin: '-30% 0px -60% 0px' });
document.querySelectorAll('.dash-main [id]').forEach(el => io.observe(el));
