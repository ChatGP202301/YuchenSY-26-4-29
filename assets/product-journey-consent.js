/* Reposition only: existing consent choices and storage remain authoritative. */
(()=>{'use strict';const place=()=>{const banner=document.querySelector('.yuchen-consent-banner');if(banner&&document.body.firstElementChild!==banner)document.body.prepend(banner);};place();new MutationObserver(place).observe(document.body,{childList:true});})();
