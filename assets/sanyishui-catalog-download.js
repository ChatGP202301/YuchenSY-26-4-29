(() => {
  const form = document.querySelector('[data-sanyishui-catalog-form]');
  if (!form) return;

  const config = window.YUCHEN_SANYISHUI_CATALOG_CONFIG || {};
  const status = form.querySelector('[data-form-status]');
  const button = form.querySelector('button[type="submit"]');
  const interestError = form.querySelector('[data-interest-error]');
  const turnstileMount = form.querySelector('[data-turnstile]');
  let widgetId = null;
  let submissionId = crypto.randomUUID();
  const catalogId = form.dataset.catalogId || 'yuchen-oem-2026-en';
  const locale = catalogId.split('-').pop() || 'en';

  const consent = form.querySelector('.catalog-consent');
  if (consent && !form.querySelector('[data-catalog-data-notice]')) {
    const privacyLink = consent.querySelector('a[href$="privacy-policy.html"]');
    if (privacyLink && new Set(['be', 'cnr', 'ga', 'lb', 'mk', 'mt']).has(locale)) privacyLink.href = '/en/privacy-policy.html';
    const notice = document.createElement('p');
    notice.dataset.catalogDataNotice = '';
    notice.className = 'catalog-form-status';
    notice.textContent = 'Your submitted business contact and project information is stored privately without automatic expiry and emailed to Yuchen Water sales. You may request correction or deletion at expresswater025@gmail.com.';
    consent.insertAdjacentElement('afterend', notice);
  }

  const copy = {
    setup: 'Secure catalog access is awaiting Cloudflare configuration. Please contact Yuchen Water for the current PDF.',
    checking: 'Checking your information…',
    preparing: 'Preparing your private catalog download…',
    done: 'Your Yuchen Water OEM catalog download has started.',
    network: 'We could not complete the request. Your entries have been kept; please try again.',
    interests: 'Select at least one product family.',
    whatsapp: 'Enter a plausible international WhatsApp number with + and country code.',
    turnstile: 'Please complete the anti-spam verification.',
    rate_limited: 'Too many recent requests. Please try again later.',
    invalid_submission: 'Check every required field and try again.',
    email_failed: 'Your request could not be delivered to our sales team. Please try again.',
    catalog_unavailable: 'The catalog is temporarily unavailable. Please try again later.'
  };

  const setStatus = (message, state = '') => {
    status.textContent = message;
    status.dataset.state = state;
    status.setAttribute('role', state === 'error' ? 'alert' : 'status');
  };

  const resetStartedAt = () => {
    form.elements.formStartedAt.value = String(Date.now());
  };

  const selectedInterests = () => Array.from(form.querySelectorAll('input[name="interests"]:checked'), input => input.value);

  const interestsAreValid = () => {
    const valid = selectedInterests().length > 0;
    if (interestError) interestError.hidden = valid;
    return valid;
  };

  const plausibleWhatsApp = value => /^\+[0-9][0-9\s().-]{6,24}$/.test(value.trim()) && value.replace(/\D/g, '').length <= 15;
  const firstTouch = () => {
    try { return JSON.parse(sessionStorage.getItem('yuchen_first_touch_v1') || '{}'); }
    catch (error) { return {}; }
  };

  const renderTurnstile = () => {
    if (!window.turnstile || widgetId !== null || !turnstileMount) return false;
    widgetId = window.turnstile.render(turnstileMount, {
      sitekey: config.turnstileSiteKey,
      action: 'oem_catalog_download'
    });
    return true;
  };

  resetStartedAt();
  form.addEventListener('change', event => {
    if (event.target && event.target.name === 'interests') interestsAreValid();
  });

  const configured = Boolean(
    config.apiBase &&
    config.turnstileSiteKey &&
    !String(config.turnstileSiteKey).startsWith('REPLACE_')
  );

  if (!configured) {
    button.disabled = true;
    setStatus(copy.setup, 'setup');
  } else if (!renderTurnstile()) {
    const poll = window.setInterval(() => {
      if (renderTurnstile()) window.clearInterval(poll);
    }, 250);
    window.setTimeout(() => window.clearInterval(poll), 10000);
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!configured) return setStatus(copy.setup, 'error');
    const validInterests = interestsAreValid();
    if (!form.checkValidity() || !validInterests) {
      form.reportValidity();
      if (!validInterests) interestError.scrollIntoView({ block: 'center' });
      return setStatus(copy.invalid_submission, 'error');
    }
    if (!plausibleWhatsApp(form.elements.whatsapp.value)) {
      form.elements.whatsapp.setCustomValidity(copy.whatsapp);
      form.elements.whatsapp.reportValidity();
      form.elements.whatsapp.setCustomValidity('');
      return setStatus(copy.whatsapp, 'error');
    }
    const widgetToken = widgetId === null || !window.turnstile ? '' : window.turnstile.getResponse(widgetId);
    const turnstileToken = widgetToken || form.querySelector('input[name="cf-turnstile-response"]')?.value || '';
    if (!turnstileToken) return setStatus(copy.turnstile, 'error');

    button.disabled = true;
    setStatus(copy.checking, 'progress');
    const data = new FormData(form);
    const query = new URLSearchParams(location.search);
    const attribution = firstTouch();
    const payload = {
      submissionId,
      catalogId,
      locale,
      name: data.get('name'),
      jobTitle: data.get('jobTitle'),
      company: data.get('company'),
      companyWebsite: data.get('companyWebsite'),
      email: data.get('email'),
      whatsapp: data.get('whatsapp'),
      country: data.get('country'),
      buyerType: data.get('buyerType'),
      productCategory: data.get('productCategory'),
      specificProduct: data.get('specificProduct'),
      interests: selectedInterests(),
      estimatedQuantity: data.get('estimatedQuantity'),
      purchaseTimeline: data.get('purchaseTimeline'),
      application: data.get('application'),
      rawWaterTds: data.get('rawWaterTds'),
      voltageFrequency: data.get('voltageFrequency'),
      message: data.get('message'),
      consent: data.get('consent') === 'yes',
      website: data.get('website'),
      formStartedAt: Number(data.get('formStartedAt')),
      turnstileToken,
      sourcePage: location.origin + location.pathname,
      firstLandingPage: attribution.landingPage || location.pathname,
      referrerDomain: attribution.referrerDomain || '',
      utmSource: query.get('utm_source') || attribution.utmSource || '',
      utmMedium: query.get('utm_medium') || attribution.utmMedium || '',
      utmCampaign: query.get('utm_campaign') || attribution.utmCampaign || '',
      utmTerm: query.get('utm_term') || attribution.utmTerm || '',
      utmContent: query.get('utm_content') || attribution.utmContent || ''
    };

    try {
      const response = await fetch(`${config.apiBase}/v1/catalog/oem-products/download`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', accept: 'application/pdf' },
        body: JSON.stringify(payload),
        cache: 'no-store'
      });
      if (!response.ok) {
        const problem = await response.json().catch(() => ({}));
        throw new Error(problem.code || 'network');
      }
      document.dispatchEvent(new CustomEvent('yuchen:catalog-submit-success', {
        detail: { submissionId, ctaLocation: 'sanyishui_catalog_form' }
      }));
      setStatus(copy.preparing, 'progress');
      const receipt = response.headers.get('x-catalog-receipt') || '';
      const blob = await response.blob();
      if (!blob.size || !receipt || !String(response.headers.get('content-type')).includes('application/pdf')) throw new Error('catalog_unavailable');
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = form.dataset.downloadFilename || 'Yuchen_Water_OEM_Product_Catalog_2026.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
      fetch(`${config.apiBase}/v1/catalog/download-events`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ submissionId, catalogId: payload.catalogId, receipt }),
        cache: 'no-store',
        keepalive: true
      }).catch(() => {});
      document.dispatchEvent(new CustomEvent('yuchen:catalog-download-complete', {
        detail: { submissionId, ctaLocation: 'sanyishui_catalog_form' }
      }));
      setStatus(copy.done, 'success');
      form.reset();
      submissionId = crypto.randomUUID();
      resetStartedAt();
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } catch (error) {
      setStatus(copy[error.message] || copy.network, 'error');
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } finally {
      button.disabled = false;
    }
  });
})();
