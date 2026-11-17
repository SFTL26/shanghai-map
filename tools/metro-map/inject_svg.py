# Вставляет metro.svg в index.html между <!-- metro-svg --> и <!-- /metro-svg -->.
import re, sys, pathlib
here = pathlib.Path(__file__).parent
idx = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here / "../../index.html"
s = idx.read_text(encoding="utf-8")
svg = (here / "metro.svg").read_text(encoding="utf-8")
new, n = re.subn(r"<!-- metro-svg -->.*?<!-- /metro-svg -->", lambda m: "<!-- metro-svg -->\n" + svg + "\n<!-- /metro-svg -->", s, flags=re.S)
assert n == 1, "маркеры схемы не найдены"
idx.write_text(new, encoding="utf-8")
print("схема вставлена,", len(svg) // 1024, "КБ")
