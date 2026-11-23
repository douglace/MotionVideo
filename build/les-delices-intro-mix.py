import sys, subprocess, numpy as np, wave
D, OUT = sys.argv[1], sys.argv[2]
SR=48000; N=int(5.5*SR)
def load(n):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f'{D}/{n}.mp3','-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,np.float32).reshape(-1,2).astype(float); return x/np.abs(x).max()
mix=np.zeros((N,2))
def place(n,anchor_t,anchor_in,db,fade_out=None):
    x=load(n)
    if fade_out:  # coupe propre de la queue
        k=int(fade_out*SR); x=x[:k].copy(); f=int(.08*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
    i=int((anchor_t-anchor_in)*SR); s=max(0,-i); i=max(0,i); j=min(N,i+len(x)-s)
    mix[i:j]+=x[s:s+j-i]*10**(db/20)
place('drop4', 0.575, 0.265, -6)              # le point touche le sol (+ petit boing)
place('pop2',  0.86,  0.007, -9)              # éclatement du point
place('whoosh2',1.45, 0.535, -13, 1.2)        # tourbillon qui monte jusqu'au pop
place('pop4',  1.76,  0.001,  0)              # grand pop de révélation
place('chime4',2.45,  0.172, -7)              # carillon qui monte sur le reflet
# limiteur doux + normalisation à -1 dBFS
mix=np.tanh(mix*1.2)/np.tanh(1.2)
f=int(.4*SR); mix[-f:]*=np.linspace(1,0,f)[:,None]
mix*=10**(-1/20)/np.abs(mix).max()
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
env=np.abs(mix).max(1); blk=int(.05*SR)
print(' '.join(f"{i*.05:.2f}:{20*np.log10(env[i*blk:(i+1)*blk].max()+1e-9):.0f}" for i in range(N//blk) if env[i*blk:(i+1)*blk].max()>0.03))
