/* Yuchen Water Interactive JS */

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    if (!menu) return;
    const overlay = ensureLangMenuOverlay();
    const isOpen = menu.classList.toggle('open');
    overlay.classList.toggle('open', isOpen);
    document.body.classList.toggle('lang-menu-open', isOpen);
}

function changeLanguage(select) {
    if (select && select.value) {
        window.location.href = select.value;
    }
}

function ensureLangMenuOverlay() {
    let overlay = document.querySelector('.lang-menu-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'lang-menu-overlay';
        overlay.setAttribute('aria-hidden', 'true');
        overlay.addEventListener('click', closeLangMenu);
        document.body.appendChild(overlay);
    }
    return overlay;
}

function closeLangMenu() {
    const menu = document.getElementById('langMenu');
    const overlay = document.querySelector('.lang-menu-overlay');
    if (menu) menu.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.classList.remove('lang-menu-open');
}

// Close menus when clicking outside
document.addEventListener('click', function(e) {
    const langSwitcher = document.querySelector('.lang-switcher');
    const langMenu = document.getElementById('langMenu');
    if (langSwitcher && langMenu && !langSwitcher.contains(e.target)) {
        closeLangMenu();
    }
});

// FAQ Accordion
document.querySelectorAll('.faq-q').forEach(button => {
    button.addEventListener('click', () => {
        const item = button.parentElement;
        item.classList.toggle('open');
    });
});

// Category Filter (for products.html)
let filterFrame = 0;
let productCardsCache;

function filterCat(cat, btn) {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    if (filterFrame) cancelAnimationFrame(filterFrame);
    filterFrame = requestAnimationFrame(() => {
        productCardsCache = productCardsCache || Array.from(document.querySelectorAll('.product-card'));
        productCardsCache.forEach(card => {
            const cardCat = card.getAttribute('data-cat');
            const badge = card.querySelector('.product-cat-badge');
            const badgeText = badge ? badge.textContent.trim() : '';
            card.hidden = !(cat === 'all' || cardCat === cat || badgeText === cat);
        });
        filterFrame = 0;
    });
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const langMenu = document.getElementById('langMenu');
        const nav = document.querySelector('.nav');
        if (langMenu) closeLangMenu();
        if (nav) nav.classList.remove('open');
    }
});

const inquirySuccessHtml = 'Your request was accepted by the form service. Please keep the submission ID shown below. Yuchen Water will verify delivery before treating it as a received lead.';
const inquiryErrorText = 'The form could not be sent right now. Please email expresswater025@gmail.com or contact WhatsApp +86-19908311885.';

function prepareInquiryForm(form) {
    if (!form) return;
    if (form.dataset.prepared !== 'true') {
        form.dataset.prepared = 'true';
        form.dataset.readyAt = String(Date.now());
    }
    form.querySelectorAll('[data-current-page]').forEach(input => {
        input.value = window.location.href;
    });
    form.querySelectorAll('[data-form-loaded-at]').forEach(input => {
        input.value = new Date().toISOString();
    });
    form.querySelectorAll('[data-submitted-language]').forEach(input => {
        input.value = document.documentElement.lang || '';
    });
    form.querySelectorAll('[data-submission-id]').forEach(input => {
        if (!input.value) {
            const randomPart = window.crypto && window.crypto.randomUUID ? window.crypto.randomUUID().replace(/-/g, '').slice(0, 20) : Math.random().toString(36).slice(2) + Date.now().toString(36);
            input.value = 'YC-' + (document.documentElement.lang || 'xx').toUpperCase() + '-' + randomPart.toUpperCase();
        }
    });
}

document.querySelectorAll('form.contact-form').forEach(prepareInquiryForm);

const pendingAppScriptForms = new Map();

function submitToAppScript(form, endpoint, submitButton) {
    const submissionId = form.querySelector('[data-submission-id]')?.value || '';
    const turnstile = form.querySelector('[name="cf-turnstile-response"]');
    if (!submissionId || !turnstile || !turnstile.value) throw new Error('Please complete the anti-spam verification.');
    const frameName = 'yuchen-form-frame-' + submissionId.replace(/[^A-Za-z0-9-]/g, '');
    let frame = document.querySelector(`iframe[name="${frameName}"]`);
    if (!frame) {
        frame = document.createElement('iframe');
        frame.name = frameName;
        frame.hidden = true;
        frame.setAttribute('aria-hidden', 'true');
        document.body.appendChild(frame);
    }
    form.action = endpoint;
    form.method = 'POST';
    form.target = frameName;
    const timeout = window.setTimeout(() => {
        const pending = pendingAppScriptForms.get(submissionId);
        if (!pending) return;
        pendingAppScriptForms.delete(submissionId);
        if (pending.button) pending.button.disabled = false;
        if (pending.error) {
            pending.error.textContent = 'The delivery service did not confirm receipt. Your form was not cleared. Please try again or use WhatsApp.';
            pending.error.hidden = false;
        }
    }, 30000);
    pendingAppScriptForms.set(submissionId, { form, button: submitButton, error: form.querySelector('.form-error'), success: form.querySelector('.form-success'), timeout });
    HTMLFormElement.prototype.submit.call(form);
}

window.addEventListener('message', function(event) {
    let messageHost = '';
    try { messageHost = new URL(event.origin).hostname; } catch (error) { return; }
    if (!/(^|\.)googleusercontent\.com$|(^|\.)google\.com$/.test(messageHost)) return;
    const data = event.data;
    if (!data || data.source !== 'yuchen-form' || !data.payload || !data.payload.id) return;
    const pending = pendingAppScriptForms.get(data.payload.id);
    if (!pending) return;
    window.clearTimeout(pending.timeout);
    pendingAppScriptForms.delete(data.payload.id);
    if (pending.button) pending.button.disabled = false;
    if (data.payload.emailSent === true && data.payload.status === 'EMAIL_SENT') {
        const localized = pending.form.dataset.successMessage || (pending.success ? pending.success.textContent.trim() : '');
        if (pending.success) {
            pending.success.textContent = (localized || 'Your inquiry was recorded and the email notification was sent.') + ' ' + data.payload.id;
            pending.success.hidden = false;
            pending.success.setAttribute('role', 'status');
        }
        pending.form.reset();
        pending.form.dataset.prepared = 'false';
        prepareInquiryForm(pending.form);
        if (window.turnstile) window.turnstile.reset();
    } else if (pending.error) {
        pending.error.textContent = data.payload.recorded ? 'Your inquiry was safely recorded, but the email notification is pending retry. Submission ID: ' + data.payload.id : 'The server rejected this inquiry: ' + (data.payload.status || 'UNKNOWN');
        pending.error.hidden = false;
        pending.error.setAttribute('role', 'alert');
    }
});

document.addEventListener('submit', async function(e) {
    const form = e.target;
    if (!form || !form.classList || !form.classList.contains('contact-form')) return;

    prepareInquiryForm(form);

    const appScriptEndpoint = form.dataset.appsScriptEndpoint;
    const endpoint = form.dataset.endpoint;
    if (appScriptEndpoint) {
        e.preventDefault();
        const submitButton = form.querySelector('[type="submit"]');
        if (!form.checkValidity()) { form.reportValidity(); return; }
        form.querySelectorAll('[data-submitted-at]').forEach(input => { input.value = new Date().toISOString(); });
        if (submitButton) submitButton.disabled = true;
        try { submitToAppScript(form, appScriptEndpoint, submitButton); }
        catch (error) {
            if (submitButton) submitButton.disabled = false;
            const formError = form.querySelector('.form-error');
            if (formError) { formError.textContent = error.message; formError.hidden = false; }
        }
        return;
    }
    if (!endpoint || !window.fetch) return;

    e.preventDefault();

    const success = form.querySelector('.form-success');
    const error = form.querySelector('.form-error');
    const submitButton = form.querySelector('[type="submit"]');
    const honeypot = form.querySelector('input[name="_honey"]');
    const readyAt = Number(form.dataset.readyAt || Date.now());
    const message = form.querySelector('textarea[name="message"]');
    const urlCount = message && message.value ? (message.value.match(/https?:\/\/|www\./gi) || []).length : 0;

    if (success) success.hidden = true;
    if (error) error.hidden = true;

    if (honeypot && honeypot.value.trim()) return;

    if (Date.now() - readyAt < Number(form.dataset.minSubmitMs || 2500)) {
        if (error) {
            error.textContent = 'Please review your inquiry before sending.';
            error.hidden = false;
        }
        return;
    }

    if (urlCount > 3) {
        if (error) {
            error.textContent = 'Please remove extra links from the message and send again.';
            error.hidden = false;
        }
        return;
    }

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    form.querySelectorAll('[data-form-loaded-at]').forEach(input => {
        if (!input.value) input.value = new Date(readyAt).toISOString();
    });
    form.querySelectorAll('[data-submitted-at]').forEach(input => {
        input.value = new Date().toISOString();
    });

    if (submitButton) submitButton.disabled = true;

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'Accept': 'application/json' }
        });

        let payload;
        try { payload = await response.json(); }
        catch (parseError) { throw new Error('Form endpoint returned an invalid response.'); }
        const accepted = payload && (payload.success === true || payload.success === 'true');
        if (!response.ok || !accepted) throw new Error(payload && payload.message ? payload.message : 'Form endpoint rejected the inquiry.');

        if (success) {
            const submissionId = form.querySelector('[data-submission-id]')?.value || '';
            success.innerHTML = inquirySuccessHtml + (submissionId ? '<br><strong>' + submissionId.replace(/[<>&"']/g, '') + '</strong>' : '');
            success.hidden = false;
            success.setAttribute('role', 'status');
            success.setAttribute('tabindex', '-1');
            success.focus({ preventScroll: true });
        }
        form.reset();
        form.dataset.prepared = 'false';
        prepareInquiryForm(form);
    } catch (err) {
        if (error) {
            error.textContent = inquiryErrorText;
            error.hidden = false;
            error.setAttribute('role', 'alert');
        }
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
});

// Strengthen contact-form validation without changing localized page copy.
(function(){
  function setHiddenValue(form, selector, value){
    form.querySelectorAll(selector).forEach(function(input){ input.value = value; });
  }
  function compactToken(value){
    try { return btoa(unescape(encodeURIComponent(value))).replace(/=+$/,''); }
    catch (err) { return String(Date.now()); }
  }
  function prepareProtectedForm(form){
    if (!form || form.dataset.antiSpamReady === 'true') return;
    form.dataset.antiSpamReady = 'true';
    form.dataset.lastSubmitAt = '0';
    var seed = [Date.now(), window.location.hostname, document.documentElement.lang || ''].join('|');
    setHiddenValue(form, '[data-form-token]', compactToken(seed));
    setHiddenValue(form, '[data-form-source-check]', window.location.hostname || 'local-preview');
  }
  function getWhatsAppFields(form){
    return Array.prototype.slice.call(form.querySelectorAll('[data-whatsapp-field], input[name="whatsapp"], input[name="WhatsApp"]'));
  }
  function normalizeWhatsApp(value){
    var compact = String(value || '').trim().replace(/[\s().-]/g, '');
    if (compact.indexOf('00') === 0) compact = '+' + compact.slice(2);
    var digits = compact.replace(/^\+/, '');
    return { compact: compact, digits: digits, normalized: compact.charAt(0) === '+' ? compact : '+' + digits };
  }
  function looksLikeFakeNumber(digits){
    if (!digits) return true;
    if (/^(\d)\1+$/.test(digits)) return true;
    if ('01234567890123456789'.indexOf(digits) !== -1) return true;
    if ('98765432109876543210'.indexOf(digits) !== -1) return true;
    return false;
  }
  function validateWhatsAppFields(form){
    var fields = getWhatsAppFields(form);
    var valid = true;
    var firstInvalid = null;
    fields.forEach(function(field){
      var value = field.value || '';
      if (!value.trim()) {
        field.setCustomValidity('');
        return;
      }
      var info = normalizeWhatsApp(value);
      var ok = /^\+[1-9]\d{7,14}$/.test(info.compact) && !looksLikeFakeNumber(info.digits);
      field.setCustomValidity(ok ? '' : (field.getAttribute('title') || '+86 19908311885 / +971 50 123 4567'));
      if (ok) {
        field.value = info.normalized;
        setHiddenValue(form, '[data-whatsapp-normalized]', info.normalized);
      } else {
        valid = false;
        if (!firstInvalid) firstInvalid = field;
      }
    });
    if (!valid && firstInvalid) firstInvalid.reportValidity();
    return valid;
  }
  document.querySelectorAll('form.contact-form').forEach(prepareProtectedForm);
  document.addEventListener('submit', function(event){
    var form = event.target;
    if (!form || !form.classList || !form.classList.contains('contact-form')) return;
    prepareProtectedForm(form);
    var trap = form.querySelector('[data-spam-trap], input[name="_honey"]');
    if (trap && trap.value.trim()) {
      event.preventDefault();
      event.stopImmediatePropagation();
      return false;
    }
    var now = Date.now();
    var last = Number(form.dataset.lastSubmitAt || 0);
    var repeatDelay = Number(form.dataset.repeatSubmitMs || 8000);
    if (last && now - last < repeatDelay) {
      event.preventDefault();
      event.stopImmediatePropagation();
      return false;
    }
    var text = Array.prototype.map.call(form.querySelectorAll('input:not([type="hidden"]), textarea'), function(el){ return el.value || ''; }).join(' ');
    var urlCount = (text.match(/https?:\/\/|www\./gi) || []).length;
    if (urlCount > Number(form.dataset.maxLinks || 3)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      var error = form.querySelector('.form-error');
      if (error) { error.hidden = false; error.setAttribute('role','alert'); }
      return false;
    }
    if (!validateWhatsAppFields(form)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      return false;
    }
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopImmediatePropagation();
      form.reportValidity();
      return false;
    }
    form.dataset.lastSubmitAt = String(now);
  }, true);
})();
