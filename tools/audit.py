"""Measured mobile audit: every page at 320 and 375 (and 1280).

Fails on: page scrolls sideways, an element past the right edge, an input under 90px,
a broken image, a console error. Saves full-page screenshots to .tmp/shots/.
Needs Playwright: C:/Users/Joel/AppData/Local/Programs/Python/Python312/python.exe tools/audit.py [base]
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3456/"
PAGES = ["index.html", "classes.html", "padel.html", "book-padel.html", "gallery.html", "about.html", "contact.html"]
WIDTHS = [320, 375, 1280]
OUT = pathlib.Path(__file__).resolve().parent.parent / ".tmp" / "shots"
OUT.mkdir(parents=True, exist_ok=True)

JS = r"""() => {
  const W = document.documentElement.clientWidth, out = {sideways: document.documentElement.scrollWidth > W, past: [], small: [], broken: []};
  const inScroller = el => { for (let p = el.parentElement; p; p = p.parentElement) {
      const cs = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(cs.overflowX) && p !== document.body && p !== document.documentElement) return true; } return false; };
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (el.closest('.mobile-nav, .sf-band, iframe')) continue;
    const r = el.getBoundingClientRect(); if (!r.width) continue;
    if (r.right > W + 1 && r.left < W && !inScroller(el)) out.past.push((el.className || el.tagName) + ' ' + Math.round(r.right));
    if ((el.tagName === 'INPUT' && el.type !== 'checkbox' && el.type !== 'radio' || el.tagName === 'SELECT') && r.width < 90 && !el.closest('.bmi-input-wrap')) out.small.push(el.id || el.name);
  }
  for (const im of document.images) if (im.getAttribute("src") && im.complete && im.naturalWidth === 0) out.broken.push(im.getAttribute('src'));
  out.past = out.past.slice(0, 8); return out;
}"""

fails = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WIDTHS:
        ctx = b.new_context(viewport={"width": w, "height": 812 if w < 800 else 900}, device_scale_factor=1)
        for page in PAGES:
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + page, wait_until="load", timeout=60000)
            # scroll through so lazy images load and reveals fire
            h = pg.evaluate("document.body.scrollHeight")
            for y in range(0, h, 600):
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
            pg.wait_for_timeout(900)
            r = pg.evaluate(JS)
            errs = [e for e in errs if "leadconnector" not in e and "msgsndr" not in e and "google" not in e]
            bad = r["sideways"] or r["past"] or r["small"] or r["broken"] or errs
            fails += bool(bad)
            print(f"{'FAIL' if bad else 'ok  '} {w:4} {page:16} sideways={r['sideways']} past={r['past']} small={r['small']} broken={r['broken']} errors={errs[:3]}")
            if w != 1280:
                pg.evaluate("window.scrollTo(0,0)")
                pg.screenshot(path=str(OUT / f"{page[:-5]}-{w}.png"), full_page=True)
            pg.close()
        ctx.close()
    b.close()
print("FAILS:", fails)
sys.exit(1 if fails else 0)
