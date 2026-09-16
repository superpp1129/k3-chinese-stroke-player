"""Exact EDB outlines and source-keyframe-directed smooth reveals.

No generic stroke segmentation is used. Source animation states are decoded
without executing downloaded JavaScript. New pixels advance from the preceding
EDB reveal contour, clipped to the official completed stroke.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt

ROOT=Path(__file__).resolve().parent

def progress_from_states(states):
    final=states[-1]
    if len(states)<2 or not final.any():raise ValueError('At least two official states required')
    # EDB's hand-drawn intermediate contours have tiny non-nested edge changes.
    # Clip them to the final silhouette and keep all already revealed pixels.
    cumulative=[];seen=np.zeros_like(final)
    for state in states:
        seen=seen | (state & final);cumulative.append(seen.copy())
    first=cumulative[0]
    ys,xs=np.nonzero(first)
    added=cumulative[1]&~first
    ay,ax=np.nonzero(added)
    if not len(ax):raise ValueError('Official first two states do not advance')
    direction=np.array([ax.mean()-xs.mean(),ay.mean()-ys.mean()])
    norm=np.linalg.norm(direction)
    if norm<1e-6:raise ValueError('Ambiguous official initial direction')
    direction/=norm
    projection=xs*direction[0]+ys*direction[1]
    local=projection-projection.min()+0.01
    progress=np.full(final.shape,np.inf,np.float32)
    length=float(local.max());progress[ys,xs]=local
    thresholds=[length]
    for previous,state in zip(cumulative,cumulative[1:]):
        new=state&~previous
        distances=distance_transform_edt(~previous)
        step=float(distances[new].max()) if new.any() else 0
        progress[new]=length+distances[new]
        length+=step;thresholds.append(length)
    progress[final]/=length
    return final,progress,[float(np.nextafter(np.float32(v/length), np.float32(np.inf))) for v in thresholds]

def prepare(item):
    from audit_geometry import shapes_for,official_mask
    char=item['char'];record=json.loads((ROOT/'sources'/f'{char}.json').read_text())
    work=ROOT/'verification'/char;work.mkdir(exist_ok=True)
    shapes=shapes_for(record);masks=[];maps=[];evidence=[]
    for i,timeline in enumerate(record['official_timeline']):
        states=[]
        for j,names in enumerate(timeline['states']):
            dest=work/f'key-{i+1:02}-{j+1:02}'
            if dest.with_suffix('.png').exists():
                state=np.asarray(Image.open(dest.with_suffix('.png')).convert('RGBA'))[:,:,3]>10
            else:state=official_mask(shapes,names,dest)
            states.append(state)
        mask,progress,thresholds=progress_from_states(states)
        masks.append(mask);maps.append(progress)
        cumulative=np.zeros_like(mask);checks=[]
        for state,t in zip(states,thresholds):
            cumulative |= state & mask
            # float32 rounding at the threshold is bounded by one ULP.
            reconstructed=mask & (progress <= t+1e-6)
            checks.append(int(np.count_nonzero(cumulative ^ reconstructed)))
        if any(checks):raise ValueError(f'{char} stroke{i+1}: keyframe mismatch {checks}')
        evidence.append({'stroke':i+1,'final_shapes':timeline['states'][-1],'source_states':timeline['states'],'thresholds':thresholds,'keyframe_difference_pixels':checks,'pixels':int(mask.sum())})
    report={'character':char,'source_url':record['source_url'],'source_sha256':record['source_sha256'],'geometry':'EDB CreateJS full filled outlines, original 1080 coordinates','mapping':'Identity: chronological EDB timeline -> rendered stroke','strokes':evidence}
    (work/'official-reveal.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return masks,maps
