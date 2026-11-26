// Couverture Shorts — Mansa Moussa (dessinée avec le moteur de l'épisode)
for (const s of ['#header','#progress','#caps','#annot']) { const e=document.querySelector(s); if(e) e.style.display='none'; }
const c=ctx; c.setTransform(1,0,0,1,0,0); CURV={x:540,y:960,z:1};
dunes(c,0,{sky1:'#F6C47A',sky2:'#E0784A'});
// halo doré derrière le roi
glow(c,540,1080,760,'rgba(255,214,120,A)',.55);
// courbe du cours de l'or qui chute, derrière le personnage
c.save();c.globalAlpha=.9;c.strokeStyle='#C8463B';c.lineWidth=16;c.lineCap='round';c.lineJoin='round';c.beginPath();
c.moveTo(120,820);c.lineTo(330,800);c.lineTo(470,830);c.quadraticCurveTo(640,850,700,1050);c.lineTo(760,1240);c.stroke();
c.fillStyle='#C8463B';c.beginPath();c.moveTo(790,1310);c.lineTo(720,1230);c.lineTo(810,1210);c.closePath();c.fill();c.restore();
// Mansa Moussa en grand, sceptre
const m=soldier(c,{side:'x',outfit:'musa',x:470,y:1720,s:2.5,f:1,t:1.2,pose:{ba:.2,bb:.4,fa:.25,fb:1.25,rifle:0},rifleBack:false,smile:1});
// sceptre tenu dans la main (position renvoyée par le rig)
c.strokeStyle=C.brass;c.lineWidth=14;c.lineCap='round';c.beginPath();c.moveTo(m.hand.x,m.hand.y+260);c.lineTo(m.hand.x,m.hand.y-420);c.stroke();coin(c,m.hand.x,m.hand.y-446,36);
c.fillStyle=OUTFITS.musa.skin;c.beginPath();c.arc(m.hand.x,m.hand.y,26,0,7);c.fill();
// pièces qui tombent
[[180,1180,48],[880,1060,40],[930,1400,52],[140,1480,40],[820,1600,34],[260,980,30],[960,800,30]].forEach(([x,y,r])=>coin(c,x,y,r));
// voile bas pour la lisibilité de l'interface Shorts
const g=c.createLinearGradient(0,1500,0,1920);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(20,10,5,.75)');c.fillStyle=g;c.fillRect(0,1500,1080,420);
const gt=c.createLinearGradient(0,0,0,760);gt.addColorStop(0,'rgba(20,10,5,.75)');gt.addColorStop(1,'rgba(20,10,5,0)');c.fillStyle=gt;c.fillRect(0,0,1080,760);
// titre
const T=(s,x,y,font,col,ls='0px')=>{c.save();c.font=font;c.textAlign='center';c.textBaseline='middle';c.letterSpacing=ls;c.shadowColor='rgba(0,0,0,.6)';c.shadowBlur=24;c.shadowOffsetY=6;c.fillStyle=col;c.fillText(s,x,y);c.restore();};
label(c,540,250,'MALI · 1324',{a:1,size:30,bg:'rgba(20,10,5,.6)'});
T('LE ROI QUI A FAIT',540,380,'800 74px Inter','#FFF6E6','1px');
T('CHUTER',540,490,'800 118px Inter','#F2C46B','2px');
T('LE PRIX DE L’OR',540,605,'800 82px Inter','#FFF6E6','1px');
