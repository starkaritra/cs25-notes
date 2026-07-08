import re, glob, os

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&'
 'family=Caveat:wght@500;700&display=swap" rel="stylesheet">')

NOTE_STYLE = r"""<style>
  :root{
    --ink:#e9e6dc; --muted:#9aa6b8; --line:#333a46; --bg:#14161b; --soft:#1f232d;
    --accent:#6ea8fe; --accent2:#c8a2ff;
    --ok:#5fd48a; --warn:#f2b45c; --danger:#f5837f; --info:#6ea8fe; --think:#c8a2ff;
    --paper:#f7f2e6; --paperink:#2b2721; --paperline:#dccfb4;
    --hand:'Atkinson Hyperlegible', system-ui, -apple-system, sans-serif; --head:'Caveat', cursive;
    --maxw:860px;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;color:var(--ink);background:var(--bg);
    background-image:linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px);
    background-size:100% 32px;
    font-family:var(--hand);line-height:1.7;font-size:18px;-webkit-font-smoothing:antialiased}
  .wrap{display:grid;grid-template-columns:262px minmax(0,var(--maxw));gap:48px;
    max-width:1200px;margin:0 auto;padding:32px 28px 120px}
  /* ---- sidebar TOC ---- */
  nav.toc{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);
    overflow:auto;font-size:15px;border-right:1px solid var(--line);padding-right:16px}
  nav.toc .kicker{font-family:var(--head);font-size:19px;letter-spacing:.02em;color:var(--accent2);
    font-weight:700;margin:0 0 8px;text-transform:none}
  nav.toc a{display:block;color:var(--muted);text-decoration:none;padding:3px 0;border-radius:6px}
  nav.toc a:hover{color:var(--accent)}
  nav.toc a.sub{padding-left:14px;font-size:14px}
  nav.toc .prog{margin-top:18px;font-size:13.5px;color:var(--muted)}
  /* ---- article ---- */
  article{min-width:0}
  .hero{border:1px solid var(--line);border-radius:16px;padding:26px 30px;
    background:linear-gradient(135deg,#242b40,#2e2442);margin-bottom:8px;
    box-shadow:0 10px 30px rgba(0,0,0,.35)}
  .series{font-family:var(--hand);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);font-weight:700}
  h1{font-family:var(--head);font-size:47px;line-height:1.03;margin:8px 0 6px;font-weight:700}
  .meta{color:var(--muted);font-size:15px;margin-top:12px;display:flex;flex-wrap:wrap;gap:8px 14px}
  .meta a{color:var(--accent);text-decoration:none}
  .meta .pill{background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:999px;padding:3px 12px}
  h2{font-family:var(--head);font-size:36px;margin:46px 0 4px;padding-top:14px;font-weight:700;border-top:1px solid var(--line)}
  h2 .num{color:var(--accent);margin-right:8px}
  h3{font-family:var(--head);font-size:28px;margin:26px 0 4px;color:#e7ebf3;font-weight:700}
  h4{font-family:var(--hand);font-size:15px;margin:18px 0 4px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-weight:700}
  p{margin:11px 0}
  ul,ol{margin:11px 0;padding-left:24px} li{margin:6px 0}
  code{background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:5px;padding:1px 6px;
    font-family:"SF Mono",Consolas,Menlo,monospace;font-size:15px;color:#e7d8b8}
  pre{background:#0c0f16;color:#e6edf7;border:1px solid var(--line);border-radius:12px;padding:16px 18px;overflow:auto;
    font-family:"SF Mono",Consolas,Menlo,monospace;font-size:14px;line-height:1.55}
  pre code{background:none;border:none;color:inherit;padding:0}
  .lead{font-size:22px;color:#d7d3c8}
  strong{color:#fff;font-weight:700}
  a.ref{color:var(--accent);text-decoration:none;font-weight:700}
  a.ref:hover{text-decoration:underline}
  /* ---- callouts ---- */
  .box{border-left:4px solid var(--info);background:var(--soft);border-radius:0 12px 12px 0;
    padding:15px 20px;margin:20px 0}
  .box .lbl{font-family:var(--head);font-size:17px;letter-spacing:.02em;font-weight:700;margin-bottom:2px;display:block;text-transform:none}
  .box p:first-of-type{margin-top:2px} .box p:last-child{margin-bottom:0}
  .box.why{border-color:var(--accent);background:#182338}       .box.why .lbl{color:#8fc0ff}
  .box.intuition{border-color:var(--think);background:#241a36}  .box.intuition .lbl{color:#d3b3ff}
  .box.analogy{border-color:#43cdd4;background:#122e31}         .box.analogy .lbl{color:#6fe0e6}
  .box.check{border-color:var(--ok);background:#132c1e}         .box.check .lbl{color:#7fe6a4}
  .box.pitfall{border-color:var(--danger);background:#331b1b}   .box.pitfall .lbl{color:#ff9b97}
  .box.eqn{border-color:var(--warn);background:#302616}         .box.eqn .lbl{color:#ffc978}
  details.check{margin-top:8px} details.check summary{cursor:pointer;color:#7fe6a4;font-weight:700;font-size:16px}
  details.check[open] summary{margin-bottom:6px}
  /* ---- figures = light "paper" sketch cards on the dark page ---- */
  figure{margin:24px 0;text-align:center;background:var(--paper);color:var(--paperink);
    border:1px solid var(--paperline);border-radius:14px;padding:18px 18px 14px;
    box-shadow:0 2px 0 rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.4)}
  figure .mermaid{display:flex;justify-content:center;background:transparent}
  figcaption{font-family:var(--hand);font-size:15px;color:#6d6555;margin-top:10px;font-style:italic}
  .svgcard{background:var(--paper);color:var(--paperink);border:1px solid var(--paperline);border-radius:14px;padding:18px}
  figure .svgcard{background:transparent;border:none;padding:0;box-shadow:none}
  table{border-collapse:collapse;width:100%;margin:20px 0;font-size:16px}
  th,td{border:1px solid var(--line);padding:10px 13px;text-align:left;vertical-align:top}
  th{background:var(--soft);font-weight:700;color:#fff}
  .tt{color:var(--accent);font-weight:700;white-space:nowrap}
  /* ---- refs / footer / nav ---- */
  ol.refs{font-size:16px} ol.refs li{margin:10px 0}
  .foot{margin-top:60px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);font-size:14px}
  .navbtns{display:flex;justify-content:space-between;margin-top:32px;gap:12px}
  .navbtns a{flex:1;border:1px solid var(--line);border-radius:12px;padding:13px 16px;text-decoration:none;color:var(--ink);background:var(--soft)}
  .navbtns a:hover{border-color:var(--accent);color:var(--accent)}
  .navbtns .r{text-align:right}
  /* ---- print / PDF: force a clean light layout so ink + math stay readable ---- */
  @media print{
    nav.toc,.navbtns{display:none}
    .wrap{display:block;max-width:none;padding:0}
    body{background:#fff;color:#141414;font-size:12pt;line-height:1.5;background-image:none;
      font-family:'Atkinson Hyperlegible', system-ui, sans-serif}
    h1,h2,h3{color:#111} h2{border-top:1px solid #ccc}
    .hero{background:none;border:none;box-shadow:none;padding:0}
    .lead{color:#333} strong{color:#000}
    .box{background:#f3f3f3 !important;color:#141414;break-inside:avoid}
    .box .lbl{color:#333 !important}
    figure{box-shadow:none;break-inside:avoid;border-color:#ccc}
    th{color:#000} td,th{border-color:#bbb}
    pre{white-space:pre-wrap;background:#f0f0f0;color:#111;border-color:#ccc}
    code{color:#333}
    a,a.ref{color:#000;text-decoration:underline}
  }
  @media (max-width:880px){
    .wrap{grid-template-columns:1fr;gap:0} nav.toc{position:static;border-right:none;max-height:none;margin-bottom:24px}
  }
</style>"""

INDEX_STYLE = r"""<style>
  :root{--ink:#e9e6dc;--muted:#9aa6b8;--line:#333a46;--soft:#1f232d;--bg:#14161b;--accent:#6ea8fe;--accent2:#c8a2ff;
    --hand:'Atkinson Hyperlegible',system-ui,-apple-system,sans-serif;--head:'Caveat','Atkinson Hyperlegible',cursive}
  *{box-sizing:border-box}
  body{margin:0;color:var(--ink);background:var(--bg);
    background-image:linear-gradient(rgba(255,255,255,.028) 1px,transparent 1px);background-size:100% 32px;
    line-height:1.65;font-size:18px;font-family:var(--hand)}
  .wrap{max-width:920px;margin:0 auto;padding:44px 24px 100px}
  .hero{border:1px solid var(--line);border-radius:18px;padding:34px 34px;
    background:linear-gradient(135deg,#242b40,#2e2442);margin-bottom:28px;box-shadow:0 12px 34px rgba(0,0,0,.4)}
  .series{font-family:var(--hand);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);font-weight:700}
  h1{font-family:var(--head);font-size:52px;line-height:1;margin:8px 0 10px;font-weight:700}
  .sub{color:#cfcabf;font-size:21px;margin:0}
  h2{font-family:var(--head);font-size:34px;margin:38px 0 10px;font-weight:700}
  p{margin:10px 0}
  .path{display:grid;gap:14px;margin-top:8px}
  a.card{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:14px;
    padding:18px 22px;background:var(--soft);transition:.15s}
  a.card:hover{border-color:var(--accent);box-shadow:0 8px 26px rgba(0,0,0,.4);transform:translateY(-1px)}
  .card .n{display:inline-block;min-width:34px;height:34px;line-height:34px;text-align:center;border-radius:9px;
    background:var(--accent);color:#0c0f16;font-family:var(--head);font-weight:700;font-size:20px;margin-right:12px}
  .card h3{display:inline;font-family:var(--head);font-size:25px;font-weight:700}
  .card .tag{float:right;color:var(--muted);font-size:14px;margin-top:6px}
  .card p{color:var(--muted);font-size:16px;margin:10px 0 0}
  .note{background:var(--soft);border-left:4px solid var(--accent);border-radius:0 12px 12px 0;padding:15px 20px;font-size:16.5px}
  .foot{margin-top:50px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);font-size:14px}
  code{background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:5px;padding:1px 6px;font-size:15px;color:#e7d8b8}
  ul{padding-left:22px} li{margin:6px 0} strong{color:#fff}
  @media print{body{background:#fff;color:#111;background-image:none} .hero{background:none;box-shadow:none} a.card{background:#f5f5f5}}
</style>"""

def add_fonts(html):
    # strip any existing Google Fonts <link> tags, then insert the current FONTS
    html = re.sub(r'\s*<link[^>]*fonts\.(?:googleapis|gstatic)[^>]*>', '', html)
    return re.sub(r'(<meta name="viewport"[^>]*>)', r'\1\n' + FONTS, html, count=1)

notes = [f for f in glob.glob('notes/*.html') if os.path.basename(f) != 'index.html']
for f in notes:
    h = open(f, encoding='utf-8').read()
    h = add_fonts(h)
    h = re.sub(r'<style>.*?</style>', lambda m: NOTE_STYLE, h, count=1, flags=re.S)
    h = re.sub(r"fontFamily: '[^']*'", "fontFamily: 'Atkinson Hyperlegible, sans-serif'", h)
    open(f, 'w', encoding='utf-8').write(h)
    print('themed', os.path.basename(f))

# index.html
idx = 'notes/index.html'
h = open(idx, encoding='utf-8').read()
h = add_fonts(h)
h = re.sub(r'<style>.*?</style>', lambda m: INDEX_STYLE, h, count=1, flags=re.S)
h = h.replace('href="notes/', 'href="')   # fix broken links (index is already inside notes/)
open(idx, 'w', encoding='utf-8').write(h)
print('themed + fixed links: index.html')
