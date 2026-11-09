/* Add the owner's GA4 measurement ID only after their property is configured.
   Events never include form contents, calculator amounts or URL queries. */
(()=>{
'use strict';
const measurementId='';
window.nobletonTrack=()=>{};
if(!/^G-[A-Z0-9]+$/.test(measurementId))return;
const fr=document.documentElement.lang.startsWith('fr'),key='nobleton-analytics-consent';
let choice=null,loaded=false;
try{choice=localStorage.getItem(key);}catch{}
const allowed=new Set(['contact_click','inquiry_submit','valuation_request','consultation_request','mortgage_calculation','profile_view','listing_view']);
const safePath=()=>location.pathname;
function start(){
 if(loaded)return;loaded=true;window.dataLayer=window.dataLayer||[];
 window.gtag=function(){window.dataLayer.push(arguments);};
 window.gtag('js',new Date());window.gtag('config',measurementId,{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false});
 window.gtag('event','page_view',{page_location:location.origin+safePath(),page_title:document.title,page_referrer:''});
 window.nobletonTrack=(event,details={})=>{
  if(choice!=='accepted'||!allowed.has(event))return;
  const properties={source_page:safePath(),language:fr?'fr-CA':'en-CA',page_location:location.origin+safePath(),page_referrer:''};
  if(/^[a-z_-]{1,40}$/.test(details.inquiry_type||''))properties.inquiry_type=details.inquiry_type;
  window.gtag('event',event,properties);
 };
 const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id='+measurementId;document.head.append(script);
 if(/\/(real-estate|mortgages)\/$/.test(safePath()))window.nobletonTrack('profile_view');
}
const banner=document.createElement('aside');banner.className='analytics-banner';banner.setAttribute('aria-label',fr?'Statistiques facultatives':'Optional analytics');
const text=document.createElement('p');text.textContent=fr?'Autorisez-vous les statistiques de fréquentation? Les champs des formulaires et les montants saisis sont exclus.':'Allow usage analytics? Form contents and calculator amounts are excluded.';banner.append(text);
function choose(value){choice=value;try{localStorage.setItem(key,value);}catch{}banner.hidden=true;if(value==='accepted')start();else if(loaded){window['ga-disable-'+measurementId]=true;window.nobletonTrack=()=>{};location.reload();}}
for(const [value,label] of [['accepted',fr?'Autoriser':'Allow'],['declined',fr?'Refuser':'Decline']]){const b=document.createElement('button');b.type='button';b.textContent=label;b.className='button';b.onclick=()=>choose(value);banner.append(b);}
banner.hidden=choice!==null;document.body.append(banner);
document.querySelectorAll('.analytics-preferences').forEach(b=>{b.hidden=false;b.onclick=()=>{banner.hidden=false;banner.querySelector('button').focus();};});
if(choice==='accepted')start();
document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(a&&/^(tel:|mailto:|https:\/\/wa.me\/)/.test(a.getAttribute('href')))window.nobletonTrack('contact_click');});
})();
