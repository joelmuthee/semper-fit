"""Write each page's <head> SEO block: title, description, canonical, share tags, JSON-LD.

The FAQ structured data is read from the page's own .sf-faq-item blocks, so it can never
say something the visible page does not. Also writes sitemap.xml.
Run:  python tools/seo.py
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://semperfit.essenceautomations.com"
OG = BASE + "/images/og-image.jpg"

ADDRESS = {"@type": "PostalAddress",
           "streetAddress": "St. Christopher's International School",
           "addressLocality": "Karen, Nairobi", "addressCountry": "KE"}
GYM = {
    "@context": "https://schema.org", "@type": "ExerciseGym", "@id": BASE + "/#gym",
    "name": "Semper Fit Gymnasium",
    "description": "Gym and padel courts at St. Christopher's International School, Karen, Nairobi.",
    "url": BASE + "/", "telephone": "+254720720444",
    "email": "semperfitgymnasium@scsinternational.sc.ke",
    "image": BASE + "/images/gym/gym_3.webp", "logo": BASE + "/images/logo.jpg",
    "address": ADDRESS, "priceRange": "KES 1,500 - 30,000",
    "sameAs": ["https://www.instagram.com/semper_fit_gymnasium/"],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "05:00", "closes": "08:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "16:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "06:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "14:00"},
    ],
}
PADEL = {
    "@context": "https://schema.org", "@type": "SportsActivityLocation", "@id": BASE + "/padel.html#courts",
    "name": "Semper Fit Padel Courts", "sport": "Padel",
    "description": "Three covered padel courts at St. Christopher's International School, Karen. 60 or 90 minute court hire, coaching and leagues.",
    "url": BASE + "/padel.html", "telephone": "+254720720444",
    "image": BASE + "/images/gym/sf-padel2.webp", "address": ADDRESS,
    "parentOrganization": {"@id": BASE + "/#gym"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "06:00", "closes": "21:00"}],
}

PAGES = {
    "index.html": ("Semper Fit · Gym and Padel Courts in Karen, Nairobi",
                   "Semper Fit is the gym and three covered padel courts at St. Christopher's International School, Karen. Classes, personal training, membership and padel court booking.",
                   "/", [GYM, PADEL]),
    "classes.html": ("Gym in Karen, Nairobi · Classes, Membership and Hours · Semper Fit",
                     "Gym classes, personal training and membership at Semper Fit, St. Christopher's International School, Karen. From Ksh 1,500 a day or Ksh 11,000 a term.",
                     "/classes.html", [GYM]),
    "padel.html": ("Padel Courts in Karen, Nairobi · Court Hire, Coaching, Leagues · Semper Fit",
                   "Three covered padel courts at St. Christopher's International School, Karen. Book 60 or 90 minutes from Ksh 3,000, open every day 6am to 9pm.",
                   "/padel.html", [PADEL]),
    "book-padel.html": ("Book a Padel Court in Karen, Nairobi · Semper Fit",
                        "Book a padel court at Semper Fit, St. Christopher's International School, Karen. 60 minutes Ksh 3,000 or 90 minutes Ksh 4,000, every day 6am to 9pm.",
                        "/book-padel.html", [PADEL]),
    "gallery.html": ("Photos of the Gym and Padel Courts · Semper Fit, Karen",
                     "Photos of the Semper Fit gym floor, classes and padel courts at St. Christopher's International School, Karen, Nairobi.",
                     "/gallery.html", []),
    "about.html": ("About Semper Fit · Gym and Padel at SCIS, Karen",
                   "Semper Fit is the gym and padel club at St. Christopher's International School in Karen, Nairobi. What we offer and how to find us.",
                   "/about.html", [GYM]),
    "contact.html": ("Contact Semper Fit · Gym and Padel, Karen, Nairobi",
                     "Call, WhatsApp or email Semper Fit at St. Christopher's International School, Karen. Join the gym, book a padel court or ask about coaching.",
                     "/contact.html", [GYM]),
}


def faq_schema(src):
    items = re.findall(r'<div class="sf-faq-item[^"]*">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', src, re.S)
    if not items:
        return None
    strip = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
        for q, a in items]}


def head(page, src):
    title, desc, path, schemas = PAGES[page]
    url = BASE + path
    esc = lambda x: html.escape(x, quote=False).replace('"', "&quot;")
    t, d = esc(title), esc(desc)
    blocks = list(schemas)
    f = faq_schema(src)
    if f:
        blocks.append(f)
    ld = "\n".join('<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=1) + "\n</script>" for b in blocks)
    return f'''<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Semper Fit">
<meta property="og:locale" content="en_KE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{OG}">
{ld}
'''


if __name__ == "__main__":
    for page in PAGES:
        p = ROOT / page
        s = p.read_text(encoding="utf-8")
        a = s.index("<title>")
        b = s.index('<link rel="preconnect" href="https://fonts.googleapis.com">')
        assert a < b, page
        s = s[:a] + head(page, s) + s[b:]
        p.write_text(s, encoding="utf-8", newline="")
        print("ok", page)
    urls = "\n".join(f"  <url><loc>{BASE}{v[2]}</loc></url>" for v in PAGES.values())
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    print("ok sitemap.xml")
