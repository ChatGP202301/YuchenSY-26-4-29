/* Yuchen Water consent-aware, no-PII measurement layer. */
(() => {
  'use strict';

  const config = window.YUCHEN_MEASUREMENT_CONFIG || {};
  const allowedEvents = new Set([
    'whatsapp_click',
    'quote_form_start',
    'quote_submit_success',
    'catalog_submit_success',
    'catalog_download_complete'
  ]);
  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  const consentKey = 'yuchen_analytics_consent_v1';
  const dedupePrefix = 'yuchen_event_once:';
  let gtmLoaded = false;

  window.dataLayer = window.dataLayer || [];
  const gtag = (...args) => window.dataLayer.push(args);
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
  const safeCampaignValue = (value) => {
    const text = String(value || '').trim().slice(0, 120);
    if (!text || text.includes('@') || /\+?\d[\d\s().-]{6,}\d/.test(text)) return text ? 'redacted' : '';
    return text.replace(/[^\p{L}\p{N}._~\- ]/gu, '').trim();
  };
  const safeSlug = (value) => String(value || '').trim().toLowerCase()
    .replace(/\.html$/i, '').replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 120);
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
  const campaignParams = () => {
    const params = new URLSearchParams(location.search);
    const values = {};
    utmKeys.forEach((key) => { values[key] = safeCampaignValue(params.get(key)); });
    return values;
  };
  const commonParams = (ctaLocation = '') => ({
    page_path: location.pathname,
    language: language(),
    product_slug: productSlug(),
    product_family: productFamily(),
    cta_location: safeSlug(ctaLocation || 'unknown'),
    ...campaignParams()
  });
  const getConsent = () => readStorage(consentKey);
  const hasConsent = () => getConsent() === 'granted';
  const validContainer = () => /^GTM-[A-Z0-9]+$/i.test(String(config.gtmContainerId || ''));

  function loadGtm() {
    if (gtmLoaded || !config.enabled || !validContainer()) return;
    gtmLoaded = true;
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(config.gtmContainerId)}`;
    script.referrerPolicy = 'strict-origin-when-cross-origin';
    document.head.appendChild(script);
  }

  function updateConsent(value) {
    const granted = value === 'granted';
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

  function showConsentBanner() {
    if (!config.enabled || !validContainer() || config.showConsentBanner === false || getConsent()) return;
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
    if (!allowedEvents.has(eventName) || !config.enabled || !validContainer() || !hasConsent()) return;
    const uniqueId = String(detail.submissionId || detail.downloadId || '');
    if (uniqueId && onceKey(eventName, uniqueId)) return;
    window.dataLayer.push({
      event: eventName,
      ...commonParams(detail.ctaLocation || ''),
      measurement_version: '2026-07-27'
    });
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
  document.addEventListener('yuchen:catalog-submit-success', (event) => {
    emit('catalog_submit_success', event.detail || {});
  });
  document.addEventListener('yuchen:catalog-download-complete', (event) => {
    emit('catalog_download_complete', event.detail || {});
  });

  if (hasConsent()) {
    gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    loadGtm();
  } else if (getConsent() === 'denied' && config.loadWithDeniedConsent) {
    loadGtm();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showConsentBanner, { once: true });
  else showConsentBanner();

  window.YuchenMeasurement = Object.freeze({ emit, updateConsent, commonParams });
})();
