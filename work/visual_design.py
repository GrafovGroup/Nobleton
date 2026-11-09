"""Presentation components for the Nobleton community guide."""

def icon(kind):
    paths = {
        'Schools': '<path d="m3 9 9-5 9 5-9 5-9-5Z"/><path d="M7 12v5c3 2 7 2 10 0v-5M21 9v8"/>',
        'Community': '<path d="M3 10 12 3l9 7M5 9v12h14V9M9 21v-8h6v8"/>',
        'Parks & recreation': '<path d="m12 2-6 8h3l-5 7h6v5h4v-5h6l-5-7h3l-6-8Z"/>',
        'Business resources': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12c5 4 13 4 18 0M10 13h4"/>',
        'Home services': '<path d="M3 10 12 3l9 7M5 9v12h14V9M9 21v-8h6v8"/>',
        'Food & drink': '<path d="M5 3v8m4-8v8M5 7h4M7 11v10M17 3v18M17 3c-5 3-5 9 0 9"/>',
        'Health & wellness': '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6V3Z"/>',
        'Shopping': '<path d="M4 8h16l1 13H3L4 8ZM8 8V6a4 4 0 0 1 8 0v2"/>',
        'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    }
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths.get(kind,paths['Community'])+'</svg>'

def home_page(photo, card, resources):
    links = [('Schools','Schools & families','/guide/schools/'),('Parks & recreation','Parks & recreation','/guide/parks/'),('Community','Local directory','/directory/'),('Business resources','Local services','/find-a-service/')]
    shortcuts = ''.join(f'<a href="{url}"><span class="shortcut-icon">{icon(kind)}</span><span>{label}</span></a>' for kind,label,url in links)
    return f'''
<section class="home-hero" aria-labelledby="home-title">
  {photo('nobleton-hambly-house','Red-brick Hambly House with its central tower in Nobleton','',extra='home-hero-photo',eager=True)}
  <div class="home-hero-content">
    <p class="eyebrow">YOUR INDEPENDENT LOCAL GUIDE</p>
    <h1 id="home-title">Nobleton.<br><em>A little closer<br>to home.</em></h1>
    <p>Discover the places, people and everyday possibilities that make this corner of King Township feel like home.</p>
    <form class="search" action="/directory/" role="search"><label class="sr-only" for="home-search">Search the local directory</label><span>{icon('search')}</span><input id="home-search" name="q" placeholder="What are you looking for?" type="search"><button type="submit">Explore</button></form>
    <div class="hero-links"><a href="/guide/">Explore the village</a><a href="/real-estate/">Find your next chapter</a></div>
  </div>
</section>
<nav class="discovery-bar wrap" aria-label="Discover Nobleton">{shortcuts}</nav>
<section class="wrap section village-story">
  <div class="story-photo">{photo('nobleton-lakes','Pond framed by autumn foliage at Nobleton Lakes, photographed in October 2006','',extra='story-landscape')}<span class="photo-tag">A SENSE OF PLACE</span></div>
  <div class="story-copy"><p class="eyebrow">SMALL-TOWN ROOTS</p><h2>Room to breathe.<br>More to discover.</h2><p>New here or here for years? Find the everyday essentials and places that bring the community together.</p><div class="story-links"><a href="/guide/schools/"><span>01</span><div><h3>Schools & families</h3><p>Start with local schools and official resources.</p></div></a><a href="/guide/parks/"><span>02</span><div><h3>Outside & around town</h3><p>Parks, library visits and ways to spend the day.</p></div></a><a href="/guide/moving-to-nobleton/"><span>03</span><div><h3>Make your move</h3><p>A practical checklist for settling into Nobleton.</p></div></a></div></div>
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
