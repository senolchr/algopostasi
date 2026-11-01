#!/usr/bin/env python3
"""Algoritma Postası — statik site üretici.
data/posts.json -> index.html, arsiv/, posta/<slug>/, 404.html, sitemap.xml
Çalıştır: python3 tools/build.py
"""
import json, os, html, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'data', 'posts.json'), encoding='utf-8'))
SITE, POSTS, WEEKS = D['site'], {p['slug']: p for p in D['posts']}, D['weeks']
e = lambda s: html.escape(s, quote=True)

AYLAR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
GUNLER = ['Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi','Pazar']
def dt(p): return datetime.datetime.fromisoformat(p['publish'])
def tarih(p):
    d = dt(p); return f"{d.day} {AYLAR[d.month-1]} {d.year}"
def tarih_uzun(p):
    d = dt(p); return f"{GUNLER[d.weekday()]} {d.day} {AYLAR[d.month-1]}, {d.strftime('%H:%M')}"

def week_of(slug):
    for w in WEEKS:
        if slug in w['posts']: return w
    return None

def page(title, desc, body, depth, og_img=None, path=''):
    up = '../' * depth
    canon = f"https://{SITE['domain']}/{path}" if SITE['domain'] else ''
    og = f'<meta property="og:image" content="{canon.split("/" + path)[0] if canon else ""}/{og_img}">' if og_img and canon else ''
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
{f'<link rel="canonical" href="{canon}">' if canon else ''}
{og}
<link rel="icon" href="{up}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<div class="stripe" aria-hidden="true"></div>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{up or './'}"><img src="{up}assets/logo.png" alt="" width="40" height="40"><span>Algoritma <b>Postası</b></span></a>
    <nav aria-label="Ana menü">
      <a href="{up or './'}#postalar">Postalar</a>
      <a href="{up}arsiv/">Arşiv</a>
      <a href="{up or './'}#bulten">Bülten</a>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap foot-in">
    <div>
      <div class="brand small"><img src="{up}assets/logo.png" alt="" width="28" height="28"><span>Algoritma <b>Postası</b></span></div>
      <p>{e(SITE['tagline'])}</p>
    </div>
    <ul class="social">
      <li><a href="{SITE['social']['youtube']}" rel="noopener">YouTube</a></li>
      <li><a href="{SITE['social']['tiktok']}" rel="noopener">TikTok</a></li>
      <li><a href="{SITE['social']['instagram']}" rel="noopener">Instagram</a></li>
      <li><a href="{SITE['social']['x']}" rel="noopener">X</a></li>
    </ul>
    <p class="fine">© {datetime.date.today().year} Algoritma Postası · İçerikler yatırım tavsiyesi değildir.</p>
  </div>
</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
'''

def stamp_svg(cls='env'):
    return f'''<svg class="{cls}" viewBox="0 0 200 140" aria-hidden="true"><rect x="12" y="12" width="176" height="116" rx="14"/><polyline points="12,26 100,88 188,26"/><circle cx="56" cy="57" r="8" class="o"/><circle cx="144" cy="57" r="8" class="o"/><circle cx="100" cy="88" r="13" class="f"/></svg>'''

def card(p, up):
    url = f"{up}posta/{p['slug']}/"
    return f'''<li class="card gated" data-publish="{p['publish']}">
  <a class="card-open" href="{url}">
    <img src="{up}assets/kapak/{p['asset']}.jpg" alt="" loading="lazy" width="270" height="480">
    <div class="card-tx">
      <div class="meta"><span class="tag">{e(p['tag'])}</span><time datetime="{p['publish']}">{tarih(p)}</time></div>
      <h3>{e(p['title'])}</h3>
      <p>{e(p['summary'])}</p>
    </div>
  </a>
  <div class="card-sealed">
    {stamp_svg()}
    <div class="sealed-tx"><span class="tag">Kapalı zarf</span><span>Açılış</span><b>{tarih_uzun(p)}</b></div>
  </div>
</li>'''

def newsletter(up):
    act = SITE.get('newsletter_action') or ''
    if act:
        form = f'''<form class="nl-form" action="{e(act)}" method="post" target="_blank">
      <label for="nl-mail" class="sr">E-posta adresin</label>
      <input id="nl-mail" type="email" name="email" placeholder="ornek@eposta.com" required>
      <button type="submit">Abone ol</button>
    </form>'''
    else:
        form = '''<div class="nl-form soon"><input type="email" placeholder="ornek@eposta.com" disabled aria-label="E-posta adresin"><button type="button" disabled>Çok yakında</button></div>'''
    return f'''<section id="bulten" class="nl">
  <div class="wrap nl-in">
    <div>
      <div class="eyebrow">Bülten</div>
      <h2>Haftanın postası, her pazar gelen kutunda.</h2>
      <p>Haftanın yapay zekâ gelişmeleri tek e-postada. Reklam yok, spam yok.</p>
    </div>
    {form}
  </div>
</section>'''

def build_index():
    w = WEEKS[-1]
    posts = [POSTS[s] for s in w['posts']]
    feat = ''.join(f'''<article class="feature gated" data-publish="{p['publish']}" data-order="{i}">
  <div class="feature-video">{yt(p, '')}</div>
  <div class="feature-tx">
    <div class="meta"><span class="tag">{e(p['tag'])}</span><time datetime="{p['publish']}">{tarih(p)}</time></div>
    <h2>{e(p['title'])}</h2>
    <p>{e(p['summary'])}</p>
    <a class="btn" href="posta/{p['slug']}/">Yazıyı oku</a>
  </div>
</article>''' for i, p in enumerate(posts))
    body = f'''<section class="hero">
  <div class="wrap">
    <div class="eyebrow">{e(w['title'])} · {e(w['range'])}</div>
    <h1>Yeni çıkan yapay zekâ araçları: <em>denendi, anlatıldı.</em></h1>
    <p class="lead">{e(w['intro'])}</p>
  </div>
</section>
<section class="today" aria-label="Son gönderi">
  <div class="wrap">
    <div class="today-label">Son gönderi</div>
    <div class="features" data-latest>{feat}
      <div class="empty-feature">{stamp_svg()}<p>İlk posta yolda. Açılış: <b>{tarih_uzun(posts[0])}</b></p></div>
    </div>
  </div>
</section>
<section id="postalar" class="week">
  <div class="wrap">
    <div class="sec-head"><h2>Bu haftanın postaları</h2><a href="arsiv/">Tüm arşiv</a></div>
    <ol class="cards">{''.join(card(p, '') for p in posts)}</ol>
  </div>
</section>
{newsletter('')}'''
    write('index.html', page(f"{SITE['name']} · Yapay zekâ gündemi, denendi ve anlatıldı", SITE['tagline'], body, 0, path=''))

def yt(p, up):
    return f'''<div class="yt" data-id="{p['youtube']}">
    <img src="{up}assets/kapak/{p['asset']}.jpg" alt="" loading="lazy" width="270" height="480">
    <button type="button" class="play" aria-label="Videoyu oynat: {e(p['title'])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></button>
  </div>'''

def build_posts():
    order = [s for w in WEEKS for s in w['posts']]
    for i, slug in enumerate(order):
        p = POSTS[slug]; w = week_of(slug); up = '../../'
        prev = POSTS[order[i-1]] if i > 0 else None
        nxt = POSTS[order[i+1]] if i < len(order)-1 else None
        paras = ''.join(f'<p>{e(t)}</p>' for t in p['body'])
        srcs = ''.join(f'<li><a href="{e(s["url"])}" rel="noopener">{e(s["title"])}</a></li>' for s in p['sources'])
        nav = ''
        if prev: nav += f'<a class="pn prev gated-link" data-publish="{prev["publish"]}" href="{up}posta/{prev["slug"]}/"><span>Önceki posta</span>{e(prev["title"])}</a>'
        if nxt: nav += f'<a class="pn next gated-link" data-publish="{nxt["publish"]}" href="{up}posta/{nxt["slug"]}/"><span>Sonraki posta</span>{e(nxt["title"])}</a>'
        body = f'''<article class="post gated" data-publish="{p['publish']}">
  <div class="wrap post-in">
    <div class="post-head">
      <a class="crumb" href="{up}arsiv/">{e(w['title'])}</a>
      <div class="meta"><span class="tag">{e(p['tag'])}</span><time datetime="{p['publish']}">{tarih(p)}</time></div>
      <h1>{e(p['title'])}</h1>
      <p class="lead">{e(p['summary'])}</p>
    </div>
    <div class="post-grid">
      <div class="post-video">
        <div class="open-only">{yt(p, up)}</div>
        <div class="sealed-only sealed-box">{stamp_svg()}<p>Bu zarf henüz kapalı.<br>Açılış: <b>{tarih_uzun(p)}</b></p></div>
        <div class="watch">
          <a href="https://www.youtube.com/shorts/{p['youtube']}" rel="noopener">YouTube'da izle</a>
          <a href="{SITE['social']['tiktok']}" rel="noopener">TikTok</a>
          <a href="{SITE['social']['instagram']}" rel="noopener">Instagram</a>
        </div>
      </div>
      <div class="post-body">
        <div class="open-only">{paras}
        <h2>Kaynaklar</h2><ul class="sources">{srcs}</ul></div>
        <p class="sealed-only">Yazı, video yayınlandığında burada olacak.</p>
      </div>
    </div>
    <nav class="pager" aria-label="Diğer postalar">{nav}</nav>
  </div>
</article>
{newsletter(up)}'''
        write(f'posta/{slug}/index.html', page(f"{p['title']} · {SITE['name']}", p['summary'], body, 2, og_img=f"assets/kapak/{p['asset']}.jpg", path=f'posta/{slug}/'))

def build_archive():
    blocks = ''
    for w in reversed(WEEKS):
        items = ''.join(f'''<li class="gated" data-publish="{POSTS[s]['publish']}"><a href="../posta/{s}/"><time datetime="{POSTS[s]['publish']}">{tarih(POSTS[s])}</time><span class="tag">{e(POSTS[s]['tag'])}</span><b>{e(POSTS[s]['title'])}</b></a><span class="sealed-row">Kapalı zarf · {tarih_uzun(POSTS[s])}</span></li>''' for s in w['posts'])
        blocks += f'''<section class="arch-week"><h2>{e(w['title'])}</h2><div class="range">{e(w['range'])}</div><p>{e(w['intro'])}</p><ol class="arch-list">{items}</ol></section>'''
    body = f'''<section class="hero small"><div class="wrap"><div class="eyebrow">Arşiv</div><h1>Tüm postalar</h1><p class="lead">Her hafta yapay zekâ dünyasından yedi gönderi. Geçmiş sayılara buradan göz atabilirsin.</p></div></section>
<section class="arch"><div class="wrap">{blocks}</div></section>
{newsletter('../')}'''
    write('arsiv/index.html', page(f"Arşiv · {SITE['name']}", 'Algoritma Postası sayılarının arşivi.', body, 1, path='arsiv/'))

def build_misc():
    body = f'''<section class="hero small"><div class="wrap"><div class="eyebrow">404</div><h1>Bu adreste posta yok.</h1><p class="lead">Zarf yanlış adrese gitmiş olabilir. <a href="/">Ana sayfaya dön</a>.</p></div></section>'''
    write('404.html', page(f"Bulunamadı · {SITE['name']}", 'Sayfa bulunamadı.', body, 0))
    dom = SITE.get('domain')
    if dom:
        write('CNAME', dom + '\n')
        urls = ['', 'arsiv/'] + [f'posta/{p["slug"]}/' for p in D['posts']]
        write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>https://{dom}/{u}</loc></url>' for u in urls) + '</urlset>\n')
        write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: https://{dom}/sitemap.xml\n')
    else:
        write('robots.txt', 'User-agent: *\nAllow: /\n')
    write('.nojekyll', '')

def write(rel, txt):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(txt)

if __name__ == '__main__':
    build_index(); build_posts(); build_archive(); build_misc(); print('ok')
