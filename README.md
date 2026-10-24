# South African Refugees in the USA: plain-language guide

Static site. Live base URL: https://sa-refugees-usa-guide.vercel.app

- `python3 tools/build.py` regenerates `site/` (14 pages, robots.txt, sitemap.xml).
- `tools/sitelib.py`: page shell with a stage-grouped mobile menu, breadcrumbs, previous/next step links, an automatic "On this page" list (3 or more h2s), the legal notice banner and footer, the Vercel analytics script, and checks that reject em-dashes.
- Vercel: `vercel.json` serves `site/` with no build step.
- Rules: official sources only, a link beside every fact, "not stated by source" where a source is silent, conflicts shown, "Last checked" date on every page. Not legal advice.
- See `tools/backlog.md` for gaps.
