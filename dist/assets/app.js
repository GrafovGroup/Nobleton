const menu=document.querySelector('.menu-toggle');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('#navigation').classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}});
const filter=document.querySelector('.directory-filter');
if(filter){
 const input=document.querySelector('#directory-search'), category=document.querySelector('#category'), entries=[...document.querySelectorAll('#directory-results .listing')];
 const robots=document.querySelector('meta[name=robots]'), defaultRobots=robots.content;
 const params=new URLSearchParams(location.search);input.value=params.get('q')||'';
 if([...category.options].some(o=>o.value===params.get('category')))category.value=params.get('category');
 const update=()=>{const q=input.value.trim().toLowerCase(),cat=category.value;let count=0;entries.forEach(entry=>{const visible=(!q||entry.dataset.search.includes(q))&&(cat==='All categories'||entry.dataset.category===cat);entry.hidden=!visible;if(visible)count++});document.querySelector('#result-count').textContent=`${count} ${count===1?'entry':'entries'}${q?' matching “'+input.value.trim()+'”':''}`;document.querySelector('#empty-state').hidden=count>0;const next=new URLSearchParams();if(q)next.set('q',input.value.trim());if(cat!=='All categories')next.set('category',cat);robots.content=(q||cat!=='All categories')?'noindex,follow':defaultRobots;history.replaceState(null,'',location.pathname+(next.size?'?'+next.toString():''))};
 filter.addEventListener('reset',()=>{input.value='';category.value='All categories';update();});
 filter.addEventListener('submit',e=>{e.preventDefault();update()});input.addEventListener('input',update);category.addEventListener('change',update);update();
}
// Progressive enhancement: native POST still works if the helper cannot load.
if(document.querySelector('#inquiry-form')){
 window.formspree=window.formspree||function(){(window.formspree.q=window.formspree.q||[]).push(arguments)};
 window.formspree('initForm',{formElement:'#inquiry-form',formId:'xljjnzbr'});
}
// Analytics integration point: listen for this event after a provider and privacy settings are approved.
// Only action identifiers are emitted; search terms, email addresses and form contents are excluded.
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const event=a.href.startsWith('mailto:')?'email_intent':a.pathname==='/submit/'?'listing_interest':a.pathname==='/find-a-service/'?'service_interest':null;if(event)document.dispatchEvent(new CustomEvent('nobleton:action',{detail:{action:event}}));});

const nav=document.querySelector('#navigation');
nav?.addEventListener('click',e=>{if(e.target.closest('a')&&menu?.getAttribute('aria-expanded')==='true'){menu.setAttribute('aria-expanded','false');nav.classList.remove('open')}});
