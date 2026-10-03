/* Public product discovery. Compare the selected records here, never redirect. */
(() => {
 'use strict';
 const root=document.querySelector('[data-product-directory]'),q=document.querySelector('#product-search');
 if(!root||!q)return;
 const rows=[...root.querySelectorAll('[data-series-row]')],groups=[...root.querySelectorAll('[data-catalog-group]')];
 const button=document.querySelector('[data-compare-selected]'),status=document.querySelector('[data-compare-status]'),result=document.querySelector('[data-directory-result]'),empty=document.querySelector('[data-directory-empty]'),clear=document.querySelector('[data-clear-search]');
 const panel=document.querySelector('[data-journey-comparison]'),content=document.querySelector('[data-journey-comparison-content]'),modelResults=document.querySelector('[data-journey-search-results]'),models=document.querySelector('[data-journey-search-models]');
 let index=[],indexAvailable=false;
 const key=row=>row.querySelector('h4').textContent.trim()+'|'+row.querySelector('[data-series-select]').value;
 const selected=()=>rows.filter(row=>row.querySelector('[data-series-select]').checked);
 const save=()=>{try{sessionStorage.setItem('yuchen_directory_selection_v2',JSON.stringify({query:q.value,selected:selected().map(key)}));}catch{}};
 const restore=()=>{try{const s=JSON.parse(sessionStorage.getItem('yuchen_directory_selection_v2')||'{}');q.value=s.query||'';rows.forEach(row=>row.querySelector('[data-series-select]').checked=(s.selected||[]).slice(0,4).includes(key(row)));}catch{}};
 const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
 const renderModels=matches=>{
  models.replaceChildren();matches.forEach(p=>{const card=el('article');card.className='pj-model';const link=el('a'),img=el('img');link.href=p.route;img.src=p.image;img.alt=p.name;img.loading='lazy';link.append(img,el('h3',p.name));card.append(link);const dl=el('dl');p.facts.slice(0,3).forEach(([k,v])=>{const d=el('div');d.append(el('dt',k),el('dd',v));dl.append(d);});card.append(dl);models.append(card);});modelResults.hidden=!matches.length;
 };
 const filter=()=>{
  const value=q.value.trim().toLowerCase();rows.forEach(row=>row.hidden=!!value&&!row.textContent.toLowerCase().includes(value));
  groups.forEach(group=>{group.hidden=![...group.querySelectorAll('[data-series-row]')].some(row=>!row.hidden);if(value&&!group.hidden)group.open=true;});
  const matched=value?index.filter(p=>(p.name+' '+p.family+' '+p.facts.flat().join(' ')).toLowerCase().includes(value)):[];
  renderModels(matched);const count=rows.filter(row=>!row.hidden).length;
  result.textContent=value?`${count} series and ${matched.length} models match${indexAvailable?'':' — model search loading'}`:`${rows.length} series available; search model names or specifications`;
  empty.hidden=!value||count>0||matched.length>0||!indexAvailable;clear.disabled=!value;save();
 };
 const selection=()=>{const count=selected().length;status.textContent=count?`${count} series selected${count<2?' — select one more to compare.':'.'}`:'Select 2–4 series to compare.';button.setAttribute('data-selection-ready',String(count>=2));save();};
 const compare=()=>{
  const chosen=selected();if(chosen.length<2){status.textContent='Select at least two series to compare.';return;}
  content.replaceChildren();const table=el('table'),thead=el('thead'),head=el('tr');['Series','Published scope','Conditions to confirm','Models / details'].forEach(x=>head.append(el('th',x)));thead.append(head);const body=el('tbody');
  chosen.forEach(row=>{const tr=el('tr');const name=row.querySelector('h4').textContent.trim(),purpose=row.querySelector('.tx-series-copy p').textContent.trim(),conditions=row.querySelector('[data-confirm-boundary]').textContent.trim();tr.append(el('th',name),el('td',purpose||'To be confirmed'),el('td',conditions||'To be confirmed'));const td=el('td'),a=el('a','View Models');a.href=row.querySelector('[data-compare-series]').getAttribute('href');td.append(a);tr.append(td);body.append(tr);});
  table.append(thead,body);content.append(table);panel.hidden=false;panel.querySelector('h2').focus();panel.scrollIntoView({block:'start',behavior:'smooth'});
 };
 root.addEventListener('change',e=>{if(!e.target.matches('[data-series-select]'))return;if(selected().length>4){e.target.checked=false;status.textContent='Select up to four series.';return;}panel.hidden=true;selection();});
 button.addEventListener('click',compare);q.addEventListener('input',filter);clear.addEventListener('click',()=>{q.value='';filter();q.focus();});
 document.querySelectorAll('[data-search-trigger],a[href="#product-search"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();q.scrollIntoView({block:'center'});q.focus();}));
 const openHash=()=>{const id=location.hash.slice(1);const target=document.getElementById(id);if(target?.matches('details'))target.open=true;};
 window.addEventListener('hashchange',openHash);window.addEventListener('pageshow',()=>{restore();filter();selection();openHash();});restore();selection();openHash();filter();
 fetch('../assets/product-journey-index.json').then(r=>{if(!r.ok)throw Error('model index');return r.json();}).then(data=>{index=data;indexAvailable=true;filter();}).catch(()=>{indexAvailable=true;result.textContent='Model search unavailable. Browse the product families below.';empty.hidden=true;});
})();
