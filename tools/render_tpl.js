const { chromium } = require('playwright'); const path=require('path');
const src=process.argv[2], out=process.argv[3];
const jobs=[['post-slovo-dnya',1080,1080,1],['story-zapis',1080,1920,1],['sertifikat',1123,794,3]];
(async()=>{const b=await chromium.launch();
for (const [n,w,h,dsf] of jobs){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:dsf});
await p.goto('file://'+path.join(src,n+'.html'),{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:path.join(out,n+'.png'),clip:{x:0,y:0,width:w,height:h}});
if(n==='sertifikat') await p.pdf({path:path.join(out,n+'.pdf'),width:'297mm',height:'210mm',printBackground:true,pageRanges:'1'});
await p.close();}
await b.close();})();
