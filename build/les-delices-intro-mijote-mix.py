import sys, subprocess, numpy as np, wave
D1, D3, D4, OUT = sys.argv[1:5]
SR=48000; N=int(6.5*SR)
def load(p,dur=None):
    cmd=['ffmpeg','-v','error']+(['-t',str(dur)] if dur else [])+['-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-']
    x=np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,np.float32).reshape(-1,2).astype(float)
    return x/np.abs(x).max()
def rmsnorm(x,db): return x/np.sqrt((x**2).mean())*10**(db/20)
mix=np.zeros((N,2))
def place(x,at,anchor=0,db=0,cut=None,fin=0.0,fout=0.06):
    x=x.copy()
    if cut: x=x[:int(cut*SR)]
    if fin: k=int(fin*SR); x[:k]*=np.linspace(0,1,k)[:,None]
    if fout: k=int(fout*SR); x[-k:]*=np.linspace(1,0,k)[:,None]
    i=int((at-anchor)*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s); mix[i:j]+=x[s:s+j-i]*10**(db/20)
# mijotage continu (marmite) : de l'arrivée de la marmite jusqu'à sa sortie, puis il s'éteint doucement
sim=rmsnorm(load(f'{D4}/sim1.mp3',8)[int(.3*SR):],-27)
place(sim,0.05,0,0,cut=4.6,fin=0.35,fout=1.1)
# la vapeur qui monte puis se condense en lettres
place(rmsnorm(load(f'{D4}/hiss1.mp3'),-27),0.55,0,0,fin=0.3,fout=0.5)
# couverts qui se posent
tink=load(f'{D3}/bell3.mp3')
place(tink,3.05,0,-17,cut=0.45); place(tink,3.15,0,-19,cut=0.45)
# révélation du logo : pop + « ding ! »
place(load(f'{D1}/pop4.mp3'),3.2,0.001,-2)
place(load(f'{D3}/bell1.mp3'),3.22,0,-4)
# reflet
place(load(f'{D1}/chime4.mp3'),4.0,0.172,-15)
mix=np.tanh(mix*1.1)/np.tanh(1.1)
k=int(.5*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
e=np.abs(mix).max(1); b=int(.25*SR)
print(' '.join(f"{i*.25:.2f}:{20*np.log10(e[i*b:(i+1)*b].max()+1e-9):.0f}" for i in range(N//b)))
