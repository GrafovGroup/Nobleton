(function(root){
'use strict';
function payment(loan,rate,years,frequency){
 const i=Math.pow(1+rate/200,2/frequency)-1;
 return i===0 ? loan/(years*frequency) : loan*i/(1-Math.pow(1+i,-years*frequency));
}
function estimate(input){
 const {price,down,downMode,rate,years,frequency,eligible30}=input;
 if (![price,down,rate,years,frequency].every(Number.isFinite) || price<=0 || price>50000000 || down<0 || rate<0 || rate>30 || ![5,10,15,20,25,30].includes(years) || ![12,26,52].includes(frequency) || !['amount','percent'].includes(downMode)) throw new Error('invalid');
 const deposit=downMode==='percent'?price*down/100:down;
 const minimum=price>=1500000?price*.20:Math.min(price,500000)*.05+Math.max(0,price-500000)*.10;
 if (deposit>=price) throw new Error('deposit');
 if (deposit+.000001<minimum) throw new Error('minimum');
 const base=price-deposit,ltv=base/price,insured=ltv>.80000000001;
 if (insured && years===30 && !eligible30) throw new Error('eligibility');
 const premiumRate=insured?((ltv>.90000000001?.04:ltv>.85000000001?.031:.028)+(years===30?.002:0)):0;
 const premium=Math.round(base*premiumRate*100)/100,loan=base+premium;
 return {base,premium,loan,tax:premium*.08,minimum,deposit,paymentBase:payment(base,rate,years,frequency),payment:payment(loan,rate,years,frequency)};
}
if (typeof module!=='undefined' && module.exports) module.exports={estimate,payment};
if (!root.document) return;
const form=document.getElementById('mortgage-calculator'); if(!form) return;
const fr=document.documentElement.lang.startsWith('fr');
const errors=fr?{invalid:'Vérifiez les valeurs saisies. Le taux doit être entre 0 et 30 %.',deposit:'La mise de fonds doit être inférieure au prix d’achat.',minimum:'La mise de fonds est inférieure au minimum pour ce prix. Consultez les règles sous la calculatrice.',eligibility:'Pour un prêt assuré sur 30 ans, confirmez votre admissibilité comme premier acheteur ou acheteur d’une construction neuve, ou choisissez 25 ans.'}:{invalid:'Check your entries. The interest rate must be between 0 and 30%.',deposit:'The down payment must be less than the purchase price.',minimum:'The down payment is below the minimum for this price. Review the rules below the calculator.',eligibility:'For an insured 30-year estimate, confirm first-time buyer or new-build eligibility, or choose 25 years.'};
const money=new Intl.NumberFormat(fr?'fr-CA':'en-CA',{style:'currency',currency:'CAD',maximumFractionDigits:2});
const result=document.getElementById('calculator-results'),error=document.getElementById('calculator-error');
function calculate(track){
 error.textContent='';
 try {
  const data={price:Number(form.elements.price.value),down:Number(form.elements.down.value),downMode:form.elements.downMode.value,rate:Number(form.elements.rate.value),years:Number(form.elements.years.value),frequency:Number(form.elements.frequency.value),eligible30:form.elements.eligible30.checked};
  if(!form.checkValidity())throw new Error('invalid');
  const values=estimate(data);
  document.getElementById('payment-value').textContent=money.format(values.payment);
  document.getElementById('payment-heading').textContent=(fr?{12:'Versement mensuel estimé',26:'Versement estimé aux deux semaines',52:'Versement hebdomadaire estimé'}:{12:'Estimated monthly payment',26:'Estimated biweekly payment',52:'Estimated weekly payment'})[data.frequency];
  result.querySelectorAll('[data-result]').forEach(el=>el.textContent=money.format(values[el.dataset.result]));
  result.classList.remove('invalid-estimate');
  if(track){root.nobletonTrack?.('mortgage_calculation',{inquiry_type:'calculator'});result.focus({preventScroll:true});}
 }catch(e){
  error.textContent=errors[e.message]||errors.invalid;
  document.getElementById('payment-value').textContent='—';
  result.querySelectorAll('[data-result]').forEach(el=>el.textContent='—');result.classList.add('invalid-estimate');
 }
}
form.addEventListener('submit',event=>{event.preventDefault();calculate(true);});
form.addEventListener('input',()=>calculate(false));
form.addEventListener('change',()=>calculate(false));
calculate(false);
})(typeof window==='undefined'?globalThis:window);
