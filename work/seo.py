"""Search metadata and crawl policy shared by preview and production builds."""
import html, os
import json

BASE=os.environ.get('NOBLETON_SITE_ORIGIN','https://nobleton.ca').rstrip('/')
META={
 '/':('Nobleton, Ontario: Local Directory & Community Guide','Explore Nobleton, Ontario: local schools, parks, library resources, business submissions and service requests. An independent guide to life in King Township.'),
 '/directory/':('Nobleton Business & Community Directory','Browse Nobleton schools, community resources and local business categories. Find official websites or submit a free listing for a business serving Nobleton.'),
 '/guide/':('Living in Nobleton: Schools, Parks & Local Information','Get to know Nobleton with practical guides to schools, parks, the library and municipal resources, with links to official sources.'),
 '/guide/schools/':('Schools in Nobleton: Public & Catholic School Guide','Explore Nobleton Public School and St. Mary Catholic Elementary School. Find official contacts and what to check about registration and school boundaries.'),
 '/guide/parks/':('Nobleton Parks, Recreation & Library Guide','Plan time outdoors at Nobleton Community Park, find the Nobleton library and check official King Township resources for events and seasonal information.'),
 '/guide/essentials/':('Nobleton, Ontario: Location & Everyday Local Resources','Find out where Nobleton is and where to find King Township services, community information and local business resources.'),
 '/guide/moving-to-nobleton/':('Moving to Nobleton: A Practical Local Checklist','Planning a move to Nobleton? Start with schools, local amenities, address-specific checks and service planning before you choose a home.'),
 '/real-estate/':('Nobleton Real Estate & Neighbourhood Guide','Explore Nobleton schools and amenities before your next move. Property listings are coming through our brokerage partner; no homes are advertised yet.'),
 '/find-a-service/':('Request Local Services in Nobleton','Looking for a service provider in Nobleton? Tell our team what you need as we build a local referral network. Provider availability is not guaranteed.'),
 '/submit/':('Add Your Nobleton Business: Free Directory Submission','Submit a business serving Nobleton for a free directory listing, or suggest a correction. All submissions are reviewed before publication.'),
 '/about/':('About Nobleton: Independent Local Community Guide','Learn about Nobleton.ca, an independent guide to local businesses, community information, service connections and upcoming real estate.'),
 '/standards/':('Nobleton Directory Listing & Correction Standards','Read how the Nobleton directory reviews business submissions, handles corrections and identifies partnerships and sponsored placements.'),
 '/privacy/':('Nobleton Privacy Information & Contact','Contact info@nobleton.ca and learn how the website handles email drafts, inquiries and personal information.'),
}
LABELS={'/':'Home','/directory/':'Directory','/guide/':'Local guide','/real-estate/':'Real estate','/find-a-service/':'Find a service','/submit/':'Add your business','/about/':'About','/standards/':'Listing standards','/privacy/':'Privacy & contact'}
EXCLUDED={'/404.html','/real-estate/'}

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
 if path=='/directory/':
  graph.append({'@type':'ItemList','@id':BASE+path+'#entries','numberOfItems':len(resources),'itemListElement':[{'@type':'ListItem','position':i+1,'name':r['name'],'url':BASE+'/directory/'+r['slug']+'/'} for i,r in enumerate(resources)]})
  graph[1]['mainEntity']={'@id':BASE+path+'#entries'}
 for r in resources:
  if path=='/directory/'+r['slug']+'/':
   types={'Schools':'School','Community':'Library','Parks & recreation':'Park','Business resources':'Organization'}
   entity={'@type':types[r['category']],'@id':r['url']+'#entity','name':r['name'],'url':r['url'],'description':r['description']}
   graph.append(entity);graph[1]['mainEntity']={'@id':entity['@id']}
 return title,desc,body,{'@context':'https://schema.org','@graph':graph}

def finish(root,routes,production):
 indexed=sorted(set(routes)-EXCLUDED)
 root.joinpath('sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{html.escape(p)}</loc></url>\n' for p in indexed)+'</urlset>\n')
 root.joinpath('robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n')
 root.joinpath('seo-manifest.json').write_text(json.dumps({'mode':'production' if production else 'preview','canonicalOrigin':BASE,'eligibleRoutes':indexed,'excludedRoutes':sorted(EXCLUDED),'note':'Production mode prepares files only. Hosting, HTTPS, status codes and Search Console still need verification.'},indent=2))
