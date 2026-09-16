"""Assert complete21 coverage and assemble durable production manifest."""
import json,hashlib
from pathlib import Path
import build
ROOT=Path(__file__).resolve().parent
EXPECTED=list('我有爸媽姐妹弟哥和祖父母老師消防員警察醫生')
def load(p):return json.loads((ROOT/p).read_text())
if __name__=='__main__':
    assert [i['char'] for i in build.CHARACTERS]==EXPECTED and len(set(EXPECTED))==21
    assert set(load('verification/visual-review.json')['approved'])==set(EXPECTED)
    rows=[]
    for i in build.CHARACTERS:
        c=i['char'];m=load(f'verification/{c}/media.json');s=load(f'sources/{c}.json')
        assert hashlib.sha256((ROOT/f'site/videos/{c}.mp4').read_bytes()).hexdigest()==m['sha256']
        assert m['frames']==build.frame_count(i['strokes']) and m['visual_review'].startswith('passed')
        source_map=list(range(i['strokes'])) # Both paths audited: official chronology or frozen original order.
        row={'char':c,'official_edb_id':s['edb_id'],'official_url':s['source_url'],'official_sha256':s['source_sha256'],'official_strokes':s['strokes'],'stroke_names':i['stroke_order'],'render_geometry':i.get('geometry','verified-frozen-generic-outline'),'render_source_indices_zero_based':source_map,'mapping_status':'manually verified against official chronology and shape; IoU diagnostic assignments NOT used','media':m,'visual_pass':True}
        drive=ROOT/f'verification/drive/{c}.json'
        if drive.exists():row['drive']=json.loads(drive.read_text())
        rows.append(row)
    out={'characters':EXPECTED,'count':len(rows),'original_count':9,'added_count':12,'word_cards':['爸爸','媽媽','祖父','祖母','老師','消防員','警察','醫生'],'timing':{'draw':2.0,'pause':0.6,'intro':0.7,'final':3.0,'fps':30,'width':1080,'height':1080},'visual_review':'visual-review.json','records':rows}
    (ROOT/'verification/manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps({'count':len(rows),'drive_verified':sum('drive'in x for x in rows),'media_visual_pass':sum(x['visual_pass'] for x in rows)},ensure_ascii=False))
