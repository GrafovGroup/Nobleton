# Nobleton.ca IDX connection

Approved subscriber: Ekaterina Ottchenach, HomeLife Frontier Realty Inc., Brokerage.
Provider: PropTx / Amplify. Approved domain: Nobleton.ca. This is independent of ToRe.ca.

## Server layout

- `/home/nvfglyl5/nobleton-private/idx-token`: issued token, mode 0600. Never include it in source, browser JavaScript, deployment archives, diagnostics or chat.
- `/home/nvfglyl5/nobleton-private/idx/`: `lib.php` and CLI-only `sync.php`.
- `/home/nvfglyl5/nobleton-private/idx-cache.json`: atomically replaced listing/photo snapshot, mode 0600.
- `/home/nvfglyl5/nobleton-private/idx-health.json`: success/error status and time only.
- `/home/nvfglyl5/nobleton.ca/api/listings.php`: bounded read-only search endpoint.

WHC PHP 8.2 with curl and SimpleXML. The secret stays outside the document root. The existing approved token is used; no new access or credentials are created.

## Synchronization and display

Cron runs `php /home/nvfglyl5/nobleton-private/idx/sync.php` every 15 minutes. Each successful run fully reconciles the Nobleton subset and its photographs. Available status and community are checked both in the upstream query and locally. Explicit distribution opt-outs are excluded; hidden addresses and confidential/unselected fields never reach the browser. Brokerage attribution is required for a record to be displayed.

Property and Media resources are fetched separately. The approved feed returned HTTP 200 with an empty body for `$expand=Media(...)` during setup; separate Media requests use the documented resource relationship. Schema metadata determines which optional fields are available. Key-based pagination avoids incomplete fixed-offset synchronization. A partial or failed refresh never replaces a complete cache. Authorization failures invalidate the cache immediately; any cache older than one hour is withheld. The browser refreshes every 15 minutes and clears expired results when it becomes visible.

Public results are limited to 12 records per request, below the agreement's 100-record limit. There is no arbitrary OData or URL passthrough. Listing remarks, addresses, transaction labels and brokerage names are preserved as supplied, with text-only DOM rendering. EN/FR controls are translated; feed content is not rewritten or machine-translated. Thumbnail and detail views show the listing brokerage and reliability notice. Subscriber contact details are separated from listing details.

The static Sites mirror links to the approved Nobleton.ca search and does not request or display feed data. Do not add CORS origins or subscriber domains without the required approval. No listing records are stored in Git, build output, analytics or AI services. WHC access logs provide the request audit trail; protect and retain those logs in accordance with the active agreement and privacy policy.

## Deployment / rollback

Build with `python3 publish-build.py`. Package `dist/`, `server/`, and `tests/idx.php` into a release outside the document root. Run `server/deploy-idx.sh` from that extracted release. It lints PHP, runs synthetic unit checks, refreshes the private cache, backs up the existing Nobleton document root and cron table, deploys the static files/API, and installs only the Nobleton IDX cron entry. Existing inquiry delivery, Apache rules and search-verification files are preserved.

If refresh fails, inspect `idx-health.json` and the private `idx-sync.log`; they contain error codes, never records or tokens. Correct the authorized credential/configuration and rerun the CLI sync. Do not log upstream response bodies. For a site rollback, restore the timestamped `backup-before-idx-*.tar.gz` and the previous cron table from `nobleton-deployments`. Remove the public listings endpoint if rolling back to a release that predates it. Stop the cron and remove cached data if feed authorization is withdrawn.

## Validation

- `php tests/idx.php`: synthetic tests for display permission, geography/status, private-field removal, address suppression, URL schemes, exact remarks, filters, pagination and metadata parsing.
- `node --check outputs/nobleton-site/assets/listings.js` and `node --check outputs/nobleton-site/assets/plan.js`.
- `node tests/idx-browser.cjs`: optional local Playwright tests with synthetic records only. Requires Playwright and a Chromium executable (`CHROMIUM_PATH`, default `/usr/bin/chromium`). The managed executor blocked Chromium's Unix socket at setup; this automated suite was not run successfully there. Live browser verification passed for EN/FR rendering, images, price-filter empty state, reset, keyboard dismissal, and inquiry-reference routing.
- Verify the live EN/FR search, filters, photo loading, modal keyboard behavior, empty/error states and inquiry reference. No real inquiries should be sent without an explicit test request.

Provider references: https://developer.ampre.us/docs/getting-started, https://developer.ampre.us/docs/replication, https://developer.ampre.us/docs/resources/media, and the active website-specific agreement in the PropTx portal.
