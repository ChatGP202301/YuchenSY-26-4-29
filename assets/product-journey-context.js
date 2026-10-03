/* Use published stable IDs. Preserve entry and buyer's final choice separately. */
(() => {
 'use strict';
 const params=new URLSearchParams(location.search),form=document.querySelector('form.contact-form,[data-catalog-form],[data-sanyishui-catalog-form]');
 if(!form)return;
 let entry=null,selected=null;
 const hidden=(name,value)=>{let field=form.querySelector(`input[name="${name}"]`);if(!field){field=document.createElement('input');field.type='hidden';field.name=name;form.append(field);}field.value=value;};
 const sync=()=>{
  hidden('Entry Product ID',entry?.id||'');hidden('Entry Product',entry?.name||'');hidden('Selected Product ID',selected?.id||'');
  hidden('Selected Product',selected?.name||form.querySelector('[data-product-field]')?.value||select?.selectedOptions[0]?.textContent||'');hidden('Source Page',source);hidden('CTA Location',params.get('cta_location')||'product_context');
 };
 let source=location.pathname;
 try{const u=new URL(params.get('source_page')||params.get('yw_source_page')||location.pathname,location.href);if(u.origin===location.origin&&!/[@\\]/.test(u.pathname))source=u.pathname;}catch{}
 let select=null;
 const contextText=()=>entry||selected?`Entry product: ${entry?.id||'not specified'} (${entry?.name||'not specified'})\nSelected product: ${selected?.id||'needs-selection'} (${selected?.name||form.querySelector('[data-product-field]')?.value||select?.selectedOptions[0]?.textContent||'needs selection help'})\nSource page: ${source}\nCTA location: ${(params.get('cta_location')||'product_context').slice(0,100)}`:'';
 window.YuchenJourney=Object.freeze({message(value){const text=String(value||'');const context=contextText();return context?`${context}\n\n${text}`:text;}});
 fetch('../assets/product-journey-index.json').then(r=>{if(!r.ok)throw Error('product index');return r.json();}).then(index=>{
  const id=params.get('entry_product')||params.get('product_id')||params.get('product_slug');entry=index.find(p=>p.id===id||p.route.replace(/\.html$/,'')===id)||null;selected=entry;
  const label=document.createElement('label');label.className='pj-context-choice';label.textContent='Product for this request (optional)';select=document.createElement('select');select.dataset.journeySelected='';select.name='Journey Product';select.add(new Option('General product inquiry',''));select.add(new Option('I need help selecting a model','needs-selection'));index.forEach(p=>select.add(new Option(p.name,p.id)));select.value=entry?.id||'';label.append(select);
  const anchor=form.querySelector('h2');if(anchor)anchor.insertAdjacentElement('afterend',label);else form.prepend(label);
  const product=form.querySelector('[data-product-field]');if(entry&&product)product.value=entry.name;
  const specific=form.elements.specificProduct;const specificSelect=specific?.tagName==='SELECT'?specific:null;if(specificSelect&&!Array.from(specificSelect.options).some(o=>o.value==='needs-selection'))specificSelect.add(new Option('I need help selecting a model','needs-selection'));
  const unknown=['rawWaterTds','voltageFrequency'].map(n=>form.elements[n]).filter(Boolean);
  if(unknown.length){const assist=document.createElement('label'),box=document.createElement('input');box.type='checkbox';box.dataset.journeyUnknown='';assist.className='pj-context-choice';assist.append(box,document.createTextNode('I do not know the water TDS or electrical requirements yet — please help confirm.'));label.after(assist);box.addEventListener('change',()=>unknown.forEach(field=>{if(box.checked&&!field.value)field.value='Not yet known — please advise';else if(!box.checked&&field.value==='Not yet known — please advise')field.value='';}));}
  if(entry&&specificSelect&&[...specificSelect.options].some(o=>o.value===entry.route.replace(/\.html$/,'')))specificSelect.value=entry.route.replace(/\.html$/,'');else if(entry&&specific&&!specificSelect)specific.value=entry.name;
  select.addEventListener('change',()=>{selected=index.find(p=>p.id===select.value)||null;if(product)product.value=selected?.name||(select.value==='needs-selection'?'I need help selecting a model':'');if(specificSelect&&select.value==='needs-selection')specificSelect.value='needs-selection';if(specificSelect&&selected&&[...specificSelect.options].some(o=>o.value===selected.route.replace(/\.html$/,'')))specificSelect.value=selected.route.replace(/\.html$/,'');if(specific&&!specificSelect)specific.value=selected?.name||'I need help selecting a model';sync();});
  if(product)product.addEventListener('input',()=>{if(product.value!==selected?.name){selected=null;select.value='needs-selection';sync();}});
  if(specific)specific.addEventListener('change',()=>{selected=index.find(p=>specificSelect?p.route.replace(/\.html$/,'')===specific.value:p.name===specific.value)||null;select.value=selected?.id||'needs-selection';sync();});
  if(entry){const patterns=[[/\b(?:GAC|UDF)\b/i,'gac-udf'],[/\bCTO\b/i,'cto'],[/\bT33\b/i,'t33'],[/\bUF\b/i,'uf'],[/RO.*Membrane/i,'ro'],[/\bPP\b/i,'pp']];const interest=patterns.find(([pattern])=>pattern.test(entry.name));if(interest&&!form.querySelector('input[name="interests"]:checked')){const box=Array.from(form.querySelectorAll('input[name="interests"]')).find(b=>b.value===interest[1]);if(box)box.checked=true;}}
  sync();form.dataset.journeyContextReady='true';
 }).catch(()=>{const p=document.createElement('p');p.setAttribute('role','status');p.textContent='Product context could not load. Please include the model name in your request.';form.prepend(p);});
 form.addEventListener('submit',e=>{
  sync();const message=form.querySelector('[name="message"]');if(message){const payload=window.YuchenJourney.message(message.value);if(payload.length>2000){e.preventDefault();e.stopImmediatePropagation();message.setCustomValidity('Please shorten the requirements so product context and your message fit within 2000 characters.');message.reportValidity();return;}message.setCustomValidity('');}
 },true);
})();
