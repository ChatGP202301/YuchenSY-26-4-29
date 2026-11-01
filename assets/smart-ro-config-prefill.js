/* Bounded Smart RO handoff: stores selections in a hidden form field without changing form protection. */
(() => {
  'use strict';
  const productId = 'product-smart-ro-water-purifier-400g-1200g';
  if (new URLSearchParams(location.search).get('product_id') !== productId) return;
  let context;
  try { context = JSON.parse(sessionStorage.getItem('smart-ro-project-context') || 'null'); } catch (_) { return; }
  if (!context || context.product !== productId || !Number.isFinite(context.created) || Date.now() - context.created > 3600000 || context.created > Date.now()) return;
  let raw = '';
  try { raw = sessionStorage.getItem('smart-ro-project-configuration') || ''; } catch (_) { return; }
  if (!raw || raw.length > 2000) return;
  let parsed;
  try { parsed = JSON.parse(raw); } catch (_) { return; }
  const allowed = ['capacity_gpd', 'filter_stage_count', 'ro_membrane_brand', 'pump_requirement', 'optional_features', 'panel_language', 'estimated_order_quantity', 'destination_market', 'project_notes'];
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed) || Object.keys(parsed).some(key => !allowed.includes(key))) return;
  if (allowed.some(key => !(key in parsed))) return;
  if (allowed.filter(key => key !== 'optional_features').some(key => typeof parsed[key] !== 'string')) return;
  if (!Array.isArray(parsed.optional_features) || parsed.optional_features.length > 4 || parsed.optional_features.some(value => typeof value !== 'string' || value.length > 80)) return;
  const text = JSON.stringify(parsed);
  document.querySelectorAll('form.contact-form').forEach(form => {
    let field = form.querySelector('[data-smart-ro-configuration]');
    if (!field) {
      field = document.createElement('input');
      field.type = 'hidden';
      field.name = 'Product Configuration';
      field.setAttribute('data-smart-ro-configuration', '');
      form.appendChild(field);
    }
    field.value = text;
    const product = new URLSearchParams(location.search).get('product');
    const productField = form.querySelector('[data-product-field]');
    if (product && productField && !productField.value) productField.value = product.slice(0, 180);
    form.dataset.smartRoConfigurationReady = 'true';
    form.dataset.smartRoConfigurationKeys = Object.keys(parsed).sort().join(',');
    form.dataset.smartRoConfigurationLength = String(text.length);
  });
})();
