"""Search metadata and crawl policy shared by preview and production builds."""
import html, os
import json

BASE=os.environ.get('NOBLETON_SITE_ORIGIN','https://nobleton.ca').rstrip('/')
META={
 '/homes-for-sale/':('Nobleton Real Estate | Homes for Sale','Explore Nobleton neighbourhoods and start a personal property search with Ekaterina Ottchenach. Online listings are pending the required feed permissions.'),
 '/':('Nobleton, Ontario: Local Directory & Community Guide','Explore Nobleton, Ontario: local schools, parks, library resources, business submissions and service requests. An independent guide to life in King Township.'),
 '/directory/':('Nobleton Business & Community Directory','Browse Nobleton schools, community resources and local business categories. Find official websites or submit a free listing for a business serving Nobleton.'),
 '/guide/':('Living in Nobleton: Schools, Parks & Local Information','Get to know Nobleton with practical guides to schools, parks, the library and municipal resources, with links to official sources.'),
 '/guide/schools/':('Schools in Nobleton: Public & Catholic School Guide','Explore Nobleton Public School and St. Mary Catholic Elementary School. Find official contacts and what to check about registration and school boundaries.'),
 '/guide/parks/':('Nobleton Parks, Recreation & Library Guide','Plan time outdoors at Nobleton Community Park, find the Nobleton library and check official King Township resources for events and seasonal information.'),
 '/guide/essentials/':('Nobleton, Ontario: Location & Everyday Local Resources','Find out where Nobleton is and where to find King Township services, community information and local business resources.'),
 '/guide/moving-to-nobleton/':('Moving to Nobleton: A Practical Local Checklist','Planning a move to Nobleton? Start with schools, local amenities, address-specific checks and service planning before you choose a home.'),
 '/real-estate/':('Nobleton Real Estate | Ekaterina Ottchenach','Contact Ekaterina Ottchenach at HomeLife Frontier Realty Inc., Brokerage about buying or selling in Nobleton. Call (647) 838-5569 or email realtor@nobleton.ca.'),
 '/find-a-service/':('Request Local Services in Nobleton','Looking for a service provider in Nobleton? Tell our team what you need as we build a local referral network. Provider availability is not guaranteed.'),
 '/submit/':('Add Your Nobleton Business: Free Directory Submission','Submit a business serving Nobleton for a free directory listing, or suggest a correction. All submissions are reviewed before publication.'),
 '/about/':('About Nobleton: Independent Local Community Guide','Learn about Nobleton.ca, an independent guide to local businesses, community information, service connections and upcoming real estate.'),
 '/standards/':('Nobleton Directory Listing & Correction Standards','Read how the Nobleton directory reviews business submissions, handles corrections and identifies partnerships and sponsored placements.'),
 '/privacy/':('Nobleton Privacy Information & Contact','Contact info@nobleton.ca and learn how the website handles Formspree submissions, inquiries and personal information.'),
}
LABELS={'/':'Home','/directory/':'Directory','/guide/':'Local guide','/real-estate/':'Real estate','/mortgages/':'Mortgage services','/find-a-service/':'Find a service','/submit/':'Add your business','/about/':'About','/standards/':'Listing standards','/privacy/':'Privacy & contact'}
META.update({'/homes-for-sale/': ('Homes for Sale in Nobleton: Personal Property Search', 'Plan your Nobleton home search with Ekaterina Ottchenach. Explore neighbourhoods and request current options while the online listing feed is being arranged.'), '/real-estate/': ('Nobleton Real Estate: Ekaterina Ottchenach', 'Buying or selling in Nobleton? Contact Ekaterina Ottchenach, HomeLife Frontier Realty Inc., Brokerage, at (647) 838-5569 or realtor@nobleton.ca.'), '/mortgages/': ('Nobleton Mortgage Agent: Anatoly Shibkov', 'Discuss home financing, renewals and refinancing with Anatoly Shibkov of Mortgage Architects Professionals Inc. Call (437) 255-5037 or mortgage@nobleton.ca.'), '/mortgage-calculator/': ('Canadian Mortgage Calculator: Payments & Down Payment', 'Estimate mortgage payments, minimum down payment, insurance premiums and Ontario tax. Compare monthly, biweekly and weekly payments for your home budget.'), '/community/': ('Nobleton Community: Local News & Events', 'Explore Nobleton community updates, upcoming events and local resources, with links to official organizers and King Township information.'), '/events/': ('Nobleton & King Township Community Events', 'Find upcoming community events in Nobleton and King Township. Check dates, locations and official organizer details before you go.'), '/neighbourhoods/': ('Nobleton Neighbourhoods: Compare Areas & Amenities', 'Explore the village core, established streets and newer residential areas of Nobleton. Compare amenities and property-specific questions before your move.'), '/home-evaluation/': ('Request a Nobleton Home Evaluation', 'Thinking of selling your Nobleton home? Ask Ekaterina Ottchenach for a property evaluation and discuss your selling plans.'), '/ask-realtor/': ('Ask a Nobleton Real Estate Question', 'Ask Ekaterina Ottchenach about buying, selling or moving to Nobleton. Send a question or call (647) 838-5569.'), '/mortgage-consultation/': ('Request a Mortgage Consultation in Nobleton', 'Contact Anatoly Shibkov about a purchase, renewal, refinance or investment mortgage. Send a consultation request or call (437) 255-5037.'), '/contact/': ('Contact Nobleton Real Estate & Mortgage Professionals', 'Choose the right contact for buying, selling, home valuation or mortgage questions in Nobleton. Reach Ekaterina Ottchenach or Anatoly Shibkov directly.'), '/guide/buying-a-home/': ('Buying a Home in Nobleton: Step-by-Step Guide', 'Plan your Nobleton home purchase: budget, pre-approval, property checks, offers and closing. Find practical steps and official Canadian mortgage resources.'), '/guide/selling-and-buying/': ('Selling & Buying a Home in Nobleton: Planning Guide', 'Coordinate the sale of your current home with your next purchase. Explore timing, financing and closing-date questions to discuss with your professionals.'), '/guide/down-payments/': ('Ontario Down Payments & Closing Costs: Homebuyer Guide', 'Understand down payment planning, mortgage insurance and closing-cost categories for an Ontario home purchase, with links to official resources.'), '/guide/mortgage-renewal/': ('Mortgage Renewal in Ontario: Compare Your Options', 'Prepare for your mortgage renewal. Review the balance, payment, term and switching questions to discuss with your lender or mortgage agent.'), '/advertise/': ('Advertise on Nobleton.ca: Reach Local Customers', 'Promote a business serving Nobleton. Ask about advertising opportunities, directory visibility and clearly labelled sponsored placements on Nobleton.ca.'), '/about/': ('About Nobleton.ca: Independent Community Guide', 'Meet Nobleton.ca, an independent guide to local resources, community life, real estate and mortgage contacts. Learn how to contribute or suggest a correction.'), '/privacy/': ('Nobleton.ca Privacy & Inquiry Information', 'Learn how Nobleton.ca handles business submissions and professional inquiries, where forms are sent, and how to contact us about your personal information.'), '/photo-credits/': ('Nobleton Photography: Sources & Image Credits', 'View sources, photographers and licences for the Nobleton photographs used on this site, including Hambly House, Nobleton Lakes and Roslyn House.')})
LABELS.update({'/homes-for-sale/': 'Homes for sale', '/mortgage-calculator/': 'Mortgage calculator', '/community/': 'Community', '/events/': 'Events', '/neighbourhoods/': 'Neighbourhoods', '/home-evaluation/': 'Home evaluation', '/ask-realtor/': 'Ask a realtor', '/mortgage-consultation/': 'Mortgage consultation', '/contact/': 'Contact', '/advertise/': 'Advertise', '/photo-credits/': 'Photo credits', '/guide/buying-a-home/': 'Buying a home', '/guide/selling-and-buying/': 'Selling and buying', '/guide/down-payments/': 'Down payments', '/guide/mortgage-renewal/': 'Mortgage renewal', '/guide/schools/': 'Schools', '/guide/parks/': 'Parks and library', '/guide/essentials/': 'Local essentials', '/guide/moving-to-nobleton/': 'Moving checklist'})
EXCLUDED={'/404.html','/thank-you/'}

def prepare(title,desc,body,path,resources):
 title,desc=META.get(path,(title,desc))
 schema_type='CollectionPage' if path in ['/directory/','/guide/'] else 'AboutPage' if path=='/about/' else 'WebPage'
 graph=[{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Nobleton','alternateName':'Nobleton.ca','inLanguage':'en-CA'},
        {'@type':schema_type,'@id':BASE+path+'#webpage','url':BASE+path,'name':title,'description':desc,'inLanguage':'en-CA','isPartOf':{'@id':BASE+'/#website'}}]
 if path!='/404.html':graph[1]['about']={'@type':'Place','name':'Nobleton, Ontario','containedInPlace':{'@type':'AdministrativeArea','name':'King Township, Ontario, Canada'}}
 if path not in ['/','/404.html']:
  crumbs=[('Home','/')]
  if path.count('/')>2:
   parent='/'+path.split('/')[1]+'/'
   crumbs.append((LABELS.get(parent,parent),parent))
  crumbs.append((LABELS.get(path,title),path))
  graph.append({'@type':'BreadcrumbList','@id':BASE+path+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':BASE+u} for i,(n,u) in enumerate(crumbs)]})
  graph[1]['breadcrumb']={'@id':BASE+path+'#breadcrumb'}
  trail='<nav class="breadcrumbs wrap" aria-label="Breadcrumb"><ol>'+''.join('<li>'+ (f'<a href="{u}">{html.escape(n)}</a>' if i<len(crumbs)-1 else f'<span aria-current="page">{html.escape(n)}</span>')+'</li>' for i,(n,u) in enumerate(crumbs))+'</ol></nav>'
  body=trail+body
 if path=='/real-estate/':
  graph[1]['@type']='ProfilePage'
  agent={'@type':'Person','@id':BASE+path+'#ekaterina-ottchenach','name':'Ekaterina Ottchenach','jobTitle':'Real Estate Sales Representative','image':BASE+'/assets/images/ekaterina-ottchenach.webp','telephone':'+1-647-838-5569','email':'realtor@nobleton.ca','worksFor':{'@id':BASE+path+'#brokerage'},'sameAs':['https://www.instagram.com/family.realtor/']}
  brokerage={'@type':'RealEstateAgent','@id':BASE+path+'#brokerage','name':'HomeLife Frontier Realty Inc., Brokerage','logo':BASE+'/assets/images/homelife-frontier-logo.jpg','address':{'@type':'PostalAddress','streetAddress':'7620 Yonge St #400','addressLocality':'Thornhill','addressRegion':'ON','postalCode':'L4J 1V9','addressCountry':'CA'}}
  graph.extend([agent,brokerage]);graph[1]['mainEntity']={'@id':agent['@id']}
 if path=='/mortgages/':
  graph[1]['@type']='ProfilePage'
  agent={'@type':'Person','@id':BASE+path+'#anatoly-shibkov','name':'Anatoly Shibkov','jobTitle':'Mortgage Agent','image':BASE+'/assets/images/anatoly-shibkov.jpg','telephone':'+1-437-255-5037','email':'mortgage@nobleton.ca','worksFor':{'@id':BASE+path+'#brokerage'}}
  brokerage={'@type':'Organization','@id':BASE+path+'#brokerage','name':'Mortgage Architects Professionals Inc.','logo':BASE+'/assets/images/mortgage-architects-logo.jpg','areaServed':{'@type':'AdministrativeArea','name':'Ontario, Canada'},'identifier':{'@type':'PropertyValue','propertyID':'Ontario brokerage licence','value':'12168'}}
  graph.extend([agent,brokerage]);graph[1]['mainEntity']={'@id':agent['@id']}
 if path=='/directory/':
  graph.append({'@type':'ItemList','@id':BASE+path+'#entries','numberOfItems':len(resources),'itemListElement':[{'@type':'ListItem','position':i+1,'name':r['name'],'url':BASE+'/directory/'+r['slug']+'/'} for i,r in enumerate(resources)]})
  graph[1]['mainEntity']={'@id':BASE+path+'#entries'}
 for r in resources:
  if path=='/directory/'+r['slug']+'/':
   types={'Schools':'School','Community':'Library','Parks & recreation':'Park','Business resources':'Organization'}
   entity={'@type':('LocalBusiness' if r.get('commercial') else types[r['category']]),'@id':r['url']+'#entity','name':r['name'],'url':r['url'],'description':r['description']}
   if r.get('commercial'):
    entity.update({'telephone':r['phone'],'address':{'@type':'PostalAddress','streetAddress':r['address'],'addressLocality':'Nobleton','addressRegion':'ON','addressCountry':'CA'}})
   graph.append(entity);graph[1]['mainEntity']={'@id':entity['@id']}
 publisher={'@type':'Organization','@id':BASE+'/#publisher','name':'Nobleton.ca','url':BASE+'/about/','email':'info@nobleton.ca'}
 graph.append(publisher)
 graph[0]['publisher']={'@id':publisher['@id']}
 graph[1]['publisher']={'@id':publisher['@id']}
 if path.startswith('/guide/') and path!='/guide/':
  graph.append({'@type':'Article','@id':BASE+path+'#article','headline':title,'description':desc,'inLanguage':'en-CA','author':{'@id':publisher['@id']},'publisher':{'@id':publisher['@id']},'mainEntityOfPage':{'@id':graph[1]['@id']}})
 return title,desc,body,{'@context':'https://schema.org','@graph':graph}

def finish(root,routes,production):
 indexed=sorted(set(routes)-EXCLUDED)
 root.joinpath('sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{html.escape(p)}</loc></url>\n' for p in indexed)+'</urlset>\n')
 root.joinpath('robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n')
 root.joinpath('seo-manifest.json').write_text(json.dumps({'mode':'production' if production else 'preview','canonicalOrigin':BASE,'eligibleRoutes':indexed,'excludedRoutes':sorted(EXCLUDED),'note':'Production mode prepares files only. Hosting, HTTPS, status codes and Search Console still need verification.'},indent=2))
