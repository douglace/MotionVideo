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
def full(m):
    o=[]
    for c in curves(m):
        o.append("M"+f(c.start_point))
        for s in c.segments:
            o.append(("L"+f(s.c)+"L"+f(s.end_point)) if s.is_corner else ("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point)))
        o.append("Z")
    return "".join(o)
P_st=full(stf); P_ink=full(ink); P_or=full(orng)
CR='#FFF4E2'; BR='#351200'; OR='#FE8502'
EB='cubic-bezier(.34,1.56,.64,1)'   # easeOutBack
EO='cubic-bezier(.22,1,.36,1)'      # easeOutQuint
EIO='cubic-bezier(.65,0,.35,1)'
css=f'''
.s{{fill:none;stroke:{CR};stroke-width:22;stroke-linecap:round;stroke-linejoin:round}}
.dr{{stroke-dasharray:1 1;stroke-dashoffset:1}}
@keyframes on{{to{{stroke-dashoffset:0}}}}
@keyframes off{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1}}}}
@keyframes fo{{to{{opacity:0}}}}
@keyframes fi{{from{{opacity:0}}to{{opacity:1}}}}
/* 1. point qui rebondit */
#dotx{{animation:dotx .8s cubic-bezier(.3,.6,.4,1) both}}
@keyframes dotx{{from{{transform:translateX(-820px)}}to{{transform:none}}}}
#doty{{animation:doty .8s linear both}}
@keyframes doty{{0%{{transform:translateY(-420px);animation-timing-function:cubic-bezier(.55,0,1,.45)}}32%{{transform:translateY(0);animation-timing-function:cubic-bezier(0,.55,.45,1)}}52%{{transform:translateY(-170px);animation-timing-function:cubic-bezier(.55,0,1,.45)}}72%{{transform:translateY(0);animation-timing-function:cubic-bezier(0,.55,.45,1)}}84%{{transform:translateY(-55px);animation-timing-function:cubic-bezier(.55,0,1,.45)}}96%,100%{{transform:translateY(0)}}}}
#dot{{transform-box:fill-box;transform-origin:50% 100%;animation:squish .8s linear both, dotOut .2s .85s ease-in both}}
@keyframes squish{{0%,30%{{transform:none}}32%{{transform:scale(1.4,.7)}}38%{{transform:none}}70%{{transform:none}}72%{{transform:scale(1.3,.75)}}78%,94%{{transform:none}}96%{{transform:scale(1.2,.85)}}100%{{transform:none}}}}
@keyframes dotOut{{to{{transform:scale(2.2);opacity:0}}}}
/* 2. assiette + couverts */
#plate{{transform-origin:627px 600px;animation:platePop .5s .85s {EB} both, plateSquash .35s 1.5s {EIO} both, fo .15s 1.78s linear both}}
@keyframes platePop{{from{{transform:scale(.4)}}to{{transform:none}}}}
@keyframes plateSquash{{from{{transform:none}}to{{transform:translateY(120px) scaleY(.06)}}}}
#p1{{animation:on .45s .85s {EO} both}} #p2{{animation:on .45s .97s {EO} both}}
#fork .dr,#spoon .dr{{animation:on .45s 1.05s {EO} both}}
#fork{{animation:forkOut .45s 3.6s {EIO} both}} #spoon{{animation:spoonOut .45s 3.6s {EIO} both}}
@keyframes forkOut{{to{{transform:translateX(-230px);opacity:0}}}}
@keyframes spoonOut{{to{{transform:translateX(230px);opacity:0}}}}
/* 3. cloche */
#base{{animation:on .3s 1.62s {EO} both, off .3s 2.95s {EIO} forwards}}
#dome{{animation:on .5s 1.7s {EO} both, off .4s 2.95s {EIO} forwards}}
#knob{{transform-box:fill-box;transform-origin:50% 100%;animation:knob .35s 2.1s {EB} both, knobOut .25s 2.95s ease-in forwards}}
@keyframes knob{{from{{transform:scale(0)}}to{{transform:none}}}}
@keyframes knobOut{{to{{transform:scale(0)}}}}
#lid{{transform-origin:860px 700px;animation:lift .45s 2.35s {EB} both}}
@keyframes lift{{from{{transform:none}}to{{transform:translateY(-270px) rotate(-14deg)}}}}
.st{{animation:on .5s {EO} both, fo .3s 3.0s ease both}}
#steam{{animation:rise 1s 2.5s ease-out both}}
@keyframes rise{{from{{transform:translateY(30px)}}to{{transform:translateY(-30px)}}}}
/* 4. toque */
#toque{{transform-origin:627px 560px;animation:tq .55s 3.62s {EIO} both}}
@keyframes tq{{0%{{transform:none;opacity:1}}100%{{transform:translateY(-200px) scale(1.65);opacity:0}}}}
.tq{{animation:on .55s 3.0s {EO} both}}
/* 5. logo */
#logo{{transform-origin:627px 600px;animation:logo .65s 3.68s {EB} both}}
@keyframes logo{{0%{{transform:scale(.35);opacity:0}}25%{{opacity:1}}100%{{transform:none;opacity:1}}}}
#ring{{transform-box:fill-box;transform-origin:50% 50%;opacity:0;animation:ring .8s 3.7s {EO} both}}
@keyframes ring{{0%{{opacity:0;transform:scale(.2);stroke-width:40}}5%{{opacity:1}}100%{{opacity:0;transform:scale(1);stroke-width:2}}}}
#shine{{animation:shine 1s 4.45s cubic-bezier(.45,0,.25,1) both}}
@keyframes shine{{0%{{transform:translateX(-500px) skewX(-22deg)}}100%{{transform:translateX(1700px) skewX(-22deg)}}}}
.tw{{transform-box:fill-box;transform-origin:50% 50%;animation:tw 1s ease both}}
@keyframes tw{{0%{{transform:scale(0) rotate(0);opacity:1}}50%{{transform:scale(1) rotate(45deg);opacity:1}}100%{{transform:scale(0) rotate(90deg);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}#stage{{display:none}}}}
'''
star=lambda x,y,s,dl: f'<path class="tw" fill="{CR}" style="animation-delay:{dl}s" d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z"/>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
<title>Les Délices de Kevinne – intro transformation</title>
<style>{css}</style>
<defs>
  <radialGradient id="bg" cx="627" cy="600" r="1500" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF9C24"/><stop offset=".5" stop-color="#F57F05"/><stop offset="1" stop-color="#C95A00"/></radialGradient>
  <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF" stop-opacity=".75"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
  <filter id="ds" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#5A2600" flood-opacity=".35"/></filter>
  <clipPath id="stc"><path d="{P_st}"/></clipPath>
</defs>
<rect x="-3000" y="-3000" width="{W+6000}" height="{H+6000}" fill="url(#bg)"/>
<g id="stage">
  <g id="plate">
    <circle id="p1" class="s dr" pathLength="1" cx="627" cy="600" r="225" transform="rotate(-90 627 600)"/>
    <circle id="p2" class="s dr" pathLength="1" cx="627" cy="600" r="150" transform="rotate(-90 627 600)" style="stroke-width:14"/>
  </g>
  <g id="fork"><path class="s dr" pathLength="1" d="M300 830 V655 M300 655 C262 650 258 620 258 585 V500 M300 655 C338 650 342 620 342 585 V500 M300 500 V585"/></g>
  <g id="spoon"><path class="s dr" pathLength="1" d="M954 830 V640 M954 640 C912 640 900 590 900 545 C900 495 925 470 954 470 C983 470 1008 495 1008 545 C1008 590 996 640 954 640"/></g>
  <path id="base" class="s dr" pathLength="1" d="M380 720 H874"/>
  <g id="lid">
    <path id="dome" class="s dr" pathLength="1" d="M412 705 A215 215 0 0 1 842 705"/>
    <g id="knob"><circle cx="627" cy="465" r="24" fill="{CR}"/><rect x="619" y="468" width="16" height="26" fill="{CR}"/></g>
  </g>
  <g id="steam">
    <path class="s dr st" pathLength="1" style="animation-delay:2.5s,3.0s;stroke-width:16" d="M560 700 C530 660 590 640 560 600 S590 540 562 505"/>
    <path class="s dr st" pathLength="1" style="animation-delay:2.58s,3.0s;stroke-width:16" d="M627 690 C597 650 657 630 627 590 S657 530 629 490"/>
    <path class="s dr st" pathLength="1" style="animation-delay:2.66s,3.0s;stroke-width:16" d="M694 700 C664 660 724 640 694 600 S724 540 696 505"/>
  </g>
  <g id="toque">
    <path class="s dr tq" pathLength="1" d="M497 640 C392 640 380 485 482 468 C478 362 610 330 627 410 C644 330 776 362 772 468 C874 485 862 640 757 640"/>
    <path class="s dr tq" pathLength="1" style="animation-delay:3.12s" d="M497 640 V735 H757 V640"/>
    <path class="s dr tq" pathLength="1" style="animation-delay:3.25s;stroke-width:14" d="M545 690 H709"/>
  </g>
</g>
<circle id="ring" cx="627" cy="600" r="760" fill="none" stroke="{CR}"/>
<g transform="translate(627 600) scale(.84) translate(-627 -600)"><g id="logo">
  <g filter="url(#ds)"><path fill="#FFFDF8" d="{P_st}"/></g>
  <path fill="{BR}" fill-rule="evenodd" d="{P_ink}"/>
  <path fill="{OR}" fill-rule="evenodd" d="{P_or}"/>
  <g clip-path="url(#stc)"><rect id="shine" x="0" y="-100" width="200" height="1500" fill="url(#sh)"/></g>
</g></g>
{star(1185,330,30,4.6)}{star(95,800,22,4.8)}{star(1120,1010,24,5.0)}{star(170,180,18,5.15)}
<g id="dotx"><g id="doty"><circle id="dot" cx="627" cy="566" r="34" fill="{CR}"/></g></g>
</svg>
'''
open(OUT,'w').write(svg); print(len(svg)//1024,'KB')
