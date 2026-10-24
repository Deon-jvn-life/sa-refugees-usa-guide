"""Shared helpers: page shell, nav, breadcrumbs, prev/next, jump list, robots.txt, sitemap.xml, checks."""
import os,html as H,shutil,re,json,math
D="24 October 2026"; ISO="2026-10-24"
NOTICE=('This is general information, not legal advice. Refugee status questions can affect your status: '
 'confirm with your resettlement agency, an accredited representative or an immigration attorney.')
def esc(s): return H.escape(s,quote=True)
def a(url,text='source'): return f'<a href="{esc(url)}" rel="noopener">{text}</a>'
INTAKE_FORM="https://us-dos.unqorkgov.state.gov/?#/display/68a77f413cdb0fe7ab8817a8"
def intake_button():
    return f'<a class="intake" href="{esc(INTAKE_FORM)}" target="_blank" rel="noopener">Start the official online intake questionnaire</a>'
def slug(t):
    t=H.unescape(re.sub(r'<[^>]+>','',t))
    return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
def href(path):
    """Root-relative clean URL with a trailing slash."""
    if path in ('index.html','/'): return '/'
    if path.endswith('/index.html'): return '/'+path[:-len('index.html')]
    return '/'+path
def canon_url(base, path):
    return base.rstrip('/')+href(path)
VOID={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
SKIP_LINK={'script','style','h2','h3','h4','textarea'}
def link_terms(html, terms, used):
    """Link the first plain-text use of each glossary term. Skips existing links and h2 to h4."""
    if not terms or not html: return html
    out=[]; i=0; n=len(html); stack=[]; section=None
    tag_re=re.compile(r'<(/?)([a-zA-Z0-9]+)?([^>]*)>')
    while i<n:
        if html[i]=='<':
            m=tag_re.match(html, i)
            if not m:
                out.append(html[i]); i+=1; continue
            raw=m.group(0); closing=m.group(1)=='/'; name=(m.group(2) or '').lower(); attrs=m.group(3) or ''
            if name=='h2' and not closing:
                idm=re.search(r'\bid="([^"]*)"', raw)
                if idm: section=idm.group(1)
            if closing:
                if name in stack:
                    while stack and stack[-1]!=name: stack.pop()
                    if stack: stack.pop()
            elif name and name not in VOID and not attrs.rstrip().endswith('/'):
                stack.append(name)
            out.append(raw); i=m.end()
        else:
            j=html.find('<', i)
            if j<0: j=n
            text=html[i:j]
            if text and not any(t in SKIP_LINK or t=='a' for t in stack):
                text=_link_text(text, terms, used, section)
            out.append(text); i=j
    return ''.join(out)
def _link_text(text, terms, used, section):
    pos=0; parts=[]
    while pos<len(text):
        best=None
        for anchor, regs in terms:
            if anchor in used or anchor==section: continue
            for cre in regs:
                m=cre.search(text, pos)
                if not m or m.end()==m.start(): continue
                key=(m.start(), -(m.end()-m.start()))
                if best is None or key<best[0]:
                    best=(key, anchor, m.end(), m.group(0))
        if not best:
            parts.append(text[pos:]); break
        start=best[0][0]
        parts.append(text[pos:start])
        parts.append(f'<a href="/glossary/#{best[1]}">{best[3]}</a>')
        used.add(best[1]); pos=best[2]
    return ''.join(parts)
def _star(cx,cy,r):
    pts=[]
    for i in range(10):
        ang=-math.pi/2+i*math.pi/5
        rad=r if i%2==0 else r*0.381966
        pts.append(f'{cx+rad*math.cos(ang):.2f},{cy+rad*math.sin(ang):.2f}')
    return ' '.join(pts)
def _us_flag_inner():
    stripes=[]
    sh=100/13
    for i in range(13):
        if i%2==0:
            stripes.append(f'<rect y="{i*sh:.3f}" width="190" height="{sh+0.15:.3f}" fill="#B22234"/>')
    ch=7*sh
    E=76/12
    F=ch/10
    stars=[]
    for row in range(9):
        y=F*(row+1)
        xs=[E*(1+2*k) for k in range(6)] if row%2==0 else [E*(2+2*k) for k in range(5)]
        for x in xs:
            stars.append(f'<polygon fill="#fff" points="{_star(x,y,E*0.42)}"/>')
    return ('<rect width="190" height="100" fill="#fff"/>'+''.join(stripes)+
            f'<rect width="76" height="{ch:.3f}" fill="#3C3B6E"/>'+''.join(stars))
def _us_flag_svg():
    return ('<svg class="flag" role="img" aria-label="United States flag" viewBox="0 0 190 100" xmlns="http://www.w3.org/2000/svg">'
            +_us_flag_inner()+'</svg>')
SA_FLAG='''<svg class="flag" role="img" aria-label="South African flag" viewBox="0 0 90 60" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="za-t"><path d="m0 0 45 30L0 60z"/></clipPath><clipPath id="za-f"><path d="m0 0h90v60H0z"/></clipPath></defs><path fill="#E03C31" d="m0 0h90v30H45z"/><path fill="#001489" d="m0 60h90V30H45z"/><g clip-path="url(#za-f)" fill="none"><path stroke="#FFF" stroke-width="20" d="m90 30H45L0 0v60l45-30"/><path fill="#000" stroke="#ffb81c" stroke-width="20" clip-path="url(#za-t)" d="m0 0 45 30L0 60"/><path stroke="#007749" stroke-width="12" d="m0 0 45 30h45M0 60l45-30"/></g></svg>'''
US_FLAG=_us_flag_svg()
FLAGS=f'<span class="flags">{SA_FLAG}{US_FLAG}</span>'
class Site:
    def __init__(s,root,base,brand,groups,order,footer,css,terms=None,gsc='',msvalidate='',related=None):
        s.out=os.path.join(root,'site'); s.base=base.rstrip('/'); s.brand=brand; s.groups=groups; s.order=order
        s.footer=footer; s.css=css; s.pages=[]; s.indexable=[]; s.seo=[]
        s.gsc=gsc or ''; s.msvalidate=msvalidate or ''; s.related=related or []
        s.titles={p:t for g,items in groups for p,t in items}; s.titles['index.html']='Home'
        s.terms=[(anchor,[re.compile(p,re.I) for p in pats]) for anchor,pats in (terms or [])]
        if os.path.exists(s.out): shutil.rmtree(s.out)
        os.makedirs(s.out)
    def page(s,path,title,desc,body,stage=None,kind='article',faqs=None):
        if faqs:
            body+='<h2>Questions and answers</h2>'+''.join(f'<details class="card"><summary>{q}</summary><div>{ahtml}</div></details>' for q,ahtml in faqs)
        nav=''.join('<div class="grp"><span class="glabel">'+esc(g)+'</span>'+''.join(f'<a href="{href(p)}">{esc(t)}</a>' for p,t in items)+'</div>' for g,items in s.groups)
        url=canon_url(s.base, path)
        h1m=re.search(r'<h1>(.*?)</h1>', body, re.S)
        headline=H.unescape(re.sub(r'<[^>]+>','', h1m.group(1))) if h1m else title
        h2=re.findall(r'<h2>(.*?)</h2>',body)
        def addid(m): return f'<h2 id="{slug(m.group(1))}">{m.group(1)}</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',addid,body)
        used=set()
        body=link_terms(body, s.terms, used)
        foot=link_terms(s.footer, s.terms, used)
        toc=''
        if len(h2)>=3: toc='<nav class="toc" aria-label="On this page"><strong>On this page</strong><ul>'+''.join(f'<li><a href="#{slug(x)}">{re.sub("<[^>]+>","",x)}</a></li>' for x in h2)+'</ul></nav>'
        crumbs=f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>'
        if stage: crumbs+=f' &rsaquo; <span>{esc(stage)}</span>'
        if path!='index.html': crumbs+=f' &rsaquo; <span>{esc(s.titles.get(path,title))}</span>'
        crumbs+='</nav>'
        pn=''
        if path in s.order:
            i=s.order.index(path); pv=s.order[i-1] if i>0 else None; nx=s.order[i+1] if i+1<len(s.order) else None
            pn='<nav class="pn" aria-label="Previous and next step">'+(f'<a class="prev" href="{href(pv)}">&larr; Previous step: {esc(s.titles[pv])}</a>' if pv else '<span></span>')+(f'<a class="next" href="{href(nx)}">Next step: {esc(s.titles[nx])} &rarr;</a>' if nx else '')+'</nav>'
        for label,text,lo,hi in (('title',title,50,60),('description',desc,120,160)):
            if not (lo<=len(text)<=hi):
                s.seo.append(f'WARNING: {path} {label} is {len(text)} characters (want {lo} to {hi}): {text}')
        crumbs_ld=[{"@type":"ListItem","position":1,"name":"Home","item":s.base+"/"}]
        if path!='index.html':
            item={"@type":"ListItem","position":2,"name":headline}
            if kind!='error': item["item"]=url
            crumbs_ld.append(item)
        graph=[{"@type":"BreadcrumbList","itemListElement":crumbs_ld}]
        if kind=='home':
            graph.insert(0,{"@type":"WebSite","name":s.brand,"url":s.base+"/","description":desc,"inLanguage":"en"})
            graph.insert(1,{"@type":"Organization","name":s.brand,"url":s.base+"/","description":"Independent unofficial guide. Not affiliated with any government or agency."})
        elif kind=='article':
            graph.insert(0,{"@type":"Article","headline":headline,"description":desc,"datePublished":ISO,"dateModified":ISO,
                            "inLanguage":"en","mainEntityOfPage":url,
                            "author":{"@type":"Organization","name":s.brand,"url":s.base+"/"},
                            "publisher":{"@type":"Organization","name":s.brand,"url":s.base+"/"}})
        if faqs:
            graph.append({"@type":"FAQPage","mainEntity":[
                {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":H.unescape(re.sub(r'<[^>]+>','',ahtml))}}
                for q,ahtml in faqs]})
        ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
        robots='<meta name="robots" content="noindex,follow">' if kind=='error' else ''
        canonical='' if kind=='error' else f'<link rel="canonical" href="{esc(url)}">'
        verify=''
        if s.gsc: verify+=f'<meta name="google-site-verification" content="{esc(s.gsc)}">'
        if s.msvalidate: verify+=f'<meta name="msvalidate.01" content="{esc(s.msvalidate)}">'
        og_url='' if kind=='error' else f'<meta property="og:url" content="{esc(url)}">'
        og_type='website' if kind!='article' else 'article'
        image=s.base+'/og.png'
        related=''
        if s.related:
            related='<p><strong>Related guides</strong></p><ul>'+''.join(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>' for u,t in s.related)+'</ul>'
        h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{canonical}{robots}{verify}<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(s.brand)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">{og_url}<meta property="og:image" content="{esc(image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(image)}">{ld}<style>{s.css}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<header><div class="bar"><a class="brand" href="/">{FLAGS}<span class="name">{esc(s.brand)}</span></a><a class="headlink" href="/glossary/">Glossary</a></div><div class="headcta">{intake_button()}</div><details class="menu"><summary>Menu: all steps</summary><nav class="top" aria-label="Main">{nav}</nav></details></header>
<div class="notice" role="note"><strong>Important:</strong> {NOTICE}</div>
<main>{crumbs}<p class="checked">Last checked: {D}</p>
{toc}{body}
{pn}</main><footer><p><a href="/glossary/">Glossary</a> | <a href="/disclaimer/">Disclaimer</a></p><p><strong>{NOTICE}</strong></p>{foot}{related}<p>Last checked: {D}.</p></footer></body></html>'''
        for bad in ('\u2014','\u2013','&mdash;','&ndash;'): assert bad not in h,(path,bad)
        assert 'myuscisgov.com' not in h
        p=os.path.join(s.out,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(h); s.pages.append(path)
        if kind!='error': s.indexable.append(path)
    def finish(s):
        if s.seo:
            raise SystemExit('SEO length check failed:\n'+'\n'.join(s.seo))
        _write_assets(s.out)
        bots=['GPTBot','OAI-SearchBot','PerplexityBot','Bingbot','Googlebot','*']
        open(os.path.join(s.out,'robots.txt'),'w').write(''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {s.base}/sitemap.xml\n')
        urls=''.join(f'<url><loc>{canon_url(s.base,p)}</loc><lastmod>{ISO}</lastmod></url>\n' for p in sorted(s.indexable))
        open(os.path.join(s.out,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
        missing=_check_links(s.out, s.pages)
        if missing: raise SystemExit('Broken internal links:\n'+'\n'.join(missing))
def _check_links(out, pages):
    missing=[]
    for path in pages:
        html=open(os.path.join(out, path), encoding='utf-8').read()
        ids=set(re.findall(r'\bid="([^"]*)"', html))
        for href_v in re.findall(r'\bhref="([^"]*)"', html):
            if href_v.startswith(('http://','https://','mailto:','tel:')): continue
            url, _, frag = href_v.partition('#')
            if url=='':
                if frag and frag not in ids: missing.append(f'{path} -> {href_v}')
                continue
            if url.startswith('/'):
                rel=url.lstrip('/')
                target='index.html' if rel=='' else (rel+'index.html' if rel.endswith('/') else rel)
            else:
                target=os.path.normpath(os.path.join(os.path.dirname(path), url)).replace('\\','/')
            dest=os.path.join(out, target)
            if not os.path.isfile(dest):
                missing.append(f'{path} -> {href_v} (missing {target})'); continue
            if frag:
                tids=set(re.findall(r'\bid="([^"]*)"', open(dest, encoding='utf-8').read()))
                if frag not in tids: missing.append(f'{path} -> {href_v} (missing #{frag})')
    return missing
def _write_assets(out):
    open(os.path.join(out,'favicon.svg'),'w').write(_favicon_svg())
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as e:
        raise SystemExit('Pillow is required to build og.png and the apple touch icon') from e
    bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    og=Image.new('RGB',(1200,630),'#123b5c')
    d=ImageDraw.Draw(og)
    d.rounded_rectangle((48,48,1152,582), radius=28, fill='#fafaf7')
    d.rectangle((48,48,1152,168), fill='#123b5c')
    sa=_raster_sa(280,187); us=_raster_us(320,168)
    og.paste(sa,(88,210)); og.paste(us,(400,220))
    fb=ImageFont.truetype(bold,54)
    fr=ImageFont.truetype(regular,30)
    d.text((80,78),'South African refugees in the USA', font=fb, fill='#ffffff')
    d.text((88,430),'A plain-language guide to the U.S. refugee programme.', font=fr, fill='#123b5c')
    d.text((88,490),'Independent. Not a government website.', font=fr, fill='#3d4c59')
    og.save(os.path.join(out,'og.png'),'PNG')
    icon=Image.new('RGB',(180,180),'#123b5c')
    icon.paste(_raster_sa(150,100).resize((78,52), Image.Resampling.LANCZOS),(12,64))
    icon.paste(_raster_us(160,84).resize((78,41), Image.Resampling.LANCZOS),(96,70))
    icon.save(os.path.join(out,'apple-touch-icon.png'),'PNG')
def _favicon_svg():
    sa='''<defs><clipPath id="fav-t"><path d="m0 0 45 30L0 60z"/></clipPath><clipPath id="fav-f"><path d="m0 0h90v60H0z"/></clipPath></defs><path fill="#E03C31" d="m0 0h90v30H45z"/><path fill="#001489" d="m0 60h90V30H45z"/><g clip-path="url(#fav-f)" fill="none"><path stroke="#FFF" stroke-width="20" d="m90 30H45L0 0v60l45-30"/><path fill="#000" stroke="#ffb81c" stroke-width="20" clip-path="url(#fav-t)" d="m0 0 45 30L0 60"/><path stroke="#007749" stroke-width="12" d="m0 0 45 30h45M0 60l45-30"/></g>'''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 112 32" role="img" aria-label="South African and United States flags">'
            f'<g transform="scale(0.533)">{sa}</g>'
            f'<g transform="translate(50 0) scale(0.32)">{_us_flag_inner()}</g></svg>')
def _raster_sa(w,h):
    from PIL import Image, ImageDraw
    W,H=900,600
    im=Image.new('RGB',(W,H),'#FFFFFF')
    d=ImageDraw.Draw(im)
    S=10
    sc=lambda pts: [(x*S,y*S) for x,y in pts]
    d.polygon(sc([(0,0),(90,0),(90,30),(45,30)]), fill='#E03C31')
    d.polygon(sc([(0,60),(90,60),(90,30),(45,30)]), fill='#001489')
    def thick(p1,p2,width,fill):
        d.line([(p1[0]*S,p1[1]*S),(p2[0]*S,p2[1]*S)], fill=fill, width=width*S)
    thick((90,30),(45,30),20,'#FFFFFF')
    thick((45,30),(0,0),20,'#FFFFFF')
    thick((0,60),(45,30),20,'#FFFFFF')
    d.polygon(sc([(0,0),(45,30),(0,60)]), fill='#ffb81c')
    hyp=math.hypot(45,30)
    svec=(-30/hyp*10, 45/hyp*10)
    bvec=(-30/hyp*10, -45/hyp*10)
    def intersect(p1,d1,p2,d2):
        det=d1[0]*d2[1]-d1[1]*d2[0]
        dx=p2[0]-p1[0]; dy=p2[1]-p1[1]
        a=(dx*d2[1]-dy*d2[0])/det
        return (p1[0]+a*d1[0], p1[1]+a*d1[1])
    top_p=svec; top_d=(45,30)
    bot_p=(45+bvec[0], 30+bvec[1]); bot_d=(-45,30)
    apex=intersect(top_p, top_d, bot_p, bot_d)
    a=(0-top_p[0])/top_d[0]
    b=(0-bot_p[0])/bot_d[0]
    black=[(0, top_p[1]+a*top_d[1]), apex, (0, bot_p[1]+b*bot_d[1])]
    d.polygon(sc(black), fill='#000000')
    thick((0,0),(45,30),12,'#007749')
    thick((45,30),(90,30),12,'#007749')
    thick((0,60),(45,30),12,'#007749')
    return im.resize((w,h), Image.Resampling.LANCZOS)
def _raster_us(w,h):
    from PIL import Image, ImageDraw
    W,H=950,500
    im=Image.new('RGB',(W,H),'#FFFFFF')
    d=ImageDraw.Draw(im)
    sh=H/13
    for i in range(13):
        if i%2==0:
            d.rectangle((0, int(i*sh), W, int((i+1)*sh)+1), fill='#B22234')
    cw=int(round(W*0.4)); ch=sh*7
    d.rectangle((0,0,cw,ch), fill='#3C3B6E')
    E=cw/12; F=ch/10
    def star(cx,cy,r):
        pts=[]
        for i in range(10):
            ang=-math.pi/2+i*math.pi/5
            rad=r if i%2==0 else r*0.381966
            pts.append((cx+rad*math.cos(ang), cy+rad*math.sin(ang)))
        d.polygon(pts, fill='#FFFFFF')
    for row in range(9):
        y=F*(row+1)
        xs=[E*(1+2*k) for k in range(6)] if row%2==0 else [E*(2+2*k) for k in range(5)]
        for x in xs: star(x,y,E*0.42)
    return im.resize((w,h), Image.Resampling.LANCZOS)
CSS='''body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a;line-height:1.65;background:#fafaf7;font-size:19px}header{background:#123b5c;color:#fff;padding:.7rem 1rem}header a{color:#fff}.bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.45rem .8rem}.brand{display:flex;align-items:center;gap:.45rem;font-weight:700;font-size:1.05rem;line-height:1.25;text-decoration:none;color:#fff;min-width:0;flex:1 1 16rem}.brand .name{min-width:0}.flags{display:inline-flex;gap:.28rem;flex:none;align-items:center}.flag{height:22px;width:auto;display:block;border-radius:1px;box-shadow:0 0 0 1px rgba(255,255,255,.45)}.headlink{font-weight:600;text-decoration:underline;white-space:nowrap}.menu summary,details.card summary{cursor:pointer;font-weight:600}details.card summary{font-size:1.05rem}.menu summary{padding:.35rem 0}.menu[open] summary{margin-bottom:.4rem}nav.top{display:flex;flex-wrap:wrap;gap:.8rem 1.6rem}.grp{display:flex;flex-direction:column;min-width:11rem}.glabel{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#bcd3e6}.grp a{padding:.2rem 0;text-decoration:none}.grp a:hover{text-decoration:underline}@media(max-width:640px){nav.top{flex-direction:column}.brand{font-size:1rem}.headcta a.intake,.home-cta a.intake{display:block;width:100%;box-sizing:border-box}}.notice{background:#fff4d6;border-bottom:2px solid #e6cf8a;padding:.7rem 1rem;font-size:1rem}main{max-width:1140px;margin:0 auto;padding:1rem}main p,main li,.card p{max-width:75ch}main .toc,main .toc p,main .toc li,main .cards,main h1,main h2,main h3,main table,main .wrap{max-width:none}.crumbs{font-size:.95rem;margin:.3rem 0 .6rem}h1{font-size:2rem;line-height:1.25}h2{margin-top:2rem;font-size:1.45rem}.checked{display:inline-block;background:#e6f2ea;border:1px solid #a9d1b5;border-radius:4px;padding:.15rem .5rem;font-size:.95rem}.toc{background:#eef3f7;border-radius:6px;padding:.6rem 1rem;margin:1rem 0}.toc ul{margin:.3rem 0;padding-left:1.2rem}.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:.9rem 1.1rem;margin:.9rem 0}.warn{border-left:6px solid #c0392b;background:#fdeeee}.note{border-left:6px solid #d68910;background:#fff8ec}.conf{border-left:6px solid #8e44ad;background:#f6effa}.stage{border-left:6px solid #123b5c}.stage h2{margin-top:.2rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem}.cards a.card{display:block;text-decoration:none;color:#1a1a1a;margin:0}.cards a.card strong{color:#0b5394;font-size:1.1rem}.cards a.card:hover{border-color:#0b5394}.src{font-size:.88rem;color:#555}.pn{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.8rem;margin-top:2.5rem;border-top:1px solid #ddd;padding-top:1rem}.pn a{font-weight:600}footer{max-width:1140px;margin:2rem auto;padding:1rem;font-size:.95rem;color:#444;border-top:1px solid #ddd}footer ul{padding-left:1.2rem}a{color:#0b5394}table{border-collapse:collapse;width:100%;background:#fff;font-size:.95rem}th,td{border:1px solid #ddd;padding:.45rem;text-align:left;vertical-align:top}th{background:#eef3f7}.wrap{overflow-x:auto}.headcta{margin:.55rem 0 .15rem}a.intake{display:inline-block;background:#a85f00;color:#fff;font-weight:700;text-decoration:none;border-radius:8px;padding:.6rem 1rem;line-height:1.3;text-align:center;max-width:100%;box-sizing:border-box}a.intake:hover{background:#8f4e00;color:#fff;text-decoration:none}a.intake:focus{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 5px #123b5c}a.intake:focus:not(:focus-visible){outline:none;box-shadow:none}a.intake:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 5px #123b5c}.home-cta{margin:.2rem 0 1.1rem}.home-cta a.intake{font-size:1.15rem;padding:.8rem 1.2rem}a.guide-link{display:block;width:fit-content;margin-top:.45rem;font-size:.95rem;font-weight:600;text-decoration:underline}'''
