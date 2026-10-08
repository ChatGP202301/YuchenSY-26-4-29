/* Public product discovery. Compare the selected records here, never redirect. */
(() => {
 'use strict';
 const root=document.querySelector('[data-product-directory]'),q=document.querySelector('#product-search');
 if(!root||!q)return;
 const rows=[...root.querySelectorAll('[data-series-row]')],groups=[...root.querySelectorAll('[data-catalog-group]')];
 const button=document.querySelector('[data-compare-selected]'),status=document.querySelector('[data-compare-status]'),result=document.querySelector('[data-directory-result]'),empty=document.querySelector('[data-directory-empty]'),clear=document.querySelector('[data-clear-search]');
 const panel=document.querySelector('[data-journey-comparison]'),content=document.querySelector('[data-journey-comparison-content]'),modelResults=document.querySelector('[data-journey-search-results]'),models=document.querySelector('[data-journey-search-models]');
 let index=[],indexAvailable=false,indexError=false;
 const key=row=>row.querySelector('h4').textContent.trim()+'|'+row.querySelector('[data-series-select]').value;
 const selected=()=>rows.filter(row=>row.querySelector('[data-series-select]').checked);
 const save=()=>{try{sessionStorage.setItem('yuchen_directory_selection_v2_vi',JSON.stringify({query:q.value,selected:selected().map(key)}));}catch{}};
 const restore=()=>{try{const s=JSON.parse(sessionStorage.getItem('yuchen_directory_selection_v2_vi')||'{}');q.value=s.query||'';rows.forEach(row=>row.querySelector('[data-series-select]').checked=(s.selected||[]).slice(0,4).includes(key(row)));}catch{}};
 const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
 const renderModels=matches=>{
  models.replaceChildren();matches.forEach(p=>{const card=el('article');card.className='pj-model';const link=el('a'),img=el('img');link.href='/vi/'+p.route;img.src=p.image;img.alt=p.name;img.loading='lazy';link.append(img,el('h3',p.name));card.append(link);const dl=el('dl');p.facts.slice(0,3).forEach(([k,v])=>{const d=el('div');d.append(el('dt',k),el('dd',v));dl.append(d);});card.append(dl);models.append(card);});modelResults.hidden=!matches.length;
 };
 const filter=()=>{
  const value=q.value.trim().toLowerCase();rows.forEach(row=>row.hidden=!!value&&!row.textContent.toLowerCase().includes(value));
  groups.forEach(group=>{group.hidden=![...group.querySelectorAll('[data-series-row]')].some(row=>!row.hidden);if(value&&!group.hidden)group.open=true;});
  const matched=value?index.filter(p=>(p.name+' '+(p.englishName||'')+' '+(p.familyLabel||'')+' '+p.family+' '+p.facts.flat().join(' ')).toLowerCase().includes(value)):[];
  renderModels(matched);const count=rows.filter(row=>!row.hidden).length;
  result.textContent=value?`Có ${count} dòng sản phẩm và ${matched.length} model phù hợp${indexAvailable?'':' — đang tải dữ liệu tìm kiếm model sản phẩm'}`:`Có ${rows.length} dòng sản phẩm; tìm theo tên model hoặc thông số kỹ thuật`;
  if(indexError)result.textContent='Không thể tìm kiếm model sản phẩm lúc này. Vui lòng xem các dòng sản phẩm bên dưới.';
  empty.hidden=indexError||!value||count>0||matched.length>0||!indexAvailable;clear.disabled=!value;save();
 };
 const selection=()=>{const count=selected().length;status.textContent=count?`Đã chọn ${count} dòng sản phẩm${count<2?' — chọn thêm một dòng để so sánh.':'.'}`:'Chọn 2–4 dòng sản phẩm để so sánh.';button.setAttribute('data-selection-ready',String(count>=2));save();};
 const compare=()=>{
  const chosen=selected();if(chosen.length<2){status.textContent='Chọn ít nhất hai dòng sản phẩm để so sánh.';return;}
  content.replaceChildren();const table=el('table'),thead=el('thead'),head=el('tr');['Dòng sản phẩm','Phạm vi sản phẩm đã công bố','Điều kiện cần xác nhận','Mẫu sản phẩm / chi tiết'].forEach(x=>head.append(el('th',x)));thead.append(head);const body=el('tbody');
  chosen.forEach(row=>{const tr=el('tr');const name=row.querySelector('h4').textContent.trim(),purpose=row.querySelector('.tx-series-copy p').textContent.trim(),conditions=row.querySelector('[data-confirm-boundary]').textContent.trim();tr.append(el('th',name),el('td',purpose||'Cần xác nhận'),el('td',conditions||'Cần xác nhận'));const td=el('td'),a=el('a','Xem các model sản phẩm');a.href=row.querySelector('[data-compare-series]').getAttribute('href');td.append(a);tr.append(td);body.append(tr);});
  table.append(thead,body);content.append(table);panel.hidden=false;panel.querySelector('h2').focus();panel.scrollIntoView({block:'start',behavior:'smooth'});
 };
 root.addEventListener('change',e=>{if(!e.target.matches('[data-series-select]'))return;if(selected().length>4){e.target.checked=false;status.textContent='Chọn tối đa bốn dòng sản phẩm.';return;}panel.hidden=true;selection();});
 button.addEventListener('click',compare);q.addEventListener('input',filter);clear.addEventListener('click',()=>{q.value='';filter();q.focus();});
 document.querySelectorAll('[data-search-trigger],a[href="#product-search"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();q.scrollIntoView({block:'center'});q.focus();}));
 const openHash=()=>{const id=location.hash.slice(1);const target=document.getElementById(id);if(target?.matches('details'))target.open=true;};
 window.addEventListener('hashchange',openHash);window.addEventListener('pageshow',()=>{restore();filter();selection();openHash();});restore();selection();openHash();filter();
 fetch(new URL('/assets/product-journey-index.vi.json', location.origin)).then(r=>{if(!r.ok)throw Error('model index');return r.json();}).then(data=>{if(!Array.isArray(data)||!data.length)throw Error('empty model index');index=data;indexAvailable=true;filter();}).catch(()=>{indexError=true;indexAvailable=false;result.textContent='Không thể tìm kiếm model sản phẩm lúc này. Vui lòng xem các nhóm sản phẩm bên dưới.';empty.hidden=true;});
})();
