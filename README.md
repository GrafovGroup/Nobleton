# Nobleton

Independent community guide and directory. Static HTML, CSS and JavaScript; Python 3 builds 61 English and 61 French pages without third-party dependencies.

## Build

```sh
python3 publish-build.py
```

Deploy `dist/` with real 404 handling using `dist/404.html`. The default canonical origin is https://nobleton.ca. Set `NOBLETON_SITE_ORIGIN` to an active production custom domain before rebuilding if the domain changes. Submit that origin's `/sitemap.xml` to Search Console.

## Edit

- `work/build.py`: templates, directory resources, forms and routes.
- `work/local_content.py`: local guide text.
- `work/guide_enrichment.py`: practical local guide details and dated source links.
- `work/businesses.json`: 25 business records with official sources and bilingual descriptions.
- `work/growth.py`: business profiles, discovery cards and advertising formats.
- `work/seo.py`: canonical URLs, metadata, structured data, robots and sitemap.
- `outputs/nobleton-site/assets/`: source CSS, JavaScript and images.
- `publish-build.py`: production build entry point.
- `.openai/hosting.json`: existing Sites deployment identity.

Business submissions and service requests POST to `https://formspree.io/f/xljjnzbr`. The Formspree AJAX CDN helper provides loading, success and validation/error states; native HTML POST is the fallback when JavaScript is unavailable. Both forms use the `email` reply-to field, `message`, distinct `_subject` and `inquiry_type` fields. Formspree dashboard settings control recipient notifications, spam protection and allowed domains. Generated imagery is labelled and is not a photograph of an actual location or property listing. Resource review dates reflect the source content, not the most recent software build.

## October 2026 UX/search improvements

Fluid page containers, readable article widths, responsive navigation, larger text and touch targets, populated homepage categories, directory filter reset, guide contents links, explicit location heading and social sharing metadata. Existing canonical URLs, crawl policy, sitemap, breadcrumbs and entity markup are preserved. The property search page clearly explains that the listing feed is pending.

Content growth remains the main opportunity: verified business listings, real local photographs and maintained official-resource links. Search rankings and inclusion in AI answers are not guaranteed.

## Local photography

Hambly House (Peter Broster, CC BY-SA 4.0), Nobleton Lakes (Ken Mist, CC BY 2.0), Roslyn House (Kingrd, CC BY-SA 3.0), and two Tasca Park photographs (Magnolia677, CC BY 4.0 and CC BY-SA 4.0) are locally hosted, resized photographs. See `/photo-credits/` for original sources, license links, dates and change notices. Reuse retains each image license. Other luxury property imagery remains labelled AI-generated inspiration.

Advertising inquiries: `/advertise/` uses the same Formspree endpoint with `inquiry_type=advertising` and a dedicated email subject. Homepage and footer calls to action link to this page. No prices, audience claims or paid bookings are offered.

## English and French

English routes remain at `/`; equivalent French routes are under `/fr/`. Every page has an EN/FR switcher, self-canonical URL, reciprocal `hreflang` links and localized metadata/JSON-LD. The switcher preserves query strings and section anchors. Official organization names and external source URLs are retained.

`work/fr.json` is the exact French text catalogue; `work/bilingual.py` generates the French HTML during `python3 publish-build.py`. Untranslated new visible text fails the production build. Update the catalogue when editing English copy. Shared CSS/JS/images are not duplicated. Forms include `preferred_language`, with localized sending, success and error messages. General business forms use Formspree. Professional inquiries use the separately deployed WHC PHP endpoint in `server/inquiry.php`.

## November 2026 search and usability updates

Unique bilingual metadata, concise breadcrumbs, publisher identity and visible editorial attribution on guides; direct homes/mortgage navigation and contextual mobile contact links. The sitemap lists 118 canonical URLs with reciprocal English/French alternates. `work/content-revisions.json` records content hashes and last-modified dates; unchanged builds do not change dates, and CSS/navigation-only changes do not reset them.

WHC-specific Apache configuration is maintained in `server/nobleton.htaccess` and deployed separately from `dist/`. Preserve search-verification files when deploying. Search submissions are requests for discovery, not a guarantee of indexing.

## Consent-based analytics and local discovery

GA4 property `563488180`, web stream `16308299110`, measurement ID `G-W01L22WKDM` belongs to Nobleton.ca in the Grafov Group account. Analytics load only on `nobleton.ca`/`www.nobleton.ca`, after consent. Footer preferences allow withdrawal. Enhanced Measurement is disabled in the property. Tracking excludes query strings, form fields, contact identifiers and calculator amounts. `generate_lead` fires after a successful inquiry response, not when a visitor merely presses Submit. Other events measure contact clicks, directory actions, advertising interest and calculator use.

The directory includes 25 sourced businesses and five public resources. Entries are free editorial listings; paid examples on `/advertise/` are labelled samples. Homepage and events pages share a dated event dataset and hide past events using Ontario local dates. Maintain the dataset in `work/plan_content.py`; automatic expiry does not discover new events. Practical guide questions for the professionals are editorial prompts, not attributed quotes or claimed professional review.

## Temporary remembrance tribute

A red remembrance poppy appears beside the header wordmark in both languages until `2026-11-15T02:55:29Z` (five days after activation). `assets/remembrance.js` checks the fixed expiry before rendering, removes it from open tabs at expiry and rechecks when a tab becomes visible. It does not repeat in future years.

The poppy uses the owner-supplied photograph, edited to remove the metal pin and white background; a transparent WebP is used in the header.
