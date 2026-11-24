import sys, subprocess, numpy as np, wave
D1, OUT = sys.argv[1:3]
SR=48000; N=int(2.5*SR)
def load(p):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout,np.float32).reshape(-1,2).astype(float)
    return x/np.abs(x).max()
mix=np.zeros((N,2))
def place(x,at,anchor=0,db=0,cut=None):
    x=x.copy()
    if cut: x=x[:int(cut*SR)]; k=int(.05*SR); x[-k:]*=np.linspace(1,0,k)[:,None]
    i=int((at-anchor)*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s); mix[i:j]+=x[s:s+j-i]*10**(db/20)
w=load(f'{D1}/whoosh4.mp3'); w[:,0]*=np.linspace(1.3,.7,len(w)); w[:,1]*=np.linspace(.7,1.3,len(w))  # le souffle passe de gauche à droite
place(w,0.13,0.269,-3,cut=0.6)                     # entrée en trombe
place(load(f'{D1}/pop4.mp3'),0.41,0.001,-5)        # freinage
place(load(f'{D1}/chime4.mp3'),0.80,0.172,-10)     # reflet + étincelles
mix=np.tanh(mix*1.1)/np.tanh(1.1)
k=int(.4*SR); mix[-k:]*=np.linspace(1,0,k)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((mix*32767).astype('<i2').tobytes())
e=np.abs(mix).max(1); b=int(.1*SR)
print(' '.join(f"{i*.1:.1f}:{20*np.log10(e[i*b:(i+1)*b].max()+1e-9):.0f}" for i in range(N//b)))
