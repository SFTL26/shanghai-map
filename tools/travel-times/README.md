# Время от отеля до мест

Пересчёт таблицы `TT` в index.html (запускать из этой папки, Python 3):

1. Скопировать index.html сюда как `../shanghai-map/index.html` или поправить путь в `coords.py`; `python coords.py` → pts.json
2. `python osrm.py` → osrm.json (пешком и на машине, routing.openstreetmap.de)
3. Схема метро Amap: `curl -A "Mozilla/5.0" -e https://map.amap.com/subway/index.html "https://map.amap.com/service/subway?srhdata=3100_drw_shanghai.json" -o amap_subway.json`
4. `python metro.py` → tt.json, его содержимое вставить в `const TT=` в index.html

Координаты отеля — `HOTEL` в osrm.py и metro.py (GCJ-02, как на карте).
