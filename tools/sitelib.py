"""Shared helpers: page shell, nav, breadcrumbs, prev/next, jump list, robots.txt, sitemap.xml, checks."""
import os,html as H,shutil,re
D="24 October 2026"; ISO="2026-10-24"
NOTICE=('This is general information, not legal advice. Refugee status questions can affect your status: '
 'confirm with your resettlement agency, an accredited representative or an immigration attorney.')
def esc(s): return H.escape(s,quote=True)
def a(url,text='source'): return f'<a href="{esc(url)}" rel="noopener">{text}</a>'
def slug(t): return re.sub(r'[^a-z0-9]+','-',re.sub(r'<[^>]+>','',t).lower()).strip('-')
class Site:
    def __init__(s,root,base,brand,groups,order,footer,css):
        s.out=os.path.join(root,'site'); s.base=base.rstrip('/'); s.brand=brand; s.groups=groups; s.order=order
        s.footer=footer; s.css=css; s.pages=[]; s.titles={p:t for g,items in groups for p,t in items}; s.titles['index.html']='Home'
        if os.path.exists(s.out): shutil.rmtree(s.out)
        os.makedirs(s.out)
    def page(s,path,title,desc,body,stage=None):
        r='../'*path.count('/')
        nav=''.join(f'<div class="grp"><span class="glabel">{esc(g)}</span>'+''.join(f'<a href="{r}{p}">{esc(t)}</a>' for p,t in items)+'</div>' for g,items in s.groups)
        canon=s.base+'/'+path.replace('index.html','')
        # jump list from h2
        h2=re.findall(r'<h2>(.*?)</h2>',body)
        def addid(m): return f'<h2 id="{slug(m.group(1))}">{m.group(1)}</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',addid,body)
        toc=''
        if len(h2)>=3: toc='<nav class="toc" aria-label="On this page"><strong>On this page</strong><ul>'+''.join(f'<li><a href="#{slug(x)}">{re.sub("<[^>]+>","",x)}</a></li>' for x in h2)+'</ul></nav>'
        crumbs=f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{r}index.html">Home</a>'
        if stage: crumbs+=f' &rsaquo; <span>{esc(stage)}</span>'
        if path!='index.html': crumbs+=f' &rsaquo; <span>{esc(s.titles.get(path,title))}</span>'
        crumbs+='</nav>'
        pn=''
        if path in s.order:
            i=s.order.index(path); pv=s.order[i-1] if i>0 else None; nx=s.order[i+1] if i+1<len(s.order) else None
            pn='<nav class="pn" aria-label="Previous and next step">'+(f'<a class="prev" href="{r}{pv}">&larr; Previous step: {esc(s.titles[pv])}</a>' if pv else '<span></span>')+(f'<a class="next" href="{r}{nx}">Next step: {esc(s.titles[nx])} &rarr;</a>' if nx else '')+'</nav>'
        h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}"><style>{s.css}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<header><a class="brand" href="{r}index.html">{esc(s.brand)}</a><details class="menu"><summary>Menu: all steps</summary><nav class="top" aria-label="Main">{nav}</nav></details></header>
<div class="notice" role="note"><strong>Important:</strong> {NOTICE}</div>
<main>{crumbs}<p class="checked">Last checked: {D}</p>
{toc}{body}
{pn}</main><footer><p><strong>{NOTICE}</strong></p>{s.footer}<p>Last checked: {D}.</p></footer></body></html>'''
        for bad in ('\u2014','&mdash;'): assert bad not in h,(path,bad)
        assert 'myuscisgov.com' not in h
        p=os.path.join(s.out,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(h); s.pages.append(path)
    def finish(s):
        bots=['GPTBot','OAI-SearchBot','PerplexityBot','Bingbot','Googlebot','*']
        open(os.path.join(s.out,'robots.txt'),'w').write(''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {s.base}/sitemap.xml\n')
        open(os.path.join(s.out,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{s.base}/{p.replace("index.html","")}</loc><lastmod>{ISO}</lastmod></url>\n' for p in sorted(s.pages))+'</urlset>\n')
CSS='''body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a;line-height:1.65;background:#fafaf7;font-size:19px}header{background:#123b5c;color:#fff;padding:.7rem 1rem}header a{color:#fff;text-decoration:none}.brand{font-weight:700;font-size:1.15rem;display:block;margin-bottom:.3rem}.menu summary{cursor:pointer;font-weight:600;padding:.3rem 0}.menu[open] summary{margin-bottom:.4rem}nav.top{display:flex;flex-wrap:wrap;gap:.8rem 1.6rem}.grp{display:flex;flex-direction:column;min-width:11rem}.glabel{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#bcd3e6}.grp a{padding:.2rem 0}.grp a:hover{text-decoration:underline}@media(max-width:640px){nav.top{flex-direction:column}}.notice{background:#fff4d6;border-bottom:2px solid #e6cf8a;padding:.7rem 1rem;font-size:1rem}main{max-width:900px;margin:0 auto;padding:1rem}.crumbs{font-size:.95rem;margin:.3rem 0 .6rem}h1{font-size:2rem;line-height:1.25}h2{margin-top:2rem;font-size:1.45rem}.checked{display:inline-block;background:#e6f2ea;border:1px solid #a9d1b5;border-radius:4px;padding:.15rem .5rem;font-size:.95rem}.toc{background:#eef3f7;border-radius:6px;padding:.6rem 1rem;margin:1rem 0}.toc ul{margin:.3rem 0;padding-left:1.2rem}.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:.9rem 1.1rem;margin:.9rem 0}.warn{border-left:6px solid #c0392b;background:#fdeeee}.note{border-left:6px solid #d68910;background:#fff8ec}.conf{border-left:6px solid #8e44ad;background:#f6effa}.stage{border-left:6px solid #123b5c}.stage h2{margin-top:.2rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem}.cards a.card{display:block;text-decoration:none;color:#1a1a1a;margin:0}.cards a.card strong{color:#0b5394;font-size:1.1rem}.cards a.card:hover{border-color:#0b5394}.src{font-size:.88rem;color:#555}.pn{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.8rem;margin-top:2.5rem;border-top:1px solid #ddd;padding-top:1rem}.pn a{font-weight:600}footer{max-width:900px;margin:2rem auto;padding:1rem;font-size:.95rem;color:#444;border-top:1px solid #ddd}a{color:#0b5394}table{border-collapse:collapse;width:100%;background:#fff;font-size:.95rem}th,td{border:1px solid #ddd;padding:.45rem;text-align:left;vertical-align:top}th{background:#eef3f7}.wrap{overflow-x:auto}'''
