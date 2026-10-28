# Nobleton

Independent community guide and directory. Static HTML, CSS and JavaScript; Python 3 builds the 19 pages without third-party dependencies.

## Build

```sh
python3 publish-build.py
```

Deploy `dist/` with real 404 handling using `dist/404.html`. The default canonical origin is https://nobleton.dimagrafov.chatgpt.site. Set `NOBLETON_SITE_ORIGIN` to an active production custom domain before rebuilding if the domain changes. Submit that origin's `/sitemap.xml` to Search Console.

## Edit

- `work/build.py`: templates, directory resources, forms and routes.
- `work/local_content.py`: local guide text.
- `work/seo.py`: canonical URLs, metadata, structured data, robots and sitemap.
- `outputs/nobleton-site/assets/`: source CSS, JavaScript and images.
- `publish-build.py`: production build entry point.
- `.openai/hosting.json`: existing Sites deployment identity.

Business submissions and service requests POST to `https://formspree.io/f/xljjnzbr`. The Formspree AJAX CDN helper provides loading, success and validation/error states; native HTML POST is the fallback when JavaScript is unavailable. Both forms use the `email` reply-to field, `message`, distinct `_subject` and `inquiry_type` fields. Formspree dashboard settings control recipient notifications, spam protection and allowed domains. No analytics is configured. Generated imagery is labelled and is not a photograph of an actual location or property listing. Resource review dates reflect the source content, not the most recent software build.

## October 2026 UX/search improvements

Fluid page containers, readable article widths, responsive navigation, larger text and touch targets, populated homepage categories, directory filter reset, guide contents links, explicit location heading and social sharing metadata. Existing canonical URLs, crawl policy, sitemap, breadcrumbs and entity markup are preserved. The incomplete real-estate section remains noindex.

Content growth remains the main opportunity: verified business listings, real local photographs and maintained official-resource links. Search rankings and inclusion in AI answers are not guaranteed.

## Local photography

Hambly House (Peter Broster, CC BY-SA 4.0), Nobleton Lakes (Ken Mist, CC BY 2.0) and Roslyn House (Kingrd, CC BY-SA 3.0) are locally hosted, resized photographs. See `/photo-credits/` for original sources, license links, dates and change notices. Reuse retains each image license. Other luxury property imagery remains labelled AI-generated inspiration.

Advertising inquiries: `/advertise/` uses the same Formspree endpoint with `inquiry_type=advertising` and a dedicated email subject. Homepage and footer calls to action link to this page. No prices, audience claims or paid bookings are offered.
