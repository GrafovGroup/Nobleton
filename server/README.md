# Professional inquiry delivery

WHC runs `inquiry.php` at `/home/nvfglyl5/nobleton.ca/api/inquiry.php`. Keep PHP outside the static Sites `dist` directory. Form actions use the canonical Nobleton.ca endpoint; the Sites mirror is allowlisted for CORS.

Recipients are fixed in the handler: real estate and valuations to realtor@nobleton.ca, mortgages to mortgage@nobleton.ca. Both receive an inquiry only when the visitor separately opts in. No addresses from request data are accepted as destinations. PHP mail acceptance does not establish inbox delivery; confirm both mailbox delivery after deployment using an owner-authorized test. No test emails were sent during implementation.

Deploy static files, lint PHP (`php -l server/inquiry.php`), then copy it to `api/inquiry.php`. Rate counters live outside the public root; 4 valid attempts per IP hash per hour. No inquiry body is written to disk by this handler. Invalid/honeypot requests do not send mail.

Analytics are deliberately inactive: set `measurementId` in `assets/analytics.js` only after the owner supplies a valid GA4 property ID. Disable Enhanced Measurement automatic form interactions and site-search tracking in that property, and update the privacy notice when activated. The custom events exclude PII and user-entered amounts. Search Console ownership verification still requires the owner's property access; the bilingual sitemap is `/sitemap.xml`.

The approved live property feed remains a separate dependency: a website-specific data agreement, feed access and provider display/inquiry requirements must be available before enabling listing search. Do not seed invented listings.
