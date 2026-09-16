"""Download authoritative EDB input, persisting each completed character."""
import json, re, urllib.request, urllib.parse, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'sources';OUT.mkdir(exist_ok=True)
def fetch(url, data=None):
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:return r.read()
if __name__=='__main__':
    for char in '我有爸媽姐妹弟哥和祖父母老師消防員警察醫生':
        dst=OUT/f'{char}.json'
        if dst.exists():continue
        data=urllib.parse.urlencode({'searchMethod':'char','searchCriteria':char,'sortBy':'stroke','jpC':'lshk'}).encode()
        html=fetch('https://www.edbchinese.hk/lexlist_ch/result.jsp',data).decode('utf-8')
        (OUT/f'{char}-lookup.html').write_text(html)
        m=re.search(r'stkdemo_js/([0-9A-Z]+-[0-9A-Z]+)/(\d+)\.html',html)
        if not m:raise ValueError(f'No official iframe {char}')
        bucket, eid=m.groups();url=f'https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/{bucket}/{eid}.js'
        src=fetch(url);(OUT/f'{eid}.js').write_bytes(src)
        text=src.decode('utf-8-sig')
        grey=re.search(r'this\.(shape(?:_\d+)?)\.graphics\.f\("#999999"\).*?this\.\1\.setTransform\(([-\d.]+),([-\d.]+)\)',text,re.S)
        if not grey:raise ValueError(f'No registration {char}')
        timelines=[]
        for line in text.splitlines():
            if 'Tween.get({})' not in line:continue
            states=re.findall(r'\.to\(\{state:\[(.*?)\]\}(?:,(\d+))?\)',line)
            nonempty=[(re.findall(r't:this\.(shape(?:_\d+)?)',s),int(t or 0)) for s,t in states if s]
            if nonempty:timelines.append({'start':nonempty[0][1],'states':[x[0] for x in nonempty],'durations':[x[1] for x in nonempty]})
        timelines.sort(key=lambda x:x['start'])
        record={'char':char,'edb_id':eid,'bucket':bucket,'target':[float(grey[2]),float(grey[3])],'source_url':url,'source_sha256':hashlib.sha256(src).hexdigest(),'strokes':len(timelines),'official_timeline':timelines}
        dst.write_text(json.dumps(record,ensure_ascii=False,indent=2))
        print(char,eid,len(timelines),flush=True)
