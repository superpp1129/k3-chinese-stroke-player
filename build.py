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
DRAW_SECONDS = 1.15
PAUSE_SECONDS = 0.28
INTRO_SECONDS = 0.70
FINAL_SECONDS = 2.0
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
     "stroke_order": ["橫", "豎", "橫折", "橫", "豎鈎", "橫", "豎", "橫折", "橫", "豎鈎"]},
    {"char": "和", "edb_id": "0551", "bucket": "0001-1000", "target": [511.5, 550.2], "strokes": 8,
     "stroke_order": ["撇", "橫", "豎", "撇", "點", "豎", "橫折", "橫"]},
]


def colour_for(index: int) -> str:
    return COLOURS[index % 4]


def frame_count(strokes: int) -> int:
    return round(INTRO_SECONDS * FPS) + strokes * (round(DRAW_SECONDS * FPS) + round(PAUSE_SECONDS * FPS)) + round(FINAL_SECONDS * FPS)


def optical_translation(bounds: tuple[float, float, float, float], target: tuple[float, float]) -> tuple[float, float]:
    left, top, right, bottom = bounds
    return target[0] - (left + right) / 2, target[1] - (top + bottom) / 2


def data_path(char: str) -> Path:
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


def render_character(item: dict, destination: Path) -> Path:
    char = item["char"]
    data = json.loads(data_path(char).read_text())
    paths, medians = data["strokes"], data["medians"]
    if len(paths) != item["strokes"]:
        raise ValueError(f"{char}: expected {item['strokes']} strokes, got {len(paths)}")

    work = CACHE / f"render-{ord(char):x}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
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

    frames = work / "frames"
    frames.mkdir()
    frame = 0

    def save(done, active=None, fraction=0.0):
        nonlocal frame
        array = base_array.copy()
        for stroke in range(done):
            array[masks[stroke]] = RGB_COLOURS[stroke % 4]
        if active is not None:
            reveal = masks[active] & (progress_maps[active] <= fraction)
            array[reveal] = RGB_COLOURS[active % 4]
        Image.fromarray(array).save(frames / f"frame_{frame:05d}.png", optimize=True)
        frame += 1

    for _ in range(round(INTRO_SECONDS * FPS)):
        save(0)
    for stroke in range(len(paths)):
        drawing_frames = round(DRAW_SECONDS * FPS)
        for step in range(drawing_frames):
            save(stroke, stroke, (step + 1) / drawing_frames)
        for _ in range(round(PAUSE_SECONDS * FPS)):
            save(stroke + 1)
    for _ in range(round(FINAL_SECONDS * FPS)):
        save(len(paths))
    assert frame == frame_count(len(paths))

    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "frame_%05d.png"),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(destination)], check=True)
    return destination


def page_html() -> str:
    cards = []
    for item in CHARACTERS:
        char = item["char"]
        filename = f"videos/{char}.mp4"
        cards.append(f'''<article class="character-card">
<button class="character-button" data-video="{filename}" data-char="{char}" aria-label="播放「{char}」字筆順">
<span class="character">{char}</span><span class="play-mark">▶ 播放筆順</span></button>
<a class="download" href="{filename}" download="{char}字彩色筆順動畫.mp4">↓ 下載影片</a>
</article>''')
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>他們都愛我｜中文筆順播放器</title><link rel="stylesheet" href="styles.css"></head><body>
<header><p class="eyebrow">K3 中文筆順播放器</p><h1>他們都愛我</h1><p class="intro">揀一個字，睇清楚每一筆。</p></header>
<main><section class="character-grid" aria-label="生字">{''.join(cards)}</section></main>
<dialog id="player"><div class="dialog-top"><div><span class="small">正在播放</span><strong id="current-char"></strong></div><button id="close" aria-label="關閉">×</button></div>
<video id="video" controls playsinline preload="metadata"></video><div class="dialog-actions"><button id="replay">↻ 重新播放</button><a id="dialog-download" download>↓ 下載影片</a></div></dialog>
<script src="app.js"></script></body></html>'''


def write_site(destination: Path = SITE, render_videos: bool = True):
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(page_html())
    (destination / "styles.css").write_text(CSS)
    (destination / "app.js").write_text(JS)
    (destination / "manifest.json").write_text(json.dumps({"theme": "他們都愛我", "characters": CHARACTERS}, ensure_ascii=False, indent=2))
    if render_videos:
        for item in CHARACTERS:
            render_character(item, destination / "videos" / f"{item['char']}.mp4")


CSS = r''':root{--ink:#202020;--muted:#6f6b64;--paper:#fffdf7;--line:#ece8de;--accent:#e53935}*{box-sizing:border-box}body{margin:0;background:#f7f3eb;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC","PingFang HK",sans-serif}header{max-width:980px;margin:auto;padding:58px 24px 28px;text-align:center}.eyebrow{margin:0 0 10px;color:#a24735;font-size:15px;font-weight:750;letter-spacing:.16em}h1{margin:0;font-size:clamp(38px,7vw,64px);letter-spacing:.08em}.intro{margin:14px 0 0;color:var(--muted);font-size:18px}main{max-width:980px;margin:auto;padding:10px 24px 64px}.character-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.character-card{overflow:hidden;border:1px solid var(--line);border-radius:22px;background:white;box-shadow:0 8px 25px rgba(73,61,43,.06)}.character-button{display:flex;width:100%;min-height:210px;border:0;background:var(--paper);cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:16px}.character-button:hover,.character-button:focus-visible{background:#fff8e9;outline:3px solid #f6cf72;outline-offset:-3px}.character{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;font-size:100px;line-height:1}.play-mark{font-size:15px;font-weight:700;color:#765f4e}.download{display:block;padding:15px;text-align:center;text-decoration:none;color:#3f6296;font-weight:750;border-top:1px solid var(--line)}.download:hover{background:#f5f8fc}dialog{width:min(92vw,720px);border:0;border-radius:24px;padding:0;box-shadow:0 30px 90px #28231c55;background:white}dialog::backdrop{background:#27221dbd}.dialog-top{display:flex;align-items:center;justify-content:space-between;padding:18px 22px}.dialog-top>div{display:flex;align-items:baseline;gap:12px}.small{color:var(--muted)}#current-char{font-size:28px}#close{border:0;background:#f1eee7;border-radius:50%;width:44px;height:44px;font-size:30px;cursor:pointer}video{display:block;width:100%;aspect-ratio:1;background:var(--paper)}.dialog-actions{display:flex;gap:12px;padding:16px 20px 20px}.dialog-actions>*{flex:1;padding:14px;border-radius:12px;border:1px solid var(--line);background:white;color:var(--ink);text-align:center;text-decoration:none;font-size:16px;font-weight:750;cursor:pointer}@media(max-width:650px){header{padding-top:34px}.character-grid{grid-template-columns:repeat(2,1fr);gap:12px}.character-button{min-height:170px}.character{font-size:80px}main{padding-inline:14px}.dialog-actions{flex-direction:column}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}'''

JS = r'''const dialog=document.querySelector('#player');const video=document.querySelector('#video');const label=document.querySelector('#current-char');const download=document.querySelector('#dialog-download');document.querySelectorAll('.character-button').forEach(button=>button.addEventListener('click',()=>{const src=button.dataset.video;label.textContent=button.dataset.char;video.src=src;download.href=src;download.download=`${button.dataset.char}字彩色筆順動畫.mp4`;dialog.showModal();video.play();}));document.querySelector('#close').addEventListener('click',()=>{video.pause();dialog.close();});document.querySelector('#replay').addEventListener('click',()=>{video.currentTime=0;video.play();});dialog.addEventListener('click',event=>{if(event.target===dialog){video.pause();dialog.close();}});'''


if __name__ == "__main__":
    write_site()
