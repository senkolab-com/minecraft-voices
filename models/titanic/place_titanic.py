"""snap every speaking NPC of titanic_talk.NPCS to a standing cell of the built ship (simulated from the installed
pack, south face, marker-relative coordinates) and report the groups."""
import numpy as np, math, json, importlib
import titanic_talk as T
d=np.load('titanic_grid.npz'); g=d['g']; lo=d['lo']; pal=open('titanic_grid.npz.pal').read().split('\n')
AIR={pal.index(p) for p in ('air','light') if p in pal}
BAD_BELOW={i for i,p in enumerate(pal) if p in ('air','light','water','glass_pane','iron_bars','iron_chain') or 'ladder' in p or 'bed' in p or 'sign' in p or 'door' in p}
FT=0.3048; DECK_FT={'boat':92.5,'A':83.0,'B':74.0,'C':65.0,'D':54.5,'E':45.5,'F':37.0,'G':29.0,'orlop':21.0,'tank':5.25}
XS=259.84-130.5
def sheer(x): return 3.35*((x-XS)/130.5)**2 if x>=XS else 1.22*((XS-x)/138.5)**2
def deck_k(n,x): return int(round((DECK_FT[n]*FT+sheer(x))/0.6))-1
def cell(x,y,z):
    a,b,c=x-lo[0],y-lo[1],z-lo[2]
    if 0<=a<g.shape[0] and 0<=b<g.shape[1] and 0<=c<g.shape[2]: return int(g[a,b,c])
    return 0
def stand(x,y,z): return cell(x,y,z) in AIR and cell(x,y+1,z) in AIR and cell(x,y-1,z) not in BAD_BELOW
def rel_xz(xr,ym): return -int(round(ym/0.6)), int(round((269.06-xr)/0.6))+4
# existing NPCs: keep the named / non-replaced ones as obstacles
existing=[]
for l in open('titanic_npcs.txt').read().splitlines():
    pos,prof,name,noai=l.split('|'); p=[int(v[1:] or 0) for v in pos.split()]
    existing.append((tuple(p),prof,name,noai))
taken={(p[0],p[2]) for p,_,n,_ in existing if n not in T.REPLACE_GENERIC}
out=[]
for (nid,role,name,deck,xr,ym,face,intro) in T.NPCS:
    x0,z0=rel_xz(xr,ym); y0=deck_k(deck,269.06-xr)+1; best=None
    for r in range(0,12):
        for dx in range(-r,r+1):
            for dz in range(-r,r+1):
                if max(abs(dx),abs(dz))!=r: continue
                for dy in (0,-1,1,-2,2,-3,3):
                    x,y,z=x0+dx,y0+dy,z0+dz
                    if (x,z) in taken: continue
                    if stand(x,y,z) and best is None: best=(x,y,z)
        if best: break
    if not best: print('NO SPOT',nid,name,deck,xr,ym); continue
    taken.add((best[0],best[2])); out.append((nid,role,name,best,face))
json.dump(out,open('titanic_spots.json','w'))
# groups: talkers within 8 blocks of each other
for nid,role,name,p,face in out:
    near=[n2 for (i2,_,n2,p2,_) in out if i2!=nid and math.dist(p,p2)<=8]
    print(f'{nid:3} {role:10} {name:9} {p} near: {near}')
