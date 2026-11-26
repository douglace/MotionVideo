// Couverture Shorts — Berlin 1989 (dessinée avec le moteur de l'épisode)
for (const s of ['#header','#progress','#caps','#annot']) { const e=document.querySelector(s); if(e) e.style.display='none'; }
const c=ctx; c.setTransform(1,0,0,1,0,0);
c.save();c.translate(540,1000);c.scale(1.05,1.05);c.translate(-560,-1060);
checkpoint(c,0,.62,.9);
for (const [x,i] of [[820,0],[900,1]]) soldier(c,{side:'x',outfit:'guard',x,y:1300,s:.9,f:-1,t:i,rifleBack:false});
const out=['citA','citB','citC','citD'];
for (let j=0;j<9;j++) soldier(c,{side:'x',outfit:out[j%4],x:-20+j*85,y:1340+(j%3)*22,s:.85,f:1,t:j,rifleBack:false,pose:mixPose(POSE.idle,POSE.up,j%2?1:.4),smile:1});
c.restore();
// mur en avant-plan, avec la brèche de lumière
wallH(c,-60,330,1920,330,{graffiti:1});wallH(c,750,1140,1920,330,{graffiti:1});
glow(c,540,1700,420,'rgba(255,214,140,A)',.45);
// le papier, fil rouge de l'épisode
paper(c,880,330,1.0,.12,1,{hl:1});
const g=c.createLinearGradient(0,0,0,820);g.addColorStop(0,'rgba(8,10,18,.85)');g.addColorStop(1,'rgba(8,10,18,0)');c.fillStyle=g;c.fillRect(0,0,1080,820);
const T=(s,x,y,font,col,ls='0px')=>{c.save();c.font=font;c.textAlign='center';c.textBaseline='middle';c.letterSpacing=ls;c.shadowColor='rgba(0,0,0,.7)';c.shadowBlur=26;c.shadowOffsetY=6;c.fillStyle=col;c.fillText(s,x,y);c.restore();};
label(c,400,250,'BERLIN · 9 NOV. 1989',{a:1,size:28,bg:'rgba(8,10,18,.6)'});
T('UN SEUL MOT',420,400,'800 84px Inter','#FFF6E6','1px');
T('A OUVERT LE MUR',540,505,'800 84px Inter','#FFF6E6','1px');
T('« IMMÉDIATEMENT »',540,640,'italic 700 104px Cormorant','#F2C46B');
