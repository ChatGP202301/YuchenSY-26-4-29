(() => {
  const form = document.querySelector('[data-evidence-form]');
  if (!form) return;
  const config = window.YUCHEN_EVIDENCE_CONFIG || {};
  const copy = window.YUCHEN_EVIDENCE_I18N || {};
  const status = form.querySelector('[data-evidence-status]');
  const submit = form.querySelector('button[type="submit"]');
  const dialog = document.querySelector('[data-evidence-dialog]');
  const dialogImage = dialog?.querySelector('img');
  const dialogTitle = dialog?.querySelector('[data-dialog-title]');
  let widgetId = null;

  form.elements.formStartedAt.value = String(Date.now());

  function setStatus(message, state = '') {
    status.textContent = message;
    status.dataset.state = state;
    status.setAttribute('role', state === 'error' ? 'alert' : 'status');
  }

  document.querySelectorAll('[data-view-evidence]').forEach((button) => {
    button.addEventListener('click', () => {
      if (!dialog || !dialogImage) return;
      dialogImage.src = button.dataset.image;
      dialogImage.alt = button.dataset.title;
      dialogImage.hidden = false;
      dialogTitle.textContent = button.dataset.title;
      dialog.showModal();
    });
  });
  dialog?.querySelector('[data-dialog-close]')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });

  document.querySelectorAll('[data-request-evidence]').forEach((button) => {
    button.addEventListener('click', () => {
      const checkbox = form.querySelector(`input[name="evidenceTopics"][value="${CSS.escape(button.dataset.requestEvidence)}"]`);
      if (checkbox) checkbox.checked = true;
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
      form.elements.name.focus({ preventScroll: true });
    });
  });

  const configured = config.apiBase && config.turnstileSiteKey && !String(config.turnstileSiteKey).startsWith('REPLACE_');
  if (!configured) {
    submit.disabled = true;
    setStatus(copy.setup || 'The protected document request service is being configured. Please contact expresswater025@gmail.com in the meantime.', 'setup');
  } else {
    const renderTurnstile = () => {
      if (window.turnstile && widgetId === null) {
        widgetId = window.turnstile.render(form.querySelector('[data-turnstile]'), { sitekey: config.turnstileSiteKey });
      }
    };
    if (window.turnstile) renderTurnstile();
    else window.addEventListener('load', renderTurnstile, { once: true });
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!configured) return;
    submit.disabled = true;
    setStatus(copy.checking || 'Checking your application…', 'progress');
    try {
      const data = new FormData(form);
      const payload = {
        submissionId: crypto.randomUUID(), locale: form.dataset.locale || document.documentElement.lang || 'en', sourcePage: location.href,
        name: data.get('name'), company: data.get('company'), email: data.get('email'), whatsapp: data.get('whatsapp'),
        country: data.get('country'), role: data.get('role'), buyerType: data.get('buyerType'),
        companyWebsite: data.get('companyWebsite'), businessProfile: data.get('businessProfile'),
        evidenceTopics: data.getAll('evidenceTopics'), products: data.get('products'),
        estimatedQuantity: data.get('estimatedQuantity'), targetMarket: data.get('targetMarket'),
        requestPurpose: data.get('requestPurpose'), consent: data.get('consent') === 'yes',
        nonRedistribution: data.get('nonRedistribution') === 'yes', website: data.get('website'),
        formStartedAt: Number(data.get('formStartedAt')),
        turnstileToken: widgetId === null ? '' : window.turnstile.getResponse(widgetId)
      };
      const response = await fetch(`${config.apiBase}/v1/evidence/request`, {
        method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload)
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.code || 'request_failed');
      const success = copy.success || 'Check your email for the verification link. No document is released until manual review.';
      setStatus(`${success}${result.submissionId ? ` (${result.submissionId})` : ''}`, 'success');
      form.reset();
      form.elements.formStartedAt.value = String(Date.now());
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } catch (error) {
      const messages = {
        missing_fields: copy.missing || 'Complete every required field and select at least one test topic.',
        invalid_email: copy.email || 'Enter a valid email address.', invalid_whatsapp: copy.whatsapp || 'Enter a plausible international WhatsApp number with country code.',
        invalid_company_website: copy.error,
        submitted_too_fast: copy.error || 'Please review the form before submitting.', turnstile_failed: copy.turnstile || 'Complete the anti-spam verification.',
        rate_limited: copy.error, duplicate_submission_id: copy.error
      };
      setStatus(messages[error.message] || copy.error || 'The request could not be recorded. Your entries remain in the form; please try again.', 'error');
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } finally {
      submit.disabled = false;
    }
  });
})();
