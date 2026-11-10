/* Temporary Remembrance Day tribute. Expires once; does not recur annually. */
(()=>{
 'use strict';
 const expiresAt=Date.parse('2026-11-15T02:55:29Z');
 if(Date.now()>=expiresAt)return;
 const brand=document.querySelector('header > .brand');
 if(!brand)return;
 const french=document.documentElement.lang.startsWith('fr');
 const label=french?'Jour du Souvenir — Nous nous souviendrons':'Remembrance Day — Lest we forget';
 const style=document.createElement('style');
 style.textContent='.remembrance-brand{display:inline-flex;align-items:center;gap:13px;flex-shrink:0}.remembrance-brand>.brand{white-space:nowrap}.remembrance-poppy{display:inline-flex;width:44px;height:44px;flex:none;align-items:center;justify-content:center}.remembrance-poppy img{display:block;width:100%;height:100%;object-fit:contain}@media(max-width:480px){.remembrance-brand{gap:9px}.remembrance-poppy{width:34px;height:34px}}';
 document.head.append(style);
 const group=document.createElement('div');group.className='remembrance-brand';
 brand.replaceWith(group);group.append(brand);
 const poppy=document.createElement('span');poppy.className='remembrance-poppy';poppy.setAttribute('role','img');poppy.setAttribute('aria-label',label);poppy.title=label;
 poppy.innerHTML='<img src="/assets/images/remembrance-poppy.webp" width="44" height="44" alt="" decoding="async">';
 group.append(poppy);
 function remove(){group.replaceWith(brand);style.remove();document.removeEventListener('visibilitychange',check);clearTimeout(timer);}
 function check(){if(Date.now()>=expiresAt)remove();}
 const timer=setTimeout(remove,Math.max(0,expiresAt-Date.now()));
 document.addEventListener('visibilitychange',check);
})();
