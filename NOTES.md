# Semper Fit website: build notes

Static site on GitHub Pages (`semperfit.essenceautomations.com`). Light theme by default,
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
