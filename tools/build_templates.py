"""Write HTML sources for Maple Lingua social/print templates."""
import sys, os, re
LOGOS, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def svg(name, w=None, h=None):
    s = open(f"{LOGOS}/{name}.svg").read().strip()
    s = re.sub(r"<title>.*?</title>", "", s)
    if w: s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w}" height="{h}"', s, count=1)
    return s

LEAF = "50,5 57,20 64,16 61,36 74,24 77,31 90,28 85,42 92,46 73,62 76,70 54,67 55,90 45,90 46,67 24,70 27,62 8,46 15,42 10,28 23,31 26,24 39,36 36,16 43,20"
def leaf(size, uid, gap="#FFFFFF"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><defs>'
            f'<clipPath id="l{uid}"><rect width="48.6" height="100"/></clipPath>'
            f'<clipPath id="r{uid}"><rect x="51.4" width="48.6" height="100"/></clipPath></defs>'
            f'<polygon clip-path="url(#l{uid})" fill="#1F4E9C" points="{LEAF}"/>'
            f'<polygon clip-path="url(#r{uid})" fill="#C8332B" points="{LEAF}"/></svg>')

HEAD = """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap">
<style>*{box-sizing:border-box}body{margin:0;font-family:Manrope,sans-serif;color:#1B2A41}
.frame{position:relative;overflow:hidden;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:18px;font-weight:800;letter-spacing:.14em}
</style></head><body>"""

def page(name, w, h, inner, bg="#FFFFFF"):
    html = HEAD + f'<div class="frame" style="width:{w}px;height:{h}px;background:{bg}">{inner}</div></body></html>'
    open(f"{OUT}/{name}.html", "w").write(html)

# ---- Post 1080x1080: word of the day ----
page("post-slovo-dnya", 1080, 1080, f"""
<div style="padding:72px 80px;display:flex;flex-direction:column;height:100%;gap:0">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div class="brand" style="font-size:30px">{leaf(56,'p')}MAPLE LINGUA</div>
    <div style="font-size:24px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#5A6472">Слово дня</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px">
    <div style="display:flex;flex-direction:column;gap:8px">
      <div style="font-size:26px;font-weight:800;letter-spacing:.12em;color:#1F4E9C">FRANÇAIS</div>
      <div style="font-size:120px;font-weight:800;line-height:1;letter-spacing:-.03em;color:#1F4E9C">le logement</div>
    </div>
    <div style="height:4px;width:120px;background:#1B2A41;border-radius:2px"></div>
    <div style="display:flex;flex-direction:column;gap:8px">
      <div style="font-size:26px;font-weight:800;letter-spacing:.12em;color:#C8332B">ENGLISH</div>
      <div style="font-size:120px;font-weight:800;line-height:1;letter-spacing:-.03em;color:#C8332B">housing</div>
    </div>
    <div style="font-size:44px;font-weight:600;color:#1B2A41;margin-top:12px">жильё</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;font-size:28px;color:#5A6472;font-weight:600">
    <div style="max-width:640px">Chercher un logement à Toronto.<br>Looking for housing in Toronto.</div>
    <div style="font-weight:800;color:#1B2A41">@maplelingua</div>
  </div>
</div>""", "#FFFFFF")

# ---- Story 1080x1920: sign-up ----
cells = "".join(
    f'<div style="height:72px;border-radius:12px;display:grid;place-items:center;font-size:30px;font-weight:800;'
    f'background:{"#C8332B" if i==7 else ("#7FA6EE" if i<7 else "rgba(255,255,255,.12)")};color:{"#FFFFFF" if i==7 else ("#0F1726" if i<7 else "rgba(255,255,255,.55)")}">{i}</div>'
    for i in range(1, 13))
page("story-zapis", 1080, 1920, f"""
<div style="padding:150px 90px 170px;display:flex;flex-direction:column;height:100%;color:#FFFFFF">
  <div class="brand" style="font-size:34px">{leaf(64,'s')}MAPLE LINGUA</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:56px">
    <div style="font-size:112px;font-weight:800;line-height:1.02;letter-spacing:-.03em">
      <span style="color:#7FA6EE">Français</span><br>и <span style="color:#F2766C">English</span><br>для Канады
    </div>
    <div style="font-size:40px;font-weight:600;line-height:1.35;color:#C9D1DD">С нуля и подготовка<br>к TEF, TCF, IELTS и CELPIP</div>
    <div style="display:flex;flex-direction:column;gap:20px">
      <div style="font-size:26px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#A4AEBC">Цель для Express Entry — CLB 7</div>
      <div style="display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px">{cells}</div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:28px">
    <div style="font-size:64px;font-weight:800">$25 <span style="font-size:40px;color:#A4AEBC">/ час</span></div>
    <div style="background:#C8332B;border-radius:999px;padding:34px 0;text-align:center;font-size:44px;font-weight:800">Пишите @maplelingua</div>
  </div>
</div>""", "#1B2A41")

# ---- Certificate A4 landscape (297x210mm at 96dpi = 1123x794) ----
page("sertifikat", 1123, 794, f"""
<div style="position:absolute;inset:28px;border:2px solid #1B2A41;border-radius:6px"></div>
<div style="position:absolute;inset:36px;border:1px solid #C9D1DD;border-radius:4px"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:14px;background:#1F4E9C"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:14px;background:#C8332B"></div>
<div style="position:relative;padding:80px 110px 70px;display:flex;flex-direction:column;height:100%">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div class="brand" style="font-size:20px">{leaf(40,'c')}MAPLE LINGUA</div>
    <div style="width:132px;height:132px">{svg('maple-lingua-4-pechat',132,132)}</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:14px;margin-top:-30px">
    <div style="font-size:15px;font-weight:800;letter-spacing:.3em;color:#5A6472">СЕРТИФИКАТ · CERTIFICAT · CERTIFICATE</div>
    <div style="font-size:20px;font-weight:600;color:#5A6472">Настоящий сертификат подтверждает, что</div>
    <div style="font-size:54px;font-weight:800;letter-spacing:-.02em;line-height:1.1">[Имя Фамилия ученика]</div>
    <div style="font-size:20px;font-weight:600;color:#5A6472;max-width:720px;line-height:1.5">прошёл(ла) курс <b style="color:#1B2A41">«[Название курса]»</b> в объёме <b style="color:#1B2A41">[N] академических часов</b> и достиг(ла) уровня <b style="color:#1B2A41">[уровень]</b>.</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;font-size:15px;color:#5A6472;font-weight:600">
    <div style="display:flex;flex-direction:column;gap:6px"><div style="width:240px;border-top:1.5px solid #1B2A41"></div>Эльвира Волкова, преподаватель</div>
    <div style="display:flex;flex-direction:column;gap:6px;align-items:flex-end"><div style="width:180px;border-top:1.5px solid #1B2A41"></div>Дата: [ДД.ММ.ГГГГ]</div>
  </div>
</div>""", "#FFFFFF")
print("ok")
