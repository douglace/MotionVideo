import json, re
lines=[l for l in open('script.txt').read().split('\n') if l]
chunks=[]; sent=[]
for si,l in enumerate(lines):
    for c in l.split('|'): chunks.append(c); sent.append(si)
ev=[int(x) for x in open('src/events.txt').read().split()]
# chunk index shown at each event (read from caption crop sheets)
seq=[0,0,1,2,3,4,5,5,6,7,7,8,9,10,10,11,12,12,13,13,14,14,15,15,16,17,17,18,19,19,20,21,22,23,24,25,25,26,26,27,
     27,28,29,30,31,31,32,32,33,33,34,35,36,36,37,37,38,39,39,40,41,41,42,42,43,44,44,45,45,46,47,47,48,49,50,51,51,52,52,53,
     54,55,55,56,56,57,57,58,58,59,60,61,62,63,64,65,66,67,67,68,68,69,70,70,71,71,72,72,73,73,74,74,75,76,77,77,78,78,79,80,
     80,81,82,83,83,84,85,85,86,87,88,89,89,90,90,91,91,92,92,93,93,94,95,96,96]
assert len(seq)==len(ev),(len(seq),len(ev))
assert len(chunks)==97, len(chunks)
assert max(seq)==96
cs={}; second={}
for e,c in zip(ev,seq):
    t=e/30
    if c not in cs: cs[c]=t
    elif c not in second and t-cs[c]>0.12: second[c]=t
END=68.23
words=[]; out=[]
for k,c in enumerate(chunks):
    t0=cs[k]; t1=cs[k+1] if k+1<len(chunks) else END
    ws=c.split()
    if len(ws)==1: ts=[t0]
    else:
        t2=second.get(k)
        if t2 is None or not (t0<t2<t1): t2=t0+(t1-t0)*len(ws[0])/(len(ws[0])+len(ws[1]))
        ts=[t0,t2]
    for w,t in zip(ws,ts): words.append(dict(w=w,t=round(t,3),chunk=k,sent=sent[k]))
    out.append(dict(text=c,t=round(t0,3),end=round(t1,3),sent=sent[k]))
json.dump(dict(duration=69.5,chunks=out,words=words),open('src/timing.json','w'),ensure_ascii=False,indent=1)
for s in range(len(lines)):
    cc=[o for o in out if o['sent']==s]; print(f"{cc[0]['t']:6.2f}-{cc[-1]['end']:6.2f}  {lines[s].replace('|',' ')}")
