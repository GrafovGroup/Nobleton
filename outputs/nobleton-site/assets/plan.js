(()=>{
'use strict';
const fr=document.documentElement.lang.startsWith('fr');
const form=document.querySelector('.professional-form');
if(form){
 form.elements.source_page.value=location.pathname;
 const listingRef=new URLSearchParams(location.search).get('listing');
 if(form.dataset.kind==='realtor'&&listingRef&&/^[A-Za-z0-9_-]{1,80}$/.test(listingRef)&&!form.elements.message.value)form.elements.message.value=(fr?'Je souhaite en savoir plus sur la propriété MLS® ':'I would like to learn more about MLS® ')+listingRef+'.';

 form.elements.preferred_language.value=fr?'fr-CA':'en-CA';
 if(form.elements.topic && new URLSearchParams(location.search).get('topic')==='question') form.elements.topic.value='question';
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(!form.reportValidity())return;
  const btn=form.querySelector('button[type=submit]'),status=form.querySelector('.professional-status'),label=btn.textContent;
  if(btn.disabled)return;btn.disabled=true;form.setAttribute('aria-busy','true');btn.textContent=fr?'Envoi en cours…':'Sending…';status.textContent='';
  try{
   const response=await fetch(form.action,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
   let data;try{data=await response.json();}catch{throw new Error('failed');}
   if(!response.ok||data.ok!==true)throw new Error(data.error||'failed');
   window.nobletonTrack?.('inquiry_submit',{inquiry_type:form.dataset.kind});
   window.nobletonTrack?.('generate_lead',{inquiry_type:form.dataset.kind});
   if(form.dataset.kind==='valuation')window.nobletonTrack?.('valuation_request',{inquiry_type:'valuation'});
   if(form.dataset.kind==='mortgage')window.nobletonTrack?.('consultation_request',{inquiry_type:form.elements.topic.value});
   form.reset();form.elements.source_page.value=location.pathname;form.elements.preferred_language.value=fr?'fr-CA':'en-CA';
   status.textContent=fr?'Merci. Votre demande a été transmise au service de messagerie pour le professionnel choisi.':'Thank you. Your request has been handed to our mail service for the selected professional.';
   status.setAttribute('role','status');
  }catch(err){
   status.setAttribute('role','alert');status.textContent=err.message==='rate_limit'?(fr?'Trop de demandes. Réessayez plus tard ou utilisez le lien courriel ci-dessous.':'Too many requests. Try again later or use the email link below.'):(fr?'L’envoi n’a pas pu être confirmé. Vos renseignements sont conservés dans ce formulaire. Réessayez ou utilisez le lien courriel ci-dessous.':'We could not confirm submission. Your entries are still in this form. Please retry or use the email link below.');
  }finally{form.removeAttribute('aria-busy');btn.disabled=false;btn.textContent=label;status.focus({preventScroll:true});}
 });
}
const events = [...document.querySelectorAll('[data-event-date]')];
const localDate = new Intl.DateTimeFormat('en-CA', {
 timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit'
}).formatToParts(new Date());
const {year, month, day} = Object.fromEntries(localDate.map(({type, value}) => [type, value]));
const today = `${year}-${month}-${day}`;
const upcoming = events.filter(event => {
 event.hidden = event.dataset.eventDate < today;
 return !event.hidden;
});

const weekendList = document.getElementById('weekend-event-list');
if (weekendList) {
 // Use UTC only for calendar arithmetic after deriving today's date in Toronto.
 const saturday = new Date(`${today}T00:00:00Z`);
 const weekday = saturday.getUTCDay();
 saturday.setUTCDate(saturday.getUTCDate() + (weekday === 0 ? -1 : 6 - weekday));
 const sunday = new Date(saturday);
 sunday.setUTCDate(sunday.getUTCDate() + 1);
 const start = saturday.toISOString().slice(0, 10);
 const end = sunday.toISOString().slice(0, 10);
 const weekend = upcoming.filter(event => event.dataset.eventStart <= end && event.dataset.eventDate >= start);
 weekendList.append(...weekend);
 document.getElementById('no-weekend-events').hidden = weekend.length > 0;
 document.getElementById('upcoming-events').hidden = weekend.length === upcoming.length;
}

const limitedList = document.querySelector('[data-event-limit]');
if (limitedList) {
 const limit = Number(limitedList.dataset.eventLimit);
 upcoming.slice(limit).forEach(event => event.hidden = true);
}
const empty = document.getElementById('no-upcoming-events');
if (empty) empty.hidden = upcoming.length > 0;
})();
