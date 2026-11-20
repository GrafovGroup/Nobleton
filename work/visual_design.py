"""Presentation components for the Nobleton community guide."""

from plan_content import t
from history_content import photograph

ICON_PATHS = {
    'Schools': (
        '<path d="m3 9 9-5 9 5-9 5-9-5Z"/>'
        '<path d="M7 11.3v4.2c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5v-4.2M21 9v6"/>'
    ),
    'Community': (
        '<path d="M12 6.5C9.4 4.5 6.6 4 3 5v13c3.6-1 6.4-.5 9 1.5'
        ' 2.6-2 5.4-2.5 9-1.5V5c-3.6-1-6.4-.5-9 1.5Zm0 0v13"/>'
    ),
    'Parks & recreation': '<path d="m12 2-6 8h3l-5 7h6v5h4v-5h6l-5-7h3l-6-8Z"/>',
    'Business resources': (
        '<rect x="3" y="7" width="18" height="14" rx="2"/>'
        '<path d="M8 7V3h8v4M3 12.5h18m-11 0v2h4v-2"/>'
    ),
    'Home services': '<path d="m3 10 9-7 9 7M5 10v10h14V10m-9.5 7 4-4M12 11.5l3 3"/>',
    'Food & drink': '<path d="M5 3v5a2 2 0 0 0 4 0V3M7 3v18m10-18v18m0-18c-2 1.5-3 5-3 9h3"/>',
    'Health & wellness': (
        '<path d="M20 6c-2.2-2.2-5.7-1.6-8 .8C9.7 4.4 6.2 3.8 4 6'
        'c-2.2 2.2-2.1 5.7.4 8l7.6 7 7.6-7c2.5-2.3 2.6-5.8.4-8Z"/>'
        '<path d="M7 12h3l1.5-2.5 2 4.5 1-2H17"/>'
    ),
    'Shopping': (
        '<path d="M4 12v8h16v-8M3 11l2-6h14l2 6'
        'M3 11c1.5 1.5 3 1.5 4.5 0 1.5 1.5 3 1.5 4.5 0'
        ' 1.5 1.5 3 1.5 4.5 0 1.5 1.5 3 1.5 4.5 0'
        'M10 20v-5h4v5"/>'
    ),
    'Automotive': (
        '<path d="m5 11 2-5h10l2 5M4 17v2m16-2v2M4 17h16v-4'
        'a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v4Zm3-3h2m6 0h2"/>'
    ),
    'Pet care': (
        '<circle cx="5.4" cy="10.2" r="1.55"/><circle cx="9.2" cy="6.5" r="1.65"/>'
        '<circle cx="14.8" cy="6.5" r="1.65"/><circle cx="18.6" cy="10.2" r="1.55"/>'
        '<path d="M7 16.5c0-1.5.8-2.3 1.7-2.8.8-.5 1.5-1.7 3.3-1.7'
        's2.5 1.2 3.3 1.7c.9.5 1.7 1.3 1.7 2.8 0 1.6-1.1 2.7-2.6 2.7'
        '-.9 0-1.4-.4-2.4-.4s-1.5.4-2.4.4c-1.5 0-2.6-1.1-2.6-2.7Z"/>'
    ),
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
}


def icon(kind):
    paths = ICON_PATHS.get(kind, ICON_PATHS['Community'])
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{paths}</svg>'
    )

def home_page(photo, card, resources, feature_photos):
    links = [
        ('Schools', 'Schools & families', '/guide/schools/'),
        ('Community', 'Local essentials', '/guide/essentials/'),
        ('Business resources', 'Moving to Nobleton', '/guide/moving-to-nobleton/'),
        ('search', 'Local services', '/find-a-service/'),
    ]
    shortcuts = ''.join(f'<a href="{url}"><span class="shortcut-icon">{icon(kind)}</span><span>{label}</span></a>' for kind,label,url in links)
    neighbour_links = [
        ('/events/', t('Meet your neighbours', 'Rencontrez vos voisins'),
         t('Find upcoming events and community calendars.', 'Découvrez les activités à venir et les calendriers communautaires.')),
        ('/guide/parks/', t('Explore parks and trails', 'Explorez les parcs et sentiers'),
         t('Check trail access and plan a visit to local conservation areas.', 'Vérifiez l’accès aux sentiers et planifiez une visite dans les aires de conservation des environs.')),
        ('/directory/', t('Support local businesses', 'Soutenez les entreprises locales'),
         t('Find shops, restaurants and services in the directory.', 'Trouvez des commerces, des restaurants et des services dans le répertoire.')),
    ]
    neighbour_cards = []
    for url, label, description in neighbour_links:
        image = photo(*feature_photos[url], extra='village-card-photo')
        neighbour_cards.append(
            f'<article class="village-card">{image}'
            f'<div class="village-card-copy"><h3><a href="{url}">{label}'
            '<span aria-hidden="true">→</span></a></h3>'
            f'<p>{description}</p></div></article>'
        )
    return f'''
<section class="home-hero" aria-labelledby="home-title">
  {photograph(hero=True)}
  <div class="home-hero-content">
    <p class="eyebrow">YOUR INDEPENDENT LOCAL GUIDE</p>
    <h1 id="home-title">Nobleton.<br><em>A little closer<br>to home.</em></h1>
    <p>Discover the places, people and everyday possibilities that make this corner of King Township feel like home.</p>
    <form class="search" action="/directory/" role="search"><label class="sr-only" for="home-search">Search the local directory</label><span>{icon('search')}</span><input id="home-search" name="q" placeholder="What are you looking for?" type="search"><button type="submit">Explore</button></form>
    <div class="hero-links"><a href="/guide/">Explore the village</a><a href="/homes-for-sale/">Explore homes</a></div>
  </div>
</section>
<nav class="discovery-bar wrap" aria-label="Discover Nobleton">{shortcuts}</nav>
<section class="wrap section village-story" aria-labelledby="village-story-title">
  <div class="section-heading"><h2 id="village-story-title">{t('Neighbourly by nature', 'L’esprit de voisinage')}</h2></div>
  <div class="village-card-grid">{''.join(neighbour_cards)}</div>
</section>
<section class="professionals-section section">
 <div class="wrap"><div class="section-heading"><div><p class="eyebrow">YOUR NEXT CHAPTER</p><h2>Start with a conversation.</h2></div><p>Real estate and mortgage guidance,<br>with a person you can reach.</p></div>
 <div class="professional-grid">
  <article class="professional-card"><div class="professional-copy"><p class="eyebrow">REAL ESTATE</p><h3>Ekaterina<br>Ottchenach</h3><p>Planning to buy or sell in Nobleton? Talk through your next move.</p><a class="button light" href="/real-estate/">Meet Ekaterina</a><div class="professional-broker"><img src="/assets/images/homelife-frontier-logo.jpg" width="668" height="299" alt="HomeLife Frontier Realty Inc., Brokerage logo" loading="lazy"><p>HomeLife Frontier Realty Inc., Brokerage</p></div></div><img class="professional-portrait" src="/assets/images/ekaterina-ottchenach.webp" width="1122" height="1402" alt="Ekaterina Ottchenach, Real Estate Sales Representative" loading="lazy" decoding="async"></article>
  <article class="professional-card mortgage-card"><div class="professional-copy"><p class="eyebrow">MORTGAGE SERVICES</p><h3>Anatoly<br>Shibkov</h3><p>Explore financing options for your first home, your next home or a renewal.</p><a class="button light" href="/mortgages/">Meet Anatoly</a><div class="professional-broker"><img src="/assets/images/mortgage-architects-logo.jpg" width="447" height="447" alt="Mortgage Architects logo" loading="lazy"><p>Mortgage Architects Professionals Inc.<br><span>Brokerage Licence #12168</span></p></div></div><img class="professional-portrait" src="/assets/images/anatoly-shibkov.jpg" width="1036" height="1280" alt="Anatoly Shibkov, Mortgage Agent" loading="lazy" decoding="async"></article>
 </div></div>
</section>
<section class="wrap section neighbourhood-section"><div class="section-heading"><div><p class="eyebrow">PART OF THE NEIGHBOURHOOD</p><h2>A few places to start.</h2></div><a class="text-link" href="/directory/">Explore the directory</a></div><div class="cards">{''.join(card(r) for r in [resources[2],resources[0],resources[3]])}</div><p class="fine">Public-resource entries link to official sources. Inclusion does not imply a partnership or endorsement.</p></section>
<section class="wrap community-invite"><div><p class="eyebrow">LOCAL BUSINESS OWNER?</p><h2>You belong here, too.</h2><p>Help neighbours discover what you do. Business submissions are free at launch.</p></div><a class="button" href="/submit/">Add your business — free</a></section>
'''
