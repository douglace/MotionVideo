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
# autocollant : contour décalé de ~18 px autour de tout le logo
d=ndi.distance_transform_edt(~(lab0>0)); st=ndi.binary_fill_holes(d<18)
stf=ndi.gaussian_filter(np.kron(st.astype(float),np.ones((S,S))),S*2)>0.5
def curves(m): return potrace.Bitmap(~m).trace(turdsize=20,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.2)
f=lambda p:f"{p.x/S:.1f} {p.y/S:.1f}"
def cd(c):
    o=["M"+f(c.start_point)]; xs=[c.start_point.x]
    for s in c.segments:
        if s.is_corner: o.append("L"+f(s.c)+"L"+f(s.end_point))
        else: o.append("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point))
        xs.append(s.end_point.x)
    o.append("Z"); return "".join(o), sum(xs)/len(xs)/S
full=lambda m:"".join(cd(c)[0] for c in curves(m))
P_st=full(stf); P_ink=full(ink); P_or=full(orng)
lines=[]
for m in (ink,orng):
    for c in curves(m):
        dd,cx=cd(c); lines.append((dd,0.55+1.1*(cx/W)))
GOLD='#F3C56E'; BR='#351200'; OR='#FE8502'
rng=np.random.default_rng(3)
parts=[]
for k in range(70):
    x=rng.uniform(-350,W+350); y=rng.uniform(-500,H+500); r=rng.choice([2.4,3.4,4.8,7.5],p=[.4,.3,.2,.1])
    dy=rng.uniform(60,170); dur=rng.uniform(4,8); dl=-rng.uniform(0,dur); op=rng.uniform(.35,.95)
    parts.append(f'<circle class="pt" cx="{x:.0f}" cy="{y:.0f}" r="{r}" style="--dy:-{dy:.0f}px;--o:{op:.2f};animation-duration:{dur:.1f}s,1.2s;animation-delay:{dl:.1f}s,{rng.uniform(0,.8):.1f}s"/>')
E='cubic-bezier(.65,0,.35,1)'
css=f'''
.pt{{fill:{GOLD};opacity:0;animation-name:float,ptIn;animation-timing-function:linear,ease;animation-iteration-count:infinite,1;animation-fill-mode:none,both}}
@keyframes float{{0%{{transform:translateY(0)}}100%{{transform:translateY(var(--dy))}}}}
@keyframes ptIn{{from{{opacity:0}}to{{opacity:var(--o)}}}}
#dust{{filter:url(#soft)}}
.ln{{fill:none;stroke:{GOLD};stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 1;stroke-dashoffset:1;animation:draw 1.7s {E} both}}
#border{{fill:none;stroke:{GOLD};stroke-width:5;stroke-dasharray:1 1;stroke-dashoffset:1;animation:draw 2.4s .35s {E} both}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
#lines{{filter:url(#glow);animation:out .7s 3.3s ease both}}
@keyframes out{{to{{opacity:0}}}}
#halo{{opacity:0;transform-origin:627px 600px;animation:halo 1.4s 2.85s ease-out both, breathe 4s 4.25s ease-in-out infinite alternate}}
@keyframes halo{{0%{{opacity:0;transform:scale(.6)}}35%{{opacity:.75}}100%{{opacity:.38;transform:scale(1)}}}}
@keyframes breathe{{from{{opacity:.38}}to{{opacity:.22}}}}
#logo{{transform-origin:627px 600px;animation:logoIn 1s 2.9s cubic-bezier(.22,1,.36,1) both}}
@keyframes logoIn{{0%{{opacity:0;transform:scale(1.05)}}100%{{opacity:1;transform:none}}}}
#flash{{opacity:0;animation:flash .9s 2.9s ease-out both}}
@keyframes flash{{0%{{opacity:0}}15%{{opacity:.55}}100%{{opacity:0}}}}
#shine{{animation:shine 1.2s 4.0s cubic-bezier(.45,0,.25,1) both}}
@keyframes shine{{0%{{transform:translateX(-500px) skewX(-22deg)}}100%{{transform:translateX(1700px) skewX(-22deg)}}}}
#border2{{opacity:0;animation:fadein .6s 3.1s ease both}}
@keyframes fadein{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}#lines,#flash{{display:none}}#logo,#halo,#border2{{opacity:1}}}}
'''
ln="\n".join(f'<path class="ln" pathLength="1" style="animation-delay:{dl:.2f}s" d="{p}"/>' for p,dl in lines)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<title>Les Délices de Kevinne – intro premium</title>
<style>{css}</style>
<defs>
  <radialGradient id="bg" cx="627" cy="600" r="1700" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3B1C0C"/><stop offset=".45" stop-color="#220E05"/><stop offset="1" stop-color="#0C0401"/></radialGradient>
  <radialGradient id="hg" cx="627" cy="600" r="820" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFB347" stop-opacity=".75"/><stop offset=".45" stop-color="#E07A10" stop-opacity=".35"/><stop offset="1" stop-color="#E07A10" stop-opacity="0"/></radialGradient>
  <radialGradient id="fg" cx="627" cy="600" r="900" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFF1CF"/><stop offset="1" stop-color="#FFF1CF" stop-opacity="0"/></radialGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#FFF6DE" stop-opacity="0"/><stop offset=".5" stop-color="#FFF6DE" stop-opacity=".8"/><stop offset="1" stop-color="#FFF6DE" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="1.2"/></filter>
  <clipPath id="stc"><path d="{P_st}"/></clipPath>
</defs>
<rect x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#bg)"/>
<g id="dust">{"".join(parts)}</g>
<rect id="halo" x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#hg)"/>
<g id="lines">
<path id="border" pathLength="1" d="{P_st}"/>
{ln}
</g>
<g id="logo">
  <path fill="#FFFDF8" d="{P_st}"/>
  <path fill="{BR}" fill-rule="evenodd" d="{P_ink}"/>
  <path fill="{OR}" fill-rule="evenodd" d="{P_or}"/>
  <g clip-path="url(#stc)"><rect id="shine" x="0" y="-100" width="220" height="1500" fill="url(#sh)"/></g>
  <path id="border2" fill="none" stroke="{GOLD}" stroke-width="5" d="{P_st}"/>
</g>
<rect id="flash" x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#fg)"/>
</svg>
'''
open(OUT,'w').write(svg); print(len(svg)//1024,'KB',len(lines),'lines')
