import sys, subprocess, numpy as np, wave
D1, D3, OUT = sys.argv[1:4]
SR=48000; N=int(6.5*SR)
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,np.float32).reshape(-1,2).astype(float); return x/np.abs(x).max()
mix=np.zeros((N,2))
def place(x,at,anchor,db,cut=None):
    if cut: k=int(cut*SR); x=x[:k].copy(); fl=int(.06*SR); x[-fl:]*=np.linspace(1,0,fl)[:,None]
    i=int((at-anchor)*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s); mix[i:j]+=x[s:s+j-i]*10**(db/20)
drop=load(f'{D1}/drop4.mp3'); pop2=load(f'{D1}/pop2.mp3'); pop4=load(f'{D1}/pop4.mp3')
place(drop,0.256,0.265,-6,0.9)     # 1er rebond du point
place(drop,0.576,0.265,-12,0.9)    # 2e rebond
place(pop2,0.77,0.007,-17)         # petit 3e rebond
place(pop2,0.86,0.007,-7)          # le point s'ouvre en assiette
place(pop2,2.12,0.007,-13)         # le bouton de la cloche apparaît
place(load(f'{D3}/bell3.mp3'),1.12,0.0,-20,0.5)      # tintement léger des couverts
place(load(f'{D1}/whoosh2.mp3'),1.68,0.535,-15,1.0)  # assiette -> cloche
place(load(f'{D3}/lid4.mp3'),2.42,0.74,-4)          # couvercle soulevé
place(load(f'{D1}/whoosh2.mp3'),3.25,0.535,-12,1.1) # cloche -> toque
place(pop4,3.70,0.001,0)                            # pop du logo
place(load(f'{D3}/bell1.mp3'),3.76,0.0,-5)          # « ding ! » c'est servi
place(load(f'{D1}/chime4.mp3'),4.6,0.172,-14)       # étincelles
mix=np.tanh(mix*1.1)/np.tanh(1.1)
fl=int(.5*SR); mix[-fl:]*=np.linspace(1,0,fl)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
e=np.abs(mix).max(1); b=int(.1*SR)
print(' '.join(f"{i*.1:.1f}:{20*np.log10(e[i*b:(i+1)*b].max()+1e-9):.0f}" for i in range(N//b)))
