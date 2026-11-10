"""Sourced, bilingual local detail for Nobleton's existing guides.

Call enrich_guide before layout builds its table of contents, then merge
TRANSLATIONS into the production translation catalogue. No professional
authorship or review is implied by the editorial question prompts.
"""
from html import escape

TRANSLATIONS = {}


def enrich_guide(body, path, photo, t):
    if path not in {'/guide/parks/', '/guide/essentials/', '/guide/moving-to-nobleton/', '/guide/schools/'}:
        return body

    def tr(en, fr):
        TRANSLATIONS[en] = fr
        return t(en, fr)

    def para(en, fr):
        return '<p>' + escape(tr(en, fr)) + '</p>'

    def heading(en, fr):
        return '<h2>' + escape(tr(en, fr)) + '</h2>'

    def link(url, en, fr):
        return '<a class="text-link" href="' + escape(url, quote=True) + '">' + escape(tr(en, fr)) + '</a>'

    def bullets(items):
        return '<ul>' + ''.join('<li>' + escape(tr(en, fr)) + '</li>' for en, fr in items) + '</ul>'

    extra = ''
    if path == '/guide/parks/':
        extra += heading('Choose a park for the outing you have in mind', 'Choisissez un parc selon votre sortie')
        extra += para('For a neighbourhood outing, Davis Park at 45 MacTaggart Drive has a playground, mini-soccer fields and walking trails. Tasca Park, at 49 Parkheights Trail, has a trail and a designated off-leash dog area. Check the Township’s current notices before using the dog park or seasonal facilities.', 'Pour une sortie dans le quartier, le parc Davis, au 45 MacTaggart Drive, offre une aire de jeux, des terrains de mini-soccer et des sentiers. Le parc Tasca, au 49 Parkheights Trail, comprend un sentier et une aire pour chiens sans laisse. Consultez les avis du Canton avant d’utiliser le parc canin ou les installations saisonnières.')
        extra += link('https://www.king.ca/parks', 'Park locations and current notices', 'Emplacements des parcs et avis en vigueur')
        extra += photo('nobleton-tasca-playground', tr('Green and blue playground equipment at Tasca Park, Nobleton, photographed in 2021', 'Structures de jeux vertes et bleues au parc Tasca, à Nobleton, photographiées en 2021'), '', extra='guide-detail-photo')
        extra += heading('Make room for a longer walk', 'Prévoyez une promenade plus longue')
        extra += para('Cold Creek Conservation Area is at 14125 11th Concession. King Township lists marked trails, a picnic shelter and opportunities for birdwatching; dogs must remain on leash. For an accessible trail option, the Township identifies the York Regional Forest entrance at 5345 15th Sideroad, with accessible parking. Check current conditions and the route before setting out.', 'L’aire de conservation Cold Creek se trouve au 14125 11th Concession. Le canton de King y répertorie des sentiers balisés, un abri de pique-nique et des possibilités d’observation des oiseaux; les chiens doivent rester en laisse. Pour un parcours accessible, le Canton indique l’entrée de la forêt régionale de York au 5345 15th Sideroad, avec stationnement accessible. Vérifiez les conditions et le parcours avant de partir.')
        extra += link('https://www.king.ca/trails', 'Official trail information and map', 'Renseignements officiels et carte des sentiers')
        extra += heading('Plan a library stop', 'Prévoyez un arrêt à la bibliothèque')
        extra += para('The Nobleton library is at 8 Sheardown Drive; call 905-859-4188. Its published schedule currently includes Wednesday and Thursday evenings until 8 p.m. The branch is closed on Sundays and Mondays. Check the library’s own hours page for holiday changes before you leave.', 'La bibliothèque de Nobleton se trouve au 8 Sheardown Drive; téléphone : 905-859-4188. Son horaire publié comprend actuellement les mercredis et jeudis soirs jusqu’à 20 h. La succursale est fermée les dimanches et lundis. Consultez son horaire officiel pour les changements liés aux jours fériés avant de partir.')
        extra += link('https://www.kinglibrary.ca/hours-locations', 'Confirm library hours', 'Confirmer les heures de la bibliothèque')

    elif path == '/guide/essentials/':
        extra += heading('Waste collection: start with your address', 'Collecte des déchets : commencez par votre adresse')
        extra += para('Use King Township’s waste calendar and collection-area map to find the schedule for your home. The Township also links to Recycle Coach for sorting questions. Extra garbage tags are sold through the Township and at King Township library branches, including Nobleton. Check current limits and accepted materials before putting items at the curb.', 'Utilisez le calendrier des déchets et la carte des secteurs de collecte du canton de King pour trouver l’horaire de votre domicile. Le Canton propose aussi Recycle Coach pour les questions de tri. Des étiquettes pour sacs supplémentaires sont vendues par le Canton et dans ses bibliothèques, dont Nobleton. Vérifiez les limites et les matières acceptées avant de déposer vos articles en bordure de rue.')
        extra += link('https://www.king.ca/collection', 'Collection resources and calendar links', 'Ressources de collecte et liens vers le calendrier')
        extra += heading('Water and wastewater are property-specific', 'L’eau et les égouts varient selon la propriété')
        extra += para('King Township operates local municipal water distribution in Nobleton and local wastewater collection where properties are connected. Do not assume every property has the same connections or charges. Before buying or renting, ask which services supply the address and where to arrange the account change.', 'Le canton de King exploite le réseau local de distribution d’eau municipale à Nobleton et la collecte des eaux usées pour les propriétés raccordées. Les raccordements et frais ne sont pas nécessairement les mêmes partout. Avant d’acheter ou de louer, demandez quels services desservent l’adresse et comment effectuer le changement de compte.')
        extra += link('https://www.king.ca/waterbilling', 'Water billing and connection information', 'Facturation de l’eau et renseignements sur les raccordements')
        extra += heading('Keep one local contact sheet', 'Gardez une fiche de contacts locaux')
        extra += para('Save your collection schedule, school office, library and service-provider contacts in one place. For municipal service questions, King Township lists 905-833-5321. For a business or community resource, browse our directory and contact the organization directly to confirm availability.', 'Regroupez votre horaire de collecte et les coordonnées de l’école, de la bibliothèque et de vos fournisseurs. Pour les services municipaux, le canton de King indique le 905-833-5321. Pour une entreprise ou une ressource communautaire, consultez notre répertoire et confirmez la disponibilité directement auprès de l’organisation.')
        extra += link('/directory/', 'Browse local businesses and resources', 'Parcourir les entreprises et ressources locales')

    elif path == '/guide/schools/':
        extra += heading('Local school contacts at a glance', 'Les coordonnées des écoles en bref')
        extra += para('Nobleton Public School serves Junior Kindergarten through Grade 8 at 13375 Highway 27. Its published office number is 905-859-4590. St. Mary Catholic Elementary School is at 75 Greenside Drive; its office number is 905-859-3336.', 'Nobleton Public School accueille les élèves de la prématernelle à la 8e année au 13375 Highway 27. Son numéro publié est le 905-859-4590. St. Mary Catholic Elementary School se trouve au 75 Greenside Drive; son numéro est le 905-859-3336.')
        extra += '<div class="plan-actions">' + link('https://nobleton-ps.yrdsb.ca/', 'Nobleton Public School contact details', 'Coordonnées de Nobleton Public School') + link('https://smy.ycdsb.ca/contact/', 'St. Mary contact details', 'Coordonnées de St. Mary') + '</div>'
        extra += heading('Use the exact home address when checking boundaries', 'Vérifiez le secteur scolaire avec l’adresse exacte')
        extra += para('The York Region District School Board reviews attendance areas and warns that some new residents may be directed to a different school because of enrolment pressures. Use the board’s elementary or secondary boundary tool, then confirm the result with the school before making plans around a particular address.', 'Le York Region District School Board révise les secteurs de fréquentation et précise que certains nouveaux résidents peuvent être dirigés vers une autre école en raison du nombre d’inscriptions. Utilisez l’outil de secteurs du primaire ou du secondaire, puis confirmez le résultat auprès de l’école avant de planifier votre déménagement en fonction d’une adresse.')
        extra += link('https://www2.yrdsb.ca/schools-programs/school-boundaries', 'Check public-school boundaries', 'Vérifier les secteurs des écoles publiques')
        extra += heading('Questions for your registration call', 'Questions à poser pour l’inscription')
        extra += bullets([
            ('Which school and program serve this address for the intended school year?', 'Quelle école et quel programme desservent cette adresse pour l’année scolaire visée?'),
            ('Which eligibility documents and proof of address will the school require?', 'Quels documents d’admissibilité et justificatifs d’adresse l’école demande-t-elle?'),
            ('Where can we confirm transportation, before-school care and after-school care?', 'Où confirmer le transport ainsi que les services de garde avant et après l’école?'),
        ])

    elif path == '/guide/moving-to-nobleton/':
        extra += heading('Compare homes using the same everyday checklist', 'Comparez les maisons avec la même liste pratique')
        extra += para('For each address, record your school confirmation, the routes you actually travel, service connections and the local places you will use. Keep dated answers together so you can compare properties consistently instead of relying on a neighbourhood label.', 'Pour chaque adresse, notez la confirmation scolaire, vos trajets habituels, les raccordements aux services et les lieux que vous utiliserez. Conservez ensemble les réponses datées pour comparer les propriétés de façon cohérente, au-delà du nom du quartier.')
        extra += heading('Bring focused questions to your professionals', 'Préparez des questions précises pour vos professionnels')
        extra += para('Use these editorial prompts to prepare a conversation; they are not quotations or recommendations from the professionals.', 'Ces questions préparées par notre rédaction servent à amorcer une discussion; il ne s’agit pas de citations ni de recommandations des professionnels.')
        extra += '<h3>' + tr('Questions for Ekaterina', 'Questions pour Ekaterina') + '</h3>' + bullets([
            ('Which property details need a closer check before we make an offer?', 'Quels détails de la propriété faut-il examiner avant de présenter une offre?'),
            ('Which comparable sales and property differences support the asking price?', 'Quelles ventes comparables et différences entre les propriétés permettent d’évaluer le prix demandé?'),
            ('What timing should we plan for our sale, purchase and move?', 'Quel échéancier prévoir pour la vente, l’achat et le déménagement?'),
        ]) + link('/ask-realtor/', 'Start a conversation with Ekaterina', 'Commencer une discussion avec Ekaterina')
        extra += '<h3>' + tr('Questions for Anatoly', 'Questions pour Anatoly') + '</h3>' + bullets([
            ('What information should I prepare for a financing discussion?', 'Quels renseignements préparer pour discuter du financement?'),
            ('Which costs should I include beyond the mortgage payment?', 'Quels coûts prévoir en plus du versement hypothécaire?'),
            ('How do the available terms fit my likely moving or repayment plans?', 'Comment les modalités offertes correspondent-elles à mes projets de déménagement ou de remboursement?'),
        ]) + link('/mortgage-consultation/?topic=question', 'Ask Anatoly a mortgage question', 'Poser une question hypothécaire à Anatoly')
        extra += heading('Set up the first week before moving day', 'Préparez la première semaine avant le déménagement')
        extra += para('Confirm key handover and service-account changes, save the local waste schedule, and check opening hours before collecting library materials or visiting facilities. Share only the information a provider needs for your booking and keep written confirmations of the work and price.', 'Confirmez la remise des clés et les changements de comptes, enregistrez l’horaire des déchets et vérifiez les heures avant de passer à la bibliothèque ou aux installations locales. Ne communiquez que les renseignements nécessaires à votre réservation et conservez les confirmations écrites des travaux et du prix.')
        extra += link('/guide/essentials/', 'Open the local essentials guide', 'Ouvrir le guide des services essentiels')

    marker = '<p class="fine">Sources linked above · Reviewed September 7, 2026.</p>'
    stamp = '<p class="fine">' + tr('Local details checked November 9, 2026 against the official sources linked above. Confirm schedules and availability before visiting.', 'Renseignements locaux vérifiés le 9 novembre 2026 dans les sources officielles indiquées ci-dessus. Confirmez les horaires et la disponibilité avant de vous déplacer.') + '</p>'
    if marker in body:
        body = body.replace(marker, '<div class="guide-enrichment">' + extra + '</div>' + stamp)
    else:
        body = body.replace('</article>', '<div class="guide-enrichment">' + extra + '</div>' + stamp + '</article>', 1)
    body = body.replace('Editorial checklist · September 7, 2026. Local resource details are sourced in the linked guides. Property-specific questions should be confirmed directly.', tr('Editorial checklist · November 9, 2026. Local resource details are sourced in the linked guides. Property-specific questions should be confirmed directly.', 'Liste de vérification éditoriale · 9 novembre 2026. Les renseignements locaux sont documentés dans les guides liés. Confirmez directement les questions propres à une propriété.'))
    return body
