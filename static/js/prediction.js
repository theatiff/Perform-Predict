// Validates the form, sends it to Flask, and shows the result.
const form = document.getElementById('predForm');
const formCard = document.getElementById('formCard');
const resultCard = document.getElementById('resultCard');
const loader = document.getElementById('loader');
const formError = document.getElementById('formError');
const type = form.dataset.type;

const GRADE_NOTE = 'Grade labels (Fail, DD to AA) follow the original dataset mapping and are not a universal grading system. The model reached about 35.86% accuracy on a small dataset, so treat this as a rough indication.';

function setError(field, msg) {
  field.classList.toggle('bad', !!msg);
  field.querySelector('.err').textContent = msg || '';
}

function validate() {
  let ok = true;
  form.querySelectorAll('.field').forEach(f => {
    const el = f.querySelector('select,input');
    let msg = '';
    if (el.value === '') msg = 'This field is required.';
    else if (el.type === 'number') {
      const v = Number(el.value);
      if (Number.isNaN(v) || v < 0 || v > 100) msg = 'Enter a number from 0 to 100.';
    }
    setError(f, msg);
    if (msg) ok = false;
  });
  return ok;
}

function summary() {
  return [...form.querySelectorAll('.field')].map(f => {
    const el = f.querySelector('select,input');
    const val = el.tagName === 'SELECT' ? el.options[el.selectedIndex].text : el.value;
    return `<dt>${f.querySelector('span').textContent}</dt><dd>${val}</dd>`;
  }).join('');
}

function show(html) {
  resultCard.innerHTML = html + `<button class="btn btn-ghost" id="again" type="button">Predict Again</button>`;
  formCard.hidden = true; resultCard.hidden = false;
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  document.getElementById('again').onclick = () => {
    resultCard.hidden = true; formCard.hidden = false; form.reset();
    form.querySelectorAll('.field').forEach(f => setError(f, ''));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  formError.textContent = '';
  if (!validate()) { formError.textContent = 'Please fix the highlighted fields.'; return; }
  const payload = {};
  new FormData(form).forEach((v, k) => (payload[k] = v));
  loader.hidden = false;
  try {
    const res = await fetch(form.dataset.endpoint, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      Object.entries(data.errors || {}).forEach(([k, m]) => {
        const el = form.querySelector(`[name="${k}"]`);
        if (el) setError(el.closest('.field'), m);
      });
      formError.textContent = 'The server could not accept some inputs. Please check the highlighted fields.';
      return;
    }
    if (type === 'school') {
      show(`<p class="muted">Predicted mathematics score</p><div class="big">${data.score}</div>
        <p class="note">An estimate out of 100 from a linear regression model. Individual results can differ.</p>
        <dl>${summary()}</dl>`);
    } else {
      show(`<p class="muted">Predicted grade</p><div class="big">${data.category}</div>
        <p><b>Grade code ${data.grade}</b> (${data.category})</p>
        <p class="note">${GRADE_NOTE}</p><dl>${summary()}</dl>`);
    }
  } catch (err) {
    formError.textContent = 'Could not reach the server. Check that the Flask app is running and try again.';
  } finally {
    loader.hidden = true;
  }
});
