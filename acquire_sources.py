"""Download authoritative EDB input, persisting each completed character."""
import json, re, urllib.request, urllib.parse, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'sources';OUT.mkdir(exist_ok=True)
def fetch(url, data=None):
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:return r.read()
EXISTING='我有爸媽姐妹弟哥和祖父母老師消防員警察醫生'
NEW='們中國是人在香港北京長城鳥巢故宮慶節煙花萬里'
if __name__=='__main__':
    for char in EXISTING+NEW:
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
            nonempty=[]
            for state,duration in states:
                names=re.findall(r't:this\.(shape(?:_\d+)?)',state)
                if names:
                    nonempty.append((names,int(duration or 0)))
            # Static one-state timelines are completed-character/grid layers, not strokes.
            if len(nonempty) >= 2:
                timelines.append({'start':nonempty[0][1],'states':[x[0] for x in nonempty],'durations':[x[1] for x in nonempty]})
        timelines.sort(key=lambda x:x['start'])
        official_count_match=re.search(r'總筆畫數.*?<td>\s*(\d+)\s*畫',html,re.S)
        if not official_count_match:raise ValueError(f'No official stroke count {char}')
        official_count=int(official_count_match.group(1))
        if official_count != len(timelines):raise ValueError(f'{char}: listed {official_count}, decoded {len(timelines)}')
        record={'char':char,'edb_id':eid,'bucket':bucket,'target':[float(grey[2]),float(grey[3])],'source_url':url,'source_sha256':hashlib.sha256(src).hexdigest(),'strokes':len(timelines),'official_listed_strokes':official_count,'official_timeline':timelines}
        dst.write_text(json.dumps(record,ensure_ascii=False,indent=2))
        print(char,eid,len(timelines),flush=True)
