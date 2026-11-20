"""Local food coverage and the Nobleton dining guide."""
from html import escape
from urllib.parse import urlencode

from plan_content import h, p, t


HUB_PATH = '/where-to-eat-in-nobleton/'
BAKERY_PATH = '/st-phillips-bakery-nobleton/'
BAKERY_SLUG = 'st-phillips-nobleton'
BAKERY_DIRECTORY_PATH = f'/directory/{BAKERY_SLUG}/'
HUB_TITLE = 'Where to Eat in Nobleton'
BAKERY_NAME = 'St. Phillips Bakery'
BAKERY_TITLE = 'St. Phillips Bakery in Nobleton: A Sweet Spot for Cakes, Pastries & Coffee'
HERO_IMAGE = 'st-phillips-pastry-counter.webp'
HERO_ALT = 'A Christmas tree beside the pastry counter at St. Phillips Bakery in Nobleton'
HERO_ALT_FR = 'Un sapin de Noël près du comptoir de pâtisseries de St. Phillips Bakery à Nobleton'
DINING_GROUPS = (
    ('coffee-and-bakeries', 'Coffee & bakeries', 'Cafés et boulangeries'),
    ('sit-down-meals', 'Sit-down meals', 'Repas sur place'),
    ('takeout', 'Takeout', 'Repas à emporter'),
)


def dining_link():
    return f'<a class="text-link" href="{HUB_PATH}">{t(HUB_TITLE, "Où manger à Nobleton")}</a>'


def bakery_link():
    return (f'<a class="text-link" href="{BAKERY_PATH}">'
            f'{t("Read about our visit to St. Phillips Bakery", "Lire le récit de notre visite chez St. Phillips Bakery")}</a>')


def photo(filename, width, height, sizes, alt, alt_fr, caption, caption_fr, eager=False):
    stem = filename.removesuffix('.webp')
    priority = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<figure class="editorial-photo dining-photo">
        <img src="/assets/images/{filename}" srcset="/assets/images/{stem}-480.webp 480w, /assets/images/{filename} {width}w"
             sizes="{sizes}" width="{width}" height="{height}" alt="{t(alt, alt_fr)}" {priority} decoding="async">
        <figcaption>{t(caption, caption_fr)}</figcaption>
    </figure>'''


def pastry_photo(sizes, eager=False):
    return photo(
        HERO_IMAGE, 960, 1280, sizes, HERO_ALT, HERO_ALT_FR,
        'Christmas decorations and the pastry counter at St. Phillips Bakery.',
        'Les décorations de Noël et le comptoir de pâtisseries chez St. Phillips Bakery.', eager,
    )


def bakery_article(bakery, deck):
    hero = f'''<div class="page-intro bakery-hero"><div class="wrap">
        <div>
            <p class="eyebrow">{t('Local food & businesses', 'Restaurants et commerces locaux')}</p>
            <h1>{t(BAKERY_TITLE, 'St. Phillips Bakery à Nobleton : gâteaux, pâtisseries et café')}</h1>
            <p class="lead">{deck}</p>
        </div>
        {pastry_photo('(max-width: 680px) calc(100vw - 44px), 44vw', eager=True)}
    </div></div>'''

    story = h('Discover St. Phillips Bakery in Nobleton', 'Découvrez St. Phillips Bakery à Nobleton')
    story += p(
        'If you’re looking for a bakery in Nobleton, Ontario, whether it’s for a morning coffee, a freshly baked pastry, or a beautiful cake for a special occasion, St. Phillips Bakery is a place worth discovering.',
        'Si vous cherchez une boulangerie à Nobleton, en Ontario, pour un café le matin, une pâtisserie fraîchement préparée ou un beau gâteau pour une occasion spéciale, St. Phillips Bakery mérite le détour.',
    )
    story += p(
        'I recently stopped by St. Phillips in Nobleton, and what immediately caught my attention was the beautiful interior, the impressive selection of desserts, and the inviting atmosphere.',
        'Je suis récemment passée chez St. Phillips à Nobleton. Le décor, le choix de desserts et l’ambiance chaleureuse m’ont tout de suite frappée.',
    )
    story += h('Cakes, Pastries & Sweet Treats', 'Gâteaux, pâtisseries et douceurs')
    story += p(
        'One of the highlights of St. Phillips is its selection of desserts. From beautifully decorated cakes topped with fresh berries to individual pastries, cream-filled treats, and chocolate desserts, there’s plenty to choose from.',
        'Le choix de desserts est l’un des points forts de St. Phillips. Gâteaux décorés de petits fruits frais, pâtisseries individuelles, douceurs fourrées à la crème et desserts au chocolat : le choix est vaste.',
    )
    story += p(
        'Whether you’re looking for a birthday cake, something to bring to a family gathering, or simply a little treat to enjoy with your coffee, the bakery offers plenty of tempting options. The display alone is worth a look!',
        'Que vous cherchiez un gâteau d’anniversaire, un dessert à apporter à une réunion de famille ou une petite douceur avec votre café, les options sont nombreuses. La vitrine vaut à elle seule le coup d’œil!',
    )
    story += h('A Beautiful Place to Stop in Nobleton', 'Une belle halte à Nobleton')
    story += p(
        'The tall windows fill the space with natural light, while the high ceilings and modern finishes make it feel open and welcoming. During my visit, the bakery was already decorated for Christmas, adding a lovely festive touch.',
        'Les grandes fenêtres laissent entrer la lumière naturelle, tandis que les hauts plafonds et les finitions modernes donnent au lieu une impression d’espace. Lors de ma visite, la boulangerie avait déjà installé ses décorations de Noël, ce qui ajoutait une touche festive.',
    )
    story += p(
        'It’s the kind of place where you can stop for a coffee, pick up dessert for dinner, or take a break while exploring the Nobleton community.',
        'C’est le genre d’endroit où l’on s’arrête pour prendre un café, acheter un dessert pour le souper ou faire une pause en découvrant Nobleton.',
    )
    story += photo(
        'st-phillips-bakery-visit.webp', 1280, 960, '(max-width: 780px) calc(100vw - 44px), 720px',
        'Two people, including a bakery employee in an apron, standing beside the pastry display',
        'Deux personnes, dont une employée de la boulangerie en tablier, devant le comptoir de pâtisseries',
        'A moment with a member of the bakery team during our visit.',
        'Un moment avec une membre de l’équipe de la boulangerie lors de notre visite.',
    )
    story += h('Supporting Local Businesses in Nobleton', 'Soutenir les commerces de Nobleton')
    story += p(
        'One of the things that makes Nobleton special is discovering the businesses that bring people together. Local bakeries, cafés, restaurants, and family-owned shops all contribute to the character of a community.',
        'Le plaisir de découvrir des commerces qui rassemblent les gens fait partie du charme de Nobleton. Les boulangeries, cafés, restaurants et boutiques familiales contribuent tous au caractère de la communauté.',
    )
    story += p(
        'St. Phillips Bakery is a wonderful example of a place that adds to Nobleton’s appeal, whether you’re a longtime resident, new to the neighbourhood, or just passing through.',
        'St. Phillips Bakery illustre bien ce qui fait le charme de Nobleton, que vous y habitiez depuis longtemps, que vous veniez d’emménager ou que vous soyez simplement de passage.',
    )
    story += h('Looking for Places to Eat in Nobleton?', 'Vous cherchez où manger à Nobleton?')
    story += p(
        'If you’re exploring Nobleton and wondering where to find cakes, pastries, desserts, or a great spot for a coffee break, add St. Phillips Bakery to your list.',
        'Si vous explorez Nobleton et cherchez des gâteaux, des pâtisseries, des desserts ou un endroit où prendre un café, ajoutez St. Phillips Bakery à votre liste.',
    )
    story += f'<p>{dining_link()}</p>'

    gallery_sizes = '(max-width: 440px) calc(100vw - 44px), (max-width: 780px) 45vw, 350px'
    cakes = photo(
        'st-phillips-cake-display.webp', 960, 1280, gallery_sizes,
        'Cakes topped with strawberries and cream along the bakery counter',
        'Gâteaux garnis de fraises et de crème le long du comptoir de la boulangerie',
        'Berry-topped cakes in the dessert display.', 'Des gâteaux garnis de petits fruits dans la vitrine.',
    )
    interior = photo(
        'st-phillips-bakery-interior.webp', 960, 1280, gallery_sizes,
        'A customer at the pastry counter under the Pasticceria sign inside the bakery',
        'Une cliente devant le comptoir de pâtisseries, sous l’enseigne Pasticceria à l’intérieur de la boulangerie',
        'The bakery’s light-filled pasticceria counter.', 'Le comptoir de pâtisseries baigné de lumière.',
    )
    story += f'<div class="bakery-gallery">{cakes}{interior}</div>'

    hours = t(*bakery['dining']['hours'])
    details = f'''<section id="visit" class="business-facts bakery-visit">
        <h2>{t('Plan your visit to St. Phillips Bakery', 'Préparer votre visite chez St. Phillips Bakery')}</h2>
        <dl>
            <div><dt>{t('Address', 'Adresse')}</dt><dd>{escape(bakery['address'])}</dd></div>
            <div><dt>{t('Phone', 'Téléphone')}</dt><dd><a href="tel:+1{bakery['phone'].replace('-', '')}">{escape(bakery['phone'])}</a></dd></div>
            <div><dt>{t('Hours', 'Heures d’ouverture')}</dt><dd>{hours}</dd></div>
        </dl>
        <p class="fine">{t('Hours verified November 20, 2026. Check with the bakery before visiting, especially around holidays.', 'Heures vérifiées le 20 novembre 2026. Confirmez auprès de la boulangerie avant de vous déplacer, surtout pendant les fêtes.')}</p>
        <div class="plan-actions">
            <a class="button" href="{escape(bakery['source_url'])}">{t('Official website', 'Site officiel')}</a>
            <a class="text-link" href="{BAKERY_DIRECTORY_PATH}">{t('View directory listing', 'Voir la fiche du répertoire')}</a>
        </div>
    </section>'''
    return f'<article>{hero}<div class="wrap reading section bakery-story">{story}{details}</div></article>'


def dining_place(place):
    facts = place['dining']
    name = BAKERY_NAME if place['slug'] == BAKERY_SLUG else place['name']
    directory = f'/directory/{place["slug"]}/'
    description = t(*facts['spotlight']) if 'spotlight' in facts else place['description']
    directions_params = urlencode({'api': 1, 'destination': f'{name}, {place["address"]}'})
    directions = escape(f'https://www.google.com/maps/dir/?{directions_params}')
    menu = t(*facts.get('menu_label', ('Menu', 'Menu')))

    if 'hours' in facts:
        source = escape(facts.get('hours_source', place['source_url']))
        hours = f'<a href="{source}">{escape(t(*facts["hours"]))}</a>'
    else:
        phone = place['phone'].replace('-', '')
        hours = f'<a href="tel:+1{phone}">{t("Call for hours", "Appeler pour connaître les heures")}</a>'

    return f'''<article class="dining-place">
        <h3><a href="{directory}">{escape(name)}</a></h3>
        <p>{escape(description)}</p>
        <dl>
            <dt>{t('Address', 'Adresse')}</dt><dd>{escape(place['address'])}</dd>
            <dt>{t('Hours', 'Heures d’ouverture')}</dt><dd>{hours}</dd>
        </dl>
        <div class="dining-place-actions">
            <a class="text-link" data-directory-action="menu" href="{escape(facts['menu_url'])}">{escape(menu)}</a>
            <a class="text-link" data-directory-action="directions" href="{directions}">{t('Get directions', 'Itinéraire')}</a>
        </div>
    </article>'''


def dining_listings(resources):
    groups = {slug: [] for slug, _, _ in DINING_GROUPS}
    for place in resources:
        if 'dining' in place:
            groups[place['dining']['group']].append(dining_place(place))

    sections = ''.join(
        f'<section id="{slug}" class="dining-group">{h(title, title_fr)}'
        f'<div class="dining-places">{"".join(groups[slug])}</div></section>'
        for slug, title, title_fr in DINING_GROUPS
    )
    return f'''<div class="wrap section dining-listings">
        <p class="fine">{t('Hours checked November 20, 2026. Follow the hours links for updates, including holiday changes.', 'Heures vérifiées le 20 novembre 2026. Consultez les liens pour les mises à jour, notamment les horaires des jours fériés.')}</p>
        {sections}
    </div>'''


def register(page, intro, resources):
    bakery = next(resource for resource in resources if resource['slug'] == BAKERY_SLUG)
    title = t('Best Bakery in Nobleton? Visit St. Phillips for Cakes & Pastries', 'Boulangerie à Nobleton? Découvrez les gâteaux et pâtisseries de St. Phillips')
    description = t(
        'Looking for cakes, pastries or coffee in Nobleton? Explore St. Phillips Bakery, see our photos and discover this local favourite.',
        'Vous cherchez des gâteaux, des pâtisseries ou un café à Nobleton? Découvrez en photos St. Phillips Bakery, une adresse appréciée du quartier.',
    )
    deck = t(
        'Discover local places to eat, enjoy a coffee, and shop for delicious desserts in Nobleton, Ontario.',
        'Découvrez les bonnes adresses de Nobleton, en Ontario, pour manger, prendre un café ou acheter des desserts.',
    )
    page(BAKERY_PATH.strip('/'), title, description, bakery_article(bakery, deck), 'Local guide')

    title = t(HUB_TITLE, 'Où manger à Nobleton')
    description = t(
        'Find cafés, bakeries, sit-down restaurants and takeout in Nobleton, Ontario, with menus, posted hours and directions.',
        'Trouvez des cafés, des boulangeries et des restaurants à Nobleton, en Ontario. Consultez les menus, les heures d’ouverture et les itinéraires.',
    )
    category_links = ''.join(f'<a href="#{slug}">{t(en, fr)}</a>' for slug, en, fr in DINING_GROUPS)
    categories = f'<nav class="wrap dining-nav" aria-label="{t("Dining categories", "Catégories de restaurants")}">{category_links}</nav>'
    feature = f'''<section class="wrap section dining-feature">
        {pastry_photo('(max-width: 680px) calc(100vw - 44px), 34vw', eager=True)}
        <div>
            {h(BAKERY_NAME, BAKERY_NAME)}
            <p>{bakery['description']}</p>
            {bakery_link()}
        </div>
    </section>'''
    header = intro(t('Local food & drink', 'Restaurants et cafés du coin'), title, description)
    page(HUB_PATH.strip('/'), title, description, header + categories + feature + dining_listings(resources), 'Local guide')
