import math
A=6378245.0; EE=0.00669342162296594323
def _tl(x,y):
    r=-100.0+2.0*x+3.0*y+0.2*y*y+0.1*x*y+0.2*math.sqrt(abs(x))
    r+=(20.0*math.sin(6.0*x*math.pi)+20.0*math.sin(2.0*x*math.pi))*2.0/3.0
    r+=(20.0*math.sin(y*math.pi)+40.0*math.sin(y/3.0*math.pi))*2.0/3.0
    r+=(160.0*math.sin(y/12.0*math.pi)+320*math.sin(y*math.pi/30.0))*2.0/3.0
    return r
def _tg(x,y):
    r=300.0+x+2.0*y+0.1*x*x+0.1*x*y+0.1*math.sqrt(abs(x))
    r+=(20.0*math.sin(6.0*x*math.pi)+20.0*math.sin(2.0*x*math.pi))*2.0/3.0
    r+=(20.0*math.sin(x*math.pi)+40.0*math.sin(x/3.0*math.pi))*2.0/3.0
    r+=(150.0*math.sin(x/12.0*math.pi)+300.0*math.sin(x/30.0*math.pi))*2.0/3.0
    return r
def wgs2gcj(lng,lat):
    dl=_tl(lng-105.0,lat-35.0); dg=_tg(lng-105.0,lat-35.0)
    rl=lat/180.0*math.pi; m=math.sin(rl); m=1-EE*m*m; s=math.sqrt(m)
    dl=(dl*180.0)/((A*(1-EE))/(m*s)*math.pi); dg=(dg*180.0)/(A/s*math.cos(rl)*math.pi)
    return lng+dg, lat+dl
def gcj2wgs(lng,lat):
    w=[lng,lat]
    for _ in range(4):
        g=wgs2gcj(*w); w=[w[0]-(g[0]-lng), w[1]-(g[1]-lat)]
    return w
def hav(a,b):
    k=math.pi/180; dx=(b[0]-a[0])*k*math.cos((a[1]+b[1])/2*k); dy=(b[1]-a[1])*k
    return 6371000*math.hypot(dx,dy)
