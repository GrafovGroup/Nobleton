"""Nobleton history, supplied by the owner and checked against municipal sources."""
from plan_content import t, p, h
from seo import META, LABELS

PATH = '/guide/history/'
IMAGE = '/assets/images/hambly-house-history.jpeg'
HERO_IMAGE = '/assets/images/hambly-house-history-1280.webp'
HERO_SIZES = '(max-width: 780px) 100vw, 72vw'
HERO_SOURCES = ', '.join(f'/assets/images/hambly-house-history-{width}.webp {width}w' for width in (640, 960, 1280))

def title():
    return t('Nobleton: Over 200 Years of History', 'Nobleton : plus de 200 ans d’histoire')

def heritage_mark(tone='dark'):
    return f'<span class="heritage-mark heritage-mark--{tone}" aria-hidden="true"><span></span><span></span><span></span></span>'

def photograph(eager=False, *, hero=False):
    alt = t('Hambly House in Nobleton, with red and cream brickwork, a central tower and a veranda', 'La maison Hambly à Nobleton, avec sa maçonnerie rouge et crème, sa tour centrale et sa véranda')
    name = t('Hambly House', 'Maison Hambly')
    date = t('Built in 1884', 'Construite en 1884')
    credit = t('Photo supplied for Nobleton.ca', 'Photo fournie pour Nobleton.ca')
    if hero:
        image = (f'<img src="{HERO_IMAGE}" srcset="{HERO_SOURCES}" sizes="{HERO_SIZES}" alt="{alt}" '
                 'width="1280" height="950" loading="eager" decoding="async" fetchpriority="high">')
        return (f'<figure class="editorial-photo home-hero-photo">{image}'
                f'<figcaption><span>{name}</span> · <span>{credit}</span></figcaption></figure>')
    loading = 'eager' if eager else 'lazy'
    image = f'<img src="{IMAGE}" alt="{alt}" width="1280" height="950" loading="{loading}" decoding="async">'
    return (f'<figure class="history-photo heritage-photo">{image}'
            f'<figcaption class="landmark-caption"><strong>{name}</strong><span>{date}</span><span>{credit}</span></figcaption></figure>')

def teaser(image=None):
    return '<section class="wrap section history-feature">'+(image or photograph())+'<div><p class="eyebrow">'+heritage_mark()+t('OUR VILLAGE STORY', 'L’HISTOIRE DE NOTRE VILLAGE')+'</p><h2>'+title()+'</h2>'+p('From an early crossroads settlement to the community we know today, discover the people, places and landmarks that shaped Nobleton.', 'D’un petit établissement à la croisée des chemins à la communauté d’aujourd’hui, découvrez les gens, les lieux et les bâtiments qui ont façonné Nobleton.')+f'<a class="button" href="{PATH}">'+t('Discover Nobleton’s history', 'Découvrez l’histoire de Nobleton')+'</a></div></section>'

def register(page, intro):
    desc = t('Discover Nobleton’s history, from its early 19th-century crossroads and Joseph Noble to Hambly House and village life in King Township.', 'Découvrez l’histoire de Nobleton, de son carrefour du début du XIXe siècle et de Joseph Noble à la maison Hambly et à la vie dans le canton de King.')
    META[PATH] = (title(), desc)
    LABELS[PATH] = t('Nobleton history', 'Histoire de Nobleton')
    body = '<article class="wrap reading section history-article">'+photograph(True)
    body += h('A community at the crossroads', 'Une communauté à la croisée des chemins')
    body += p('Nobleton’s story as a settlement began in the early 19th century. King Township’s heritage history dates its beginnings to 1812, at the crossroads now known as King Road and Highway 27. The community was named after Joseph Noble, one of its early settlers and its first tavern keeper.', 'L’histoire de Nobleton en tant qu’établissement remonte au début du XIXe siècle. Selon les documents patrimoniaux du canton de King, ses débuts datent de 1812, au carrefour aujourd’hui formé par King Road et la route 27. La communauté doit son nom à Joseph Noble, l’un de ses premiers colons et son premier aubergiste.')
    body += p('Over time, shops, hotels, workshops and a post office appeared, gradually turning Nobleton into a trading hub for surrounding farming communities.', 'Au fil du temps, des boutiques, des hôtels, des ateliers et un bureau de poste ont vu le jour, faisant peu à peu de Nobleton un centre d’échanges pour les communautés agricoles des environs.')
    body += h('Hambly House: a link to the past', 'La maison Hambly : un lien avec le passé')
    body += p('One reminder of those early days is Hambly House at 6012 King Road. Built in 1884, this historic landmark is known for its distinctive tower, decorative brickwork and veranda. King Township designated the property for its heritage value in 1982.', 'La maison Hambly, située au 6012 King Road, témoigne de cette époque. Construite en 1884, elle se distingue par sa tour, sa maçonnerie décorative et sa véranda. Le canton de King a désigné la propriété pour sa valeur patrimoniale en 1982.')
    body += h('Village character, still part of everyday life', 'Un caractère villageois toujours présent')
    body += p('Today, Nobleton is part of King Township. Despite its growth and development, it retains the charm of a small community with more than two centuries of history.', 'Aujourd’hui, Nobleton fait partie du canton de King. Malgré sa croissance et son développement, la communauté conserve le charme d’un village riche de plus de deux siècles d’histoire.')
    body += h('Explore the history', 'Pour en savoir plus')
    body += '<ul><li><a href="https://www.king.ca/sites/default/files/docs/recreation-living/heritage-culture/king-heritage-and-cultural-centre/King%20Heritage%20Map.pdf">'+t('King Township heritage map and community history', 'Carte patrimoniale et histoire des communautés du canton de King')+'</a></li><li><a href="https://storymaps.arcgis.com/stories/fcfdf64f060b40deb9abfc3153616910">'+t('King Township heritage register: Hambly House', 'Registre patrimonial du canton de King : maison Hambly')+'</a></li></ul>'
    body += '<p class="fine">'+t('Historical sources checked November 19, 2026. The photograph is an undated view and does not indicate current conditions or public access.', 'Sources historiques vérifiées le 19 novembre 2026. La photographie, non datée, ne renseigne pas sur l’état actuel du bâtiment ni sur son accessibilité au public.')+'</p></article>'
    page('guide/history', title(), desc, intro(t('LOCAL HISTORY', 'HISTOIRE LOCALE'), title(), t('The crossroads, the people and the places behind the village.', 'Le carrefour, les gens et les lieux à l’origine du village.'))+body, 'Local guide')
