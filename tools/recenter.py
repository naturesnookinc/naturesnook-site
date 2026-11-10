"""Center product photos: trim uneven white space so the item sits in the middle.
Usage: python3 tools/recenter.py [files...]   (default: every photo_lib front/facts/back image)"""
import os, sys, numpy as np
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
def recenter(p, tol=0.04):
    im=Image.open(p).convert('RGB'); a=np.asarray(im.convert('L')).astype(int); H,W=a.shape
    m=a<245; cols=np.nonzero(m.sum(0)>H*0.005)[0]; rows=np.nonzero(m.sum(1)>W*0.005)[0]
    if not len(cols) or not len(rows): return False
    l,r,t,b=cols[0],W-1-cols[-1],rows[0],H-1-rows[-1]
    if abs(l-r)<=W*tol and abs(t-b)<=H*tol: return False
    c=im.crop((cols[0],rows[0],cols[-1]+1,rows[-1]+1))
    pad=max(8,int(max(c.size)*0.03))
    out=Image.new('RGB',(c.size[0]+2*pad,c.size[1]+2*pad),'white'); out.paste(c,(pad,pad))
    out.save(p,quality=82,optimize=True); return True
if __name__=='__main__':
    L=ROOT+'photo_lib/'
    files=sys.argv[1:] or [L+f for f in sorted(os.listdir(L)) if f.endswith(('-front.jpg','-facts.jpg','-back.jpg'))]
    print('recentered',sum(recenter(f) for f in files))
