#!/usr/bin/env python3
"""ONSPORTS.UZ: qidiruv tizimlari uchun statik sahifalar yaratadi.

Ishga tushirish:   python generate_seo.py            (natija: ./seo-out papkasida)
Natijani saytning ildiziga (index.html yonidagi papkaga) yuklang:
  seo-out/robots.txt, seo-out/sitemap.xml, seo-out/kanal/<kanal>/index.html

Kanal qo'shish yoki olib tashlash uchun pastdagi CHANNELS ro'yxatini tahrirlang.
Har bir qator: (saytda ko'rinadigan nom, havola uchun nom, ruscha nom yoki None)
"""
import json, os, sys, datetime
from html import escape

SITE = "https://onsports.uz"          # domen boshqacha bo'lsa shu yerni o'zgartiring
BRAND = "ONSPORTS.UZ"

CHANNELS = [
    ("Match TV", "match-tv", "Матч ТВ"),
    ("Match Futbol 1", "match-futbol-1", "Матч! Футбол 1"),
    ("Match Futbol 2", "match-futbol-2", "Матч! Футбол 2"),
    ("Match Futbol 3", "match-futbol-3", "Матч! Футбол 3"),
    ("Setanta Sports 1", "setanta-sports-1", None),
    ("Setanta Sports 2", "setanta-sports-2", None),
    ("Nova Sport 1", "nova-sport-1", None),
    ("Nova Sport 2", "nova-sport-2", None),
    ("Nova Sport 3", "nova-sport-3", None),
    ("Nova Sport 4", "nova-sport-4", None),
    ("TNT Sports 1", "tnt-sports-1", None),
    ("TNT Sports 2", "tnt-sports-2", None),
    ("Okko Sport", "okko-sport", "Окко Футбол"),
    ("DAZN 1", "dazn-1", None),
    ("DAZN 2", "dazn-2", None),
    ("Sport TV 1", "sport-tv-1", None),
    ("Sport TV 2", "sport-tv-2", None),
    ("Sport TV 3", "sport-tv-3", None),
]

CSS = ("*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#eef2fa;font:16px/1.6 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}"
       "a{color:#c6ff3d}header{padding:14px 18px;border-bottom:1px solid #22304d}"
       ".lg{font-weight:800;letter-spacing:1px;text-decoration:none;color:#fff}.lg span{color:#c6ff3d}"
       "main{max-width:760px;margin:0 auto;padding:18px}.bc{font-size:13px;color:#8a98b5}.bc a{color:#8a98b5}"
       "h1{font-size:28px;line-height:1.2;margin:14px 0 10px}h2{font-size:18px;margin:26px 0 8px}"
       ".btn{display:inline-block;margin:10px 0 4px;padding:13px 26px;border-radius:99px;background:#c6ff3d;color:#0a0a0a;font-weight:800;text-decoration:none}"
       "ul{display:flex;flex-wrap:wrap;gap:8px 14px;padding:0;list-style:none}li a{color:#eef2fa;text-decoration:none;border-bottom:1px solid #22304d}"
       ".n{font-size:12px;color:#8a98b5;margin-top:30px}")

def page(ch):
    name, slug, ru = ch
    url = f"{SITE}/kanal/{slug}/"
    ru_alt = f" ({ru})" if ru else ""
    title = f"{name} jonli efir — onlayn ko'rish | {BRAND}"
    desc = f"{name}{ru_alt} jonli efir — {BRAND} da onlayn ko'ring: futbol o'yinlari, sport TV, natijalar va o'yinlar jadvali."
    p_uz = (f"{name} kanalini {BRAND} saytida onlayn ko'rishingiz mumkin. Saytda jonli futbol o'yinlari, o'yinlar jadvali, "
            f"natijalar va sport yangiliklari o'zbek tilida jamlangan. Efirni ko'rish uchun «TV» bo'limiga o'ting va "
            f"ro'yxatdan {name} kanalini tanlang.")
    p_ru = (f"Смотрите {ru or name} онлайн на {BRAND}: прямые трансляции футбола, расписание матчей, результаты и новости спорта. "
            f"Откройте раздел «TV» и выберите канал {name}.")
    others = "".join(f'<li><a href="/kanal/{s}/">{escape(n)}</a></li>' for n, s, _ in CHANNELS if s != slug)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": ["uz", "ru"],
         "isPartOf": {"@type": "WebSite", "name": BRAND, "url": SITE + "/"},
         "about": {"@type": "TelevisionChannel", "name": name}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bosh sahifa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]}]}
    return f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title, quote=False)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="icon" type="image/png" href="/favicon.png">
<meta name="theme-color" content="#0b1220">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/favicon.png">
<meta property="og:locale" content="uz_UZ">
<meta property="og:locale:alternate" content="ru_RU">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header><a class="lg" href="/">ONSPORTS<span>.UZ</span></a></header>
<main>
<nav class="bc" aria-label="Yo'l"><a href="/">Bosh sahifa</a> › <a href="/#tv">TV</a> › {escape(name)}</nav>
<h1>{escape(name)} — jonli efir</h1>
<p>{escape(p_uz)}</p>
<p lang="ru">{escape(p_ru)}</p>
<a class="btn" href="/#tv">Efirni ko'rish</a>
<h2>Boshqa sport kanallar</h2>
<ul>{others}</ul>
<p class="n">Kanal nomi va belgilari tegishli egalarining mulki.</p>
</main>
</body>
</html>
"""

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "seo-out"
    today = datetime.date.today().isoformat()
    urls = [f"{SITE}/"]
    for ch in CHANNELS:
        d = os.path.join(out, "kanal", ch[1]); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f: f.write(page(ch))
        urls.append(f"{SITE}/kanal/{ch[1]}/")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls] + ["</urlset>", ""]
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f: f.write("\n".join(sm))
    with open(os.path.join(out, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Tayyor: {len(CHANNELS)} ta kanal sahifasi, sitemap.xml, robots.txt -> {out}/")

if __name__ == "__main__":
    main()
