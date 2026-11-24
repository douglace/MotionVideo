import sys, numpy as np, potrace
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
d=ndi.distance_transform_edt(~(lab0>0)); st=ndi.binary_fill_holes(d<18)
stf=ndi.gaussian_filter(np.kron(st.astype(float),np.ones((S,S))),S*2)>0.5
def curves(m): return potrace.Bitmap(~m).trace(turdsize=20,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.2)
f=lambda p:f"{p.x/S:.1f} {p.y/S:.1f}"
def cd(c):
    o=["M"+f(c.start_point)]; ys=[c.start_point.y]
    for s in c.segments:
        o.append(("L"+f(s.c)+"L"+f(s.end_point)) if s.is_corner else ("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point)))
        ys.append(s.end_point.y)
    o.append("Z"); return "".join(o), sum(ys)/len(ys)/S
full=lambda m:"".join(cd(c)[0] for c in curves(m))
P_st=full(stf); P_ink=full(ink); P_or=full(orng)
lines=[]
for m,w in ((ink,5),(orng,6.5)):
    for c in curves(m):
        dd,cy=cd(c); lines.append((dd,w,1.3+0.9*(1-cy/H)))
CR='#FFF4E2'; BR='#351200'; OR='#FE8502'
EB='cubic-bezier(.34,1.56,.64,1)'; EO='cubic-bezier(.22,1,.36,1)'; EIO='cubic-bezier(.65,0,.35,1)'
css=f'''
@keyframes on{{to{{stroke-dashoffset:0}}}}
@keyframes fo{{to{{opacity:0}}}}
.s{{fill:none;stroke:{CR};stroke-linecap:round;stroke-linejoin:round}}
.dr{{stroke-dasharray:1 1;stroke-dashoffset:1}}
#pot{{animation:potIn .7s .05s {EB} both, potOut .6s 3.3s cubic-bezier(.55,0,1,.45) forwards}}
@keyframes potIn{{from{{transform:translateY(380px)}}to{{transform:none}}}}
@keyframes potOut{{to{{transform:translateY(900px);opacity:0}}}}
.w{{stroke-width:34;opacity:.42;animation:on 1.5s {EO} both}}
#wisps{{filter:url(#wisp);animation:fo .6s 2.15s ease both}}
.ln{{animation:on 1.2s {EO} both}}
#lines{{filter:url(#vap);animation:fo .4s 3.3s ease both}}
#fork{{animation:drop .5s 2.65s cubic-bezier(.5,0,.75,0) both, fo .3s 3.35s ease forwards}}
#spoon{{animation:drop .5s 2.75s cubic-bezier(.5,0,.75,0) both, fo .3s 3.35s ease forwards}}
@keyframes drop{{0%{{transform:translateY(-700px);opacity:0}}20%{{opacity:1}}80%{{transform:translateY(0)}}90%{{transform:translateY(-18px)}}100%{{transform:none;opacity:1}}}}
#logo{{transform-origin:627px 600px;animation:logo .6s 3.2s {EB} both}}
@keyframes logo{{0%{{opacity:0;transform:scale(.9)}}30%{{opacity:1}}100%{{opacity:1;transform:none}}}}
#ring{{transform-box:fill-box;transform-origin:50% 50%;opacity:0;animation:ring .8s 3.2s {EO} both}}
@keyframes ring{{0%{{opacity:0;transform:scale(.3);stroke-width:36}}5%{{opacity:.9}}100%{{opacity:0;transform:scale(1);stroke-width:2}}}}
#shine{{animation:shine 1s 4.0s cubic-bezier(.45,0,.25,1) both}}
@keyframes shine{{0%{{transform:translateX(-500px) skewX(-22deg)}}100%{{transform:translateX(1700px) skewX(-22deg)}}}}
.lw{{stroke-width:24;opacity:0;animation:loop 3s ease-in-out infinite}}
@keyframes loop{{0%{{stroke-dashoffset:1;opacity:0;transform:translateY(20px)}}25%{{opacity:.5}}60%{{stroke-dashoffset:0;opacity:.4}}100%{{stroke-dashoffset:-1;opacity:0;transform:translateY(-40px)}}}}
#after{{filter:url(#wisp)}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}#pot,#wisps,#lines,#fork,#spoon,#ring,#after{{display:none}}}}
'''
wx=[465,546,627,708,789]
wisps="".join(f'<path class="s dr w" pathLength="1" style="animation-delay:{.55+.12*i:.2f}s" d="M{x} 1045 C{x-45} 960 {x+45} 880 {x} 800 S{x-45} 640 {x} 560 S{x+40} 420 {x} 340"/>' for i,x in enumerate(wx))
after="".join(f'<path class="s dr lw" pathLength="1" style="animation-delay:{3.9+.6*i:.1f}s" d="M{x} 250 C{x-30} 210 {x+30} 170 {x} 130 S{x-30} 70 {x} 30"/>' for i,x in enumerate([560,627,694]))
ln="\n".join(f'<path class="s dr ln" pathLength="1" style="stroke-width:{w};animation-delay:{dl:.2f}s" d="{p}"/>' for p,w,dl in lines)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<title>Les Délices de Kevinne – intro ça mijote</title>
<style>{css}</style>
<defs>
  <radialGradient id="bg" cx="627" cy="620" r="1500" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#D86E2C"/><stop offset=".45" stop-color="#A8471A"/><stop offset="1" stop-color="#4E1C06"/></radialGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF" stop-opacity=".75"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
  <filter id="wisp" x="-50%" y="-50%" width="200%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.0035 0.009" numOctaves="2" seed="4" result="n">
      <animate attributeName="baseFrequency" values="0.0035 0.009;0.005 0.012;0.0035 0.009" dur="4s" repeatCount="indefinite"/>
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="110" xChannelSelector="R" yChannelSelector="G"/>
    <feGaussianBlur stdDeviation="11"/>
  </filter>
  <filter id="vap" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.004 0.011" numOctaves="2" seed="9" result="n">
      <animate attributeName="baseFrequency" values="0.004 0.011;0.006 0.015" dur="3s" fill="freeze"/>
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="140" xChannelSelector="R" yChannelSelector="G" result="d">
      <animate attributeName="scale" values="140;0" begin="1.35s" dur="1.75s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 .5 .25 1"/>
    </feDisplacementMap>
    <feGaussianBlur in="d" stdDeviation="8">
      <animate attributeName="stdDeviation" values="8;0" begin="1.35s" dur="1.6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 .5 .25 1"/>
    </feGaussianBlur>
  </filter>
  <filter id="ds" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#2A0E02" flood-opacity=".45"/></filter>
  <clipPath id="stc"><path d="{P_st}"/></clipPath>
</defs>
<rect x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#bg)"/>
<g id="pot" class="s" style="stroke-width:20">
  <path d="M430 1060 H824"/>
  <path d="M470 1075 V1140 Q470 1205 535 1205 H719 Q784 1205 784 1140 V1075"/>
  <path d="M470 1100 H420 M784 1100 H834"/>
</g>
<g id="wisps">{wisps}</g>
<g id="after">{after}</g>
<g transform="translate(627 600) scale(.84) translate(-627 -600)">
  <g id="lines">{ln}</g>
  <g id="logo">
    <g filter="url(#ds)"><path fill="#FFFDF8" d="{P_st}"/></g>
    <path fill="{BR}" fill-rule="evenodd" d="{P_ink}"/>
    <path fill="{OR}" fill-rule="evenodd" d="{P_or}"/>
    <g clip-path="url(#stc)"><rect id="shine" x="0" y="-100" width="200" height="1500" fill="url(#sh)"/></g>
  </g>
</g>
<g id="fork" class="s" style="stroke-width:13"><path d="M197 585 V470 M197 470 C168 466 163 440 163 412 V355 M197 470 C226 466 231 440 231 412 V355 M197 355 V412"/></g>
<g id="spoon" class="s" style="stroke-width:13"><path d="M1031 655 V505 M1031 505 C992 505 980 465 980 430 C980 385 1003 355 1031 355 C1059 355 1082 385 1082 430 C1082 465 1070 505 1031 505"/></g>
<circle id="ring" cx="627" cy="600" r="760" fill="none" stroke="{CR}"/>
</svg>
'''
open(OUT,'w').write(svg); print(len(svg)//1024,'KB',len(lines),'lines')
