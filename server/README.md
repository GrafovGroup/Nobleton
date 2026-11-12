# Professional inquiry delivery

WHC runs `inquiry.php` at `/home/nvfglyl5/nobleton.ca/api/inquiry.php`. Keep PHP outside the static Sites `dist` directory. Form actions use the canonical Nobleton.ca endpoint; the Sites mirror is allowlisted for CORS.

Recipients are fixed in the handler: real estate and valuations to realtor@nobleton.ca, mortgages to mortgage@nobleton.ca. Both receive an inquiry only when the visitor separately opts in. No addresses from request data are accepted as destinations. PHP mail acceptance does not establish inbox delivery; confirm both mailbox delivery after deployment using an owner-authorized test. No test emails were sent during implementation.

Deploy static files, lint PHP (`php -l server/inquiry.php`), then copy it to `api/inquiry.php`. Rate counters live outside the public root; 4 valid attempts per IP hash per hour. No inquiry body is written to disk by this handler. Invalid/honeypot requests do not send mail.

Analytics use GA4 `G-W01L22WKDM` in the dedicated Nobleton.ca property. The script loads only on the canonical domain after consent; visitors can withdraw via footer preferences. Enhanced Measurement is disabled. The custom events exclude query strings, personal form data and user-entered amounts; `generate_lead` fires only on a successful inquiry response. The privacy notice describes this. Preserve the live search-verification file and Bing verification meta tag; the bilingual sitemap is `/sitemap.xml`.

See `IDX.md` for the approved Nobleton.ca feed connector, private credential location, synchronization, recovery and deployment instructions.
