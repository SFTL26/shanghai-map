# Схема метро Шанхая для «Памятки»: SVG из схемы Amap (map.amap.com/subway).
# Вход: amap_subway.json (как скачать — README рядом). Выход: metro.svg.
import json, sys, html
src = sys.argv[1] if len(sys.argv) > 1 else "amap_subway.json"
d = json.load(open(src, encoding="utf-8"))
pt = lambda s: tuple(map(float, s.split()))
# lg — сторона подписи у Amap: 0 сверху, дальше по часовой через 45°
DIRS = {0:(0,-1),1:(1,-1),2:(1,0),3:(1,1),4:(0,1),5:(-1,1),6:(-1,0),7:(-1,-1)}
KEY = {"大世界":"hotel","龙阳路":"key","浦东1号2号航站楼":"key","陆家嘴":"key","人民广场":"key","豫园":"key","南京东路":"key","虹桥火车站":"key"}
paths, stations = [], {}
for L in d["l"]:
    c = "#" + L["cl"]
    ln = L["multilang"]["ln"]["en"].replace("Line ", "") if L.get("multilang") else L["ln"]
    if L["ln"] == "磁浮线": ln = "Maglev"
    if L["ln"] == "市域机场线": ln = "Airport Link"
    if L["ln"] == "浦江线": ln = "Pujiang"
    pts = [pt(p) for p in L["c"]]
    if L["lo"] == "1": pts.append(pts[0])
    dash = ' stroke-dasharray="14 8"' if ln == "Maglev" else ""
    paths.append(f'<polyline points="{" ".join(f"{x:g},{y:g}" for x,y in pts)}" stroke="{c}"{dash}/>')
    for s in L["st"]:
        n = s["n"]; en = (s.get("multilang", {}).get("n", {}).get("en") or s.get("sp") or n)
        st = stations.setdefault(n, {"p": pt(s["p"]), "en": en, "lg": int(s.get("lg") or 2), "t": s["t"] == "1", "lines": [], "c": c})
        if ln not in st["lines"]: st["lines"].append(ln)
    # подпись линии у конечных
    lp = L.get("lp") or []
    for p in lp[:1]:
        x, y = pt(p)
        paths.append(f'<g class="lnum"><rect x="{x-22:g}" y="{y-13:g}" width="44" height="26" rx="6" fill="{c}"/><text x="{x:g}" y="{y+6:g}">{html.escape(ln if len(ln)<4 else ln[:3])}</text></g>')
# Подписи: сначала сторона Amap (lg), при наложении — следующая свободная из 8 сторон.
# Английские названия длиннее китайских, под которые размечен lg, поэтому без перебора они наезжают.
FS, CW = 15, 0.62          # кегль и средняя ширина символа в долях кегля
placed = []                # прямоугольники уже занятых подписей и станций
for n, s in stations.items():
    x, y = s["p"]; placed.append((x-10, y-10, x+10, y+10))
def box(x, y, dx, dy, w, h):
    off = 13
    tx = x + dx*off; ty = y + dy*off + (5 if dy == 0 else (14 if dy > 0 else -4))
    x0 = tx if dx > 0 else (tx - w if dx < 0 else tx - w/2)
    return tx, ty, (x0-3, ty-13, x0+w+3, ty-11+h)
def hits(r, own):
    return sum(1 for q in placed if q is not own and not (r[2] <= q[0] or q[2] <= r[0] or r[3] <= q[1] or q[3] <= r[1]))
order = sorted(stations.items(), key=lambda kv: (0 if KEY.get(kv[0]) else (1 if kv[1]["t"] else 2)))
out = []
for idx, (n, s) in enumerate(order):
    x, y = s["p"]; k = KEY.get(n, "")
    w = len(s["en"]) * FS * CW * (1.08 if k else 1); h = 16 + (16 if k else 0)
    own = next(q for q in placed if q[0] == x-10 and q[1] == y-10)
    best = None
    for i in range(8):
        dd = (s["lg"] + i) % 8; dx, dy = DIRS[dd]
        tx, ty, r = box(x, y, dx, dy, w, h)
        c = hits(r, own)
        if best is None or c < best[0]: best = (c, dx, dy, tx, ty, r)
        if c == 0: break
    _, dx, dy, tx, ty, r = best
    placed.append(r)
    anchor = "start" if dx > 0 else ("end" if dx < 0 else "middle")
    istr = s["t"] or len(s["lines"]) > 1
    cls = ("st t" if istr else "st") + (" " + k if k else "")
    rad = 9 if istr else 6
    title = html.escape(f'{s["en"]} · {n} · линии {", ".join(s["lines"])}')
    zh = f'<text class="zh" x="{tx:g}" y="{ty+16:g}" text-anchor="{anchor}">{n}</text>' if k else ""
    fill = "#fff" if istr else s["c"]
    dot = (f'<circle cx="{x:g}" cy="{y:g}" r="15"/><text class="hm" x="{x:g}" y="{y+6:g}">H</text>' if k == "hotel"
           else f'<circle cx="{x:g}" cy="{y:g}" r="{rad}" fill="{fill}"/>')
    out.append(f'<g class="{cls}" data-n="{n}"><title>{title}</title>{dot}<text x="{tx:g}" y="{ty:g}" text-anchor="{anchor}">{html.escape(s["en"])}</text>{zh}</g>')
svg = ('<svg class="msvg" id="msvg" viewBox="0 60 3000 2420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Схема метро Шанхая">'
       '<g class="mlines" fill="none" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">' + "".join(paths) + '</g>'
       '<g class="mst">' + "".join(out) + '</g></svg>')
open("metro.svg", "w", encoding="utf-8").write(svg)
print(len(stations), "станций,", len(svg)//1024, "КБ")
