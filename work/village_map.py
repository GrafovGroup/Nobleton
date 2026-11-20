"""A bilingual, north-up schematic of the main Nobleton village landmarks."""

from plan_content import t


# Park placement follows the Township's Parks & Forestry Services Master Plan,
# Figure 2.0 (Nobleton Distribution). The library address and location are
# from King Township Public Library and YorkMaps. King Township's Hambly
# House heritage statement places the property northwest of the crossroads.
LANDMARKS = (
    (
        (231, 271),
        ('Hambly House', 'Maison Hambly'),
        ('6012 King Road · Northwest corner of the crossroads',
         '6012 King Road · Angle nord-ouest du carrefour'),
        '/guide/history/',
    ),
    (
        (157, 158),
        ('Nobleton Library', 'Bibliothèque de Nobleton'),
        ('8 Sheardown Drive · North of King Road, just west of Highway 27',
         '8 Sheardown Drive · Au nord de King Road, juste à l’ouest de la route 27'),
        'https://www.kinglibrary.ca/hours-locations',
    ),
    (
        (430, 96),
        ('Tasca Park', 'Parc Tasca'),
        ('49 Parkheights Trail · Northeast of the village crossroads',
         '49 Parkheights Trail · Au nord-est du carrefour du village'),
        'https://www.king.ca/recreation-living/parks-trails-and-forestry/parks/tasca-park',
    ),
    (
        (412, 329),
        ('Nobleton Community Park', 'Parc communautaire de Nobleton'),
        ('15 Old King Road · Southeast of the village crossroads',
         '15 Old King Road · Au sud-est du carrefour du village'),
        'https://www.king.ca/recreation-living/parks-trails-and-forestry/parks/nobleton-community-park',
    ),
)


def village_map():
    pins = []
    legend = []
    for number, (point, name, location, link) in enumerate(LANDMARKS, 1):
        x, y = point
        pins.append(
            f'<g class="village-map__pin" transform="translate({x} {y})">'
            '<circle r="18"></circle>'
            f'<text y="0" text-anchor="middle" dominant-baseline="central">{number}</text></g>'
        )
        legend.append(
            f'<li><span class="village-map__number" aria-hidden="true">{number}</span>'
            f'<div><a href="{link}">{t(*name)}</a>'
            f'<p>{t(*location)}</p></div></li>'
        )

    # The roads illustrate orientation around the crossroads. Only the two
    # main corridors are marked because this is a landmark schematic.
    markup = f'''
<section class="wrap section village-map" aria-labelledby="village-map-title">
  <h2 id="village-map-title">{t('Nobleton village map', 'Carte du village de Nobleton')}</h2>
  <p class="village-map__intro">{t(
      'Find local landmarks around the King Road and Highway 27 crossroads.',
      'Repérez les lieux d’intérêt autour du carrefour de King Road et de la route 27.'
  )}</p>
  <div class="village-map__layout">
    <figure class="village-map__figure">
      <svg class="village-map__drawing" viewBox="0 0 600 380" aria-hidden="true" focusable="false">
        <defs>
          <path id="village-map-king-road" d="M-12 320 C83 312 187 305 269 296 S382 282 432 259 Q496 229 612 216"></path>
          <path id="village-map-highway-27" d="M128 -12 L308 392"></path>
        </defs>
        <path class="village-map__park" d="M352 67 Q400 40 453 44 Q519 48 523 91 Q530 136 473 139 Q429 158 377 131 Q339 112 352 67Z"></path>
        <path class="village-map__park" d="M366 331 Q387 299 455 293 Q518 282 547 311 Q573 343 539 368 Q503 384 429 378 Q369 378 366 331Z"></path>
        <g class="village-map__trees">
          <path d="M378 101V78m-8 8 8-15 8 15m-18 8 10-14 10 14 M482 115V88m-8 9 8-16 8 16m-18 8 10-15 10 15"></path>
          <path d="M482 351v-25m-8 9 8-16 8 16m-18 8 10-15 10 15 M520 345v-19m-6 7 6-13 6 13m-14 6 8-12 8 12"></path>
        </g>
        <g class="village-map__road-border">
          <use href="#village-map-king-road"></use>
          <use href="#village-map-highway-27"></use>
        </g>
        <g class="village-map__road-fill">
          <use href="#village-map-king-road"></use>
          <use href="#village-map-highway-27"></use>
        </g>
        <g class="village-map__street-names">
          <text x="32" y="293">{t('King Road', 'King Road')}</text>
          <text x="197" y="65">{t('Highway 27', 'Route 27')}</text>
        </g>
        <g class="village-map__north" transform="translate(559 51)">
          <text x="0" y="-7" text-anchor="middle">{t('N', 'N')}</text>
          <path d="M0 1 9 21 0 17 -9 21Z"></path>
        </g>
        {''.join(pins)}
      </svg>
      <figcaption>{t('Schematic map. Locations are approximate.', 'Carte schématique. Les emplacements sont approximatifs.')}</figcaption>
    </figure>
    <ol class="village-map__legend" role="list">
      {''.join(legend)}
    </ol>
  </div>
  <p class="village-map__sources"><a href="https://www.king.ca/maps">{t('Explore Township maps', 'Consultez les cartes du canton')}</a></p>
</section>
'''
    return ''.join(line.strip() for line in markup.splitlines())
