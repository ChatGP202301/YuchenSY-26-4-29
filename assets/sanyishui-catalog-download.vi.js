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
  const locale = document.documentElement.lang.toLowerCase() === 'vi' ? 'vi' : (catalogId.split('-').pop() || 'en');

  const consent = form.querySelector('.catalog-consent');
  if (consent && !form.querySelector('[data-catalog-data-notice]')) {
    const privacyLink = consent.querySelector('a[href$="privacy-policy.html"]');
    if (privacyLink && new Set(['be', 'cnr', 'ga', 'lb', 'mk', 'mt']).has(locale)) privacyLink.href = '/en/privacy-policy.html';
    const notice = document.createElement('p');
    notice.dataset.catalogDataNotice = '';
    notice.className = 'catalog-form-status';
    notice.textContent = 'Thông tin liên hệ doanh nghiệp và thông tin dự án bạn đã gửi được lưu trữ riêng tư, không tự động hết hạn lưu trữ, và được gửi qua email đến đội ngũ bán hàng của Yuchen Water. Bạn có thể yêu cầu chỉnh sửa hoặc xóa thông tin qua expresswater025@gmail.com.';
    consent.insertAdjacentElement('afterend', notice);
  }

  const copy = {
    setup: 'Chức năng truy cập catalog bảo mật đang chờ cấu hình Cloudflare. Vui lòng liên hệ Yuchen Water để nhận bản PDF hiện tại.',
    checking: 'Đang kiểm tra thông tin của bạn…',
    preparing: 'Đang chuẩn bị tải xuống catalog riêng của bạn…',
    done: 'Quá trình tải xuống danh mục sản phẩm OEM của Yuchen Water của bạn đã bắt đầu.',
    network: 'Chúng tôi không thể hoàn tất yêu cầu. Nội dung bạn đã nhập đã được giữ lại; vui lòng thử lại.',
    interests: 'Chọn ít nhất một nhóm sản phẩm.',
    whatsapp: 'Nhập số WhatsApp quốc tế có vẻ hợp lệ, bao gồm dấu + và mã quốc gia.',
    turnstile: 'Vui lòng hoàn tất bước xác minh chống thư rác.',
    rate_limited: 'Có quá nhiều yêu cầu được gửi trong thời gian gần đây. Vui lòng thử lại sau.',
    invalid_submission: 'Kiểm tra tất cả các trường bắt buộc rồi thử lại.',
    email_failed: 'Không thể chuyển yêu cầu của bạn đến đội ngũ bán hàng của chúng tôi. Vui lòng thử lại.',
    catalog_unavailable: 'Catalog tạm thời không khả dụng. Vui lòng thử lại sau.'
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
  const sourcePage = () => {
    const params = new URLSearchParams(location.search);
    const candidate = params.get('yw_source_page') || params.get('source_page') || location.pathname;
    try {
      const resolved = new URL(candidate, location.origin);
      if (resolved.origin === location.origin && !/[@\\]/.test(resolved.pathname)) return location.origin + resolved.pathname.slice(0, 240);
    } catch (error) { /* Use the current public catalog page. */ }
    return location.origin + location.pathname;
  };
  const resourceId = location.pathname.includes('commercial-ro-water-systems-catalog') ? 'commercial' : 'oem';

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
      message: window.YuchenJourney ? window.YuchenJourney.message(data.get('message')) : data.get('message'),
      consent: data.get('consent') === 'yes',
      website: data.get('website'),
      formStartedAt: Number(data.get('formStartedAt')),
      turnstileToken,
      sourcePage: sourcePage(),
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
        detail: { submissionId, resourceId, ctaLocation: 'sanyishui_catalog_form' }
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
      const receiptPayload = { submissionId, catalogId: payload.catalogId, receipt };
      if (window.YuchenDownloadReceipts) window.YuchenDownloadReceipts.report({ apiBase: config.apiBase, payload: receiptPayload });
      else fetch(`${config.apiBase}/v1/catalog/download-events`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(receiptPayload), cache:'no-store', keepalive:true }).catch(() => {});
      document.dispatchEvent(new CustomEvent('yuchen:catalog-download-complete', {
        detail: { submissionId, resourceId, ctaLocation: 'sanyishui_catalog_form' }
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
