import re, json, math
s=open("shanghai-map/index.html",encoding="utf-8").read()
pts=set()
for m in re.finditer(r'"?ll"?\s*:\s*\[\s*(1[12]\d\.\d+)\s*,\s*(3\d\.\d+)\s*\]',s):
    pts.add((round(float(m.group(1)),5),round(float(m.group(2)),5)))
print(len(pts))
json.dump(sorted(pts),open("tt/pts.json","w"))
