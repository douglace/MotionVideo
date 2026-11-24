import sys, subprocess, numpy as np, wave
D1, D5, OUT = sys.argv[1:4]
SR=48000; N=int(5.0*SR)
def load(p):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout,np.float32).reshape(-1,2).astype(float)
    return x/np.abs(x).max()
mix=np.zeros((N,2))
def place(x,at,anchor=0,db=0,cut=None,pan=0.0):
    x=x.copy()
    if cut: x=x[:int(cut*SR)]; k=int(.05*SR); x[-k:]*=np.linspace(1,0,k)[:,None]
    x[:,0]*=np.sqrt(1-pan); x[:,1]*=np.sqrt(1+pan)
    i=int((at-anchor)*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s); mix[i:j]+=x[s:s+j-i]*10**(db/20)
drops={k:(load(f'{D1}/drop{k}.mp3'),a) for k,a in [(1,.232),(2,.592),(3,.303),(4,.265)]}
pop2=load(f'{D1}/pop2.mp3')
# ingrédients : (retard de chute, prise, niveau, panoramique gauche/droite selon sa position)
items=[(0.00,4,-7,-.6),(0.12,1,-8,.4),(0.24,3,-8,-.15),(0.36,2,-9,.65),(0.48,4,-9,-.4)]
for dl,k,db,pan in items:
    x,a=drops[k]
    place(x,dl+0.504,a,db,cut=a+0.45,pan=pan)          # atterrissage
    place(pop2,dl+0.861,0.007,db-12,pan=pan)           # petit 2e rebond
for dl,pan in [(0.55,.1),(0.62,.2),(0.68,0.0)]:          # grains de poivre
    place(pop2,dl+0.504,0.007,-15,pan=pan)
place(load(f'{D1}/whoosh2.mp3'),1.78,0.535,-11,cut=1.0) # aspiration en tourbillon
place(load(f'{D5}/poof2.mp3'),1.95,0.13,0)              # « pouf ! »
place(load(f'{D1}/pop4.mp3'),2.05,0.001,-8)             # le logo surgit
place(load(f'{D1}/chime4.mp3'),2.95,0.172,-14)          # reflet
mix=np.tanh(mix*1.1)/np.tanh(1.1)
k=int(.4*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
e=np.abs(mix).max(1); b=int(.1*SR)
print(' '.join(f"{i*.1:.1f}:{20*np.log10(e[i*b:(i+1)*b].max()+1e-9):.0f}" for i in range(N//b)))
