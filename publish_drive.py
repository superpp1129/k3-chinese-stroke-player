"""Upload only visually approved videos with the registered Drive connector.
Read each exact returned ID back and download its bytes before recording success.
"""
import subprocess,json,re,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CONNECTOR=['/opt/homebrew/bin/python3','/Users/claudeuser/projects/claude-tools/tools/gdrive.py']
FOLDER='1iZwfwFdhM2pEDiojTRf-stwYjgMebRDK'
OUT=ROOT/'verification/drive';OUT.mkdir(exist_ok=True)
READBACK=ROOT/'.cache/drive-readback';READBACK.mkdir(exist_ok=True)

def call(args):return subprocess.check_output(CONNECTOR+args,text=True,stderr=subprocess.STDOUT)
if __name__=='__main__':
    approved=json.loads((ROOT/'verification/visual-review.json').read_text())['approved']
    for c in sys.argv[1]:
        assert c in approved,f'{c} not visually approved'
        local=ROOT/'site/videos'/f'{c}.mp4'
        media=json.loads((ROOT/'verification'/c/'media.json').read_text())
        assert hashlib.sha256(local.read_bytes()).hexdigest()==media['sha256']
        dest=OUT/f'{c}.json'
        if dest.exists():
            old=json.loads(dest.read_text())
            if old['sha256']==media['sha256']:
                print('Already byte-verified',c,old['url'],flush=True);continue
        output=call(['upload',str(local),'--folder-id',FOLDER,'--name',f'{c}字彩色筆順動畫.mp4','--replace'])
        (OUT/f'{c}-upload.txt').write_text(output)
        ids=re.findall(r'(?:ID:\s*|/file/d/)([-\w]+)',output)
        if not ids:raise ValueError('Cannot parse Drive ID: '+output)
        fid=ids[0];link=call(['link',fid]);(OUT/f'{c}-link.txt').write_text(link)
        downloaded=call(['download',fid,'--dest',str(READBACK),'--name',f'{c}.mp4'])
        remote=READBACK/f'{c}.mp4'
        assert remote.read_bytes()==local.read_bytes(),f'{c}: exact byte mismatch'
        record={'char':c,'id':fid,'folder_id':FOLDER,'url':f'https://drive.google.com/file/d/{fid}/view','bytes':local.stat().st_size,'sha256':media['sha256'],'exact_byte_readback':True,'connector':'registered gdrive.py upload --replace, link, download'}
        dest.write_text(json.dumps(record,ensure_ascii=False,indent=2))
        print(json.dumps(record,ensure_ascii=False),flush=True)
