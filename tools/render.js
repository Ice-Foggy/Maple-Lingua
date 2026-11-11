const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = process.argv[2], preview = process.argv[3];
(async () => {
  const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const w = +m[1], h = +m[2];
    const target = 2000, scale = target / Math.max(w, h);
    const W = Math.round(w * scale), H = Math.round(h * scale);
    const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    const html = `<html><body style="margin:0;background:transparent">${svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${W}" height="${H}"`)}</body></html>`;
    await p.setContent(html);
    await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')), omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } });
    // preview on light grey for my own check
    await p.setContent(html.replace('background:transparent', 'background:#e6e6e6'));
    await p.screenshot({ path: path.join(preview, f.replace('.svg', '.prev.png')), clip: { x: 0, y: 0, width: W, height: H } });
    await p.close();
  }
  await b.close();
})();
