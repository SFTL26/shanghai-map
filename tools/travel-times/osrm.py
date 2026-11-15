import json, urllib.request, time, sys
from geo import gcj2wgs
HOTEL=(121.4818,31.22647)
pts=[p for p in json.load(open("pts.json")) if p[0]>120.6]
def table(profile):
    out={}
    o=gcj2wgs(*HOTEL)
    for i in range(0,len(pts),80):
        ch=pts[i:i+80]
        cs=";".join(f"{x:.6f},{y:.6f}" for x,y in [o]+[gcj2wgs(*p) for p in ch])
        url=f"https://routing.openstreetmap.de/routed-{profile}/table/v1/driving/{cs}?sources=0&annotations=duration,distance"
        for t in range(4):
            try:
                d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"shanghai-family-map/1.0"}),timeout=60)); break
            except Exception as e: print("retry",e,file=sys.stderr); time.sleep(5)
        for j,p in enumerate(ch):
            out[f"{p[0]:.5f},{p[1]:.5f}"]=[d["durations"][0][j+1],d["distances"][0][j+1]]
        time.sleep(1.2)
    return out
res={"foot":table("foot"),"car":table("car")}
json.dump(res,open("osrm.json","w"))
print(len(res["foot"]),len(res["car"]))
