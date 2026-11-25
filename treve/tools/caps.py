import numpy as np
from PIL import Image, ImageDraw
W,H=540,960
a=np.fromfile('src/small.rgb',np.uint8).reshape(-1,H,W,3)
band=a[:,580:635,60:480].astype(np.int16)
# text pixels: bright
txt=(band.min(axis=3)>200)|((band[...,0]>215)&(band[...,1]>160)&(band[...,2]<170))
d=np.array([np.logical_xor(txt[i],txt[i-1]).sum() for i in range(1,len(a))])
ev=[0]+[i for i in range(1,len(a)) if d[i-1]>60]
# merge events closer than 3 frames
m=[]
for e in ev:
    if m and e-m[-1]<3: m[-1]=e
    else: m.append(e)
print(len(m))
open('src/events.txt','w').write('\n'.join(map(str,m)))
crops=[Image.fromarray(a[min(e+2,len(a)-1),570:645,40:500]) for e in m]
per=40
for p in range(0,len(crops),per):
    sheet=Image.new('RGB',(2*470,(per//2)*80),'black'); dr=ImageDraw.Draw(sheet)
    for k,c in enumerate(crops[p:p+per]):
        x=(k%2)*470; y=(k//2)*80
        sheet.paste(c,(x,y)); dr.text((x+2,y+2),str(p+k),fill='red')
    sheet.save(f'src/caps_{p//per}.png')
