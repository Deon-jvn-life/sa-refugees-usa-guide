"""Shared helpers: page shell, topic menu, breadcrumbs, timeline steps, read next, search, robots.txt, sitemap.xml, checks."""
import os,html as H,shutil,re,json,math
D="26 October 2026"; ISO="2026-10-26"
NOTICE=('This is general information for information purposes only, not legal advice. Refugee status questions can affect your status: '
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

SEARCH_JS=r'''(function(){
  var el=document.getElementById("search-data");
  var input=document.getElementById("q");
  var box=document.getElementById("search-results");
  if(!el||!input||!box) return;
  var pages=[];
  try { pages=JSON.parse(el.textContent); } catch(e){ return; }
  function esc(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c];
    });
  }
  function activeWords(q){
    var t=String(q||"").trim().toLowerCase();
    if(t.length<2) return [];
    return t.split(/\s+/).filter(function(w){ return w; });
  }
  function match(blob, ws){
    if(!ws.length) return true;
    blob=String(blob).toLowerCase();
    for(var i=0;i<ws.length;i++) if(blob.indexOf(ws[i])<0) return false;
    return true;
  }
  function filterIndex(q){
    var root=document.getElementById("page-index");
    if(!root) return;
    var ws=activeWords(q);
    var items=root.querySelectorAll("li");
    var shown=0;
    for(var i=0;i<items.length;i++){
      var li=items[i];
      var blob=li.textContent+" "+(li.getAttribute("data-keywords")||"");
      var ok=match(blob, ws);
      li.hidden=!ok;
      if(ok) shown++;
    }
    var sections=root.querySelectorAll("section");
    for(var s=0;s<sections.length;s++){
      var sec=sections[s];
      var lis=sec.querySelectorAll("li");
      var any=false;
      for(var k=0;k<lis.length;k++) if(!lis[k].hidden) any=true;
      sec.hidden=!any;
    }
    var status=document.getElementById("index-status");
    if(status){
      if(!ws.length) status.textContent="Showing every page.";
      else if(!shown) status.textContent="No page matches. Try a different word, or clear the search.";
      else status.textContent="Showing "+shown+" of "+items.length+" pages.";
    }
  }
  function show(q){
    var ws=activeWords(q);
    if(!ws.length){
      box.hidden=true;
      box.innerHTML="";
    } else {
      var hits=[];
      for(var i=0;i<pages.length;i++){
        var p=pages[i];
        var blob=p.t+" "+p.s+" "+p.g+" "+(p.k||"");
        if(match(blob, ws)) hits.push(p);
        if(hits.length===8) break;
      }
      if(!hits.length){
        box.innerHTML="<p class=\"search-empty\">No matching page. Open the <a href=\"/find/\">full page list</a>.</p>";
      } else {
        var html="<ul>";
        for(var j=0;j<hits.length;j++){
          var hit=hits[j];
          html+="<li><a href=\""+esc(hit.u)+"\"><strong>"+esc(hit.t)+"</strong><span>"+esc(hit.s)+"</span></a></li>";
        }
        html+="</ul>";
        box.innerHTML=html;
      }
      box.hidden=false;
    }
    filterIndex(q);
  }
  input.addEventListener("input", function(){ show(input.value); });
  input.addEventListener("keydown", function(e){
    if(e.key==="Escape"){ box.hidden=true; box.innerHTML=""; }
  });
  document.addEventListener("click", function(e){
    if(!box.contains(e.target) && e.target!==input){ box.hidden=true; }
  });
  var initial="";
  try { initial=new URLSearchParams(window.location.search).get("q")||""; } catch(err){ initial=""; }
  if(initial){ input.value=initial; show(initial); }
  else filterIndex("");
  var sums=document.querySelectorAll(".grp > summary");
  for(var n=0;n<sums.length;n++){
    sums[n].addEventListener("click", function(){
      var parent=this.parentNode;
      var open=document.querySelectorAll(".grp[open]");
      for(var i=0;i<open.length;i++) if(open[i]!==parent) open[i].removeAttribute("open");
    });
  }
})();'''
TOC_BOOT='<script>if(window.matchMedia("(min-width:960px)").matches){var d=document.currentScript.previousElementSibling;if(d&&d.tagName==="DETAILS")d.open=true;}</script>'
class Site:
    def __init__(s,root,base,brand,groups,order,footer,css,terms=None,gsc='',msvalidate='',related=None):
        s.out=os.path.join(root,'site'); s.base=base.rstrip('/'); s.brand=brand; s.groups=groups; s.order=order
        s.footer=footer; s.css=css; s.pages=[]; s.indexable=[]; s.seo=[]
        s.gsc=gsc or ''; s.msvalidate=msvalidate or ''; s.related=related or []
        s.titles={p:t for g,items in groups for p,t in items}; s.titles['index.html']='Home'
        s.terms=[(anchor,[re.compile(p,re.I) for p in pats]) for anchor,pats in (terms or [])]
        s.when={}; s.summaries={}; s.read_next={}; s.aliases={}; s._search_cache=None
        if os.path.exists(s.out): shutil.rmtree(s.out)
        os.makedirs(s.out)
    def _search_json(s):
        if s._search_cache is not None: return s._search_cache
        rows=[{"u":"/","t":"Home","s":"Start here, top tasks, and every topic.","g":"Home","k":"guide home"}]
        for g,items in s.groups:
            for p,t in items:
                rows.append({"u":href(p),"t":t,"s":s.summaries.get(p,""),"g":g,"k":s.aliases.get(p,"")})
        s._search_cache=json.dumps(rows,ensure_ascii=False).replace("<","\\u003c")
        return s._search_cache
    def page(s,path,title,desc,body,stage=None,kind='article',faqs=None,show_faqs=True):
        if faqs and show_faqs:
            body+='<h2>Questions and answers</h2>'+''.join(f'<details class="card"><summary>{q}</summary><div>{ahtml}</div></details>' for q,ahtml in faqs)
        summary=s.summaries.get(path,'')
        if '<h1>' in body:
            body=body.replace('<h1>','<h1 id="page-title">',1)
        if summary and kind!='home' and '<h1' in body:
            body=body.replace('</h1>','</h1><div class="inshort"><p><strong>In short.</strong> '+esc(summary)+'</p></div>',1)
        nav_bits=[]
        for g,items in s.groups:
            links=[]
            here=False
            for p,t in items:
                cur=' aria-current="page"' if p==path else ''
                cls=' class="is-current"' if p==path else ''
                if p==path: here=True
                links.append(f'<a href="{href(p)}"{cls}{cur}>{esc(t)}</a>')
            mark=' aria-current="true"' if here else ''
            nav_bits.append(f'<details class="grp{" has-current" if here else ""}"><summary{mark}>{esc(g)}</summary><div class="glinks">'+''.join(links)+'</div></details>')
        nav=''.join(nav_bits)
        url=canon_url(s.base, path)
        h1m=re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        headline=H.unescape(re.sub(r'<[^>]+>','', h1m.group(1))) if h1m else title
        if path not in s.titles:
            s.titles[path]=headline
        h2=re.findall(r'<h2>(.*?)</h2>',body)
        def addid(m): return f'<h2 id="{slug(m.group(1))}">{m.group(1)}</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',addid,body)
        used=set()
        body=link_terms(body, s.terms, used)
        foot=link_terms(s.footer, s.terms, used)
        h2pos=body.find('<h2')
        if h2pos==-1:
            head, rest = body, ''
        else:
            head, rest = body[:h2pos], body[h2pos:]
        toc=''
        if len(h2)>=3:
            opened=' open' if len(h2)<=8 else ''
            lis=''.join(
                f'<li><a href="#{slug(x)}">{esc(H.unescape(re.sub("<[^>]+>","",x)))}</a></li>' for x in h2)
            toc=f'<nav class="toc" aria-label="On this page"><details class="toc-details"{opened}><summary>On this page</summary><ul>{lis}</ul></details>{TOC_BOOT}</nav>'
        plain=s.titles.get(path, headline)
        if path=='index.html':
            crumbs='<nav class="crumbs" aria-label="Breadcrumb"><ol><li><span aria-current="page">Home</span></li></ol></nav>'
        else:
            items_html=['<li><a href="/">Home</a></li>']
            if stage:
                items_html.append(f'<li><a href="/#{slug(stage)}">{esc(stage)}</a></li>')
            items_html.append(f'<li><span aria-current="page">{esc(plain)}</span></li>')
            crumbs='<nav class="crumbs" aria-label="Breadcrumb"><ol>'+''.join(items_html)+'</ol></nav>'
        when=s.when.get(path,'')
        when_html=f'<a class="when" href="/#{slug(when)}">When you need this: {esc(when)}</a>' if when else ''
        meta=f'<p class="meta"><span class="checked">Last checked: {D}</span>{when_html}</p>'
        def step_link(target, kind):
            label=s.titles.get(target)
            if not label: return ''
            w=s.when.get(target,'')
            whtml=f'<span class="pn-when">{esc(w)}</span>' if w else ''
            word='Previous' if kind=='prev' else 'Next'
            return f'<a class="{kind}" href="{href(target)}"><span class="pn-k">{word}</span><span class="pn-t">{esc(label)}</span>{whtml}</a>'
        pn=''
        if path in s.order:
            i=s.order.index(path)
            prev=step_link(s.order[i-1],'prev') if i>0 else ''
            nxt=step_link(s.order[i+1],'next') if i+1<len(s.order) else ''
            if prev or nxt:
                pn='<nav class="pn" aria-label="Pages in time order">'+prev+nxt+'</nav>'
        rn_items=[]
        for dest in s.read_next.get(path) or []:
            label=s.titles.get(dest)
            if not label: continue
            blurb=s.summaries.get(dest,'')
            blurb_html=f'<span class="ls">{esc(blurb)}</span>' if blurb else ''
            rn_items.append(f'<li><a class="jump" href="{href(dest)}"><span class="lt">{esc(label)}</span>{blurb_html}</a></li>')
        readnext='<aside class="readnext" aria-labelledby="read-next"><h2 id="read-next">Read next</h2><ul>'+''.join(rn_items)+'</ul></aside>' if rn_items else ''
        for label,text,lo,hi in (('title',title,50,60),('description',desc,120,160)):
            if not (lo<=len(text)<=hi):
                s.seo.append(f'WARNING: {path} {label} is {len(text)} characters (want {lo} to {hi}): {text}')
        crumbs_ld=[{"@type":"ListItem","position":1,"name":"Home","item":s.base+"/"}]
        if path!='index.html':
            pos=2
            if stage:
                crumbs_ld.append({"@type":"ListItem","position":pos,"name":stage,"item":s.base+"/#"+slug(stage)})
                pos+=1
            item={"@type":"ListItem","position":pos,"name":plain}
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
        if s.gsc: verify+=f'<meta name="google-site-verification" content="{esc(s.gsc)}" />'
        if s.msvalidate: verify+=f'<meta name="msvalidate.01" content="{esc(s.msvalidate)}">'
        og_url='' if kind=='error' else f'<meta property="og:url" content="{esc(url)}">'
        og_type='website' if kind!='article' else 'article'
        image=s.base+'/og.png'
        related=''
        if s.related:
            related='<p><strong>Related guides</strong></p><ul>'+''.join(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>' for u,t in s.related)+'</ul>'
        layout_cls='layout has-toc' if toc else 'layout'
        h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#1e3a32"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{canonical}{robots}{verify}<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(s.brand)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">{og_url}<meta property="og:image" content="{esc(image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(image)}">{ld}<style>{s.css}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<a class="skip" href="#content">Skip to content</a>
<header><div class="shell"><div class="bar"><a class="brand" href="/">{FLAGS}<span class="name"><span class="name-main">{esc(s.brand)}</span><span class="name-sub">Independent guide. Not a government website.</span></span></a><a class="headlink" href="/glossary/">Word list</a><span class="headcta">{intake_button()}</span></div>
<div class="search-wrap"><form class="sitesearch" role="search" action="/find/" method="get"><label for="q">Search this guide</label><input id="q" name="q" type="search" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"><button type="submit">Search</button></form><div id="search-results" class="search-results" hidden role="region" aria-live="polite" aria-label="Matching pages"></div></div>
<details class="menu"><summary aria-controls="site-nav">Topics</summary></details><nav id="site-nav" class="top" aria-label="Topics">{nav}</nav></div></header>
<main id="content" tabindex="-1"><div class="notice" role="note"><div class="shell"><strong>Important:</strong> {NOTICE}</div></div><div class="shell">{crumbs}{meta}<article class="content" aria-labelledby="page-title"><div class="head-block">{head}</div><div class="{layout_cls}">{toc}<div class="rest">{rest}{pn}{readnext}</div></div></article></div></main>
<footer><div class="shell"><nav class="footnav" aria-label="About this guide"><a href="/glossary/">Word list</a><a href="/find/">All pages</a><a href="/disclaimer/">Disclaimer</a><a href="/about/">About</a></nav><p><strong>{NOTICE}</strong></p>{foot}{related}<p>Last checked: {D}.</p></div></footer>
<script type="application/json" id="search-data">{s._search_json()}</script><script>{SEARCH_JS}</script></body></html>'''
        for bad in ('\u2014','\u2013','&mdash;','&ndash;'): assert bad not in h,(path,bad)
        assert 'myuscisgov.com' not in h
        assert 'not legal advice' in h and 'information purposes only' in h
        p=os.path.join(s.out,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w',encoding='utf-8').write(h); s.pages.append(path)
        if kind!='error': s.indexable.append(path)
    def finish(s):
        if s.seo:
            raise SystemExit('SEO length check failed:\n'+'\n'.join(s.seo))
        _write_assets(s.out)
        bots=['GPTBot','OAI-SearchBot','PerplexityBot','Bingbot','Googlebot','*']
        open(os.path.join(s.out,'robots.txt'),'w').write(''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {s.base}/sitemap.xml\n')
        urls=''.join(f'<url><loc>{canon_url(s.base,p)}</loc><lastmod>{ISO}</lastmod></url>\n' for p in sorted(s.indexable))
        open(os.path.join(s.out,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
        needles=('not legal advice','information purposes only','Last checked:','/_vercel/insights/script.js')
        for path in s.pages:
            html=open(os.path.join(s.out,path),encoding='utf-8').read()
            for needle in needles:
                if needle not in html:
                    raise SystemExit(f'Missing {needle} on {path}')
            if s.gsc and s.gsc not in html:
                raise SystemExit('Missing Google verification on '+path)
            if path!='404.html':
                if 'rel="canonical" href="https://www.sarefugeesusa.org/' not in html:
                    raise SystemExit('Missing canonical on '+path)
                if 'noindex' in html:
                    raise SystemExit('Unexpected noindex on '+path)
            elif 'noindex,follow' not in html:
                raise SystemExit('404 should be noindex')
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

CSS=r'''*,*::before,*::after{box-sizing:border-box}html{scroll-padding-top:.75rem}body{margin:0;color:#1a1814;background:#f4f1ea;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:1.1875rem;line-height:1.6}[hidden]{display:none!important}img,svg{max-width:100%}.flag{height:22px;width:auto;max-width:none;display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(255,255,255,.45)}.shell{max-width:76rem;margin:0 auto;padding:0 1rem;min-width:0}.skip{position:absolute;left:.5rem;top:0;transform:translateY(-120%);background:#fff;color:#1a1814;padding:.6rem 1rem;z-index:40;min-height:44px;font-weight:700}.skip:focus,.skip:focus-visible{transform:none}header{background:#1e3a32;color:#fff;position:relative;z-index:20}header a{color:#fff}.bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.5rem 1rem;padding-top:.85rem}.brand{display:flex;align-items:center;gap:.55rem;min-width:0;flex:1 1 16rem;color:#fff;text-decoration:none;font-weight:700}.flags{display:inline-flex;gap:.3rem;flex:none;align-items:center}.name{display:flex;flex-direction:column;min-width:0}.name-main{font-size:1.05rem;line-height:1.25}.name-sub{font-size:.95rem;font-weight:600;color:#e7f2ec;line-height:1.35}.headlink{display:inline-flex;align-items:center;min-height:44px;padding:.25rem 0;font-weight:700;text-decoration:underline;text-underline-offset:.15em}.search-wrap{position:relative;margin:.75rem 0 .35rem}.sitesearch{display:flex;flex-wrap:wrap;gap:.5rem;align-items:flex-end}.sitesearch label{flex:1 1 100%;color:#fff;font-weight:700}.sitesearch input[type="search"]{flex:1 1 12rem;min-width:0;min-height:48px;font:inherit;color:#1a1814;background:#fff;border:2px solid #fff;border-radius:8px;padding:.4rem .7rem}.sitesearch button{min-height:48px;min-width:5.5rem;padding:.4rem 1rem;font:inherit;font-weight:700;color:#1a1814;background:#ffe08a;border:2px solid #ffe08a;border-radius:8px;cursor:pointer}.search-results{position:absolute;z-index:30;left:0;right:0;top:100%;background:#fff;color:#1a1814;border:2px solid #1a1814;border-radius:8px;max-height:70vh;overflow:auto}.search-results ul{list-style:none;margin:0;padding:0}.search-results a{display:flex;flex-direction:column;gap:.15rem;min-height:48px;justify-content:center;padding:.55rem .75rem;color:#0a3d66;text-decoration:underline;text-underline-offset:.12em}.search-results a span{color:#1a1814;font-weight:400}.search-empty{margin:0;padding:.75rem;color:#1a1814}.headcta{display:flex;align-items:center}.bar a.intake{min-height:44px;padding:.45rem .8rem;font-size:1rem}a.intake{display:inline-flex;align-items:center;justify-content:center;min-height:48px;background:#6e3b12;color:#fff;font-weight:700;text-decoration:none;border-radius:8px;padding:.65rem 1rem;line-height:1.3;text-align:center}a.intake:hover{background:#5c310e;color:#fff}a.intake:visited,header a.intake{color:#fff}.menu{margin:.15rem 0 .55rem}.menu summary{display:flex;align-items:center;width:100%;min-height:48px;padding:.65rem 1rem;background:#fff;color:#1a1814;border-radius:8px;font-weight:700;cursor:pointer;list-style:none}.menu summary::-webkit-details-marker,.grp summary::-webkit-details-marker{display:none}.menu summary::marker,.grp summary::marker{content:""}nav.top{display:none;flex-wrap:wrap;align-items:flex-start;gap:.15rem .35rem;border-top:1px solid rgba(255,255,255,.28);margin-top:.15rem;padding:.35rem 0 .7rem}details.menu[open]~nav.top{display:flex}.grp{position:relative;flex:1 1 auto;min-width:0}.grp>summary{display:flex;align-items:center;justify-content:space-between;gap:.6rem;min-height:48px;padding:.45rem .7rem;color:#fff;font-weight:700;cursor:pointer;list-style:none}.grp>summary::after{content:"";border:solid #fff;border-width:0 2px 2px 0;width:.45rem;height:.45rem;transform:rotate(45deg);flex:none}.grp[open]>summary::after{transform:rotate(-135deg);margin-top:.3rem}.grp.has-current>summary{box-shadow:inset 0 -3px 0 #ffe08a}.glinks{display:flex;flex-direction:column;min-width:16rem}.glinks a{display:flex;align-items:center;min-height:48px;padding:.4rem .7rem;color:#fff;text-decoration:underline;text-underline-offset:.15em}.glinks a.is-current{font-weight:700;background:rgba(255,255,255,.16);border-radius:6px}@media(min-width:960px){details.menu{display:none}nav.top{display:flex}.grp{flex:0 1 auto}.grp[open] .glinks{position:absolute;z-index:30;top:100%;left:0;background:#143028;border:2px solid #fff;border-radius:8px;padding:.35rem;box-shadow:0 8px 24px rgba(0,0,0,.28)}}@media(max-width:959px){nav.top{flex-direction:column;gap:.15rem}.grp{width:100%}.glinks a{border-bottom:1px solid rgba(255,255,255,.22)}}@media(max-width:720px){.bar .headcta{flex:1 1 100%}.bar a.intake{width:100%}}@media(max-width:640px){.headcta a.intake,.home-cta a.intake{display:flex;width:100%}.name-main{font-size:1rem}}@media(max-width:359px){body{font-size:1.125rem}.shell{padding:0 .75rem}}.notice{background:#fff6db;color:#1a1814;border-bottom:3px solid #8a5a00}.notice .shell{padding-top:.8rem;padding-bottom:.8rem;font-size:1.125rem}main{min-width:0}main .shell{padding-top:1rem;padding-bottom:2.5rem}main:focus{outline:none}main:focus-visible{outline:3px solid #1a1814;outline-offset:-3px}.crumbs ol{display:flex;flex-wrap:wrap;list-style:none;padding:0;margin:.35rem 0 .15rem;gap:0}.crumbs li{display:flex;align-items:center;min-height:44px}.crumbs li+li::before{content:"/";margin:0 .45rem;color:#3e3a34}.crumbs a{display:inline-flex;align-items:center;min-height:44px}.meta{display:flex;flex-wrap:wrap;gap:.5rem .75rem;align-items:center;margin:.15rem 0 1rem;max-width:none}.checked{display:inline-flex;align-items:center;background:#e5f2ea;color:#143024;border:1px solid #1d4f3e;border-radius:6px;padding:.25rem .7rem;font-size:1rem}.when{display:inline-flex;align-items:center;min-height:44px;padding:.25rem .7rem;background:#fff;border:1px solid #d9d3c7;border-radius:8px;font-weight:700}article.content{min-width:0}.head-block{margin-bottom:.25rem}.layout{display:flex;flex-direction:column;gap:1.15rem;min-width:0}.toc{order:-1}.rest{order:0;min-width:0}@media(min-width:960px){.layout.has-toc{display:grid;grid-template-columns:minmax(0,1fr) 17.5rem;column-gap:2.25rem;align-items:start}.layout.has-toc .rest{grid-column:1;grid-row:1;order:0}.layout.has-toc .toc{grid-column:2;grid-row:1;order:0;position:sticky;top:1rem;max-height:calc(100vh - 2rem);overflow:auto}}h1,h2,h3{font-family:Georgia,Palatino,"Palatino Linotype",serif;line-height:1.25;font-weight:700;scroll-margin-top:.75rem}h1{font-size:clamp(1.75rem,1.15rem + 2.2vw,2.45rem);margin:0 0 .6rem}h2{font-size:1.5rem;margin:1.75rem 0 .6rem}h3{font-size:1.28rem;margin:1.15rem 0 .45rem}.content p{max-width:66ch}.inshort{background:#eef4f1;border-left:6px solid #1d4f3e;border-radius:8px;padding:.85rem 1rem;margin:.75rem 0 1rem}.inshort p{margin:0;max-width:66ch}.toc{background:#fff;border:1px solid #d9d3c7;border-radius:10px;padding:.35rem .9rem}.toc summary{min-height:48px;display:flex;align-items:center;font-weight:700;cursor:pointer}.toc ul{list-style:none;margin:0;padding:0 0 .45rem}.toc a{display:flex;align-items:center;min-height:44px;padding:.15rem 0}@media(min-width:960px){.toc a{min-height:32px}}.card{background:#fff;border:1px solid #d9d3c7;border-radius:10px;padding:.95rem 1.05rem;margin:.95rem 0}.warn{border-left:6px solid #9b2c2c;background:#fdeeee}.note{border-left:6px solid #8a5a00;background:#fff8ec}.conf{border-left:6px solid #5c3d78;background:#f6f1fa}details.card summary{min-height:48px;display:flex;align-items:center;cursor:pointer;font-weight:700;font-size:1.05rem}.timeline{list-style:none;margin:0;padding:0;counter-reset:step}.period{counter-increment:step;background:#fff;border:1px solid #d9d3c7;border-radius:12px;padding:.9rem 1rem 1rem;margin:0 0 .85rem}.period>h3{margin:0 0 .7rem;font-size:1.35rem}.period>h3::before{content:counter(step) ". "}.period-pages{list-style:none;padding:0;margin:0;display:grid;gap:.6rem}.tasks,.link-grid,.readnext ul,.index-list{list-style:none;padding:0;margin:0;display:grid;gap:.75rem;grid-template-columns:1fr}@media(min-width:720px){.tasks,.link-grid,.readnext ul,.index-list{grid-template-columns:1fr 1fr}}.topic{margin:0 0 1.4rem}.jump{display:flex;flex-direction:column;justify-content:center;gap:.2rem;min-height:48px;padding:.85rem 1rem;background:#fff;color:#1a1814;border:1px solid #d9d3c7;border-radius:10px;text-decoration:none}.jump:hover{border-color:#0a3d66}.jump .lt{color:#0a3d66;font-weight:700;text-decoration:underline;text-underline-offset:.12em;font-size:1.125rem}.jump .ls{color:#1a1814;font-size:1rem;text-decoration:none;font-weight:400}a.jump:visited .lt{color:#3d2a6b}.home-cta{margin:.2rem 0 1.15rem}.home-cta a.intake{font-size:1.125rem}.guide-link{display:inline-flex;align-items:center;min-height:44px;margin-top:.35rem;font-weight:700}.src{color:#3e3a34;font-size:1rem}.src,.card,td,th{overflow-wrap:anywhere}.pn{display:grid;gap:.75rem;margin-top:2rem}.pn a{display:flex;flex-direction:column;justify-content:center;gap:.15rem;min-height:48px;padding:.85rem 1rem;background:#fff;border:1px solid #d9d3c7;border-radius:10px;text-decoration:none}.pn .pn-k{color:#3e3a34;font-size:1rem;font-weight:700}.pn .pn-t{color:#0a3d66;font-weight:700;text-decoration:underline;text-underline-offset:.12em}.pn .pn-when{color:#1a1814;font-size:1rem}.pn a:visited .pn-t{color:#3d2a6b}@media(min-width:720px){.pn:has(a.prev):has(a.next){grid-template-columns:1fr 1fr}.pn a.next{align-items:flex-end;text-align:right}}.readnext{margin-top:1.75rem}.readnext h2{margin-top:0}.index-status{font-weight:700}a{color:#0a3d66}a:visited{color:#3d2a6b}.content a{text-decoration:underline;text-underline-offset:.12em}table{border-collapse:collapse;width:100%;background:#fff;font-size:1rem}th,td{border:1px solid #d9d3c7;padding:.55rem .65rem;text-align:left;vertical-align:top}th{background:#e7efe9;color:#1a1814}.wrap{overflow-x:auto;max-width:100%}footer{border-top:1px solid #d9d3c7;color:#1a1814;margin-top:1rem}footer .shell{padding-top:1.25rem;padding-bottom:2.25rem}footer p{max-width:66ch}.footnav{display:flex;flex-wrap:wrap;gap:.35rem 1rem;margin:0 0 .5rem}.footnav a{display:inline-flex;align-items:center;min-height:44px;font-weight:700}:focus{outline:3px solid #1a1814;outline-offset:2px}:focus:not(:focus-visible){outline:none}:focus-visible{outline:3px solid #1a1814;outline-offset:2px}header a:focus-visible,header button:focus-visible,header input:focus-visible{outline-color:#ffe08a}.menu summary:focus-visible{outline-color:#1a1814}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media(forced-colors:active){.card,.inshort,.notice,.jump,.period,.toc,.pn a,a.intake,.menu summary{border:1px solid CanvasText}a.intake{background:ButtonFace;color:ButtonText}}
'''
