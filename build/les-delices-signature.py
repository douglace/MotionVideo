import sys, numpy as np, potrace
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
SRC, OUT, OUT_ALPHA = sys.argv[1:4]
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
sil=ndi.binary_fill_holes(ndi.binary_closing(lab0>0,iterations=6))
silf=ndi.gaussian_filter(np.kron(sil.astype(float),np.ones((S,S))),S)>0.5
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
BR='#351200'; OR='#FE8502'
css='''
#slide{transform-origin:627px 1000px;animation:slide .78s both}
@keyframes slide{
 0%{transform:translateX(-1500px) skewX(-14deg);animation-timing-function:cubic-bezier(.2,.75,.35,1)}
 52%{transform:translateX(36px) skewX(-7deg);animation-timing-function:cubic-bezier(.45,0,.4,1)}
 72%{transform:translateX(-14px) skewX(4deg);animation-timing-function:cubic-bezier(.45,0,.4,1)}
 87%{transform:translateX(5px) skewX(-1.5deg)}
 100%{transform:none}}
#shine{animation:shine .7s .72s cubic-bezier(.45,0,.25,1) both}
@keyframes shine{0%{transform:translateX(-400px) skewX(-22deg)}100%{transform:translateX(1600px) skewX(-22deg)}}
.tw{transform-box:fill-box;transform-origin:50% 50%;animation:tw .7s ease both}
@keyframes tw{0%{transform:scale(0) rotate(0);opacity:1}50%{transform:scale(1) rotate(45deg);opacity:1}100%{transform:scale(0) rotate(90deg);opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
'''
star=lambda x,y,s,dl: f'<path class="tw" fill="{OR}" style="animation-delay:{dl}s" d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z"/>'
def make(bg):
    bgr=('<rect x="-3000" y="-3000" width="%d" height="%d" fill="url(#bg)"/>'%(W+6000,H+6000)) if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<title>Les Délices de Kevinne – signature</title>
<style>{css}</style>
<defs>
  <radialGradient id="bg" cx="627" cy="600" r="1500" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFBF4"/><stop offset=".5" stop-color="#FCEBD3"/><stop offset="1" stop-color="#EFCDA2"/></radialGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF" stop-opacity=".8"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
  <filter id="mb" x="-40%" y="-10%" width="180%" height="120%">
    <feGaussianBlur stdDeviation="70 0"><animate attributeName="stdDeviation" values="70 0;0 0" keyTimes="0;1" dur=".42s" fill="freeze" calcMode="spline" keySplines=".2 .75 .35 1"/></feGaussianBlur>
  </filter>
  <filter id="ds" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#6B3A10" flood-opacity=".28"/></filter>
  <clipPath id="oc"><path d="{P_or}"/></clipPath>
</defs>
{bgr}
<g transform="translate(627 600) scale(.84) translate(-627 -600)"><g id="slide"><g filter="url(#mb)">
  <g filter="url(#ds)"><path fill="#FFFFFF" d="{P_sil}"/></g>
  <path fill="{BR}" fill-rule="evenodd" d="{P_ink}"/>
  <path fill="{OR}" fill-rule="evenodd" d="{P_or}"/>
  <g clip-path="url(#oc)"><rect id="shine" x="0" y="-100" width="180" height="1500" fill="url(#sh)"/></g>
</g></g></g>
{star(1135,300,30,1.0)}{star(150,930,22,1.18)}
</svg>
'''
open(OUT,'w').write(make(True)); open(OUT_ALPHA,'w').write(make(False))
