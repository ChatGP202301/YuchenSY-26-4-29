/* Yuchen Water consent-aware, no-PII measurement layer. */
(() => {
  'use strict';

  const config = window.YUCHEN_MEASUREMENT_CONFIG || {};
  const allowedEvents = new Set([
    'whatsapp_click',
    'email_click',
    'phone_click',
    'quote_form_start',
    'quote_submit_success',
    'download_center_open',
    'download_resource_select',
    'download_form_start',
    'catalog_submit_success',
    'catalog_download_complete',
    'manual_access_granted',
    'filter_selector_start',
    'filter_selector_result',
    'filter_rfq_copy',
    'filter_rfq_handoff',
    '3d_open',
    '3d_ready',
    '3d_part_select',
    '3d_explode',
    '3d_error'
  ]);
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  const consentKey = 'yuchen_analytics_consent_v1';
  const dedupePrefix = 'yuchen_event_once:';
  let gtmLoaded = false;

  window.dataLayer = window.dataLayer || [];
  // Google's command queue consumes Arguments objects, not ordinary arrays.
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied',
    analytics_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500
  });
  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', false);

  const readStorage = (key) => {
    try { return window.localStorage.getItem(key) || ''; }
    catch (error) { return ''; }
  };
  const writeStorage = (key, value) => {
    try { window.localStorage.setItem(key, value); }
    catch (error) { /* Storage can be unavailable in privacy modes. */ }
  };
  const containsPersonalData = (value) => {
    const text = String(value || '').trim();
    return text.includes('@') || /\+?\d[\d\s().-]{6,}\d/.test(text);
  };
  const safeCampaignValue = (value) => {
    const text = String(value || '').trim().slice(0, 120);
    if (!text || containsPersonalData(text)) return text ? 'redacted' : '';
    return text.replace(/[^\p{L}\p{N}._~\- ]/gu, '').trim();
  };
  const safeSlug = (value) => {
    const text = String(value || '').trim();
    if (containsPersonalData(text)) return text ? 'redacted' : '';
    return text.toLowerCase().replace(/\.html$/i, '').replace(/[^a-z0-9_-]+/g, '-')
      .replace(/^-+|-+$/g, '').slice(0, 120);
  };
  const safePathname = () => {
    const segments = location.pathname.split('/').map((segment) => {
      let decoded = segment;
      try { decoded = decodeURIComponent(segment); } catch (error) { /* Keep the encoded segment. */ }
      return containsPersonalData(decoded) ? 'redacted' : segment;
    });
    return segments.join('/') || '/';
  };
  const safePageLocation = () => `${location.origin}${safePathname()}`;
  const safeSourcePage = () => {
    const params = new URLSearchParams(location.search);
    const candidate = params.get('yw_source_page') || params.get('source_page');
    if (!candidate) return safePathname();
    try {
      const url = new URL(candidate, location.href || `${location.origin}${location.pathname}`);
      if (url.origin !== location.origin || containsPersonalData(decodeURIComponent(url.pathname))) return safePathname();
      return url.pathname.slice(0, 240);
    } catch (error) { return safePathname(); }
  };
  const safeReferrer = () => {
    try { return document.referrer ? new URL(document.referrer).origin + '/' : ''; }
    catch (error) { return ''; }
  };
  const language = () => (document.documentElement.lang || 'und').toLowerCase().slice(0, 12);
  const productSlug = () => {
    const declared = document.body && document.body.dataset.productSlug;
    if (declared) return safeSlug(declared);
    const params = new URLSearchParams(location.search);
    if (params.get('product_slug')) return safeSlug(params.get('product_slug'));
    const name = location.pathname.split('/').pop() || '';
    return /^(product-|sanyishui-)/.test(name) ? safeSlug(name) : '';
  };
  const productFamily = () => {
    const declared = document.body && document.body.dataset.productFamily;
    if (declared) return safeSlug(declared);
    const params = new URLSearchParams(location.search);
    if (params.get('product_family')) return safeSlug(params.get('product_family'));
    const path = location.pathname.toLowerCase();
    if (path.includes('gac-udf')) return 'gac-udf';
    if (path.includes('pp-melt')) return 'pp';
    if (path.includes('cto-carbon')) return 'cto';
    if (path.includes('t33')) return 't33';
    if (path.includes('ro-membrane')) return 'ro';
    if (path.includes('uf-membrane')) return 'uf';
    return '';
  };
  const productIdentity = () => {
    const declared = document.body && document.body.dataset.productId;
    if (declared) return { id: safeSlug(declared), source: 'declared-product-id' };
    const products = [];
    const visit = (node) => {
      if (Array.isArray(node)) return node.forEach(visit);
      if (!node || typeof node !== 'object') return;
      const types = Array.isArray(node['@type']) ? node['@type'] : [node['@type']];
      if (types.includes('Product')) products.push(node);
      Object.values(node).forEach(visit);
    };
    document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
      try { visit(JSON.parse(script.textContent)); } catch (error) { /* Invalid schema is not identity evidence. */ }
    });
    const current = products.find(p => {
      try { return new URL(p.url).pathname === location.pathname && new URL(p.url).hash === location.hash; }
      catch (error) { return false; }
    });
    const product = current || (products.length === 1 ? products[0] : null);
    const identifier = product && (product.sku || product.model);
    return identifier ? { id: safeSlug(identifier), source: 'visible-product-schema' }
      : { id: productSlug(), source: productSlug() ? 'page-slug-not-verified-sku' : 'none' };
  };
  const campaignParams = () => {
    const params = new URLSearchParams(location.search);
    const values = {};
    utmKeys.forEach((key) => { values[key] = safeCampaignValue(params.get(key)); });
    return values;
  };
  const commonParams = (ctaLocation = '') => ({
    page_location: safePageLocation(),
    page_path: safePathname(),
    source_page: safeSourcePage(),
    language: language(),
    product_slug: productSlug(),
    product_family: productFamily(),
    product_id: productIdentity().id,
    product_identity_source: productIdentity().source,
    cta_location: safeSlug(ctaLocation || 'unknown'),
    ...campaignParams()
  });
  const getConsent = () => readStorage(consentKey);
  const hasConsent = () => getConsent() === 'granted';
  const validContainer = () => /^GTM-[A-Z0-9]+$/i.test(String(config.gtmContainerId || ''));
  const validMeasurement = () => /^G-[A-Z0-9]+$/i.test(String(config.ga4MeasurementId || ''));
  const validTarget = () => validContainer() || validMeasurement();
  const directGa4 = () => !validContainer() && validMeasurement();

  function captureFirstTouch() {
    if (!hasConsent()) return;
    try {
      const key = 'yuchen_first_touch_v1';
      const previous = JSON.parse(window.sessionStorage.getItem(key) || '{}');
      if (previous.landingPage) return;
      const campaign = campaignParams();
      window.sessionStorage.setItem(key, JSON.stringify({
        landingPage: safePathname(), referrerDomain: safeReferrer() ? new URL(safeReferrer()).hostname : '',
        utmSource: campaign.utm_source, utmMedium: campaign.utm_medium, utmCampaign: campaign.utm_campaign,
        utmTerm: campaign.utm_term, utmContent: campaign.utm_content
      }));
    } catch (error) { /* Consent-aware measurement must work without storage. */ }
  }

  function loadGtm() {
    if (gtmLoaded || !config.enabled || !validTarget()) return;
    gtmLoaded = true;
    captureFirstTouch();
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    window.dataLayer.push({
      event: 'yuchen_page_view',
      ...commonParams('page_view'),
      measurement_version: '2026-10-02'
    });
    const script = document.createElement('script');
    script.async = true;
    if (directGa4()) {
      const campaign = campaignParams();
      // Never send the browser's raw query string, referrer, or contact form data.
      gtag('set', { page_location: safePageLocation(), page_referrer: safeReferrer() });
      gtag('js', new Date());
      gtag('config', config.ga4MeasurementId, {
        send_page_view: false, page_location: safePageLocation(), page_referrer: safeReferrer(),
        campaign_source: campaign.utm_source, campaign_medium: campaign.utm_medium,
        campaign_name: campaign.utm_campaign, campaign_term: campaign.utm_term, campaign_content: campaign.utm_content,
        allow_google_signals: false, allow_ad_personalization_signals: false
      });
      gtag('event', 'page_view', { ...commonParams('page_view'), page_referrer: safeReferrer(),
        send_to: config.ga4MeasurementId });
      const identity = productIdentity();
      if (identity.id && identity.source !== 'page-slug-not-verified-sku' && identity.source !== 'none') {
        gtag('event', 'view_item', { ...commonParams('product_view'),
          items: [{ item_id: identity.id, item_category: productFamily() }], send_to: config.ga4MeasurementId });
      }
      script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(config.ga4MeasurementId)}`;
    } else {
      script.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(config.gtmContainerId)}`;
    }
    script.referrerPolicy = 'strict-origin-when-cross-origin';
    document.head.appendChild(script);
  }

  function updateConsent(value) {
    const granted = value === 'granted';
    if (validMeasurement()) window[`ga-disable-${config.ga4MeasurementId}`] = !granted;
    writeStorage(consentKey, granted ? 'granted' : 'denied');
    gtag('consent', 'update', {
      analytics_storage: granted ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    if (granted) loadGtm();
    document.querySelector('[data-yuchen-consent-banner]')?.remove();
  }

  function showConsentBanner(force = false) {
    if (!config.enabled || !validTarget() || config.showConsentBanner === false || (!force && getConsent())) return;
    if (document.querySelector('[data-yuchen-consent-banner]')) return;
    const banner = document.createElement('section');
    banner.className = 'yuchen-consent-banner';
    banner.dataset.yuchenConsentBanner = 'true';
    banner.setAttribute('aria-label', 'Analytics privacy choice');
    banner.innerHTML = '<p>We use optional analytics to understand which pages lead to business inquiries. Analytics stays off until you accept; form details are never sent to analytics.</p><div><button type="button" class="btn btn-gold" data-consent-accept>Accept analytics</button><button type="button" class="btn btn-secondary" data-consent-reject>Decline</button><a data-consent-policy>Privacy policy</a></div>';
    const policy = banner.querySelector('[data-consent-policy]');
    policy.href = config.privacyPolicyPath || '/en/privacy-policy.html';
    banner.querySelector('[data-consent-accept]').addEventListener('click', () => updateConsent('granted'));
    banner.querySelector('[data-consent-reject]').addEventListener('click', () => updateConsent('denied'));
    document.body.appendChild(banner);
  }

  function onceKey(eventName, uniqueId) {
    if (!uniqueId) return false;
    const key = `${dedupePrefix}${eventName}:${safeSlug(uniqueId)}`;
    try {
      if (window.sessionStorage.getItem(key)) return true;
      window.sessionStorage.setItem(key, '1');
    } catch (error) { /* In-memory dedupe is handled by the caller event flow. */ }
    return false;
  }

  function emit(eventName, detail = {}) {
    if (!allowedEvents.has(eventName)) return;
    if (directGa4()) {
      if (!config.enabled || !validMeasurement() || !hasConsent()) return;
    } else {
      if (!config.enabled || !validContainer() || !hasConsent()) return;
    }
    const uniqueId = String(detail.submissionId || detail.downloadId || '');
    if (uniqueId && onceKey(eventName, uniqueId)) return;
    window.dataLayer.push({
      event: eventName,
      ...commonParams(detail.ctaLocation || ''),
      ...(eventName === 'quote_submit_success' ? { lead_type: 'quote' } : {}),
      ...(eventName === 'catalog_submit_success' ? { lead_type: 'catalog' } : {}),
      ...(eventName === 'manual_access_granted' ? { lead_type: 'manual' } : {}),
      ...(/^download_|^catalog_|^manual_/.test(eventName) ? { resource_id: safeSlug(detail.resourceId || '') } : {}),
      ...(/^filter_/.test(eventName) ? {
        selector_id: safeSlug(detail.selectorId || ''),
        result_bucket: safeSlug(detail.resultBucket || ''),
        result_count_bucket: safeSlug(detail.resultCountBucket || ''),
        selected_count: Math.max(0, Math.min(3, Number.parseInt(detail.selectedCount, 10) || 0))
      } : {}),
      ...(/^3d_/.test(eventName) ? {
        model_id: safeSlug(detail.modelId || ''),
        part_id: safeSlug(detail.partId || ''),
        interaction_state: safeSlug(detail.state || detail.errorBucket || '')
      } : {}),
      measurement_version: '2026-10-02'
    });
    if (directGa4()) {
      const payload = { ...window.dataLayer[window.dataLayer.length - 1] };
      delete payload.event;
      const ga4Name = /^(quote_submit_success|catalog_submit_success)$/.test(eventName) ? 'generate_lead' : eventName;
      gtag('event', ga4Name, { ...payload, page_referrer: safeReferrer(), send_to: config.ga4MeasurementId });
    }
  }

  function ctaLocation(element) {
    return element.closest('[data-cta-location]')?.dataset.ctaLocation
      || element.dataset.ctaLocation
      || (element.classList.contains('whatsapp-float') ? 'floating_whatsapp' : '')
      || (element.closest('.header') ? 'header' : '')
      || (element.closest('.product-actions') ? 'product_actions' : '')
      || 'page_link';
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    if (/wa\.me\/|api\.whatsapp\.com\//i.test(href)) {
      emit('whatsapp_click', { ctaLocation: ctaLocation(link) });
    } else if (/^mailto:/i.test(href)) {
      emit('email_click', { ctaLocation: ctaLocation(link) });
    } else if (/^tel:/i.test(href)) {
      emit('phone_click', { ctaLocation: ctaLocation(link) });
    }
  }, true);

  document.addEventListener('input', (event) => {
    const form = event.target.closest('form.contact-form');
    if (!form || form.dataset.measurementStarted === 'true') return;
    form.dataset.measurementStarted = 'true';
    emit('quote_form_start', { ctaLocation: form.dataset.ctaLocation || 'quote_form' });
  }, true);

  document.addEventListener('yuchen:quote-submit-success', (event) => {
    emit('quote_submit_success', event.detail || {});
  });
  document.addEventListener('yuchen:download-center-open', (event) => {
    emit('download_center_open', event.detail || {});
  });
  document.addEventListener('yuchen:download-resource-select', (event) => {
    emit('download_resource_select', event.detail || {});
  });
  document.addEventListener('yuchen:download-form-start', (event) => {
    emit('download_form_start', event.detail || {});
  });
  document.addEventListener('yuchen:catalog-submit-success', (event) => {
    emit('catalog_submit_success', event.detail || {});
  });
  document.addEventListener('yuchen:catalog-download-complete', (event) => {
    emit('catalog_download_complete', event.detail || {});
  });
  document.addEventListener('yuchen:manual-access-granted', (event) => {
    emit('manual_access_granted', event.detail || {});
  });
  document.addEventListener('yuchen:filter-selector-start', (event) => {
    emit('filter_selector_start', event.detail || {});
  });
  document.addEventListener('yuchen:filter-selector-result', (event) => {
    emit('filter_selector_result', event.detail || {});
  });
  document.addEventListener('yuchen:filter-rfq-copy', (event) => {
    emit('filter_rfq_copy', event.detail || {});
  });
  document.addEventListener('yuchen:filter-rfq-handoff', (event) => {
    emit('filter_rfq_handoff', event.detail || {});
  });
  ['3d-open', '3d-ready', '3d-part-select', '3d-explode', '3d-error'].forEach((domName) => {
    document.addEventListener(`yuchen:${domName}`, (event) => {
      emit(domName.replaceAll('-', '_'), event.detail || {});
    });
  });

  if (hasConsent()) {
    if (validMeasurement()) window[`ga-disable-${config.ga4MeasurementId}`] = false;
    gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    loadGtm();
  } else if (getConsent() === 'denied' && config.loadWithDeniedConsent) {
    loadGtm();
  }
  function consentControls() {
    if (config.enabled && validTarget() && config.showConsentBanner !== false && !document.querySelector('[data-yuchen-consent-settings]')) {
      const control = document.createElement('button');
      control.type = 'button'; control.className = 'btn btn-secondary';
      control.dataset.yuchenConsentSettings = 'true'; control.textContent = 'Analytics privacy settings';
      control.addEventListener('click', () => showConsentBanner(true));
      (document.querySelector('footer') || document.body).appendChild(control);
    }
    showConsentBanner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', consentControls, { once: true });
  else consentControls();

  window.YuchenMeasurement = Object.freeze({ emit, updateConsent, commonParams });
})();
