#!/usr/bin/env python3
"""Build the standalone K3 stroke-order theme and its MP4 assets."""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
SITE = ROOT / "site"
SIZE = 1080
FPS = 30
SCALE = 0.90
DRAW_SECONDS = 2.0
PAUSE_SECONDS = 0.6
INTRO_SECONDS = 0.70
FINAL_SECONDS = 3.0
COLOURS = ["#E53935", "#1E63D5", "#111111", "#16A34A"]
RGB_COLOURS = np.array([[229, 57, 53], [30, 99, 213], [17, 17, 17], [22, 163, 74]], dtype=np.uint8)
BG = (255, 253, 247)
GHOST = np.array([232, 227, 216], dtype=np.uint8)
GRID = "#EEEEEE"

CHARACTERS = [
    {"char": "我", "edb_id": "1460", "bucket": "1001-2000", "target": [547.5, 550.5], "strokes": 7,
     "stroke_order": ["撇", "橫", "豎鈎", "提", "斜鈎", "撇", "點"]},
    {"char": "有", "edb_id": "1828", "bucket": "1001-2000", "target": [550.5, 534.7], "strokes": 6,
     "stroke_order": ["橫", "撇", "豎", "橫折鈎", "橫", "橫"]},
    {"char": "爸", "edb_id": "2456", "bucket": "2001-3000", "target": [555.3, 537.7], "strokes": 8,
     "stroke_order": ["撇", "點", "撇", "捺", "橫折", "豎", "橫", "豎彎鈎"]},
    {"char": "媽", "edb_id": "0948", "bucket": "0001-1000", "target": [522.5, 546.9], "strokes": 13,
     "stroke_order": ["撇點", "撇", "提", "橫", "豎", "橫", "橫", "豎", "橫折鈎", "點", "點", "點", "點"]},
    {"char": "姐", "edb_id": "0892", "bucket": "0001-1000", "target": [555.4, 537.1], "strokes": 8,
     "stroke_order": ["撇點", "撇", "提", "豎", "橫折", "橫", "橫", "橫"]},
    {"char": "妹", "edb_id": "0889", "bucket": "0001-1000", "target": [546.9, 547.4], "strokes": 8,
     "stroke_order": ["撇點", "撇", "提", "橫", "橫", "豎", "撇", "捺"]},
    {"char": "弟", "edb_id": "1238", "bucket": "1001-2000", "target": [539.8, 528.2], "strokes": 7,
     "stroke_order": ["點", "撇", "橫折", "橫", "豎折折鈎", "豎", "撇"]},
    {"char": "哥", "edb_id": "0581", "bucket": "0001-1000", "target": [552.3, 550.3], "strokes": 10,
     "stroke_order": ["橫", "豎", "橫折", "橫", "豎", "橫", "豎", "橫折", "橫", "豎鈎"]},
    {"char": "和", "edb_id": "0551", "bucket": "0001-1000", "target": [511.5, 550.2], "strokes": 8,
     "stroke_order": ["撇", "橫", "豎", "撇", "點", "豎", "橫折", "橫"]},
]

# New characters use the official EDB filled outlines AND reveal keyframes.
# Generic data is audited as a comparison only; it is not a production input.
ADDED_ORDERS = {
    '祖': '點 橫撇 豎 點 豎 橫折 橫 橫 橫',
    '父': '撇 點 撇 捺',
    '母': '豎折 橫折鈎 點 點 橫',
    '老': '橫 豎 橫 撇 撇 豎彎',
    '師': '撇 豎 橫折 橫 橫折 橫 橫 豎 橫折鈎 豎',
    '消': '點 點 提 豎 點 撇 豎 橫折鈎 橫 橫',
    '防': '橫撇 彎鈎 豎 點 橫 橫折鈎 撇',
    '員': '豎 橫折 橫 豎 橫折 橫 橫 橫 撇 點',
    '警': '橫 豎 橫 撇 撇 橫折鈎 豎 橫折 橫 撇 橫 撇 捺 點 橫 橫 橫 豎 橫折 橫',
    '察': '點 點 橫鈎 撇 橫撇 點 點 橫撇 捺 橫 橫 豎鈎 撇 點',
    '醫': '橫 撇 橫 橫 撇 點 豎折 撇 橫折彎 橫撇 捺 橫 豎 橫折 撇 豎彎 橫 橫',
    '生': '撇 橫 橫 豎 橫',
}
for _char, _order in ADDED_ORDERS.items():
    _source = json.loads((ROOT / 'sources' / f'{_char}.json').read_text())
    _source['stroke_order'] = _order.split()
    _source['geometry'] = 'official-edb'
    _source['mapping_1_based'] = list(range(1, _source['strokes'] + 1))
    assert len(_source['stroke_order']) == _source['strokes']
    CHARACTERS.append(_source)

# The expansion is rendered directly from each official EDB chronological
# reveal timeline.  Numbered labels avoid inventing stroke-type terminology:
# the frozen states are the authoritative order and shape evidence.
NEW_CHARACTERS = '們中國是人在香港北京長城鳥巢故宮慶節煙花萬里'
for _char in NEW_CHARACTERS:
    _source = json.loads((ROOT / 'sources' / f'{_char}.json').read_text())
    _source['stroke_order'] = [f'官方第{i}筆' for i in range(1, _source['strokes'] + 1)]
    _source['geometry'] = 'official-edb'
    _source['mapping_1_based'] = list(range(1, _source['strokes'] + 1))
    CHARACTERS.append(_source)


def colour_for(index: int) -> str:
    return COLOURS[index % 4]


def frame_count(strokes: int) -> int:
    return round(INTRO_SECONDS * FPS) + strokes * (round(DRAW_SECONDS * FPS) + round(PAUSE_SECONDS * FPS)) + round(FINAL_SECONDS * FPS)


def optical_translation(bounds: tuple[float, float, float, float], target: tuple[float, float]) -> tuple[float, float]:
    left, top, right, bottom = bounds
    return target[0] - (left + right) / 2, target[1] - (top + bottom) / 2


def data_path(char: str) -> Path:
    frozen = ROOT / 'sources' / 'geometry' / f'{ord(char):x}.json'
    if frozen.exists():
        return frozen
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{ord(char):x}.json"
    if not path.exists():
        url = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/" + urllib.parse.quote(char) + ".json"
        urllib.request.urlretrieve(url, path)
    return path


def screen_point(point, tx, ty):
    x, y = point
    return tx + x * SCALE, ty + (1024 - y) * SCALE


def dense(points, tx, ty, spacing=1.5):
    out = []
    total = sum(math.dist(a, b) for a, b in zip(points, points[1:]))
    travelled = 0.0
    for a, b in zip(points, points[1:]):
        segment = math.dist(a, b)
        count = max(1, math.ceil(segment / spacing))
        for step in range(count):
            raw = (a[0] + (b[0] - a[0]) * step / count, a[1] + (b[1] - a[1]) * step / count)
            out.append((screen_point(raw, tx, ty), (travelled + segment * step / count) / total))
        travelled += segment
    out.append((screen_point(points[-1], tx, ty), 1.0))
    return out


def raster_stroke(path_data: str, filename: Path, tx: float, ty: float) -> np.ndarray:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
<g transform="translate({tx},{ty + 1024 * SCALE}) scale({SCALE},-{SCALE})"><path d="{path_data}" fill="black"/></g></svg>'''
    svg_path = filename.with_suffix(".svg")
    png_path = filename.with_suffix(".png")
    svg_path.write_text(svg)
    subprocess.run(["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)], check=True, stdout=subprocess.DEVNULL)
    return np.asarray(Image.open(png_path).convert("RGBA"))[:, :, 3] > 10


def prepare_geometry(item: dict, work: Path):
    if item.get('geometry') == 'official-edb':
        from official_geometry import prepare
        return prepare(item)
    char = item["char"]
    data = json.loads(data_path(char).read_text())
    paths, medians = data["strokes"], data["medians"]
    if len(paths) != item["strokes"]:
        raise ValueError(f"{char}: expected {item['strokes']} strokes, got {len(paths)}")

    work.mkdir(parents=True, exist_ok=True)
    initial_tx = (SIZE - 1024 * SCALE) / 2
    initial_ty = (SIZE - 1024 * SCALE) / 2
    trial = [raster_stroke(path, work / f"trial-{i}", initial_tx, initial_ty) for i, path in enumerate(paths)]
    union = np.logical_or.reduce(trial)
    ys0, xs0 = np.nonzero(union)
    dx, dy = optical_translation((xs0.min(), ys0.min(), xs0.max(), ys0.max()), tuple(item["target"]))
    tx, ty = initial_tx + dx, initial_ty + dy

    masks, progress_maps = [], []
    for i, (path, median) in enumerate(zip(paths, medians)):
        mask = raster_stroke(path, work / f"stroke-{i}", tx, ty)
        ys, xs = np.nonzero(mask)
        samples = dense(median, tx, ty)
        points = np.array([point for point, _ in samples])
        progress = np.array([value for _, value in samples])
        _, nearest = cKDTree(points).query(np.column_stack((xs, ys)))
        progress_map = np.full((SIZE, SIZE), 2.0, dtype=np.float32)
        progress_map[ys, xs] = progress[nearest]
        masks.append(mask)
        progress_maps.append(progress_map)
    return masks, progress_maps


def render_character(item: dict, destination: Path) -> Path:
    """Stream RGB frames to ffmpeg; retain dense QA samples, not redundant PNGs."""
    work = CACHE / f"slow-{ord(item['char']):x}"
    work.mkdir(parents=True, exist_ok=True)
    masks, progress_maps = prepare_geometry(item, work)
    if len(masks) != item['strokes']:
        raise ValueError('Official stroke-count mismatch')
    base = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(base)
    draw.line((0, 0, SIZE, SIZE), fill=GRID, width=4)
    draw.line((SIZE, 0, 0, SIZE), fill=GRID, width=4)
    draw.line((SIZE // 2, 0, SIZE // 2, SIZE), fill=GRID, width=4)
    draw.line((0, SIZE // 2, SIZE, SIZE // 2), fill=GRID, width=4)
    draw.rectangle((2, 2, SIZE - 3, SIZE - 3), outline=GRID, width=4)
    base_array = np.array(base)
    for mask in masks:
        base_array[mask] = GHOST

    evidence_dir = ROOT / 'verification' / item['char']
    evidence_dir.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.rendering.mp4')
    command = ['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
               '-s',f'{SIZE}x{SIZE}','-r',str(FPS),'-i','-', '-an',
               '-c:v','libx264','-threads','4','-preset','fast','-crf','18',
               '-pix_fmt','yuv420p','-movflags','+faststart',str(temporary)]
    frame = 0
    samples = []
    process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def save(done, active=None, fraction=0.0, sample=None):
        nonlocal frame
        array = base_array.copy()
        for stroke in range(done):
            array[masks[stroke]] = RGB_COLOURS[stroke % 4]
        if active is not None:
            reveal = masks[active] & (progress_maps[active] <= fraction)
            array[reveal] = RGB_COLOURS[active % 4]
        if sample:
            path = evidence_dir / f'{sample}.png'
            Image.fromarray(array).save(path)
            samples.append({'file':path.name,'frame':frame,'time':frame/FPS})
        process.stdin.write(array.tobytes())
        frame += 1

    try:
        for _ in range(round(INTRO_SECONDS * FPS)):
            save(0)
        for stroke in range(len(masks)):
            drawing_frames = round(DRAW_SECONDS * FPS)
            for step in range(drawing_frames):
                sample = f's{stroke+1:02}-f{step+1:02}' if step in [5,17,29,41,53,59] else None
                save(stroke, stroke, (step + 1) / drawing_frames, sample)
            for _ in range(round(PAUSE_SECONDS * FPS)):
                save(stroke + 1)
        for hold in range(round(FINAL_SECONDS * FPS)):
            save(len(masks), sample='final' if hold == 0 else None)
        assert frame == frame_count(len(masks))
    except BaseException:
        process.stdin.close(); process.wait()
        temporary.unlink(missing_ok=True)
        raise
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError('ffmpeg encoding failed')
    temporary.replace(destination)
    (evidence_dir/'samples.json').write_text(json.dumps(samples,indent=2))
    return destination


def page_html() -> str:
    from ui import page_html as make_page
    return make_page(CHARACTERS)


def write_site(destination: Path = SITE, render_videos: bool = True):
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(page_html())
    (destination / "styles.css").write_text(CSS)
    (destination / "app.js").write_text(JS)
    (destination / "manifest.json").write_text(json.dumps({
        "themes": ["他們都愛我", "我愛中國"],
        "count": len(CHARACTERS),
        "characters": CHARACTERS,
    }, ensure_ascii=False, indent=2))
    if render_videos:
        for item in CHARACTERS:
            render_character(item, destination / "videos" / f"{item['char']}.mp4")


from ui import CSS, JS


if __name__ == "__main__":
    write_site()
