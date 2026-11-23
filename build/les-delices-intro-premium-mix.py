import sys, subprocess, numpy as np, wave
D2, D1, OUT = sys.argv[1:4]
SR=48000; DUR=6.5; N=int(DUR*SR)
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,np.float32).reshape(-1,2).astype(float); return x/np.abs(x).max()
mix=np.zeros((N,2))
def place(x,t0,db):
    i=int(t0*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s); mix[i:j]+=x[s:s+j-i]*10**(db/20)
REV=2.9
# 1) scintillement pendant le tracé doré
r=load(f'{D2}/riser1.mp3'); place(r,0.3,-9)
# 2) traîne d'impact inversée qui aspire vers la révélation
h=load(f'{D2}/hit4.mp3')[:int(1.6*SR)][::-1].copy()
env=np.linspace(0,1,len(h))**2.2; h*=env[:,None]
place(h,REV-len(h)/SR,-8)
# 3) impact de révélation (boom grave + cristal)
place(load(f'{D2}/hit1.mp3'),REV-0.005,0)
# 4) petit scintillement sur le reflet
place(load(f'{D1}/chime4.mp3'),4.0-0.172,-15)
mix=np.tanh(mix*1.1)/np.tanh(1.1)
f=int(.6*SR); mix[-f:]*=np.linspace(1,0,f)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
e=np.abs(mix).max(1); b=int(.1*SR)
print(' '.join(f"{i*.1:.1f}:{20*np.log10(e[i*b:(i+1)*b].max()+1e-9):.0f}" for i in range(N//b)))
