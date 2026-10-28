"""Generate complete French pages and reciprocal language links from the English build.
Exact text catalogue: new untranslated text fails the build instead of silently leaking English.
Run only after the English production pages have been rebuilt.
"""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import json, re, xml.etree.ElementTree as ET
from urllib.parse import urlsplit

TRANSLATIONS=json.loads(Path(__file__).with_name('fr.json').read_text())
TRANSLATIONS.update({'Nobleton, Ontario':'Nobleton, Ontario','King Township, Ontario, Canada':'Canton de King, Ontario, Canada'})
UNTRANSLATED=set()
def tr(value,strict=True):
 key=value.strip()
 if key in TRANSLATIONS:out=TRANSLATIONS[key]
 elif key+' | Nobleton' in TRANSLATIONS:out=TRANSLATIONS[key+' | Nobleton'].removesuffix(' | Nobleton')
 else:
  out=key
  if strict and re.search('[a-zA-Z]',key) and not key.startswith(('https://','mailto:','info@')):UNTRANSLATED.add(key)
 return value[:len(value)-len(value.lstrip())]+out+value[len(value.rstrip()):]

def french_url(value,base):
 if value.startswith(base+'/'):
  return base+'/fr'+value[len(base):] if not value.startswith(base+'/assets/') else value
 if value.startswith('/') and not value.startswith(('/assets/','/favicon','/fr/')):return '/fr'+value
 return value

def schema_fr(value,base,key=''):
 if isinstance(value,dict):return {k:schema_fr(v,base,k) for k,v in value.items()}
 if isinstance(value,list):return [schema_fr(v,base,key) for v in value]
 if isinstance(value,str):
  if key=='inLanguage':return 'fr-CA'
  if key in ('@id','url','item'):return french_url(value,base)
  if key in ('name','description'):return tr(value,False)
 return value

class French(HTMLParser):
 def __init__(self,base):
  super().__init__(convert_charrefs=True);self.base=base;self.out=[];self.script=None;self.script_data=[];self.option=None
 def handle_decl(self,d):self.out.append('<!'+d+'>')
 def handle_comment(self,d):self.out.append('<!--'+d+'-->')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='script':self.script=a.get('type','script');self.script_data=[]
  if tag=='html':a['lang']='fr-CA'
  for key in ('alt','placeholder','aria-label','title'):
   if key in a:a[key]=tr(a[key])
  for key in ('href','action'):
   if key in a:a[key]=french_url(a[key],self.base)
  if tag=='meta':
   if a.get('name') in ('description','twitter:title','twitter:description') or a.get('property') in ('og:title','og:description','og:image:alt'):a['content']=tr(a['content'])
   if a.get('property')=='og:url':a['content']=french_url(a['content'],self.base)
   if a.get('property')=='og:locale':a['content']='fr_CA'
  if 'data-search' in a:
   original=a['data-search'];more=' '.join(v for k,v in TRANSLATIONS.items() if len(k)>3 and k.lower() in original)
   a['data-search']=original+' '+more.lower()
  if tag=='option' and 'value' not in a:
   self.option=a;return
  self.emit_tag(tag,a)
 def emit_tag(self,tag,a):
  self.out.append('<'+tag+''.join(' '+k if v is None else ' '+k+'="'+escape(v,quote=True)+'"' for k,v in a.items())+'>')
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):
  if tag=='script':
   data=''.join(self.script_data)
   self.out.append(json.dumps(schema_fr(json.loads(data),self.base),ensure_ascii=False) if self.script=='application/ld+json' else data)
   self.script=None
  if tag=='option' and self.option is not None:self.emit_tag('option',self.option);self.option=None
  self.out.append('</'+tag+'>')
 def handle_data(self,data):
  if self.script is not None:self.script_data.append(data);return
  if self.option is not None:
   self.option['value']=data.strip();self.emit_tag('option',self.option);self.option=None
  self.out.append(escape(tr(data),quote=False))

def decorate(source,path,base,lang):
 fr='/fr'+path
 alternate=''.join(f'<link rel="alternate" hreflang="{code}" href="{base}{route}">' for code,route in [('en-CA',path),('fr-CA',fr),('x-default',path)])
 source=source.replace('</head>',alternate+'</head>')
 switch='<div class="language-switch" role="group" aria-label="'+('Langue' if lang=='fr' else 'Language')+'">'+''.join(f'<a href="{route}" lang="{code}" hreflang="{code}-CA"'+(' aria-current="true"' if code==lang else '')+f' aria-label="{label}">{code.upper()}</a>' for code,route,label in [('en',path,'English'),('fr',fr,'Français')])+'</div>'
 source=source.replace('</div><header>',switch+'</div><header>',1)
 source=source.replace('id="inquiry-form"','id="inquiry-form"')
 source=source.replace('</form>','<input type="hidden" name="preferred_language" value="'+('fr-CA' if lang=='fr' else 'en-CA')+'"></form>') if 'id="inquiry-form"' in source else source
 return source

def build(root):
 root=Path(root);manifest=json.loads((root/'seo-manifest.json').read_text());base=manifest['canonicalOrigin']
 pages=[p for p in root.rglob('*.html') if not p.relative_to(root).parts[0]=='fr']
 for p in pages:
  rel=p.relative_to(root);path='/'+str(rel).removesuffix('index.html')
  source=p.read_text();parser=French(base);parser.feed(source)
  target=root/'fr'/rel;target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(decorate(''.join(parser.out),path,base,'fr'))
  p.write_text(decorate(source,path,base,'en'))
 if UNTRANSLATED:raise ValueError('Missing French translations: '+repr(sorted(UNTRANSLATED)))
 routes=manifest['eligibleRoutes'];manifest['eligibleRoutes']=sorted(routes+['/fr'+r for r in routes]);manifest['excludedRoutes']+=['/fr'+r for r in manifest['excludedRoutes']]
 manifest['languages']=['en-CA','fr-CA'];(root/'seo-manifest.json').write_text(json.dumps(manifest,indent=2))
 ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
 sitemap=ET.parse(root/'sitemap.xml');ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
 for route in routes:ET.SubElement(ET.SubElement(sitemap.getroot(),ns+'url'),ns+'loc').text=base+'/fr'+route
 sitemap.write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
 print(f'Bilingual build: {len(pages)} English + {len(pages)} French pages')

if __name__=='__main__':
 import sys
 build(sys.argv[1])
