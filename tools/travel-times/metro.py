# Время от отеля: пешком (OSRM foot), такси (OSRM car с поправкой на пробки), метро (схема Amap)
import json, heapq, sys
from geo import hav
HOTEL=(121.4818,31.22647)
WALK=75.0          # м/мин — темп с ребёнком, как в walkText на сайте
DETOUR=1.3         # прямая → реальная дорога для подходов к метро
ENTRY, WAIT, EXIT, XFER = 3, 3, 2, 5
MAXACC=1600
d=json.load(open("amap_subway.json",encoding="utf-8"))
st={}   # имя → (ll, en)
edges={} # (st,line) → [(st2,line,min)]
for L in d["l"]:
    ln=L["multilang"]["ln"]["en"].replace("Line ","") if L.get("multilang") else L["ln"]
    ss=L["st"]
    seq=[(s["n"],tuple(map(float,s["sl"].split(",")))) for s in ss]
    for n,ll in seq:
        en=(s.get("multilang",{}).get("n",{}).get("en") for s in ss if s["n"]==n)
        st.setdefault(n,(ll,next(en) or n))
    pairs=list(zip(seq,seq[1:]))+([(seq[-1],seq[0])] if L["lo"]=="1" else [])
    for (a,la),(b,lb) in pairs:
        dk=hav(la,lb)/1000*1.15; v=36 if dk<2 else (50 if dk<4 else 65); t=dk/v*60+0.5
        edges.setdefault((a,ln),[]).append((b,ln,t)); edges.setdefault((b,ln),[]).append((a,ln,t))
lines_at={}
for (n,ln) in edges: lines_at.setdefault(n,set()).add(ln)
def acc(ll): return hav(ll,HOTEL) if False else None
# Дейкстра от отеля
dist={}; prev={}; pq=[]
for n,(ll,en) in st.items():
    a=hav(HOTEL,ll)
    if a<=MAXACC:
        for ln in lines_at.get(n,()):
            t=a*DETOUR/WALK+ENTRY+WAIT
            if t<dist.get((n,ln),1e9): dist[(n,ln)]=t; prev[(n,ln)]=None; heapq.heappush(pq,(t,(n,ln)))
while pq:
    t,u=heapq.heappop(pq)
    if t>dist[u]: continue
    nbrs=list(edges.get(u,()))+[(u[0],l2,XFER) for l2 in lines_at[u[0]] if l2!=u[1]]
    for v0,v1,w in nbrs:
        v=(v0,v1); nt=t+w
        if nt<dist.get(v,1e9): dist[v]=nt; prev[v]=u; heapq.heappush(pq,(nt,v))
def path(u):
    p=[]
    while u: p.append(u); u=prev[u]
    return p[::-1]
def describe(p):
    en=lambda n: st[n][1].split(' · ')[-1]
    segs=[]  # [line, from, to]
    for n,ln in p:
        if segs and segs[-1][0]==ln: segs[-1][2]=n
        elif segs and segs[-1][2]==n: segs.append([ln,n,n])
        else: segs.append([ln,n,n])
    segs=[s for s in segs if s[1]!=s[2]]
    if not segs: return None
    out=f"{en(segs[0][1])} → линия {segs[0][0]}"
    for s in segs[1:]: out+=f" → {en(s[1])}, пересадка на {s[0]}"
    return out+f" → {en(segs[-1][2])}"
osrm=json.load(open("osrm.json"))
res={}
for k in osrm["foot"]:
    ll=tuple(map(float,k.split(",")))
    fd,fdist=osrm["foot"][k]; cd,cdist=osrm["car"][k]
    if hav(ll,HOTEL)<60: continue
    walk=round(fdist/WALK)
    cm=cd/60; taxi=round(cm*(1.5 if cdist<10000 else 1.3)+3)
    best=None
    for n,(sl,en) in st.items():
        a=hav(sl,ll)
        if a>MAXACC: continue
        for ln in lines_at.get(n,()):
            if (n,ln) not in dist: continue
            tot=dist[(n,ln)]+EXIT+a*DETOUR/WALK
            if best is None or tot<best[0]: best=(tot,(n,ln),a)
    metro=None; mtxt=None
    if best:
        p=path(best[1]); mtxt=describe(p)
        if mtxt: metro=round(best[0])
    if metro is not None and metro>=walk-3: metro=0  # пешком не дольше — метро не нужно
    res[k]=[walk,taxi,metro,mtxt if metro else None]
json.dump(res,open("tt.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print(len(res), sum(1 for v in res.values() if v[2]), sum(1 for v in res.values() if v[2]==0), sum(1 for v in res.values() if v[2] is None))
for k in ['121.44533,31.22395','121.43695,31.19412','121.50746,31.23455','121.49190,31.22668','121.66054,31.14407','121.49937,31.24746','121.01580,30.88720','121.44560,31.24920','121.30820,31.29130','121.94870,31.51770']:
    print(k,res.get(k))
