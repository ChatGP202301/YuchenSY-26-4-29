"""Render the English accessory quote form using the site's contact transport."""
from html import escape
import re

DETAILS = {
    'housing-union': ('Filter housing model and port or thread marking', 'PP-R pipe marking or measured outside diameter'),
    'reducing-elbow': ('Mating port or thread marking', 'PE tube marking or measured outside diameter'),
    'inline-pressure-reducing-valve': ('RO model and inlet/outlet tube outside diameters', 'Measured upstream pressure (with unit)', 'Requested downstream pressure (with unit)'),
    'four-port-valve': ('RO or valve model', 'Existing port connections, port markings or available circuit drawing'),
    'leak-shutoff-device': ('Purifier model', 'Feed-tube outside diameter', 'Proposed shutoff location'),
}

STYLE = """<style>
.wa-quote{max-width:760px;margin:2rem auto;padding:clamp(1rem,4vw,2rem);border:1px solid #cadbda;border-radius:12px;background:#fff}
.wa-quote form,.wa-quote-specs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
.wa-quote-wide,.wa-quote form>p,.wa-quote .form-honeypot,.wa-quote-specs{grid-column:1/-1}
.wa-quote label{display:block;min-width:0;font-weight:600}
.wa-quote label :is(input,textarea,select){display:block;width:100%;box-sizing:border-box;min-height:44px;margin-top:.4rem}
.wa-quote [hidden]{display:none!important}
.wa-quote button{justify-self:start}
@media(max-width:600px){.wa-quote form,.wa-quote-specs{grid-template-columns:minmax(0,1fr)}}
</style>"""

SCRIPT = """<script>
(() => {
  const form = document.getElementById('accessory-quote-form');
  const status = form.elements['Specification status'];
  const specs = form.querySelector('.wa-quote-specs');
  function update() {
    const known = status.value === 'known';
    specs.hidden = !known;
    for (const field of specs.querySelectorAll('input, select')) {
      field.disabled = !known;
      if (!known) field.value = '';
    }
  }
  status.addEventListener('change', update);
  form.addEventListener('reset', () => setTimeout(update, 0));
  form.addEventListener('submit', event => {
    for (const field of form.querySelectorAll('input[required], textarea[required]')) {
      if (field.disabled || field.value.trim()) continue;
      event.preventDefault();
      event.stopImmediatePropagation();
      field.setCustomValidity('Please enter a value.');
      field.reportValidity();
      break;
    }
  });
  form.addEventListener('input', event => event.target.setCustomValidity?.(''));
  update();
})();
</script>"""


def render_accessory_quote(slug, name, contact_html):
    existing = re.search(r'<form\b[^>]*\bid="quoteForm"[^>]*>.*?</form>', contact_html, re.S)[0]
    opening = existing.split('>', 1)[0].replace('id="quoteForm"', 'id="accessory-quote-form"')
    hidden = []
    for tag in re.findall(r'<input\b[^>]*>', existing):
        if 'type="hidden"' not in tag:
            continue
        if re.search(r'\bname="(?:Product Configuration|Product Slug|Product Family|CTA Location|Form Type|_subject)"', tag):
            continue
        hidden.append(tag)
    hidden += [
        '<input type="hidden" name="_subject" value="New accessory quote request – Yuchen Water">',
        '<input type="hidden" name="Form Type" value="accessory quote">',
        f'<input type="hidden" name="Product ID" value="{slug}">',
        f'<input type="hidden" name="Product Slug" value="{slug}">',
        '<input type="hidden" name="Product Family" value="water-accessories">',
        '<input type="hidden" name="CTA Location" value="accessory_form">',
        f'<input type="hidden" name="Product Source" value="/en/{slug}.html">',
        f'<input type="hidden" name="product" value="{escape(name)}">',
        '<div class="form-honeypot" aria-hidden="true"><label>Website<input type="text" name="_honey" tabindex="-1" autocomplete="off" data-spam-trap></label></div>',
    ]
    specs = ''.join(f'<label>{escape(label)}<input name="{escape(label)}" maxlength="160" required disabled></label>' for label in DETAILS[slug])
    if slug == 'reducing-elbow':
        specs = '<label>Requested elbow version<select name="Product Configuration" required disabled><option value="">Choose a version</option><option>1/2″ (left in photo)</option><option>3/8″ (right in photo)</option></select></label>' + specs
    return f'''{STYLE}<section class="wa-quote" id="accessory-quote" aria-labelledby="accessory-quote-title">
<h2 id="accessory-quote-title">Request a quote for {escape(name)}</h2>
<p>All displayed fields are required. Select “Not sure” if you need help identifying the specification.</p>
{opening}>{''.join(hidden)}
<label>Company / buyer<input name="company" autocomplete="organization" required></label>
<label>Work email<input name="email" type="email" autocomplete="email" required></label>
<label>WhatsApp<input name="whatsapp" type="tel" autocomplete="tel" data-whatsapp-field="true" maxlength="26" placeholder="+ country code and number" required></label>
<label>Country<input name="country" autocomplete="country-name" required></label>
<label>Estimated quantity<input name="quantity" required></label>
<label>Specification status<select name="Specification status" required><option value="">Choose one</option><option value="known">I know the specification</option><option value="unsure">Not sure — help me identify it</option></select></label>
<div class="wa-quote-specs" hidden>{specs}</div>
<label class="wa-quote-wide">Notes or evidence available<textarea name="message" rows="3" required placeholder="Equipment model, markings, or photos you can share with sales"></textarea></label>
<button type="submit" class="btn btn-gold">Send inquiry</button>
<p class="form-error" hidden></p><p class="form-success" hidden></p>
</form></section>{SCRIPT}'''
