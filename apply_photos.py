import re,glob,html
K={"Tape-in Klasik":"tape-in-klasik","Tape-in Long Line":"tape-in-long-line","Tape-in Invisible":"tape-in-invisible","Keratín I-Tip":"keratin-i-tip","Keratín Flat Tip":"keratin-flat-tip","Keratín Nano Tip":"keratin-nano-tip","Keratín U-Tip":"keratin-u-tip","Keratín V-Tip":"keratin-v-tip","Mikro krúžky (Micro Loop)":"micro-loop","Clip-in Klasik":"clip-in-klasik","Clip-in Seamless":"clip-in-seamless","Strojová tresa (Machine Weft)":"tresa-machine","Genius tresa (Genius Weft)":"tresa-genius","Ručne viazaná tresa (Hand-Tied)":"tresa-hand-tied","Zväzok 100 g":"zvazok-100","Set 3 zväzky (300 g)":"zvazky-3","Set 4 zväzky (400 g)":"zvazky-4","Zväzky + closure / frontal":"zvazky-closure","Voľné vlasy rovné":"volne-rovne","Voľné vlasy kučeravé":"volne-kucerave","Voľné vlasy na zosvetlenie (do #613)":"volne-613","Cop na omotávku":"cop-omotavka","Cop so sponou (clip-in)":"cop-spona","Lace closure":"lace-closure","Lace frontal":"lace-frontal","Parochňa s closure":"parochna-closure","Parochňa s frontalom":"parochna-frontal","Mikáďo (bob)":"parochna-bob","Dlhá parochňa":"parochna-dlha","Parochňa ready-to-wear":"parochna-rtw","Vzorkovník odtieňov":"vzorkovnik","Náhradná lepiaca páska":"paska"}
HERO={"tape-in":"tape-in-long-line","keratin":"keratin-i-tip","clip-in":"clip-in-klasik","tresy":"tresa-hand-tied","zvazky":"zvazky-3","volne-vlasy":"volne-rovne","copy":"cop-spona","closure-frontal":"lace-frontal","parochne":"parochna-bob","doplnky":"vzorkovnik"}
card=re.compile(r'<div class="imgw">(?:<img[^>]*>)+</div>(<div class="body">.*?data-p="([^"]+)")',re.S)
def rep(m):
    whole=m.group(0); name=html.unescape(m.group(2)); k=K[name]
    real=re.search(r'src="(assets/c/[^"]+)"',whole)
    real=real.group(1) if real else ''
    g=f"assets/p/{k}_w.webp|assets/p/{k}_p.webp"+("|"+real if real else "")
    return (f'<div class="imgw" data-g="{g}" role="button" tabindex="0" aria-label="Galéria – {m.group(2)}">'
      f'<img loading="lazy" class="im1" src="assets/p/{k}_w.webp" alt="Velora Lux – {m.group(2)} – výsledok">'
      f'<img loading="lazy" class="im2" src="assets/p/{k}_p.webp" alt="Velora Lux – {m.group(2)} – produkt">'
      f'<span class="gcount">{3 if real else 2} foto</span></div>'+m.group(1))
JS='''<script id="vgal">(function(){var d=document,b=d.createElement('div');b.id='vlb';b.innerHTML='<button class="x" aria-label="Zavrieť">×</button><img class="big" alt=""><div class="th"></div>';d.body.appendChild(b);var big=b.querySelector('.big'),th=b.querySelector('.th');function open(w){var l=w.dataset.g.split('|'),a=w.querySelector('img').alt;th.innerHTML='';l.forEach(function(s,i){var t=d.createElement('img');t.src=s;t.alt=a;t.onclick=function(){big.src=s;th.querySelectorAll('img').forEach(function(x){x.classList.remove('on')});t.classList.add('on')};if(!i)t.classList.add('on');th.appendChild(t)});big.src=l[0];big.alt=a;b.classList.add('open')}d.querySelectorAll('.imgw[data-g]').forEach(function(w){w.addEventListener('click',function(){open(w)});w.addEventListener('keydown',function(e){if(e.key==='Enter')open(w)})});b.addEventListener('click',function(e){if(e.target===b||e.target.classList.contains('x'))b.classList.remove('open')});d.addEventListener('keydown',function(e){if(e.key==='Escape')b.classList.remove('open')})})();</script>'''
CSS='''
/*photos*/
.pcard .imgw{position:relative;cursor:zoom-in;aspect-ratio:4/3;overflow:hidden}
.pcard .imgw img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .45s ease,transform .6s ease}
.pcard .imgw .im2{opacity:0}
.pcard:hover .imgw .im2,.pcard .imgw:focus .im2{opacity:1}
.pcard:hover .imgw img{transform:scale(1.03)}
.pcard .gcount{position:absolute;right:10px;bottom:10px;background:rgba(0,0,0,.65);color:#e8c98a;font-size:12px;padding:3px 9px;border-radius:20px;border:1px solid rgba(232,201,138,.4)}
#vlb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;z-index:9999;flex-direction:column;align-items:center;justify-content:center;padding:20px;gap:14px}
#vlb.open{display:flex}
#vlb .big{max-width:min(1000px,94vw);max-height:72vh;border-radius:10px;border:1px solid rgba(232,201,138,.35)}
#vlb .th{display:flex;gap:10px}
#vlb .th img{width:90px;height:68px;object-fit:cover;border-radius:6px;cursor:pointer;opacity:.55;border:1px solid transparent}
#vlb .th img.on{opacity:1;border-color:#e8c98a}
#vlb .x{position:absolute;top:14px;right:20px;background:none;border:0;color:#e8c98a;font-size:38px;cursor:pointer}
'''
for f in sorted(glob.glob('kategoria-*.html')):
    s=open(f).read(); slug=f[10:-5]
    s,n=card.subn(rep,s)
    s=re.sub(r'(<section class="lhero sm"><div class="bg"><img[^>]*src=")assets/ai/[^"]+(")',r'\1assets/p/%s_w.webp\2'%HERO[slug],s)
    if 'id="vgal"' not in s: s=s.replace('</body>',JS+'</body>',1)
    open(f,'w').write(s); print(f,n)
c=open('style.css').read()
if '/*photos*/' not in c: open('style.css','a').write(CSS)
