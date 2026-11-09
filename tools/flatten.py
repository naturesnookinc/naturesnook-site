"""Make a flat 'label laid out' image for each product front photo.
photo_lib/UPC-front.jpg -> photo_lib/UPC-flat.jpg (used on product cards).
Bottles/jars are unwrapped from the cylinder; boxes are trimmed as-is."""
import os, sys, numpy as np
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
LIB=ROOT+'photo_lib/'

def flatten(src, out, tmax=62):
    im=Image.open(src).convert('RGB'); arr=np.asarray(im)
    nonwhite=(np.abs(255-arr.astype(np.int16)).max(axis=2)>22)
    H,W=nonwhite.shape
    L=np.full(H,-1); R=np.full(H,-1)
    for y in range(H):
        xs=np.nonzero(nonwhite[y])[0]
        if len(xs)>W*0.05: L[y],R[y]=xs[0],xs[-1]
    w=np.where(L>=0,R-L,0); mw=w.max()
    rows=np.nonzero(w>0)[0]
    if not len(rows): return False
    top=w[rows[:max(3,int(len(rows)*0.05))]]
    cyl=np.median(top)<mw*0.9          # cap narrower than body -> bottle or jar
    if cyl:
        body=w>=mw*0.93; best=(0,0); cur=None
        for y in range(H):
            if body[y]:
                if cur is None: cur=y
                if y-cur>best[1]-best[0]: best=(cur,y)
            else: cur=None
        y0,y1=best; hb=y1-y0; y0+=int(hb*0.03); y1-=int(hb*0.03)
    else:
        y0,y1=rows[0],rows[-1]
    xl=int(np.median(L[y0:y1])); xr=int(np.median(R[y0:y1]))
    crop=arr[y0:y1, xl:xr+1]
    if cyl:
        r=(xr-xl)/2; tm=np.radians(tmax); n=int(round(2*tm*r))
        src_x=r+r*np.sin(np.linspace(-tm,tm,n))
        x0=np.clip(np.floor(src_x).astype(int),0,crop.shape[1]-2); f=(src_x-x0)[None,:,None]
        flat=(crop[:,x0]*(1-f)+crop[:,x0+1]*f).astype(np.uint8)
    else:
        m=int((xr-xl)*0.02); flat=crop[:,m:crop.shape[1]-m]
    Image.fromarray(flat).save(out, quality=86, optimize=True)
    return True

def run(force=False):
    n=0
    for f in sorted(os.listdir(LIB)):
        if not f.endswith('-front.jpg'): continue
        u=f[:-10]; out=LIB+u+'-flat.jpg'
        if not force and os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(LIB+f): continue
        try:
            if flatten(LIB+f,out): n+=1
        except Exception as e: print('skip',u,e)
    return n

if __name__=='__main__':
    print('flattened',run('--force' in sys.argv))
