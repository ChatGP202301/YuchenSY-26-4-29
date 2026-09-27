/* Yuchen Water English OEM configuration selector and RFQ handoff. */
(() => {
  'use strict';

  const MAX_SELECTIONS = 3;
  const CONFIRMATION = 'Confirm for quotation';
  const BOUNDARY = 'This is a preliminary OEM sourcing shortlist. Final connection, compatibility, dimensions and project requirements must be confirmed before quotation.';

  const clean = (value) => String(value || '').trim();
  const valuesFor = (configuration, key) => {
    const values = configuration && configuration.filters && configuration.filters[key];
    return Array.isArray(values) ? values.map(clean).filter(Boolean) : [];
  };

  function classifyConfiguration(configuration, selectedFilters) {
    const unknownFields = [];
    const conflictingFields = [];
    Object.entries(selectedFilters || {}).forEach(([key, selected]) => {
      const wanted = clean(selected);
      if (!wanted) return;
      const available = valuesFor(configuration, key);
      if (!available.length) unknownFields.push(key);
      else if (!available.includes(wanted)) conflictingFields.push(key);
    });
    return {
      status: conflictingFields.length ? 'conflict' : (unknownFields.length ? 'possible' : 'exact'),
      unknownFields,
      conflictingFields
    };
  }

  function resultCountBucket(count) {
    if (count <= 0) return 'zero';
    if (count === 1) return 'one';
    if (count <= 5) return 'two_to_five';
    return 'six_plus';
  }

  const fieldMap = (payload) => new Map((payload.fields || []).map((field) => [field.key, field.label]));
  const filterText = (payload, filters) => {
    const labels = fieldMap(payload);
    return Object.entries(filters || {})
      .filter((entry) => clean(entry[1]))
      .map(([key, value]) => `${labels.get(key) || key}: ${clean(value)}`)
      .join(' | ');
  };

  function selectedConfigurations(payload, selectedIds) {
    const byId = new Map((payload.configurations || []).map((configuration) => [configuration.id, configuration]));
    return (selectedIds || []).slice(0, MAX_SELECTIONS)
      .map((id) => byId.get(id)).filter(Boolean);
  }

  function buildRfqSummary(payload, selectedIds, filters) {
    const labels = fieldMap(payload);
    const selected = selectedConfigurations(payload, selectedIds);
    const lines = [
      'OEM RFQ shortlist',
      `Guide: ${clean(payload.guideTitle)}`,
      '',
      'Selected requirements:'
    ];
    const activeFilters = Object.entries(filters || {}).filter((entry) => clean(entry[1]));
    if (!activeFilters.length) lines.push(`- ${CONFIRMATION}`);
    activeFilters.forEach(([key, value]) => lines.push(`- ${labels.get(key) || key}: ${clean(value)}`));
    lines.push('', 'Requested configurations:');
    selected.forEach((configuration, index) => {
      lines.push(`${index + 1}. ${clean(configuration.name)} [${clean(configuration.id)}]`);
      (payload.fields || []).forEach((field) => {
        const value = clean(configuration.specs && configuration.specs[field.key]);
        lines.push(`   - ${field.label}: ${value || CONFIRMATION}`);
      });
    });
    lines.push('', BOUNDARY);
    return lines.join('\n');
  }

  function buildQuoteUrl(base, payload, selectedIds, filters) {
    const selected = selectedConfigurations(payload, selectedIds);
    const params = new URLSearchParams();
    params.set('rfq_guide', clean(payload.selectorId));
    params.set('rfq_ids', selected.map((configuration) => configuration.id).join(','));
    params.set('rfq_filters', filterText(payload, filters));
    params.set('product', selected.map((configuration) => configuration.name).join('; '));
    params.set('product_family', clean(payload.selectorId));
    params.set('cta_location', 'filter_selector_result');
    return `${String(base || 'contact.html').split('?')[0]}?${params.toString()}`;
  }

  const api = Object.freeze({
    MAX_SELECTIONS,
    CONFIRMATION,
    BOUNDARY,
    classifyConfiguration,
    resultCountBucket,
    buildRfqSummary,
    buildQuoteUrl
  });
  if (typeof window !== 'undefined') window.YuchenFilterSelector = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const emit = (type, detail) => {
    document.dispatchEvent(new CustomEvent(type, { detail: detail || {} }));
  };
  const create = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const activeFilters = (form) => {
    const filters = {};
    form.querySelectorAll('[data-selector-filter]').forEach((select) => {
      if (select.value) filters[select.dataset.selectorFilter] = select.value;
    });
    return filters;
  };
  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.appendChild(field);
    field.select();
    const copied = document.execCommand('copy');
    field.remove();
    if (!copied) throw new Error('Clipboard copy was not available.');
  };

  function initialize(root) {
    const dataNode = root.querySelector('[data-sy-selector-data]');
    const form = root.querySelector('[data-selector-form]');
    if (!dataNode || !form) return;
    let payload;
    try { payload = JSON.parse(dataNode.textContent); }
    catch (error) { return; }
    if (!payload || !Array.isArray(payload.configurations) || !Array.isArray(payload.fields)) return;

    const results = root.querySelector('[data-selector-results]');
    const resultList = root.querySelector('[data-selector-result-list]');
    const resultHeading = root.querySelector('[data-selector-result-heading]');
    const resultSummary = root.querySelector('[data-selector-result-summary]');
    const rfq = root.querySelector('[data-selector-rfq]');
    const copyButton = root.querySelector('[data-selector-copy]');
    const contactLink = root.querySelector('[data-selector-contact]');
    const copyStatus = root.querySelector('[data-selector-copy-status]');
    const labels = fieldMap(payload);
    const selectedIds = new Set();
    let currentFilters = {};
    let started = false;

    const start = () => {
      if (started) return;
      started = true;
      emit('yuchen:filter-selector-start', {
        selectorId: payload.selectorId,
        ctaLocation: 'filter_selector'
      });
    };

    const updateRfq = () => {
      const selected = Array.from(selectedIds);
      const enabled = selected.length > 0;
      copyButton.disabled = !enabled;
      rfq.hidden = !enabled;
      contactLink.setAttribute('aria-disabled', enabled ? 'false' : 'true');
      if (enabled) contactLink.href = buildQuoteUrl('contact.html', payload, selected, currentFilters);
      root.querySelectorAll('[data-selector-choice]').forEach((checkbox) => {
        checkbox.disabled = !checkbox.checked && selected.length >= MAX_SELECTIONS;
      });
      copyStatus.textContent = enabled
        ? `${selected.length} of ${MAX_SELECTIONS} configurations selected.`
        : '';
    };

    const appendCriterion = (list, key, selected, configuration) => {
      const row = create('div', 'sy-selector-match-row');
      const term = create('dt', '', labels.get(key) || key);
      const available = valuesFor(configuration, key);
      const value = available.length ? available.join(' or ') : CONFIRMATION;
      const description = create('dd', available.length ? '' : 'sy-selector-confirm', value);
      if (available.length && !available.includes(selected)) description.classList.add('sy-selector-conflict');
      row.append(term, description);
      list.appendChild(row);
    };

    const render = () => {
      currentFilters = activeFilters(form);
      selectedIds.clear();
      resultList.replaceChildren();
      const matches = payload.configurations
        .map((configuration) => ({ configuration, match: classifyConfiguration(configuration, currentFilters) }))
        .filter((row) => row.match.status !== 'conflict')
        .sort((left, right) => {
          if (left.match.status !== right.match.status) return left.match.status === 'exact' ? -1 : 1;
          return left.configuration.name.localeCompare(right.configuration.name, 'en');
        });
      const exactCount = matches.filter((row) => row.match.status === 'exact').length;
      const possibleCount = matches.length - exactCount;
      resultHeading.textContent = matches.length === 1 ? '1 configuration to review' : `${matches.length} configurations to review`;
      resultSummary.textContent = matches.length
        ? `${exactCount} exact based on stated source fields; ${possibleCount} possible with confirmation required.`
        : 'No reviewed configuration satisfies every stated requirement. Reset one optional filter or send the requirement for engineering review.';

      if (!matches.length) {
        resultList.appendChild(create('p', 'sy-selector-empty', 'No match found in this reviewed configuration set. The inquiry form can still be used for a custom project review.'));
      }
      matches.forEach(({ configuration, match }) => {
        const card = create('article', `sy-selector-result-card sy-selector-result-${match.status}`);
        const choice = create('label', 'sy-selector-choice');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = configuration.id;
        checkbox.dataset.selectorChoice = 'true';
        checkbox.setAttribute('aria-label', `Add ${configuration.name} to RFQ shortlist`);
        const choiceText = create('span', '', 'Add to RFQ');
        choice.append(checkbox, choiceText);
        const badge = create('span', 'sy-selector-match-badge', match.status === 'exact' ? 'Exact on selected fields' : 'Possible · confirm missing fields');
        const heading = create('h4', '', configuration.name);
        const summary = create('p', '', configuration.summary);
        const criteria = create('dl', 'sy-selector-match-list');
        Object.entries(currentFilters).forEach(([key, value]) => appendCriterion(criteria, key, value, configuration));
        const matrixLink = create('a', 'product-link', 'View in full matrix');
        matrixLink.href = `#${encodeURIComponent(configuration.id)}`;
        card.append(choice, badge, heading, summary, criteria, matrixLink);
        resultList.appendChild(card);
        checkbox.addEventListener('change', () => {
          if (checkbox.checked) selectedIds.add(configuration.id);
          else selectedIds.delete(configuration.id);
          updateRfq();
        });
      });
      results.hidden = false;
      updateRfq();
      emit('yuchen:filter-selector-result', {
        selectorId: payload.selectorId,
        resultBucket: matches.length ? (possibleCount ? (exactCount ? 'mixed' : 'possible') : 'exact') : 'none',
        resultCountBucket: resultCountBucket(matches.length),
        ctaLocation: 'filter_selector_result'
      });
      results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    const updateProgressiveFields = () => {
      const family = form.querySelector('[data-selector-filter="family"]')?.value || '';
      const viable = family
        ? payload.configurations.filter((configuration) => valuesFor(configuration, 'family').includes(family))
        : payload.configurations;
      form.querySelectorAll('[data-selector-filter]').forEach((select) => {
        const key = select.dataset.selectorFilter;
        if (key === 'family') return;
        const allowed = new Set(viable.flatMap((configuration) => valuesFor(configuration, key)));
        Array.from(select.options).slice(1).forEach((option) => { option.disabled = family ? !allowed.has(option.value) : false; });
        if (select.value && !allowed.has(select.value)) select.value = '';
        const wrapper = select.closest('[data-selector-field-wrap]');
        if (wrapper) wrapper.hidden = !family || allowed.size < 2;
      });
    };

    form.addEventListener('change', (event) => {
      start();
      if (event.target.matches('[data-selector-filter="family"]')) updateProgressiveFields();
    });
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      start();
      if (!form.reportValidity()) return;
      render();
    });
    form.addEventListener('reset', () => {
      window.setTimeout(() => {
        selectedIds.clear();
        currentFilters = {};
        results.hidden = true;
        rfq.hidden = true;
        copyStatus.textContent = '';
        updateProgressiveFields();
      }, 0);
    });
    copyButton.addEventListener('click', async () => {
      const selected = Array.from(selectedIds);
      if (!selected.length) return;
      try {
        await copyText(buildRfqSummary(payload, selected, currentFilters));
        copyStatus.textContent = 'RFQ summary copied.';
        emit('yuchen:filter-rfq-copy', {
          selectorId: payload.selectorId,
          selectedCount: selected.length,
          ctaLocation: 'filter_selector_result'
        });
      } catch (error) {
        copyStatus.textContent = 'Copy was unavailable. Continue to the inquiry form to keep the selected configuration IDs.';
      }
    });
    contactLink.addEventListener('click', (event) => {
      const selected = Array.from(selectedIds);
      if (!selected.length) {
        event.preventDefault();
        return;
      }
      emit('yuchen:filter-rfq-handoff', {
        selectorId: payload.selectorId,
        selectedCount: selected.length,
        ctaLocation: 'filter_selector_result'
      });
    });
    updateProgressiveFields();
  }

  document.querySelectorAll('[data-sy-filter-selector]').forEach(initialize);
})();
