# Semper Fit website: build notes

Static site on **Cloudflare Pages**, project `semper-fit` (Stawisystems account
`58685495706b973821d77208248c66fc`), custom domain `semperfit.essenceautomations.com`.
**Not GitHub Pages, and pushing does NOT deploy:** the project says it is Git-connected but the
link has been dead since about May 2026 (no build since 71179d4). Deploy by hand from the
committed files, leaving out tools/, NOTES.md and booking-app/:
`git archive HEAD | tar -x -C <dir>`, remove those, then
`CLOUDFLARE_ACCOUNT_ID=58685495706b973821d77208248c66fc npx --yes wrangler@4.42.0 pages deploy <dir> --project-name semper-fit --branch main`.
Found and done 2026-10-16 (deployment 0ce2c2f4). Light theme by default,
with a dark toggle. The padel booking app lives in `booking-app/` (its own `NOTES.md`).

## How the pages are kept in step

- `python tools/chrome.py` writes the same navbar, mobile menu and footer into every page.
  Edit the nav or footer there, never in a page.
- `python tools/seo.py` writes each page's title, description, share tags and JSON-LD, and
  `sitemap.xml`. The FAQPage schema is read from the page's own `.sf-faq-item` blocks, so it
  can never say something the visible page does not. Re-run it after editing any question.
- `tools/audit.py` (Playwright, Python 3.12) loads all 7 pages at 320, 375 and 1280 and fails
  on sideways scroll, anything past the right edge, inputs under 90px, broken images and
  console errors. Screenshots land in `.tmp/shots/`. Serve the folder on port 3456 first:
  `python -m http.server 3456 --bind 127.0.0.1`.

## Rules for this site

- Only claims the club can show: no "premier", "best", "certified", "floodlit",
  "international standard", member counts or world padel statistics. The photos do show
  glass walls and a roof, so "covered, glass-walled" is fine.
- Questions are always open (`.sf-faq`), never behind a tap.
- The footer carries a draft notice until the real hours, prices and timetable are confirmed.
- `img { width:auto; height:auto }` is in `styles.css`; keep it, because images carry
  width/height attributes.
- The `.reveal` hidden state only applies once the head script adds `.js` to `<html>`, so
  with no JS every section still shows.
- The homepage booking illustration (`#sfPhone`, `site.js`) rests on its last frame, pauses
  off screen, on hover and in a hidden tab, and does not run under reduced motion.

## Found in the October 2026 review

- Two hero images (`gym_10.webp`, `gym_8.webp`) pointed at files that never existed.
- The padel intro paragraph was white on white in the light theme, and the footer's grey
  text sat at low contrast on the black footer.
- `book-padel.html` used CSS variables that do not exist (`--bg`, `--text-muted`) and
  emoji as icons.

## October 2026 redesign (padel, home, gym live; gallery, about, contact to go)

- **Display system `pd-*`** in `styles.css` is shared by every redesigned page despite the
  name: Anton for big lines (`pd-display`, `pd-h2`, every `.section-title`), kicker, facts
  line, framed hero photo with chip, court-drawn price tiles (`pd-tile`), closing band
  (`pd-cta`). Home adds `hm-*`, gym adds `gy-*`.
- **Heroes start below the menu bar**: it is ~160px tall on desktop, so `.pd-hero` has 186px
  top padding there. Buttons measured above the fold at 1440x900, 1366x768, 375x740, 360x640.
- **Reveals are bidirectional** (`.sf-rv` in `site.js`): in from below on the way down,
  from above on the way up, reset when fully off screen, with a 3s settle timer. Because of
  that, full-page screenshots show blank sections; review screen by screen instead.
- **Signature motion per page**: home = booking illustration; padel = top-down rally
  (SVG animateMotion; a resting ball and a moving ball, because animateMotion ADDS to cx/cy);
  gym = the week's hours chart with a live "now" line and an open/closed chip.
- `/admin` on the site 302s to the booking system's admin (`_redirects`).
- The school address semperfit.scsinternational.sc.ke needs one CNAME to
  `semper-fit.pages.dev` added by whoever holds the school's Cloudflare (not our account).
