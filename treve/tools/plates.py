import numpy as np, json, cv2, subprocess, sys
F=sys.argv[1]
shots=json.load(open('src/shots.json'))
W,H=1080,1920
cap=cv2.VideoCapture(F)
def load(fl):
    d={}
    for f in fl:
        cap.set(cv2.CAP_PROP_POS_FRAMES,f); ok,fr=cap.read()
        if ok: d[f]=fr
    return d
def textmask(fr,img):
    m=np.zeros((H,W),np.uint8)
    b=fr[1080:1360].astype(np.int16)  # BGR
    white=(b.min(axis=2)>185)&((b.max(axis=2)-b.min(axis=2))<45)
    gold=(b[...,2]>190)&(b[...,1]>140)&(b[...,2]-b[...,0]>45)
    t=(white|gold).astype(np.uint8)
    t=cv2.dilate(t,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
    t=cv2.dilate(t,np.ones((1,1),np.uint8))
    # drop isolated background highlights (candles etc.): keep only within caption rows
    rows=np.nonzero(t.sum(axis=1)>40)[0]
    m[1080:1360]=t
    m[150:235,0:640]=1      # header
    if img==6: m[1380:1500,280:800]=1
    return m
crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,80,1e-5)
for img in [int(x) for x in sys.argv[2].split(",")]:
    cand=[]
    for sh in shots:
        if sh['img']!=img: continue
        L=sh['e']-sh['s']; k=max(2,min(60 if L<150 else 10,L//2))
        cand+= [int(sh['s']+3+(L-6)*j/(k-1)) for j in range(k)]
    frames=load(sorted(cand)); fl=sorted(frames)
    ref=frames[fl[0]]
    small=lambda x: cv2.resize(cv2.cvtColor(x,cv2.COLOR_BGR2GRAY),(270,480)).astype(np.float32)
    rs=small(ref); emask=np.ones((480,270),np.uint8); emask[265:345]=0; emask[35:60]=0
    warps={}
    for f in fl:
        M=np.eye(2,3,dtype=np.float32)
        try:
            _,M=cv2.findTransformECC(rs,small(frames[f]),M,cv2.MOTION_AFFINE,crit,emask,5)
        except cv2.error: continue
        M[:,2]*=4; warps[f]=M   # maps ref coords -> frame coords
    # choose widest frame as ref: scale<1 means frame shows more? M maps ref->frame: frame zoomed out => scale<1
    sc={f:np.sqrt(abs(np.linalg.det(M[:,:2]))) for f,M in warps.items()}
    stack=[];valid=[]
    for f,M in warps.items():
        fr=frames[f]; tm=textmask(fr,img)
        wf=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT)
        v=cv2.warpAffine((1-tm)*255,M,(W,H),flags=cv2.INTER_NEAREST|cv2.WARP_INVERSE_MAP,borderValue=0)
        v=cv2.erode(v,np.ones((5,5),np.uint8))
        stack.append(wf); valid.append(v>0)
    med=ref.copy(); hole=np.zeros((H,W),np.uint8)
    rm=textmask(ref,img)
    for (y0,y1) in [(140,250),(1060,1520)]:
        S=np.stack([x[y0:y1] for x in stack]).astype(np.float32); V=np.stack([v[y0:y1] for v in valid])
        S[~V]=np.nan
        with np.errstate(all='ignore'): m=np.nanmedian(S,axis=0)
        need=rm[y0:y1]>0
        h=np.isnan(m[...,0])&need
        blk=med[y0:y1]; mm=np.nan_to_num(m).astype(np.uint8)
        blk[need&~h]=mm[need&~h]; hole[y0:y1]=h
        del S,V
    out=cv2.inpaint(med,hole,9,cv2.INPAINT_TELEA) if hole.any() else med
    cv2.imwrite(f'src/plate_{img}.png',out)
    stack=valid=frames=None
    print(img,len(fl),'frames','scale range',round(min(sc.values()),3),round(max(sc.values()),3),'holes',int(hole.sum()))
