/* Yuchen Water Interactive JS */

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    if (!menu) return;
    const overlay = ensureLangMenuOverlay();
    const isOpen = menu.classList.toggle('open');
    overlay.classList.toggle('open', isOpen);
    document.body.classList.toggle('lang-menu-open', isOpen);
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

const inquirySuccessHtml = 'Thank you. Your inquiry has been submitted successfully and sent to Yuchen Water at <a href="mailto:expresswater025@gmail.com">expresswater025@gmail.com</a>. Our sales engineer will contact you as soon as possible. You can also contact us anytime on <a href="https://wa.me/8619908311885" target="_blank" rel="noopener">WhatsApp +86-19908311885</a> or email <a href="mailto:expresswater025@gmail.com">expresswater025@gmail.com</a>.';
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
}

document.querySelectorAll('form.contact-form').forEach(prepareInquiryForm);

document.addEventListener('submit', async function(e) {
    const form = e.target;
    if (!form || !form.classList || !form.classList.contains('contact-form')) return;

    prepareInquiryForm(form);

    const endpoint = form.dataset.endpoint;
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

        if (!response.ok) throw new Error('Form endpoint rejected the inquiry.');

        if (success) {
            success.innerHTML = inquirySuccessHtml;
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
