(() => {
  const copy = {
    en:{setup:'Chức năng truy cập catalog bảo mật đang chờ cấu hình Cloudflare. Vui lòng liên hệ Yuchen Water để nhận bản PDF hiện tại.',sending:'Đang kiểm tra thông tin của bạn…',fetching:'Đang chuẩn bị catalog riêng của bạn…',done:'Quá trình tải xuống danh mục sản phẩm OEM của Yuchen Water của bạn đã bắt đầu.',network:'Chúng tôi không thể hoàn tất yêu cầu. Nội dung bạn đã nhập đã được giữ lại; vui lòng thử lại.',invalid_submission:'Kiểm tra tất cả các trường bắt buộc rồi thử lại.',invalid_whatsapp:'Nhập số WhatsApp quốc tế có định dạng hợp lý, bao gồm dấu + và mã quốc gia.',turnstile:'Vui lòng hoàn tất bước kiểm tra chống thư rác.',rate_limited:'Có quá nhiều yêu cầu được gửi trong thời gian gần đây. Vui lòng thử lại sau.',catalog_unavailable:'Catalog tạm thời không khả dụng. Vui lòng thử lại sau.'},
    vi:{setup:"Chức năng truy cập catalog bảo mật đang chờ cấu hình Cloudflare. Vui lòng liên hệ Yuchen Water để nhận bản PDF hiện tại.",sending:"Đang kiểm tra thông tin của bạn…",fetching:"Đang chuẩn bị catalog riêng của bạn…",done:"Quá trình tải xuống danh mục sản phẩm OEM của Yuchen Water của bạn đã bắt đầu.",network:"Chúng tôi không thể hoàn tất yêu cầu. Nội dung bạn đã nhập đã được giữ lại; vui lòng thử lại.",invalid_submission:"Kiểm tra tất cả các trường bắt buộc rồi thử lại.",invalid_whatsapp:"Nhập số WhatsApp quốc tế có định dạng hợp lý, bao gồm dấu + và mã quốc gia.",turnstile:"Vui lòng hoàn tất bước kiểm tra chống thư rác.",rate_limited:"Có quá nhiều yêu cầu được gửi trong thời gian gần đây. Vui lòng thử lại sau.",catalog_unavailable:"Catalog tạm thời không khả dụng. Vui lòng thử lại sau."},
    es:{setup:'El acceso seguro al catálogo está pendiente de configuración en Cloudflare. Solicite el PDF actual a Yuchen Water.',sending:'Comprobando sus datos…',fetching:'Preparando su catálogo privado…',done:'La descarga del catálogo OEM de Yuchen Water ha comenzado.',network:'No fue posible completar la solicitud. Sus datos se conservan; inténtelo de nuevo.',invalid_submission:'Revise todos los campos obligatorios e inténtelo de nuevo.',invalid_whatsapp:'Introduzca un WhatsApp internacional válido con + y prefijo de país.',turnstile:'Complete la verificación antispam.',rate_limited:'Demasiadas solicitudes recientes. Inténtelo más tarde.',catalog_unavailable:'El catálogo no está disponible temporalmente. Inténtelo más tarde.'},
    ar:{setup:'ينتظر الوصول الآمن إلى الكتالوج إعداد Cloudflare. تواصل مع Yuchen Water للحصول على ملف PDF الحالي.',sending:'جارٍ التحقق من البيانات…',fetching:'جارٍ إعداد الكتالوج الخاص…',done:'بدأ تنزيل كتالوج Yuchen Water OEM.',network:'تعذر إكمال الطلب. بقيت بياناتك في النموذج؛ يرجى المحاولة مرة أخرى.',invalid_submission:'تحقق من جميع الحقول المطلوبة وحاول مرة أخرى.',invalid_whatsapp:'أدخل رقم واتساب دولياً صحيحاً يبدأ بعلامة + ورمز الدولة.',turnstile:'أكمل فحص مكافحة الرسائل المزعجة.',rate_limited:'عدد الطلبات الأخيرة كبير. حاول لاحقاً.',catalog_unavailable:'الكتالوج غير متاح مؤقتاً. حاول مرة أخرى لاحقاً.'},
    fr:{setup:'L’accès sécurisé au catalogue attend la configuration Cloudflare. Contactez Yuchen Water pour recevoir le PDF actuel.',sending:'Vérification de vos informations…',fetching:'Préparation de votre catalogue privé…',done:'Le téléchargement du catalogue OEM Yuchen Water a commencé.',network:'La demande n’a pas abouti. Vos saisies sont conservées ; veuillez réessayer.',invalid_submission:'Vérifiez tous les champs obligatoires et réessayez.',invalid_whatsapp:'Saisissez un numéro WhatsApp international plausible avec + et indicatif pays.',turnstile:'Veuillez terminer le contrôle antispam.',rate_limited:'Trop de demandes récentes. Réessayez plus tard.',catalog_unavailable:'Le catalogue est temporairement indisponible. Réessayez plus tard.'},
    de:{setup:'Der sichere Katalogzugang wartet auf die Cloudflare-Konfiguration. Fordern Sie die aktuelle PDF-Datei bei Yuchen Water an.',sending:'Ihre Angaben werden geprüft…',fetching:'Ihr privater Katalog wird vorbereitet…',done:'Der Download des Yuchen Water OEM-Katalogs wurde gestartet.',network:'Die Anfrage konnte nicht abgeschlossen werden. Ihre Eingaben bleiben erhalten; bitte versuchen Sie es erneut.',invalid_submission:'Prüfen Sie alle Pflichtfelder und versuchen Sie es erneut.',invalid_whatsapp:'Geben Sie eine plausible internationale WhatsApp-Nummer mit + und Ländervorwahl ein.',turnstile:'Bitte schließen Sie die Spam-Prüfung ab.',rate_limited:'Zu viele aktuelle Anfragen. Bitte versuchen Sie es später erneut.',catalog_unavailable:'Der Katalog ist vorübergehend nicht verfügbar. Bitte versuchen Sie es später erneut.'},
    ru:{setup:'Безопасный доступ к каталогу ожидает настройки Cloudflare. Запросите актуальный PDF у Yuchen Water.',sending:'Проверяем данные…',fetching:'Готовим защищённый каталог…',done:'Загрузка OEM-каталога Yuchen Water началась.',network:'Не удалось завершить запрос. Введённые данные сохранены в форме; попробуйте ещё раз.',invalid_submission:'Проверьте все обязательные поля и повторите попытку.',invalid_whatsapp:'Укажите корректный международный номер WhatsApp со знаком + и кодом страны.',turnstile:'Пройдите проверку защиты от спама.',rate_limited:'Слишком много недавних запросов. Повторите попытку позже.',catalog_unavailable:'Каталог временно недоступен. Повторите попытку позже.'}
  };

  const config = window.YUCHEN_CATALOG_CONFIG || {};
  const form = document.querySelector('[data-catalog-form]');
  if (!form) return;
  const locale = document.documentElement.lang.toLowerCase() === 'vi' ? 'vi' : (form.dataset.locale || 'en');
  const strings = copy[locale] || copy.en;
  const interestLabels = {pp:'PP Sediment','gac-udf':'GAC / UDF',cto:'CTO Carbon Block',t33:'T33 Inline',ro:'RO Membrane',uf:'UF Membrane',specialty:'Hạt nhựa / Vật liệu xử lý nước chuyên dụng'};
  const requestedInterest = new URLSearchParams(location.search).get('interest');
  if (locale === 'en' && form.dataset.catalogId === 'filter-cartridges-2026-en' && interestLabels[requestedInterest]) {
    const input = form.querySelector(`input[name="interests"][value="${CSS.escape(requestedInterest)}"]`);
    if (input) input.checked = true;
    const context = document.createElement('p');
    context.dataset.catalogInterestContext = requestedInterest;
    context.className = 'catalog-form-status';
    context.textContent = `Selected product interest: ${interestLabels[requestedInterest]}. The full Filter Cartridge Catalog also includes the other listed filter families.`;
    form.insertAdjacentElement('beforebegin', context);
  }
  const message = form.querySelector('[data-form-status]');
  const button = form.querySelector('button[type="submit"]');
  const turnstileMount = form.querySelector('[data-turnstile]');
  let widgetId = null;
  let submissionId = crypto.randomUUID();

  const consent = form.querySelector('.catalog-consent');
  if (consent && !form.querySelector('[data-catalog-data-notice]')) {
    const notice = document.createElement('p');
    notice.dataset.catalogDataNotice = '';
    notice.className = 'catalog-form-status';
    notice.textContent = 'Thông tin liên hệ doanh nghiệp và thông tin dự án bạn đã gửi được lưu trữ riêng tư, không tự động hết hạn lưu trữ, và được gửi qua email đến đội ngũ bán hàng của Yuchen Water. Bạn có thể yêu cầu chỉnh sửa hoặc xóa thông tin qua expresswater025@gmail.com.';
    consent.insertAdjacentElement('afterend', notice);
  }

  const setStatus = (text, state = '') => {
    message.textContent = text;
    message.dataset.state = state;
    message.setAttribute('role', state === 'error' ? 'alert' : 'status');
  };
  const resetStartedAt = () => { form.elements.formStartedAt.value = String(Date.now()); };
  const selectedInterests = () => Array.from(form.querySelectorAll('input[name="interests"]:checked'), input => input.value);
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
  const configured = Boolean(config.apiBase && config.turnstileSiteKey && !String(config.turnstileSiteKey).startsWith('REPLACE_'));

  const renderTurnstile = () => {
    if (!window.turnstile || widgetId !== null || !turnstileMount) return false;
    widgetId = window.turnstile.render(turnstileMount, {
      sitekey: config.turnstileSiteKey,
      action: 'oem_catalog_download'
    });
    return true;
  };

  resetStartedAt();
  if (!configured) {
    button.disabled = true;
    setStatus(strings.setup, 'setup');
  } else if (!renderTurnstile()) {
    const poll = window.setInterval(() => {
      if (renderTurnstile()) window.clearInterval(poll);
    }, 250);
    window.setTimeout(() => window.clearInterval(poll), 10000);
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!configured) return setStatus(strings.setup, 'error');
    if (!form.checkValidity() || !selectedInterests().length) {
      form.reportValidity();
      return setStatus(strings.invalid_submission, 'error');
    }
    if (!plausibleWhatsApp(form.elements.whatsapp.value)) {
      form.elements.whatsapp.setCustomValidity(strings.invalid_whatsapp);
      form.elements.whatsapp.reportValidity();
      form.elements.whatsapp.setCustomValidity('');
      return setStatus(strings.invalid_whatsapp, 'error');
    }
    const widgetToken = widgetId === null || !window.turnstile ? '' : window.turnstile.getResponse(widgetId);
    const turnstileToken = widgetToken || form.querySelector('input[name="cf-turnstile-response"]')?.value || '';
    if (!turnstileToken) return setStatus(strings.turnstile, 'error');

    const data = new FormData(form);
    const params = new URLSearchParams(location.search);
    const attribution = firstTouch();
    const payload = {
      submissionId,
      catalogId: form.dataset.catalogId,
      locale,
      sourcePage: sourcePage(),
      firstLandingPage: attribution.landingPage || location.pathname,
      referrerDomain: attribution.referrerDomain || '',
      name: data.get('name'),
      company: data.get('company'),
      email: data.get('email'),
      whatsapp: data.get('whatsapp'),
      country: data.get('country'),
      buyerType: data.get('buyerType'),
      interests: selectedInterests(),
      estimatedQuantity: data.get('estimatedQuantity'),
      message: window.YuchenJourney ? window.YuchenJourney.message(data.get('message')) : data.get('message'),
      consent: data.get('consent') === 'yes',
      website: data.get('website'),
      formStartedAt: Number(data.get('formStartedAt')),
      turnstileToken,
      utmSource: params.get('utm_source') || attribution.utmSource || '',
      utmMedium: params.get('utm_medium') || attribution.utmMedium || '',
      utmCampaign: params.get('utm_campaign') || attribution.utmCampaign || '',
      utmTerm: params.get('utm_term') || attribution.utmTerm || '',
      utmContent: params.get('utm_content') || attribution.utmContent || ''
    };

    button.disabled = true;
    setStatus(strings.sending, 'progress');
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
      setStatus(strings.fetching, 'progress');
      const contentType = String(response.headers.get('content-type') || '').toLowerCase();
      const receipt = response.headers.get('x-catalog-receipt') || '';
      const blob = await response.blob();
      if (!contentType.includes('application/pdf') || !blob.size || !receipt) throw new Error('catalog_unavailable');

      document.dispatchEvent(new CustomEvent('yuchen:catalog-submit-success', {
        detail: { submissionId, resourceId: 'filter', ctaLocation: 'filter_catalog_form' }
      }));
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = form.dataset.downloadFilename || 'Yuchen_Water_OEM_Product_Catalog_2026.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
      const receiptPayload = { submissionId, catalogId: form.dataset.catalogId, receipt };
      if (window.YuchenDownloadReceipts) window.YuchenDownloadReceipts.report({ apiBase: config.apiBase, payload: receiptPayload });
      else fetch(`${config.apiBase}/v1/catalog/download-events`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(receiptPayload), cache:'no-store', keepalive:true }).catch(() => {});
      document.dispatchEvent(new CustomEvent('yuchen:catalog-download-complete', {
        detail: { submissionId, resourceId: 'filter', ctaLocation: 'filter_catalog_form' }
      }));
      setStatus(strings.done, 'success');
      form.reset();
      submissionId = crypto.randomUUID();
      resetStartedAt();
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } catch (error) {
      setStatus(strings[error.message] || strings.network, 'error');
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } finally {
      button.disabled = false;
    }
  });
})();
