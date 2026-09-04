/* Pure search/language functions, shared by the browser and Node regression tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.YuchenDiscoveryCore = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function normalize(value) {
    return String(value || '').normalize('NFKC').toLowerCase()
      .replace(/[\u2010-\u2015\u2212]/g, '-').replace(/\s+/g, ' ').trim();
  }
  function compact(value) { return normalize(value).replace(/[^\p{L}\p{N}]/gu, ''); }
  function prepare(documents) {
    return documents.map(function (doc) {
      return { doc: doc, title: normalize(doc.title), headings: normalize(doc.headings),
        text: normalize(doc.text), models: (doc.models || []).map(compact) };
    });
  }
  function search(prepared, query) {
    var term = normalize(query).slice(0, 120);
    if (!term) return [];
    var tokens = term.split(/[\s\-_/]+/u).filter(Boolean), model = compact(term);
    return prepared.map(function (item) {
      var exact = item.models.includes(model);
      var haystack = item.title + ' ' + item.headings + ' ' + item.text;
      var partialModel = model && /\d/.test(model) && item.models.some(function (m) { return m.includes(model); });
      if (!exact && !partialModel && !tokens.every(function (t) { return haystack.includes(t); })) return null;
      var score = exact ? 10000 : partialModel ? 600 : 0;
      score += item.title.includes(term) ? 250 : 0;
      score += item.headings.includes(term) ? 100 : 0;
      tokens.forEach(function (t) { score += item.title.includes(t) ? 30 : item.headings.includes(t) ? 10 : 1; });
      return { document: item.doc, score: score };
    }).filter(Boolean).sort(function (a, b) {
      return b.score - a.score || (a.document.url < b.document.url ? -1 : a.document.url > b.document.url ? 1 : 0);
    }).map(function (item) { return item.document; });
  }
  function localeCode(tag, available) {
    var value = normalize(tag).replace(/_/g, '-');
    if (/^sr-(?:latn-)?me$/.test(value) || value === 'cnr') value = 'cnr';
    else if (/^(nb|nn)(-|$)/.test(value)) value = 'no';
    else if (/^fil(-|$)/.test(value)) value = 'tl';
    else if (/^iw(-|$)/.test(value)) value = 'he';
    else value = value.split('-')[0];
    return available.includes(value) ? value : null;
  }
  function filterLanguages(locales, query) {
    var term = normalize(query);
    return locales.filter(function (locale) {
      return normalize([locale.code, locale.native, locale.english, locale.tag].join(' ')).includes(term);
    });
  }
  function safePath(value, base) {
    try {
      var url = new URL(value, base);
      if (!['http:', 'https:'].includes(url.protocol)) return null;
      if (![new URL(base).origin, 'https://www.yuchensy.com', 'https://yuchensy.com'].includes(url.origin)) return null;
      if (url.search || url.hash || /%2f|%5c|\\/i.test(url.pathname)) return null;
      return url.pathname;
    } catch (_) { return null; }
  }
  return { normalize: normalize, compact: compact, prepare: prepare, search: search,
    localeCode: localeCode, filterLanguages: filterLanguages, safePath: safePath };
});

/* Progressive enhancement. No query logging, geolocation, forced redirects or analytics. */
(function () {
  'use strict';
  if (window.YuchenDiscovery || new URLSearchParams(location.search).get('yw_download_embed') === '1') return;
  if (!window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal || !window.fetch) return;
  var ownScript = document.currentScript, core = window.YuchenDiscoveryCore;
  if (!ownScript || !core) return;
  var assetBase = new URL('.', ownScript.src);
  var configPromise = getJSON(new URL('search/config.json' + new URL(ownScript.src).search, assetBase));
  function getJSON(url) {
    var controller = new AbortController(), timer = setTimeout(function () { controller.abort(); }, 10000);
    return fetch(url, { signal: controller.signal, credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('Discovery data unavailable');
      return r.json();
    }).finally(function () { clearTimeout(timer); });
  }
  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function button(text, className) { var b = element('button', className, text); b.type = 'button'; return b; }
  function storageGet(key) { try { return localStorage.getItem(key); } catch (_) { return null; } }
  function storageSet(key, value) { try { localStorage.setItem(key, value); } catch (_) { /* Optional persistence. */ } }
  configPromise.then(function (config) {
    var codes = config.locales.map(function (l) { return l.code; });
    var pathLocale = location.pathname.split('/')[1];
    var code = core.localeCode(pathLocale, codes) || 'en';
    var locale = config.locales.find(function (l) { return l.code === code; }), ui = locale.ui;
    var header = document.querySelector('header.header,header.commercial-site-header,header.yt-header,header.rcu-header,header');
    var controls = element('div', 'yd-controls');
    if (header) {
      (header.querySelector('.header-actions') || header.querySelector('.header-row') || header).appendChild(controls);
    } else {
      controls.classList.add('yd-controls-fallback');
      document.body.prepend(controls);
    }
    var searchTrigger = button('⌕', 'yd-icon-button');
    searchTrigger.setAttribute('aria-label', ui.search);
    searchTrigger.title = ui.search;
    searchTrigger.setAttribute('aria-haspopup', 'dialog');
    searchTrigger.dataset.ydSearch = 'header';
    controls.appendChild(searchTrigger);
    var searchDialog = dialog('search', ui.search), languageDialog = dialog('language', ui.languages);
    var searchForm = element('form', 'yd-search-form');
    searchForm.setAttribute('role', 'search');
    var searchInput = element('input', 'yd-input');
    searchInput.type = 'search'; searchInput.maxLength = 120; searchInput.autocomplete = 'off';
    searchInput.placeholder = ui.query; searchInput.id = 'yd-search-input';
    var searchLabel = element('label', 'yd-label', ui.query); searchLabel.htmlFor = searchInput.id;
    var submit = button(ui.search, 'yd-primary'); submit.type = 'submit';
    searchForm.append(searchLabel, searchInput, submit);
    var status = element('p', 'yd-status'); status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    var results = element('ol', 'yd-results');
    var more = button(ui.more, 'yd-secondary'); more.hidden = true;
    var fallback = element('div', 'yd-fallback');
    [['products', locale.products], ['catalog', locale.catalog], ['contact', locale.contact]].forEach(function (pair) {
      if (!pair[1]) return;
      var a = element('a', '', ui[pair[0]]); a.href = pair[1];
      a.dataset.ywDownloadBypass = 'true'; // Search links navigate to public pages, not nested dialogs.
      a.addEventListener('click', function () { searchDialog.close(); });
      fallback.appendChild(a);
    });
    searchDialog.append(searchForm, status, results, more, fallback);
    var indexPromise = null, queryRevision = 0, currentResults = [], visibleCount = 0, debounce;
    function loadIndex() {
      if (!indexPromise) indexPromise = getJSON(new URL('search/' + code + '.json?v=' + locale.indexVersion, assetBase))
        .then(function (data) {
          if (data.locale !== code || !Array.isArray(data.documents)) throw new Error('Invalid search index');
          return core.prepare(data.documents.filter(function (d) {
            var p = core.safePath(d.url, location.href);
            return p && (p === '/' && code === 'en' || p.startsWith('/' + code + '/'));
          }));
        }).catch(function (error) { indexPromise = null; throw error; });
      return indexPromise;
    }
    function renderMore() {
      var next = currentResults.slice(visibleCount, visibleCount + 10);
      next.forEach(function (doc) {
        var li = element('li'), a = element('a', 'yd-result-link', doc.title); a.href = doc.url;
        a.dataset.ywDownloadBypass = 'true';
        li.append(a, element('p', 'yd-snippet', doc.description || doc.headings)); results.appendChild(li);
      });
      visibleCount += next.length; more.hidden = visibleCount >= currentResults.length;
    }
    function runSearch() {
      var revision = ++queryRevision, value = searchInput.value.trim();
      results.replaceChildren(); more.hidden = true;
      if (!value) { status.textContent = ui.query; return; }
      status.textContent = ui.loading;
      loadIndex().then(function (prepared) {
        if (revision !== queryRevision || !searchDialog.open) return;
        currentResults = core.search(prepared, value); visibleCount = 0;
        status.textContent = currentResults.length ? ui.results + ': ' + currentResults.length : ui.empty;
        renderMore();
      }).catch(function () { if (revision === queryRevision) status.textContent = ui.error; });
    }
    more.addEventListener('click', function () {
      var before = results.children.length; renderMore();
      var firstNew = results.children[before]; if (firstNew) firstNew.querySelector('a').focus();
    });
    searchForm.addEventListener('submit', function (e) { e.preventDefault(); clearTimeout(debounce); runSearch(); });
    searchInput.addEventListener('input', function () { clearTimeout(debounce); ++queryRevision; debounce = setTimeout(runSearch, 140); });
    function openSearch(query, trigger) {
      searchInput.value = query || ''; openDialog(searchDialog, trigger, searchInput); runSearch();
    }
    searchTrigger.addEventListener('click', function () { openSearch('', searchTrigger); });
    document.querySelectorAll('[data-yd-home-search]').forEach(function (form) {
      form.addEventListener('submit', function (e) { e.preventDefault(); openSearch(form.querySelector('input').value, form.querySelector('input')); });
      form.hidden = false;
    });
    var languageInput = element('input', 'yd-input');
    languageInput.type = 'search'; languageInput.autocomplete = 'off'; languageInput.placeholder = ui.languageQuery;
    languageInput.id = 'yd-language-input'; languageInput.maxLength = 80;
    var languageLabel = element('label', 'yd-label', ui.languageQuery); languageLabel.htmlFor = languageInput.id;
    var languageStatus = element('p', 'yd-status'); languageStatus.setAttribute('role', 'status');
    var suggestedTitle = element('h3', 'yd-subheading', ui.suggested);
    var suggested = element('ul', 'yd-language-list');
    var allTitle = element('h3', 'yd-subheading', ui.all);
    var all = element('ul', 'yd-language-list');
    var languageBody = element('div', 'yd-language-body');
    languageBody.append(suggestedTitle, suggested, allTitle, all);
    languageDialog.append(languageLabel, languageInput, languageStatus, languageBody);
    var languageTrigger = button('◎ ' + code.toUpperCase(), 'yd-language-button');
    languageTrigger.setAttribute('aria-label', ui.languages);
    languageTrigger.setAttribute('aria-haspopup', 'dialog');
    controls.appendChild(languageTrigger);
    var primaryNav = header && header.querySelector('nav');
    if (primaryNav) {
      primaryNav.classList.add('yd-primary-nav');
      if (!primaryNav.id) primaryNav.id = 'yd-primary-navigation';
      var navTrigger = button('☰', 'yd-icon-button yd-nav-toggle');
      navTrigger.setAttribute('aria-label', ui.menu);
      navTrigger.setAttribute('aria-controls', primaryNav.id);
      navTrigger.setAttribute('aria-expanded', 'false');
      controls.appendChild(navTrigger);
      navTrigger.addEventListener('click', function () {
        var isOpen = header.classList.toggle('yd-navigation-open');
        navTrigger.setAttribute('aria-expanded', String(isOpen));
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && header.classList.contains('yd-navigation-open')) {
          header.classList.remove('yd-navigation-open'); navTrigger.setAttribute('aria-expanded', 'false');
          navTrigger.focus();
        }
      });
    }
    var routePromise = null, destinations = null;
    // Read existing translation links; never guess an unverified target or redirect on page load.
    var existing = {};
    document.querySelectorAll('.lang-menu a[href],.commercial-language-selector a[href],link[rel="alternate"][hreflang]').forEach(function (a) {
      var lang = core.localeCode(a.getAttribute('lang') || a.getAttribute('hreflang'), codes);
      var target = core.safePath(a.getAttribute('href'), location.href);
      if (lang && target && target.indexOf('/sr-me/') !== 0) existing[lang] = target;
    });
    function loadDestinations() {
      if (!routePromise) routePromise = getJSON(new URL('search/routes.json?v=' + config.routesVersion, assetBase)).then(function (data) {
        var paths = new Set(data.paths), aliases = data.aliases || {}, current = location.pathname;
        var suffix = current.replace(/^\/[a-z]{2,3}(?:-[a-z]{2})?\//, '');
        destinations = {};
        config.locales.forEach(function (l) {
          var candidate = existing[l.code] || '/' + l.code + '/' + suffix;
          candidate = aliases[candidate] || candidate;
          var correctLocale = candidate.startsWith('/' + l.code + '/') || (l.code === 'en' && candidate === '/');
          destinations[l.code] = correctLocale && paths.has(candidate) ? candidate : l.home;
        });
      }).catch(function (error) { routePromise = null; throw error; });
      return routePromise;
    }
    var languageRevision = 0;
    function renderLanguages() {
      var filtered = core.filterLanguages(config.locales, languageInput.value);
      var stored = core.localeCode(storageGet('yd-language'), codes);
      var preferred = [stored].concat((navigator.languages || [navigator.language]).map(function (tag) { return core.localeCode(tag, codes); }));
      preferred = Array.from(new Set(preferred.filter(Boolean))).slice(0, 3);
      suggested.replaceChildren(); all.replaceChildren();
      function addLanguage(target, l) {
        var li = element('li'), a = element('a', 'yd-language-option');
        a.href = destinations ? destinations[l.code] : l.home;
        a.lang = l.tag; a.hreflang = l.tag;
        if (l.code === code) a.setAttribute('aria-current', 'true');
        var name = element('bdi', '', l.native); name.dir = l.dir;
        a.append(name, element('small', '', l.english + ' · ' + l.code.toUpperCase()));
        if (a.getAttribute('href') === l.home) a.appendChild(element('span', 'yd-home-badge', ui.home));
        a.addEventListener('click', function () { storageSet('yd-language', l.code); });
        li.appendChild(a); target.appendChild(li);
      }
      if (!languageInput.value.trim()) preferred.forEach(function (c) { addLanguage(suggested, config.locales.find(function (l) { return l.code === c; })); });
      suggestedTitle.hidden = suggested.children.length === 0;
      filtered.forEach(function (l) { addLanguage(all, l); });
      languageStatus.textContent = filtered.length ? ui.results + ': ' + filtered.length : ui.empty;
    }
    languageInput.addEventListener('input', renderLanguages);
    languageTrigger.addEventListener('click', function () {
      var revision = ++languageRevision;
      languageInput.value = ''; openDialog(languageDialog, languageTrigger, languageInput);
      renderLanguages();
      loadDestinations().then(function () { if (revision === languageRevision) renderLanguages(); }).catch(function () {
        // Home URLs remain usable when optional mapping fails.
        if (revision === languageRevision) languageStatus.textContent = ui.languages + ' — ' + ui.home;
      });
    });
    // Hide legacy controls only AFTER both accessible dialogs and triggers are usable.
    document.querySelectorAll('.lang-switcher,.commercial-language-selector,.lang-select-mobile').forEach(function (el) { el.classList.add('yd-legacy-language'); });
    if (header) header.classList.add('yd-header');
    document.documentElement.classList.add('yd-ready');
    window.YuchenDiscovery = { locale: code, search: function (query) { openSearch(query, searchTrigger); } };
    function dialog(kind, title) {
      var d = element('dialog', 'yd-dialog'); d.id = 'yd-' + kind + '-dialog'; d.dir = locale.dir;
      var top = element('div', 'yd-dialog-top'), h = element('h2', '', title); h.id = d.id + '-title';
      d.setAttribute('aria-labelledby', h.id);
      var close = button('×', 'yd-icon-button'); close.setAttribute('aria-label', ui.close);
      close.addEventListener('click', function () { d.close(); });
      top.append(h, close); d.appendChild(top); document.body.appendChild(d);
      d.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); d.close(); return; }
        if (e.key !== 'Tab') return;
        var focusable = Array.from(d.querySelectorAll('button,a[href],input,[tabindex="0"]')).filter(function (el) {
          return !el.disabled && el.getClientRects().length;
        });
        var first = focusable[0], last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      });
      d.addEventListener('click', function (e) {
        if (e.target !== d) return;
        var r = d.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close();
      });
      d.addEventListener('close', function () {
        if (!document.querySelector('dialog.yd-dialog[open]')) {
          document.documentElement.classList.remove('yd-dialog-open');
          if (d.ydReturnFocus && d.ydReturnFocus.isConnected) d.ydReturnFocus.focus();
        }
      });
      return d;
    }
    function openDialog(d, trigger, input) {
      document.querySelectorAll('dialog.yd-dialog[open]').forEach(function (other) { other.close(); });
      if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
      d.ydReturnFocus = trigger; d.showModal();
      document.documentElement.classList.add('yd-dialog-open'); input.focus();
    }
  }).catch(function () { /* Existing navigation and native language controls remain intact. */ });
})();
