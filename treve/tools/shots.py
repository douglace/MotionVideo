import numpy as np, json
W,H=540,960
a=np.fromfile('src/small.rgb',np.uint8).reshape(-1,H,W,3)
n=len(a)
mask=np.ones((H,W),bool); mask[540:700]=False
d=np.array([np.abs(a[i].astype(np.int16)-a[i-1])[mask].mean() for i in range(1,n)])
cuts=[0]+[i for i in range(1,n) if d[i-1]>12]
m=[]
for c in cuts:
    if m and c-m[-1]<5: continue
    m.append(c)
bounds=list(zip(m,m[1:]+[n]))
# thumbnails (top region only, to avoid captions)
th=[a[(s+e)//2,80:520:8,::8].astype(float).ravel() for s,e in bounds]
ids=[];reps=[]
for t in th:
    found=None
    for k,r in enumerate(reps):
        if np.corrcoef(t,r)[0,1]>0.6: found=k;break
    if found is None: reps.append(t); found=len(reps)-1
    ids.append(found)
shots=[dict(s=s,e=e,img=i) for (s,e),i in zip(bounds,ids)]
json.dump(shots,open('src/shots.json','w'))
for x in shots: print(x['img'], round(x['s']/30,2), round(x['e']/30,2))
