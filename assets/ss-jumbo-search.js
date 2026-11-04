/* Page-local presentation of the existing English search. */
(()=>{'use strict';
 const trigger=document.querySelector('[data-ss-search-open]');
 const dialog=document.querySelector('[data-ss-search-dialog]');
 if(!trigger||!dialog)return;
 const close=dialog.querySelector('[data-ss-search-close]');
 function attach(){
  const panel=document.querySelector('.en-product-search');
  if(!panel)return false;
  panel.open=true;
  panel.querySelector('summary').hidden=true;
  dialog.querySelector('[data-ss-search-content]').append(panel);
  const field=panel.querySelector('input');
  field.placeholder='e.g. housing, carbon filter, RO membrane';
  trigger.disabled=false;
  return true;
 }
 if(!attach()){
  const observer=new MutationObserver(()=>{if(attach())observer.disconnect()});
  observer.observe(document.body,{childList:true,subtree:true});
 }
 trigger.addEventListener('click',()=>{dialog.showModal();dialog.querySelector('input')?.focus()});
 close.addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close()}});
 dialog.addEventListener('close',()=>trigger.focus());
})();
