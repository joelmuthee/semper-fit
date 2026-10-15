"""Give every page the same navbar, mobile menu and footer.

The pages were hand-written with their own copies, and they had drifted: different
footer columns, a stale "Classes" label, gym hours on the padel page. Edit NAV and
FOOTER here, then run:  python tools/chrome.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "classes.html", "padel.html", "book-padel.html",
         "gallery.html", "about.html", "contact.html"]

LINKS = [("index.html", "Home"), ("classes.html", "Gym"), ("padel.html", "Padel"),
         ("gallery.html", "Gallery"), ("about.html", "About"), ("contact.html", "Contact")]

MOON = '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
SUN = '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'


def nav(page, navcls="navbar"):
    def a(href, label, cls=""):
        act = ' class="active"' if href == page else ""
        return f'<li><a href="{href}"{act}>{label}</a></li>'
    desk = "\n    ".join(a(h, l) for h, l in LINKS)
    mob = "\n    ".join(
        f'<a href="{h}" class="mn-item mn-d{i+1}{" active" if h == page else ""}">{l}</a>'
        for i, (h, l) in enumerate(LINKS))
    return f'''<nav class="{navcls}" id="navbar">
  <a href="index.html" class="nav-logo">
    <img src="images/logo.jpg" alt="Semper Fit Gymnasium logo" width="90" height="90">
  </a>
  <ul class="nav-links">
    {desk}
  </ul>
  <a href="book-padel.html" class="nav-cta">Book a Court</a>
  <button class="theme-toggle" id="themeToggle" aria-label="Switch light or dark mode">
    {MOON}
    {SUN}
  </button>
  <button class="mobile-toggle" id="mobileToggle" aria-label="Open menu"><span></span><span></span><span></span></button>
</nav>
<div class="mobile-nav" id="mobileNav">
  <div class="mobile-nav-header">
    <div class="mobile-nav-logo">
      <img src="images/logo.jpg" alt="Semper Fit" width="60" height="60">
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <button class="mobile-theme-toggle" id="mobileThemeToggle" aria-label="Switch light or dark mode">
        {MOON}
        {SUN}
      </button>
      <button class="mobile-nav-close" id="mobileClose" aria-label="Close menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
  </div>
  <nav class="mobile-nav-links">
    {mob}
  </nav>
  <div class="mobile-nav-footer">
    <a href="book-padel.html" class="mobile-nav-cta">Book a Court</a>
    <a href="https://www.instagram.com/semper_fit_gymnasium/" target="_blank" rel="noopener" class="mobile-nav-social" aria-label="Instagram">
      {IG}
    </a>
  </div>
</div>'''


FOOTER = '''<footer class="footer">
  <div class="footer-grid">
    <div class="footer-col footer-brand">
      <div class="footer-logo">
        <img src="images/logo.jpg" alt="Semper Fit" width="120" height="120" loading="lazy">
      </div>
      <p class="footer-desc">The gym and the three covered padel courts at St. Christopher's International School, Karen, Nairobi.</p>
      <div class="footer-social">
        <a href="https://www.instagram.com/semper_fit_gymnasium/" target="_blank" rel="noopener" aria-label="Instagram">
          <svg viewBox="0 0 24 24"><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M17.5 6.5h.01"/></svg>
        </a>
      </div>
    </div>
    <div class="footer-col">
      <h4>The Gym</h4>
      <ul>
        <li><a href="classes.html#classes">Classes</a></li>
        <li><a href="classes.html#personal-training">Personal training</a></li>
        <li><a href="classes.html#membership">Membership</a></li>
        <li><a href="classes.html#hours">Opening hours</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Padel</h4>
      <ul>
        <li><a href="book-padel.html">Book a court</a></li>
        <li><a href="padel.html#coaching">Coaching</a></li>
        <li><a href="padel.html#leagues">Leagues and events</a></li>
        <li><a href="padel.html#faq">Padel questions</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Visit Us</h4>
      <ul class="footer-contact">
        <li>St. Christopher's International School, Karen, Nairobi</li>
        <li><a href="tel:+254720720444">0720 720 444</a></li>
        <li><a href="tel:+254742822357">0742 822 357</a></li>
        <li><a href="mailto:semperfitgymnasium@scsinternational.sc.ke">semperfitgymnasium@scsinternational.sc.ke</a></li>
        <li>Gym: Mon-Fri 5-8am and 4-8pm, Sat 6am-6pm, Sun 10am-2pm</li>
        <li>Padel courts: daily 6am-9pm</li>
      </ul>
    </div>
  </div>
  <p class="footer-draft">Draft site for review. Opening hours, prices and the class timetable are still to be confirmed.</p>
  <div class="footer-bottom">
    <span>&copy; 2026 Semper Fit Gymnasium, St. Christopher's International School.</span>
    <span>Powered by <a href="https://essenceautomations.com/websites" target="_blank" rel="noopener">Essence Automations</a></span>
  </div>
</footer>'''


def swap(src, page):
    # navbar through the end of the mobile menu
    m = re.search(r'<nav class="(navbar[^"]*)"', src)
    assert len(re.findall(r'<nav class="navbar', src)) == 1, page
    a = m.start()
    f = src.index('class="mobile-nav-footer"', a)
    b = src.index("\n  </div>\n</div>", f) + len("\n  </div>\n</div>")
    src = src[:a] + nav(page, m.group(1)) + src[b:]
    c = src.index("<footer")
    d = src.index("</footer>", c) + len("</footer>")
    assert src.count("<footer") == 1, page
    return src[:c] + FOOTER + src[d:]


if __name__ == "__main__":
    for p in sys.argv[1:] or PAGES:
        path = ROOT / p
        s = path.read_text(encoding="utf-8")
        out = swap(s, p)
        assert out.count('id="mobileNav"') == 1 and out.count("</footer>") == 1, p
        path.write_text(out, encoding="utf-8", newline="")
        print("ok", p)
