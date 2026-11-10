/* Consent-first GA4. Only predefined event metadata is collected. */
(()=>{
'use strict';
const measurementId='G-W01L22WKDM';
window.nobletonTrack=()=>{};
if(!['nobleton.ca','www.nobleton.ca'].includes(location.hostname))return;
const fr=document.documentElement.lang.startsWith('fr'),key='nobleton-analytics-consent';
let choice=null,loaded=false;
try{choice=localStorage.getItem(key);}catch{}
if(!['accepted','declined'].includes(choice))choice=null;
const allowed=new Set(['contact_click','inquiry_submit','generate_lead','valuation_request','consultation_request','mortgage_calculation','profile_view','listing_view','directory_action','directory_search','advertising_interest']);
const values={inquiry_type:['business','service','advertising','realtor','valuation','mortgage','purchase','renewal','refinance','investment','self-employed','question'],contact_method:['phone','email','whatsapp'],action:['phone','website','directions'],placement:['featured','category','guide'],category:['Schools','Community','Parks & recreation','Business resources','Home services','Food & drink','Health & wellness','Shopping','Automotive','Pet care','All categories']};
const safePath=()=>location.pathname;
function safeReferrer(){try{return document.referrer?new URL(document.referrer).origin+'/':'';}catch{return '';}}
function start(){
 if(loaded)return;loaded=true;window.dataLayer=window.dataLayer||[];
 window.gtag=function(){window.dataLayer.push(arguments);};
 window.gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
 window.gtag('js',new Date());
 window.gtag('config',measurementId,{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:location.origin+safePath(),page_referrer:safeReferrer(),page_title:document.title});
 window.gtag('event','page_view',{page_location:location.origin+safePath(),page_title:document.title,page_referrer:safeReferrer()});
 window.nobletonTrack=(event,details={})=>{
  if(choice!=='accepted'||!allowed.has(event))return;
  const properties={source_page:safePath(),language:fr?'fr-CA':'en-CA',page_location:location.origin+safePath(),page_referrer:safeReferrer()};
  for(const [key,choices] of Object.entries(values))if(choices.includes(details[key]))properties[key]=details[key];
  window.gtag('event',event,properties);
 };
 const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id='+measurementId;document.head.append(script);
 if(/\/(real-estate|mortgages)\/$/.test(safePath()))window.nobletonTrack('profile_view');
 if(/^\/(?:fr\/)?directory\/[^/]+\/$/.test(safePath()))window.nobletonTrack('listing_view');
}
const banner=document.createElement('aside');banner.className='analytics-banner';banner.setAttribute('aria-label',fr?'Statistiques facultatives':'Optional analytics');
const text=document.createElement('p');text.textContent=fr?'Autorisez-vous les statistiques de fréquentation avec Google Analytics? Les champs des formulaires et les montants saisis sont exclus.':'Allow usage analytics with Google Analytics? Form contents and calculator amounts are excluded.';
const privacy=document.createElement('a');privacy.href=(fr?'/fr':'')+'/privacy/';privacy.textContent=fr?'Confidentialité':'Privacy';text.append(' ',privacy);banner.append(text);
function removeCookies(){
 for(const entry of document.cookie.split(';')){const name=entry.split('=')[0].trim();if(!/^_ga(?:_|$)/.test(name))continue;
  for(const domain of ['',location.hostname,'.'+location.hostname,'.nobleton.ca'])document.cookie=name+'=; Max-Age=0; path=/'+(domain?'; domain='+domain:'')+'; SameSite=Lax';}
}
function choose(value){choice=value;try{localStorage.setItem(key,value);}catch{}banner.hidden=true;if(value==='accepted'){window['ga-disable-'+measurementId]=false;start();}else{window['ga-disable-'+measurementId]=true;window.nobletonTrack=()=>{};removeCookies();if(loaded)location.reload();}}
for(const [value,label] of [['accepted',fr?'Autoriser':'Allow'],['declined',fr?'Refuser':'Decline']]){const b=document.createElement('button');b.type='button';b.textContent=label;b.className='button';b.onclick=()=>choose(value);banner.append(b);}
banner.hidden=choice!==null;document.body.append(banner);
document.querySelectorAll('.analytics-preferences').forEach(b=>{b.hidden=false;b.onclick=()=>{banner.hidden=false;banner.querySelector('button').focus();};});
if(choice==='accepted')start();
document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a)return;const href=a.getAttribute('href');const method=href.startsWith('tel:')?'phone':href.startsWith('mailto:')?'email':href.startsWith('https://wa.me/')?'whatsapp':null;if(method)window.nobletonTrack('contact_click',{contact_method:method});if(a.dataset.directoryAction)window.nobletonTrack('directory_action',{action:a.dataset.directoryAction});});
})();
