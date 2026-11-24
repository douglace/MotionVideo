import sys, math, numpy as np, potrace
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
SRC, OUT = sys.argv[1:3]
S=3
im=Image.open(SRC).convert('RGB'); W,H=im.size
cols=[(254,254,254),(53,18,0),(254,133,2)]
def classify(a): return np.stack([((a-np.array(c))**2).sum(-1) for c in cols],-1).argmin(-1)
lab0=classify(np.asarray(im).astype(float))
big=np.asarray(im.resize((W*S,H*S),Image.LANCZOS).filter(ImageFilter.GaussianBlur(S*0.6))).astype(float)
lab=classify(big); ink=lab>0
orng=ndi.binary_opening(lab==2,iterations=4)
l,n=ndi.label(orng); sz=ndi.sum(orng,l,range(1,n+1)); orng=np.isin(l,1+np.nonzero(sz>3000)[0])
orng=ndi.binary_dilation(orng,iterations=4)&(lab==2)
hat=ndi.binary_fill_holes(ndi.binary_closing(lab0>0,iterations=6))   # silhouette pleine (intérieur blanc)
silf=ndi.gaussian_filter(np.kron(hat.astype(float),np.ones((S,S))),S)>0.5
def curves(m): return potrace.Bitmap(~m).trace(turdsize=20,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.2)
f=lambda p:f"{p.x/S:.1f} {p.y/S:.1f}"
def full(m):
    o=[]
    for c in curves(m):
        o.append("M"+f(c.start_point))
        for s in c.segments:
            o.append(("L"+f(s.c)+"L"+f(s.end_point)) if s.is_corner else ("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point)))
        o.append("Z")
    return "".join(o)
P_sil=full(silf); P_ink=full(ink); P_or=full(orng)
BR='#351200'; OR='#FE8502'; CR='#FFF8EE'
K=f'stroke="{BR}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"'
icons={
 'tomate':f'''<circle r="62" fill="#E8461E" {K}/><ellipse cx="-24" cy="-20" rx="13" ry="8" fill="#fff" opacity=".55" transform="rotate(-30 -24 -20)"/>
   <path d="M-34 -52 Q-14 -46 0 -64 Q14 -46 34 -52 Q16 -36 0 -44 Q-16 -36 -34 -52Z" fill="#5E9C2F" {K}/><path d="M0 -60 V-80" {K} fill="none"/>''',
 'piment':f'''<path d="M-72 -12 C-40 -40 34 -38 66 8 C76 24 62 40 42 28 C12 8 -32 10 -66 10 C-80 8 -82 -4 -72 -12Z" fill="#D8341C" {K}/>
   <ellipse cx="-12" cy="-14" rx="22" ry="6" fill="#fff" opacity=".45" transform="rotate(-8 -12 -14)"/><path d="M-72 -2 C-88 -8 -92 -26 -84 -42" fill="none" stroke="#3F7A1F" stroke-width="13" stroke-linecap="round"/>''',
 'basilic':f'''<path d="M0 70 C-62 24 -56 -44 0 -76 C56 -44 62 24 0 70Z" fill="#5E9C2F" {K}/><path d="M0 62 V-60 M0 10 L-24 -10 M0 -14 L22 -34 M0 32 L24 14" fill="none" stroke="#2F5E17" stroke-width="6" stroke-linecap="round"/>''',
 'citron':f'''<circle r="60" fill="#FFD23F" {K}/><circle r="46" fill="#FFF1A8"/>'''+"".join(f'<path d="M0 0 L{44*math.cos(a):.1f} {44*math.sin(a):.1f}" stroke="#FFD23F" stroke-width="6"/>' for a in [k*math.pi/4 for k in range(8)])+'<circle r="7" fill="#FFD23F"/>',
 'champignon':f'''<rect x="-22" y="-6" width="44" height="62" rx="16" fill="#F6E3C6" {K}/><path d="M-66 4 C-66 -66 66 -66 66 4 Z" fill="#B5651D" {K}/>
   <circle cx="-26" cy="-26" r="8" fill="#F6E3C6"/><circle cx="16" cy="-38" r="6" fill="#F6E3C6"/><circle cx="34" cy="-14" r="7" fill="#F6E3C6"/>''',
 'poivre':f'''<circle r="17" fill="#4A2A18" stroke="{BR}" stroke-width="6"/><circle cx="-5" cy="-5" r="4" fill="#fff" opacity=".5"/>''',
}
# (icône, x, y d'atterrissage, retard, rotation de départ, échelle)
items=[('tomate',215,870,0.00,-40,1.3),('citron',860,875,0.12,30,1.25),('basilic',545,862,0.24,-25,1.25),
       ('champignon',1040,865,0.36,25,1.25),('piment',385,900,0.48,-60,1.2),('poivre',690,930,0.55,0,1.3),
       ('poivre',735,940,0.62,0,1.1),('poivre',650,945,0.68,0,1.15)]
EB='cubic-bezier(.34,1.56,.64,1)'; EO='cubic-bezier(.22,1,.36,1)'
css=[]; body=[]
for i,(ic,x,y,dl,r0,sc) in enumerate(items):
    r1=r0*0.15
    css.append(f'''#it{i}{{transform-box:fill-box;transform-origin:50% 50%;animation:fall{i} 1.05s {dl:.2f}s linear both, gather{i} .5s {1.5+0.03*i:.3f}s cubic-bezier(.6,-0.28,.735,.045) forwards}}
@keyframes fall{i}{{0%{{transform:translateY(-1900px) rotate({r0}deg);animation-timing-function:cubic-bezier(.55,0,1,.45)}}
48%{{transform:translateY(0) rotate({r1:.0f}deg) scale(1.18,.8);animation-timing-function:cubic-bezier(0,.55,.45,1)}}
66%{{transform:translateY(-130px) rotate({r1*0.5:.0f}deg) scale(.95,1.06);animation-timing-function:cubic-bezier(.55,0,1,.45)}}
82%{{transform:translateY(0) scale(1.08,.92);animation-timing-function:cubic-bezier(0,.55,.45,1)}}
91%{{transform:translateY(-32px)}}100%{{transform:none}}}}
@keyframes gather{i}{{from{{transform:none;opacity:1}}to{{transform:translate({627-x}px,{600-y}px) rotate({'-' if i%2 else ''}300deg) scale(.15);opacity:.3}}}}''')
    body.append(f'<g id="it{i}"><g transform="translate({x} {y}) scale({sc})">{icons[ic]}</g></g>')
# ombres au sol
shadows="".join(f'<ellipse class="shd" cx="{x}" cy="{y+70*sc}" rx="{55*sc:.0f}" ry="{10*sc:.0f}" style="animation-delay:{dl+0.45:.2f}s,{1.5+0.03*i:.3f}s"/>' for i,(ic,x,y,dl,r0,sc) in enumerate(items) if ic!='poivre')
puffs=[]
for k in range(9):
    a=k/9*2*math.pi+.3; r=150+40*(k%3)
    puffs.append(f'<circle class="pf" cx="{627+r*0.35*math.cos(a):.0f}" cy="{600+r*0.35*math.sin(a):.0f}" r="{110+25*(k%3)}" style="--x:{r*math.cos(a):.0f}px;--y:{r*math.sin(a):.0f}px;animation-delay:{1.92+0.015*k:.3f}s"/>')
conf=[]
ccol=['#E8461E','#5E9C2F','#FFD23F',OR,'#B5651D']
for k in range(18):
    a=k/18*2*math.pi; r=420+120*(k%3)
    conf.append(f'<circle class="cf" cx="627" cy="600" r="{9+4*(k%3)}" fill="{ccol[k%5]}" style="--x:{r*math.cos(a):.0f}px;--y:{r*math.sin(a)*0.9:.0f}px;animation-delay:{2.02+0.01*(k%4):.2f}s"/>')
css.append(f'''
.shd{{fill:#5A2A08;opacity:0;animation:shd .6s ease both, shdOut .3s ease forwards}}
@keyframes shd{{from{{opacity:0}}to{{opacity:.14}}}}
@keyframes shdOut{{to{{opacity:0}}}}
.pf{{fill:#FFE2B8;opacity:0;transform-box:fill-box;transform-origin:50% 50%;animation:pf .7s {EO} both}}
@keyframes pf{{0%{{opacity:0;transform:translate(0,0) scale(.15)}}12%{{opacity:1}}35%{{opacity:.95}}100%{{opacity:0;transform:translate(var(--x),var(--y)) scale(1.5)}}}}
#puff{{filter:url(#soft);animation:pv 3s linear both}}
@keyframes pv{{0%{{visibility:hidden}}63%{{visibility:visible}}93%,100%{{visibility:hidden}}}}
.cf{{opacity:0;animation:cf 1.1s {EO} both}}
@keyframes cf{{0%{{opacity:0;transform:translate(0,0)}}5%{{opacity:1}}70%{{opacity:1}}100%{{opacity:0;transform:translate(var(--x),var(--y))}}}}
#logo{{transform-origin:627px 600px;animation:logo .7s 2.02s {EB} both}}
@keyframes logo{{0%{{opacity:0;transform:scale(.25) rotate(-8deg)}}25%{{opacity:1}}100%{{opacity:1;transform:none}}}}
#shine{{animation:shine 1s 2.9s cubic-bezier(.45,0,.25,1) both}}
@keyframes shine{{0%{{transform:translateX(-500px) skewX(-22deg)}}100%{{transform:translateX(1700px) skewX(-22deg)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}#items,#puff,#conf,#shadows{{display:none}}}}
''')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<title>Les Délices de Kevinne – intro ingrédients</title>
<style>{"".join(css)}</style>
<defs>
  <radialGradient id="bg" cx="627" cy="600" r="1500" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFBF4"/><stop offset=".5" stop-color="#FCEBD3"/><stop offset="1" stop-color="#EFCDA2"/></radialGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF" stop-opacity=".7"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
  <filter id="ds" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#6B3A10" flood-opacity=".28"/></filter>
  <clipPath id="oc"><path d="{P_or}"/></clipPath>
</defs>
<rect x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#bg)"/>
<g id="shadows">{shadows}</g>
<g id="items">{"".join(body)}</g>
<g id="conf">{"".join(conf)}</g>
<g transform="translate(627 600) scale(.84) translate(-627 -600)"><g id="logo">
  <g filter="url(#ds)"><path fill="#FFFFFF" d="{P_sil}"/></g>
  <path fill="{BR}" fill-rule="evenodd" d="{P_ink}"/>
  <path fill="{OR}" fill-rule="evenodd" d="{P_or}"/>
  <g clip-path="url(#oc)"><rect id="shine" x="0" y="-100" width="200" height="1500" fill="url(#sh)"/></g>
</g></g>
<g id="puff">{"".join(puffs)}</g>
</svg>
'''
open(OUT,'w').write(svg); print(len(svg)//1024,'KB')
