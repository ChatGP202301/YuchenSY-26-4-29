/* Collect project requirements locally, then carry them to the same-language inquiry form. */
(() => {
  'use strict';
  const form = document.querySelector('[data-smart-ro-config]');
  if (!form) return;
  const status = form.querySelector('[data-smart-ro-config-status]');
  const clean = (value, max = 160) => String(value || '').replace(/[\u0000-\u001f\u007f<>]/g, ' ').trim().slice(0, max);
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const stagesRaw = clean(data.get('stages'), 30);
    const stageCount = (stagesRaw.match(/[0-9]+/) || [''])[0];
    const options = data.getAll('options').map(value => clean(value, 80)).filter(Boolean);
    const payload = {
      capacity_gpd: clean(data.get('capacity'), 30),
      filter_stage_count: stageCount,
      ro_membrane_brand: clean(data.get('membrane'), 80),
      pump_requirement: clean(data.get('pump'), 160),
      optional_features: options,
      panel_language: clean(data.get('language'), 60),
      estimated_order_quantity: clean(data.get('quantity'), 40),
      destination_market: clean(data.get('market'), 80),
      project_notes: clean(data.get('notes'), 300)
    };
    try {
      sessionStorage.setItem('smart-ro-project-configuration', JSON.stringify(payload));
      sessionStorage.setItem('smart-ro-project-context', JSON.stringify({product:'product-smart-ro-water-purifier-400g-1200g', created:Date.now()}));
    } catch (_) {
      if (status) status.textContent = form.dataset.messageSaveError;
      return;
    }
    const lang = document.documentElement.lang || 'en';
    const url = new URL('contact.html', location.href);
    url.searchParams.set('product_id', 'product-smart-ro-water-purifier-400g-1200g');
    url.searchParams.set('language', lang);
    url.searchParams.set('source_page', location.pathname);
    const productName = clean(document.querySelector('main h1')?.innerText || document.title, 180).replace(/\s+/g, ' ');
    url.searchParams.set('product', productName);
    if (status) status.textContent = form.dataset.messageOpening;
    location.href = url.href;
  });
})();
