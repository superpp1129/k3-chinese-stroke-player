"""Read the actual published Pages assets back; fail closed on any byte mismatch."""
import json,hashlib,urllib.request,urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
BASE='https://superpp1129.github.io/k3-chinese-stroke-player/'
CHARS=list('我有爸媽姐妹弟哥和祖父母老師消防員警察醫生們中國是人在香港北京長城鳥巢故宮慶節煙花萬里')
def check(relative):
    local=(ROOT/'site'/relative).read_bytes();url=BASE+urllib.parse.quote(relative)
    req=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'K3-production-byte-verifier/1.0'})
    with urllib.request.urlopen(req,timeout=60) as response:
        remote=response.read();status=response.status
    assert status==200 and remote==local,f'{relative}: published bytes differ'
    row={'file':relative,'url':url,'status':status,'bytes':len(remote),'sha256':hashlib.sha256(remote).hexdigest(),'exact_byte_match':True}
    print(json.dumps(row,ensure_ascii=False),flush=True);return row
if __name__=='__main__':
    targets=['index.html','styles.css','app.js','manifest.json']+[f'videos/{c}.mp4' for c in CHARS]
    with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(check,targets))
    assert len(rows)==47 and len([r for r in rows if r['file'].endswith('.mp4')])==43
    report={'base_url':BASE,'files_verified':47,'video_count':43,'all_exact_byte_match':True,'records':rows}
    (ROOT/'verification/public-readback.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
