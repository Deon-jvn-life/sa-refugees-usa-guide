# South African Refugees in the USA: plain-language guide

Static site. Live base URL: https://www.sarefugeesusa.org

- `python3 tools/build.py` regenerates `site/` (27 indexable pages, plus a noindex 404, robots.txt and sitemap.xml). The six money and tax pages sit under Work and money. The ordinary-employee checklist is the first page in the First year group on Start here.
- `tools/sitelib.py` is the page shell: topic menu, a compact sticky header, breadcrumbs, a time-order previous and next path, read next, search, an "On this page" list, glossary links, flags, Open Graph tags, JSON-LD, the legal notice, and checks that reject em dashes and en dashes.
- Public URLs are root-relative with a trailing slash (`/travel-document/`). `vercel.json` sets `cleanUrls` and `trailingSlash`. Canonical, Open Graph, JSON-LD and the sitemap use `https://www.sarefugeesusa.org`.
- Vercel serves the committed `site/` directory. There is no install or build step on Vercel.
- Rules: official sources only, a link beside every fact, "not stated by source" where a source is silent, conflicts shown, "Last checked" on every page. Not legal advice. See the disclaimer.
- See `tools/backlog.md` for gaps.
