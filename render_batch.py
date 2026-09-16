"""Durable per-character render/ffprobe/decode evidence and visual review sheets."""
import json,subprocess,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw
import build
ROOT=Path(__file__).resolve().parent

def verify(item):
    char=item['char'];work=ROOT/'verification'/char;video=ROOT/'site/videos'/f'{char}.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    st=probe['streams'][0];expected=build.frame_count(item['strokes'])
    assert st['codec_name']=='h264' and st['width']==1080 and st['height']==1080
    assert st['pix_fmt']=='yuv420p' and st['r_frame_rate']=='30/1' and int(st['nb_frames'])==expected
    assert abs(float(st['duration'])-expected/30)<0.002
    decode=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],capture_output=True,text=True,check=True)
    assert not decode.stderr,decode.stderr
    samples=json.loads((work/'samples.json').read_text())
    # Read encoded final and in-progress frames, not only source RGB images.
    times=[samples[2]['time'],samples[-1]['time']]
    for name,t in zip(['decoded-progress','decoded-final'],times):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(work/f'{name}.png')],check=True)
    sheet=Image.new('RGB',(6*180,item['strokes']*200),'white');d=ImageDraw.Draw(sheet)
    for s in range(1,item['strokes']+1):
        for col,f in enumerate([6,18,30,42,54,60]):
            p=work/f's{s:02}-f{f:02}.png';x=col*180;y=(s-1)*200
            sheet.paste(Image.open(p).convert('RGB').resize((180,180)),(x,y))
            d.text((x+4,y+182),f'{s}: {f}/60',fill='black')
    sheet.save(work/'progress-sheet.jpg',quality=90)
    record={'char':char,'strokes':item['strokes'],'path':str(video.relative_to(ROOT)),'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':expected,'duration':float(st['duration']),'codec':st['codec_name'],'width':1080,'height':1080,'fps':'30/1','pix_fmt':'yuv420p','decode':'all frames passed ffmpeg -xerror','timing':{'intro':.7,'draw':2,'pause':.6,'final':3},'samples':len(samples),'visual_review':'pending'}
    (work/'media.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    print(json.dumps(record,ensure_ascii=False),flush=True)
    return record

if __name__=='__main__':
    for c in sys.argv[1]:
        item=next(i for i in build.CHARACTERS if i['char']==c)
        if '--verify-only' not in sys.argv:build.render_character(item,ROOT/'site/videos'/f'{c}.mp4')
        verify(item)
