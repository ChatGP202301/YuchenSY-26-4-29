
/* SITE_DISCOVERY_LOADER_START */
(function(){
  if(new URLSearchParams(location.search).get('yw_download_embed')==='1') return;
  if(document.querySelector('[data-yuchen-discovery]')) return;
  var own=document.currentScript;
  if(!own || !own.src) return;
  var base=new URL('.',own.src), style=document.createElement('link');
  style.rel='stylesheet'; style.href=new URL('site-discovery.css?v=60a325121fd06700',base).href;
  style.dataset.yuchenDiscovery='style';
  style.onload=function(){var script=document.createElement('script');
    script.src=new URL('site-discovery.js?v=60a325121fd06700',base).href;
    script.dataset.yuchenDiscovery='runtime'; document.head.appendChild(script);};
  document.head.appendChild(style);
})();
/* SITE_DISCOVERY_LOADER_END */
