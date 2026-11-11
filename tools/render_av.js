const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
const dir=process.argv[2];
(async()=>{const b=await chromium.launch();
for (const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){
  const svg=fs.readFileSync(path.join(dir,f),'utf8');
  const p=await b.newPage({viewport:{width:1024,height:1024}});
  await p.setContent(`<body style="margin:0">${svg}</body>`);
  await p.screenshot({path:path.join(dir,f.replace('.svg','.png')),clip:{x:0,y:0,width:1024,height:1024}});
  await p.setContent(`<body style="margin:0;background:transparent"><div style="width:1024px;height:1024px;border-radius:50%;overflow:hidden;box-sizing:border-box;border:3px solid #d0d4da">${svg}</div></body>`);
  await p.screenshot({path:path.join(dir,f.replace('.svg','-krug-preview.png')),omitBackground:true,clip:{x:0,y:0,width:1024,height:1024}});
  await p.close();}
await b.close();})();
