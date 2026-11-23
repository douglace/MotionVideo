import sys, numpy as np, wave
SR=48000; DUR=5.5; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def place(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(sig)); s=sig[:j-i]*gain
    L[i:j]+=s*np.sqrt((1-pan)/2); R[i:j]+=s*np.sqrt((1+pan)/2)
def pop(f0=900,f1=180,dur=.12,dec=.045,click=.25):
    t=np.arange(int(dur*SR))/SR
    f=f1+(f0-f1)*np.exp(-t/0.018)
    ph=2*np.pi*np.cumsum(f)/SR
    env=(1-np.exp(-t/0.0015))*np.exp(-t/dec)
    nz=rng.standard_normal(len(t))*np.exp(-t/0.004)*click
    return np.sin(ph)*env+nz
def bell(f,dur=2.2,dec=.9):
    t=np.arange(int(dur*SR))/SR
    parts=[(1,1,1),(2.0,.35,.6),(2.76,.25,.45),(5.4,.12,.25),(8.93,.05,.15)]
    s=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t/(dec*d)) for r,a,d in parts)
    return s*(1-np.exp(-t/0.002))
def whoosh(dur=.8):
    n=int(dur*SR); x=rng.standard_normal(n); t=np.arange(n)/SR
    # bande passante qui monte : filtre passe-bas variable simple
    y=np.zeros(n); a=0
    for k in range(n):
        c=0.02+0.25*(t[k]/dur); a+=c*(x[k]-a); y[k]=a
    env=np.sin(np.pi*t/dur)**2
    return y*env
place(pop(700,220,.1,.03,.15),0.575,0.35)        # point qui touche le sol
place(pop(1100,250,.14,.05,.3),0.86,0.55)        # éclatement
place(whoosh(.85),0.85,0.25)                     # tourbillon des traits
place(pop(800,140,.18,.07,.35),1.76,0.95)        # grand pop de révélation
for k,(f,t,p) in enumerate([(1046.5,2.45,-.3),(1318.5,2.58,-.1),(1568,2.71,.1),(2093,2.86,.3)]):
    place(bell(f),t,0.15 if k<3 else 0.13,p)     # carillon do-mi-sol-do
# petite réverb (lignes de retard)
def verb(x):
    y=x.copy()
    for d,g in ((0.029,.32),(0.037,.28),(0.051,.22),(0.071,.18),(0.097,.12)):
        k=int(d*SR); z=np.zeros_like(x); z[k:]=x[:-k]
        for _ in range(3): y+=z*g; z=np.concatenate([np.zeros(k),z[:-k]])*g
    return y
L2=L*.8+verb(L)*.2; R2=R*.8+verb(R)*.2
fade=np.ones(N); fl=int(.4*SR); fade[-fl:]=np.linspace(1,0,fl)
st=np.stack([L2,R2],1)*fade[:,None]
st/=np.abs(st).max(); st*=10**(-1.5/20)
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype('<i2').tobytes())
# rapport : niveau par tranche de 50 ms
env=np.abs(st).max(1); blk=int(.05*SR)
lv=[env[i:i+blk].max() for i in range(0,N,blk)]
print(' '.join(f"{i*0.05:.2f}:{20*np.log10(v+1e-9):.0f}" for i,v in enumerate(lv) if v>0.05))
