"""Local directory presentation and advertising options. Facts live in businesses.json."""
from pathlib import Path
from html import escape as esc
from urllib.parse import quote
import json
from plan_content import t, h, p, actions

def businesses():
    path=Path(__file__).with_name('businesses.json')
    if not path.exists(): return []
    items=json.loads(path.read_text())
    for item in items:
        item['commercial']=True
        item['description']=t(item['summary_en'],item['summary_fr'])
        item['url']=item['website']
        for key in ('name','address','phone'):t(item[key],item[key])
    return items

def business_detail(r,intro):
    phone='+'+''.join(x for x in r['phone'] if x.isdigit())
    if len(phone)==11:phone='+1'+phone[1:]
    maps='https://www.google.com/maps/search/?api=1&query='+quote(r['name']+' '+r['address'])
    title=r['name']+' in Nobleton'
    t(title,r['name']+' à Nobleton')
    return title, intro(r['category'],r['name'],r['description'])+f'''<section class="wrap section business-detail"><div class="business-facts"><p class="eyebrow">{t('LOCAL BUSINESS','ENTREPRISE LOCALE')}</p><h2>{t('Plan your visit or call ahead','Préparez votre visite ou appelez')}</h2><dl><div><dt>{t('Address','Adresse')}</dt><dd>{esc(r['address'])}</dd></div><div><dt>{t('Phone','Téléphone')}</dt><dd><a href="tel:{phone}" data-directory-action="phone">{esc(r['phone'])}</a></dd></div></dl><div class="plan-actions"><a class="button" data-directory-action="website" href="{esc(r['website'])}">{t('Visit business website','Consulter le site de l’entreprise')}</a><a class="button secondary" data-directory-action="directions" href="{maps}">{t('Get directions','Itinéraire')}</a></div><p class="fine">{t('Check opening hours, availability and pricing with the business before visiting.','Vérifiez les heures, la disponibilité et les tarifs auprès de l’entreprise avant votre visite.')}</p></div><aside class="directory-source"><h2>{t('About this entry','À propos de cette fiche')}</h2><p>{t('Public business information checked November 9, 2026. This is a free editorial listing, not a paid placement or endorsement.','Renseignements publics vérifiés le 9 novembre 2026. Cette fiche éditoriale est gratuite; elle ne constitue ni une publicité ni une recommandation.')}</p><p><a href="{esc(r['source_url'])}">{t('Source: official business website','Source : site officiel de l’entreprise')}</a></p><a class="text-link" href="/submit/?type=correction&amp;business={quote(r['name'])}">{t('Own this business? Request an update','Vous êtes propriétaire? Demandez une mise à jour')}</a></aside></section>'''

def directory_intro(resources):
    count=sum(bool(r.get('commercial')) for r in resources)
    return '<div class="directory-overview"><p>'+t(f'{count} local businesses. Everyday places, closer to home.',f'{count} entreprises locales. Les adresses du quotidien, près de chez vous.')+'</p><p>'+t('Browse food, shops, wellness and services alongside schools, parks and community resources.','Découvrez restaurants, commerces, bien-être et services, ainsi que les écoles, parcs et ressources communautaires.')+'</p></div>'

def directory_feature(resources,card):
    cats=[('Food & drink','Food & drink','Restaurants et cafés'),('Health & wellness','Health & wellness','Santé et bien-être'),('Shopping','Shops & everyday essentials','Commerces et essentiels'),('Home services','Home services','Services résidentiels'),('Automotive','Auto services','Services automobiles'),('Pet care','Pet care','Soins aux animaux'),('Business resources','Business & banking','Affaires et services bancaires')]
    tiles=''.join(f'<a class="directory-category" href="/directory/?category={quote(cat)}"><span>{t(en,fr)}</span><strong>{sum(r["category"]==cat for r in resources)}</strong></a>' for cat,en,fr in cats if any(r.get('commercial') and r['category']==cat for r in resources))
    return '<section class="wrap section local-business-discovery"><div class="section-heading"><div><p class="eyebrow">'+t('KEEP IT LOCAL','CHOISISSEZ LOCAL')+'</p>'+h('Your next local find.','Votre prochaine découverte locale.')+'</div><a class="text-link" href="/directory/">'+t('Browse every listing','Voir toutes les fiches')+'</a></div><div class="directory-category-grid">'+tiles+'</div><p class="fine">'+t('Free editorial listings, sourced from official business websites. No ratings, rankings or paid endorsements.','Fiches éditoriales gratuites, établies à partir des sites officiels. Aucun classement, note ou recommandation rémunérée.')+'</p></section>'

def advertising_options():
    options=[
      ('featured','Featured business','Entreprise en vedette','Stand out in the local directory.','Démarquez-vous dans le répertoire local.','A labelled card with your business name, an approved photo, a short introduction and a link to your website.','Une carte identifiée avec votre nom, une photo autorisée, une courte présentation et un lien vers votre site.'),
      ('category','Category sponsor','Commanditaire de catégorie','Meet visitors looking for what you offer.','Rejoignez les visiteurs à la recherche de vos services.','A clearly marked sponsor placement beside a relevant directory category. Regular listings keep their editorial independence.','Un emplacement de commanditaire clairement identifié près d’une catégorie pertinente. Les fiches ordinaires conservent leur indépendance éditoriale.'),
      ('guide','Sponsored local guide','Guide local commandité','Share a useful local story.','Partagez une histoire locale utile.','A useful article developed with your business, labelled Sponsored and reviewed for accuracy before publication.','Un article utile préparé avec votre entreprise, identifié comme commandité et vérifié avant publication.')]
    cards=''
    for key,title,frtitle,subtitle,frsubtitle,desc,frdesc in options:
        cards+=f'<article class="advertise-option"><div class="placement-preview preview-{key}"><span class="sponsor-label">{t("SPONSORED · SAMPLE","COMMANDITÉ · EXEMPLE")}</span><span class="sample-wordmark">{t("Your business here","Votre entreprise ici")}</span><span class="sample-line"></span><span class="sample-line short"></span></div><div class="placement-copy"><p class="eyebrow">{t(title,frtitle)}</p><h3>{t(subtitle,frsubtitle)}</h3><p>{t(desc,frdesc)}</p><a class="button" href="#advertising-inquiry" data-ad-placement="{key}">{t("Ask about this placement","Demander des renseignements")}</a></div></article>'
    return '<section class="wrap section advertise-options"><div class="section-heading"><div><p class="eyebrow">'+t('WAYS TO BE SEEN','FAÇONS DE VOUS FAIRE VOIR')+'</p>'+h('Choose your place in the neighbourhood.','Trouvez votre place dans le quartier.')+'</div></div><p class="lead">'+t('Three formats to start a conversation. The examples below show possible placements, not current advertisers.','Trois formats pour lancer la discussion. Les exemples ci-dessous illustrent des emplacements possibles, pas des annonceurs actuels.')+'</p><div class="advertise-grid">'+cards+'</div><div class="advertise-process">'+h('A clear plan before anything goes live.','Un plan clair avant toute publication.')+'<ol><li>'+t('Share your goal, preferred format and campaign dates.','Indiquez votre objectif, le format souhaité et les dates.')+'</li><li>'+t('Receive a written proposal with placement, duration, price and reporting scope.','Recevez une proposition écrite précisant l’emplacement, la durée, le prix et les rapports prévus.')+'</li><li>'+t('Approve the creative and terms before publication.','Approuvez le contenu et les modalités avant la publication.')+'</li></ol><p>'+t('Nobleton.ca is growing. We do not promise visitor totals, leads or sales. Any reporting will distinguish measured activity from estimates.','Nobleton.ca est en développement. Nous ne promettons aucun volume de visiteurs, de demandes ou de ventes. Les rapports distingueront les données mesurées des estimations.')+'</p></div></section>'

def placement_field():
    return '<label for="placement">'+t('Preferred placement','Emplacement souhaité')+'</label><select id="placement" name="placement"><option value="unsure">'+t('Help me choose','Aidez-moi à choisir')+'</option><option value="featured">'+t('Featured business','Entreprise en vedette')+'</option><option value="category">'+t('Category sponsor','Commanditaire de catégorie')+'</option><option value="guide">'+t('Sponsored local guide','Guide local commandité')+'</option></select>'
