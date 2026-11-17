# Схема метро для «Памятки»

Схема во вкладке «Метро» — SVG, встроенный прямо в index.html (между `<!-- metro-svg -->` и `<!-- /metro-svg -->`), чтобы работала без интернета.

Пересобрать (из этой папки, Python 3):

1. `curl -A "Mozilla/5.0" -e https://map.amap.com/subway/index.html "https://map.amap.com/service/subway?srhdata=3100_drw_shanghai.json" -o amap_subway.json`
2. `python build_svg.py` → metro.svg (подписи: сторона из `lg` Amap, при наложении — следующая свободная)
3. `python inject_svg.py` → вставляет metro.svg в ../../index.html

Отель на схеме — станция 大世界 (`KEY` в build_svg.py и `HOT` в index.html — координаты схемы, не географические).
