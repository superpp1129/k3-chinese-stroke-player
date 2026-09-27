"""Create official/candidate stroke comparison evidence; never assumes source ordering."""
import json,re,subprocess,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.optimize import linear_sum_assignment
import build
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'verification';OUT.mkdir(exist_ok=True)
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
def decode(s):
    i=0;x=y=0;out=[]
    while i<len(s):
        n=ALPHABET.index(s[i]);i+=1;cmd=n>>3;size=((n>>2)&1)+2
        count=[2,2,4,6,0][cmd]
        if cmd==0:x=y=0
        vals=[]
        for p in range(count):
            z=ALPHABET.index(s[i]);sign=-1 if z>>5 else 1;v=((z&31)<<6)|ALPHABET.index(s[i+1])
            if size==3:v=(v<<6)|ALPHABET.index(s[i+2])
            v=sign*v/10;i+=size
            if p%2==0:x+=v;vals.append(x)
            else:y+=v;vals.append(y)
        out.append('MLQCZ'[cmd]+' '.join(map(str,vals)))
    return ' '.join(out)
def shapes_for(item):
    s=(ROOT/'sources'/f"{item['edb_id']}.js").read_text()
    shapes={}
    for m in re.finditer(r'this\.(shape(?:_\d+)?)\.graphics\.f\("(#[A-Fa-f0-9]+)"\)\.s\(\)\.p\("([^"]+)"\);\s*this\.\1\.setTransform\(([^)]+)\)',s):
        shapes[m[1]]={'path':decode(m[3]),'transform':list(map(float,m[4].split(','))),'colour':m[2]}
    return shapes

def svg_transform(values):
    """Convert the translation/scale subset used by the frozen EDB sources."""
    if len(values)==2:
        return f'translate({values[0]} {values[1]})'
    if len(values)==4:
        return f'translate({values[0]} {values[1]}) scale({values[2]} {values[3]})'
    raise ValueError(f'Unsupported CreateJS transform: {values}')

def official_mask(shapes,names,dest):
    paths=''
    for name in names:
        sh=shapes[name];t=sh['transform']
        paths+=f'<path d="{sh["path"]}" transform="{svg_transform(t)}" fill="black"/>'
    svg=dest.with_suffix('.svg');png=dest.with_suffix('.png')
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080">'+paths+'</svg>')
    subprocess.run(['sips','-s','format','png',str(svg),'--out',str(png)],check=True,stdout=subprocess.DEVNULL)
    return np.asarray(Image.open(png).convert('RGBA'))[:,:,3]>10

def panel(mask):
    a=np.full((1080,1080,3),255,dtype=np.uint8);a[mask]=0
    return Image.fromarray(a).resize((180,180))

def audit(char):
    item=json.loads((ROOT/'sources'/f'{char}.json').read_text());shapes=shapes_for(item)
    work=OUT/char;work.mkdir(exist_ok=True)
    official=[official_mask(shapes,t['states'][-1],work/f'official-{i+1:02}') for i,t in enumerate(item['official_timeline'])]
    data=json.loads(build.data_path(char).read_text());n=len(official)
    tx=ty=(1080-1024*build.SCALE)/2
    trial=[build.raster_stroke(s,work/f'trial-{i}',tx,ty) for i,s in enumerate(data['strokes'])]
    ys,xs=np.nonzero(np.logical_or.reduce(trial));dx,dy=build.optical_translation((xs.min(),ys.min(),xs.max(),ys.max()),item['target']);tx+=dx;ty+=dy
    candidate=[build.raster_stroke(s,work/f'candidate-{i}',tx,ty) for i,s in enumerate(data['strokes'])]
    cost=np.array([[1-np.count_nonzero(a&b)/np.count_nonzero(a|b) for b in candidate] for a in official])
    rows,cols=linear_sum_assignment(cost)
    mapping=[int(c)+1 for c in cols]
    sheet=Image.new('RGB',(4*360,((n+3)//4)*205),'#eeeeee');d=ImageDraw.Draw(sheet)
    for i,c in zip(rows,cols):
        x=(i%4)*360;y=(i//4)*205;sheet.paste(panel(official[i]),(x,y));sheet.paste(panel(candidate[c]),(x+180,y));d.text((x+5,y+182),f'EDB {i+1} | candidate {c+1} IoU {1-cost[i,c]:.2f}',fill='black')
    sheet.save(work/'comparison.jpg')
    record={**item,'candidate_geometry_sha256':hashlib.sha256(build.data_path(char).read_bytes()).hexdigest(),'candidate_count':len(candidate),'mapping_1_based':mapping,'overlap_iou':[round(float(1-cost[r,c]),4) for r,c in zip(rows,cols)],'translation':[tx,ty],'comparison':'verification/'+char+'/comparison.jpg'}
    (work/'mapping.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    print(char,n,len(candidate),mapping,record['overlap_iou'],flush=True)
if __name__=='__main__':
    import sys
    for char in (sys.argv[1] if len(sys.argv)>1 else '我有爸媽姐妹弟哥和祖父母老師消防員警察醫生'):audit(char)
