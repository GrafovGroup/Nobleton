(()=>{
'use strict';
const fr=document.documentElement.lang.startsWith('fr');
const form=document.querySelector('.professional-form');
if(form){
 form.elements.source_page.value=location.pathname;
 form.elements.preferred_language.value=fr?'fr-CA':'en-CA';
 if(form.elements.topic && new URLSearchParams(location.search).get('topic')==='question') form.elements.topic.value='question';
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(!form.reportValidity())return;
  const btn=form.querySelector('button[type=submit]'),status=form.querySelector('.professional-status'),label=btn.textContent;
  if(btn.disabled)return;btn.disabled=true;btn.textContent=fr?'Envoi en cours…':'Sending…';status.textContent='';
  try{
   const response=await fetch(form.action,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
   let data;try{data=await response.json();}catch{throw new Error('failed');}
   if(!response.ok||data.ok!==true)throw new Error(data.error||'failed');
   window.nobletonTrack?.('inquiry_submit',{inquiry_type:form.dataset.kind});
   if(form.dataset.kind==='valuation')window.nobletonTrack?.('valuation_request',{inquiry_type:'valuation'});
   if(form.dataset.kind==='mortgage')window.nobletonTrack?.('consultation_request',{inquiry_type:form.elements.topic.value});
   form.reset();form.elements.source_page.value=location.pathname;form.elements.preferred_language.value=fr?'fr-CA':'en-CA';
   status.textContent=fr?'Merci. Votre demande a été transmise au service de messagerie pour le professionnel choisi.':'Thank you. Your request has been handed to our mail service for the selected professional.';
   status.setAttribute('role','status');
  }catch(err){
   status.setAttribute('role','alert');status.textContent=err.message==='rate_limit'?(fr?'Trop de demandes. Réessayez plus tard ou utilisez le lien courriel ci-dessous.':'Too many requests. Try again later or use the email link below.'):(fr?'L’envoi n’a pas pu être confirmé. Vos renseignements sont conservés dans ce formulaire. Réessayez ou utilisez le lien courriel ci-dessous.':'We could not confirm submission. Your entries are still in this form. Please retry or use the email link below.');
  }finally{btn.disabled=false;btn.textContent=label;status.focus({preventScroll:true});}
 });
}
const events=[...document.querySelectorAll('[data-event-date]')];
const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
events.forEach(event=>event.hidden=event.dataset.eventDate<today);
const empty=document.getElementById('no-upcoming-events');if(empty)empty.hidden=events.some(e=>!e.hidden);
})();
