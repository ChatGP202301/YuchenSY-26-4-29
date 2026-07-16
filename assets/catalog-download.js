(() => {
  const copy = {
    en:{setup:'Catalog download is being configured. Please contact us for the current PDF.',sending:'Checking your information…',fetching:'Preparing your private catalog…',done:'Download complete. A 24-hour link has also been sent to your email.',recorded:'The PDF was delivered, but download confirmation is pending.',network:'We could not complete the request. Your entries have been kept; please try again.',invalid_whatsapp:'Enter a plausible international WhatsApp number including + and country code.',invalid_email:'Enter a valid work email address.',turnstile_failed:'Please complete the anti-spam check.',rate_limited:'Too many recent requests. Please try again later.'},
    es:{setup:'La descarga del catálogo se está configurando. Solicite el PDF actual a nuestro equipo.',sending:'Comprobando sus datos…',fetching:'Preparando su catálogo privado…',done:'Descarga completada. También enviamos a su correo un enlace válido durante 24 horas.',recorded:'El PDF se entregó, pero la confirmación de descarga está pendiente.',network:'No fue posible completar la solicitud. Sus datos se conservan; inténtelo de nuevo.',invalid_whatsapp:'Introduzca un WhatsApp internacional válido con + y prefijo de país.',invalid_email:'Introduzca un correo profesional válido.',turnstile_failed:'Complete la verificación antispam.',rate_limited:'Demasiadas solicitudes recientes. Inténtelo más tarde.'},
    ar:{setup:'يجري إعداد تنزيل الكتالوج. يرجى التواصل معنا للحصول على النسخة الحالية.',sending:'جارٍ التحقق من البيانات…',fetching:'جارٍ إعداد الكتالوج الخاص…',done:'اكتمل التنزيل. أرسلنا أيضاً رابطاً صالحاً لمدة 24 ساعة إلى بريدك.',recorded:'تم تسليم الملف، لكن تأكيد اكتمال التنزيل ما زال قيد الانتظار.',network:'تعذر إكمال الطلب. بقيت بياناتك في النموذج؛ يرجى المحاولة مرة أخرى.',invalid_whatsapp:'أدخل رقم واتساب دولياً صحيحاً يبدأ بعلامة + ورمز الدولة.',invalid_email:'أدخل بريداً إلكترونياً مهنياً صحيحاً.',turnstile_failed:'أكمل فحص مكافحة الرسائل المزعجة.',rate_limited:'عدد الطلبات الأخيرة كبير. حاول لاحقاً.'},
    fr:{setup:'Le téléchargement du catalogue est en cours de configuration. Contactez-nous pour recevoir le PDF actuel.',sending:'Vérification de vos informations…',fetching:'Préparation de votre catalogue privé…',done:'Téléchargement terminé. Un lien valable 24 heures a aussi été envoyé par e-mail.',recorded:'Le PDF a été livré, mais la confirmation du téléchargement reste en attente.',network:'La demande n’a pas abouti. Vos saisies sont conservées ; veuillez réessayer.',invalid_whatsapp:'Saisissez un numéro WhatsApp international plausible avec + et indicatif pays.',invalid_email:'Saisissez une adresse e-mail professionnelle valide.',turnstile_failed:'Veuillez terminer le contrôle antispam.',rate_limited:'Trop de demandes récentes. Réessayez plus tard.'},
    de:{setup:'Der Katalog-Download wird eingerichtet. Bitte fordern Sie die aktuelle PDF-Datei direkt bei uns an.',sending:'Ihre Angaben werden geprüft…',fetching:'Ihr privater Katalog wird vorbereitet…',done:'Download abgeschlossen. Ein 24 Stunden gültiger Link wurde zusätzlich per E-Mail gesendet.',recorded:'Die PDF-Datei wurde übertragen, die Download-Bestätigung steht jedoch noch aus.',network:'Die Anfrage konnte nicht abgeschlossen werden. Ihre Eingaben bleiben erhalten; bitte versuchen Sie es erneut.',invalid_whatsapp:'Geben Sie eine plausible internationale WhatsApp-Nummer mit + und Ländervorwahl ein.',invalid_email:'Geben Sie eine gültige geschäftliche E-Mail-Adresse ein.',turnstile_failed:'Bitte schließen Sie die Spam-Prüfung ab.',rate_limited:'Zu viele aktuelle Anfragen. Bitte versuchen Sie es später erneut.'},
    ru:{setup:'Система скачивания каталога настраивается. Запросите актуальный PDF у нашей команды.',sending:'Проверяем данные…',fetching:'Готовим защищённый каталог…',done:'Скачивание завершено. Ссылка сроком на 24 часа также отправлена на вашу почту.',recorded:'PDF передан, но подтверждение завершения скачивания ещё ожидается.',network:'Не удалось завершить запрос. Введённые данные сохранены в форме; попробуйте ещё раз.',invalid_whatsapp:'Укажите корректный международный номер WhatsApp со знаком + и кодом страны.',invalid_email:'Укажите действующий рабочий адрес электронной почты.',turnstile_failed:'Пройдите проверку защиты от спама.',rate_limited:'Слишком много недавних запросов. Повторите попытку позже.'}
  };

  const config = window.YUCHEN_CATALOG_CONFIG || {};
  let widgetId = null;
  const form = document.querySelector('[data-catalog-form]');
  if (!form) return;
  const locale = form.dataset.locale || 'en';
  const message = form.querySelector('[data-form-status]');
  const button = form.querySelector('button[type="submit"]');
  const strings = copy[locale] || copy.en;
  form.elements.formStartedAt.value = String(Date.now());

  const setStatus = (text, state = '') => {
    message.textContent = text;
    message.dataset.state = state;
    message.setAttribute('role', state === 'error' ? 'alert' : 'status');
  };

  const configured = config.apiBase && config.turnstileSiteKey && !String(config.turnstileSiteKey).startsWith('REPLACE_');
  if (!configured) {
    button.disabled = true;
    setStatus(strings.setup, 'setup');
  } else {
    const renderTurnstile = () => {
      if (window.turnstile && widgetId === null) widgetId = window.turnstile.render(form.querySelector('[data-turnstile]'), { sitekey: config.turnstileSiteKey });
    };
    if (window.turnstile) renderTurnstile();
    else window.addEventListener('load', renderTurnstile, { once: true });
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!configured) return setStatus(strings.setup, 'error');
    button.disabled = true;
    setStatus(strings.sending, 'progress');
    try {
      const data = new FormData(form);
      const interests = data.getAll('interests');
      const turnstileToken = widgetId === null ? '' : window.turnstile.getResponse(widgetId);
      const params = new URLSearchParams(location.search);
      const payload = {
        submissionId: crypto.randomUUID(), locale, sourcePage: location.href,
        name:data.get('name'), company:data.get('company'), email:data.get('email'), whatsapp:data.get('whatsapp'),
        country:data.get('country'), buyerType:data.get('buyerType'), interests,
        estimatedQuantity:data.get('estimatedQuantity'), message:data.get('message'), consent:data.get('consent') === 'yes',
        website:data.get('website'), formStartedAt:Number(data.get('formStartedAt')), turnstileToken,
        utmSource:params.get('utm_source') || '', utmMedium:params.get('utm_medium') || '', utmCampaign:params.get('utm_campaign') || ''
      };
      const access = await fetch(`${config.apiBase}/v1/catalog/access`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(payload) });
      const result = await access.json().catch(() => ({}));
      if (!access.ok || !result.downloadUrl) throw new Error(result.code || 'network');
      setStatus(strings.fetching, 'progress');
      const fileResponse = await fetch(result.downloadUrl, { cache:'no-store' });
      if (!fileResponse.ok) throw new Error('network');
      const blob = await fileResponse.blob();
      if (!blob.size) throw new Error('network');
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = `yuchen-water-filter-cartridge-catalog-${locale}-2026.pdf`;
      document.body.appendChild(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
      const token = decodeURIComponent(new URL(result.downloadUrl).pathname.split('/').pop());
      const complete = await fetch(`${config.apiBase}/v1/catalog/complete`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({ token, bytes:blob.size }) });
      setStatus(complete.ok ? strings.done : strings.recorded, complete.ok ? 'success' : 'warning');
      if (complete.ok) form.reset();
    } catch (error) {
      setStatus(strings[error.message] || strings.network, 'error');
      if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
    } finally {
      button.disabled = false;
    }
  });
})();
