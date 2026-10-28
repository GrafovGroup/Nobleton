const isFrench=document.documentElement.lang.toLowerCase().startsWith('fr');
const normalized=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const menu=document.querySelector('.menu-toggle');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('#navigation').classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}});
const filter=document.querySelector('.directory-filter');
if(filter){
 const input=document.querySelector('#directory-search'), category=document.querySelector('#category'), entries=[...document.querySelectorAll('#directory-results .listing')];
 const robots=document.querySelector('meta[name=robots]'), defaultRobots=robots.content;
 const params=new URLSearchParams(location.search);input.value=params.get('q')||'';
 if([...category.options].some(o=>o.value===params.get('category')))category.value=params.get('category');
 const update=()=>{const q=normalized(input.value.trim()),cat=category.value;let count=0;entries.forEach(entry=>{const visible=(!q||normalized(entry.dataset.search).includes(q))&&(cat==='All categories'||entry.dataset.category===cat);entry.hidden=!visible;if(visible)count++});document.querySelector('#result-count').textContent=isFrench?`${count} ${count===1?'fiche':'fiches'}${q?' pour « '+input.value.trim()+' »':''}`:`${count} ${count===1?'entry':'entries'}${q?' matching “'+input.value.trim()+'”':''}`;document.querySelector('#empty-state').hidden=count>0;const next=new URLSearchParams();if(q)next.set('q',input.value.trim());if(cat!=='All categories')next.set('category',cat);robots.content=(q||cat!=='All categories')?'noindex,follow':defaultRobots;history.replaceState(null,'',location.pathname+(next.size?'?'+next.toString():''))};
 filter.addEventListener('reset',()=>{input.value='';category.value='All categories';update();});
 filter.addEventListener('submit',e=>{e.preventDefault();update()});input.addEventListener('input',update);category.addEventListener('change',update);update();
}
// Progressive enhancement: native POST still works if the helper cannot load.
if(document.querySelector('#inquiry-form')){
 window.formspree=window.formspree||function(){(window.formspree.q=window.formspree.q||[]).push(arguments)};
 const showError=({form})=>{
  const error=form.querySelector('[data-fs-error=""]');
  error.textContent=isFrench?'L’envoi n’a pas pu être confirmé. Vérifiez vos renseignements et réessayez. Vous pouvez aussi écrire à info@nobleton.ca.':'We could not confirm your submission. Check your details and try again, or email info@nobleton.ca.';
  error.style.display='block';error.setAttribute('tabindex','-1');error.focus();
 };
 window.formspree('initForm',{
  formElement:'#inquiry-form',formId:'xljjnzbr',
  disable:({form})=>{
   const button=form.querySelector('[type="submit"]');button.dataset.label=button.textContent;button.disabled=true;button.textContent=isFrench?'Envoi en cours…':'Sending…';form.setAttribute('aria-busy','true');
   form.querySelectorAll('[data-fs-error]').forEach(e=>{e.textContent='';e.style.display='none'});form.querySelector('[data-fs-success]').style.display='none';
  },
  enable:({form})=>{const button=form.querySelector('[type="submit"]');button.disabled=false;if(button.dataset.label)button.textContent=button.dataset.label;form.removeAttribute('aria-busy')},
  renderSuccess:({form})=>{form.reset();const success=form.querySelector('[data-fs-success]');success.style.display='block';success.focus()},
  renderFieldErrors:showError,renderFormError:showError,onFailure:showError
 });
}
// Analytics integration point: listen for this event after a provider and privacy settings are approved.
// Only action identifiers are emitted; search terms, email addresses and form contents are excluded.
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const event=a.href.startsWith('mailto:')?'email_intent':a.pathname==='/submit/'?'listing_interest':a.pathname==='/find-a-service/'?'service_interest':null;if(event)document.dispatchEvent(new CustomEvent('nobleton:action',{detail:{action:event}}));});

const nav=document.querySelector('#navigation');
nav?.addEventListener('click',e=>{if(e.target.closest('a')&&menu?.getAttribute('aria-expanded')==='true'){menu.setAttribute('aria-expanded','false');nav.classList.remove('open')}});

// Keep the same page, directory filters and section when switching language.
document.querySelectorAll('.language-switch a').forEach(link=>{
 link.addEventListener('click',()=>{const target=new URL(link.href);target.search=location.search;target.hash=location.hash;link.href=target.href});
});
