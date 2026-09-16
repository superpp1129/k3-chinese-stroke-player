"""Page markup, styling and player behaviour for the K3 stroke-order site.

build.py owns the MP4s; this module owns everything the browser sees. Each
character only needs its ``char`` here — the stroke metadata stays with the
renderer — so the UI can be generated and tested without any render step.
"""
from __future__ import annotations

from pathlib import Path

THEME = "他們都愛我"
# The 21 taught characters, in the approved teaching order.
CHARACTER_ORDER = "我有爸媽姐妹弟哥和祖父母老師消防員警察醫生"
# The original nine of the first theme, kept one tap away at the top.
THEME_CHARACTERS = "我有爸媽姐妹弟哥和"
# Reading words; every character is played individually, duplicates included.
WORDS = ("爸爸", "媽媽", "祖父", "祖母", "老師", "消防員", "警察", "醫生")
ORDINALS = "一二三四"


def video_path(char: str) -> str:
    return f"videos/{char}.mp4"


def download_name(char: str) -> str:
    return f"{char}字彩色筆順動畫.mp4"


def _ordered(characters) -> list[str]:
    """Canonical teaching order, de-duplicated; unknown characters keep their place at the end."""
    seen = []
    for item in characters:
        char = item["char"] if isinstance(item, dict) else item
        if char not in seen:
            seen.append(char)
    known = [c for c in CHARACTER_ORDER if c in seen]
    return known + [c for c in seen if c not in CHARACTER_ORDER]


def _character_card(char: str) -> str:
    src = video_path(char)
    return (f'<article class="character-card">'
            f'<button class="character-button" data-video="{src}" data-char="{char}" aria-label="播放「{char}」字筆順">'
            f'<span class="character">{char}</span><span class="play-mark">▶ 播放筆順</span></button>'
            f'<a class="download" href="{src}" download="{download_name(char)}">↓ 下載影片</a></article>')


def _quick_button(char: str) -> str:
    return (f'<button class="quick-button" data-video="{video_path(char)}" data-char="{char}" '
            f'aria-label="快速播放「{char}」字筆順">{char}</button>')


def _word_card(word: str) -> str:
    parts = "".join(
        f'<button class="word-button" data-video="{video_path(char)}" data-char="{char}" data-word="{word}" '
        f'aria-label="播放「{word}」第{ORDINALS[index]}個字「{char}」筆順">{char}</button>'
        for index, char in enumerate(word))
    return (f'<article class="word-card" data-word="{word}">'
            f'<p class="word">{word}</p>'
            f'<div class="word-parts">{parts}</div></article>')


def page_html(characters) -> str:
    """Full index.html for the given characters (dicts with a "char", or bare characters)."""
    chars = _ordered(characters)
    required = list(THEME_CHARACTERS) + [c for word in WORDS for c in word]
    missing = sorted({c for c in required if c not in chars})
    if missing:
        raise ValueError(f"missing characters needed by the page: {''.join(missing)}")
    cards = "".join(_character_card(char) for char in chars)
    quick = "".join(_quick_button(char) for char in THEME_CHARACTERS)
    words = "".join(_word_card(word) for word in WORDS)
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{THEME}｜中文筆順播放器</title><link rel="stylesheet" href="styles.css"></head><body>
<header><p class="eyebrow">K3 中文筆順播放器</p><h1>{THEME}</h1><p class="intro">揀一個字，睇清楚每一筆。</p></header>
<main>
<section class="panel" aria-labelledby="theme-title"><h2 class="panel-title" id="theme-title">{THEME}</h2>
<p class="panel-note">主題九個字，一撳就睇到。</p><div class="quick-row">{quick}</div></section>
<section class="panel" aria-labelledby="words-title"><h2 class="panel-title" id="words-title">讀詞語</h2>
<p class="panel-note">讀成個詞，再逐個字睇筆順。</p><div class="word-grid">{words}</div></section>
<section class="panel" aria-labelledby="all-title"><h2 class="panel-title" id="all-title">全部生字（{len(chars)}）</h2>
<p class="panel-note">每個字都可以播放同下載。</p><div class="character-grid">{cards}</div></section>
</main>
<dialog id="player" aria-labelledby="current-char"><div class="dialog-top"><div><span class="small">正在播放</span><span class="small" id="current-word"></span><strong id="current-char"></strong></div><button id="close" aria-label="關閉">×</button></div>
<video id="video" controls playsinline preload="metadata"></video><div class="dialog-actions"><button id="replay">↻ 重新播放</button><a id="dialog-download" download>↓ 下載影片</a></div></dialog>
<script src="app.js"></script></body></html>'''


def write_ui(destination: Path, characters) -> None:
    """Write index.html, styles.css and app.js into destination."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(page_html(characters), encoding="utf-8")
    (destination / "styles.css").write_text(CSS, encoding="utf-8")
    (destination / "app.js").write_text(JS, encoding="utf-8")


CSS = r''':root{--ink:#202020;--muted:#6f6b64;--paper:#fffdf7;--line:#ece8de;--accent:#e53935}*{box-sizing:border-box}body{margin:0;background:#f7f3eb;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC","PingFang HK",sans-serif}
header{max-width:980px;margin:auto;padding:58px 24px 22px;text-align:center}.eyebrow{margin:0 0 10px;color:#a24735;font-size:15px;font-weight:750;letter-spacing:.16em}h1{margin:0;font-size:clamp(38px,7vw,64px);letter-spacing:.08em}.intro{margin:14px 0 0;color:var(--muted);font-size:18px}
main{max-width:980px;margin:auto;padding:10px 24px 64px}.panel{margin:0 0 42px}.panel-title{margin:0;font-size:24px;letter-spacing:.06em}.panel-note{margin:6px 0 16px;color:var(--muted);font-size:16px}
.quick-row{display:flex;flex-wrap:wrap;gap:12px}.quick-button{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;line-height:1;width:84px;height:84px;font-size:44px;border:1px solid var(--line);border-radius:20px;background:var(--paper);color:var(--ink);cursor:pointer;box-shadow:0 6px 18px rgba(73,61,43,.06)}
.word-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.word-card{padding:18px;border:1px solid var(--line);border-radius:22px;background:white;box-shadow:0 8px 25px rgba(73,61,43,.06);text-align:center}.word{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;line-height:1;margin:0 0 14px;font-size:46px;letter-spacing:.06em}
.word-parts{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}.word-button{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;line-height:1;width:66px;height:66px;font-size:34px;border:1px solid var(--line);border-radius:16px;background:var(--paper);color:var(--ink);cursor:pointer}
.character-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.character-card{overflow:hidden;border:1px solid var(--line);border-radius:22px;background:white;box-shadow:0 8px 25px rgba(73,61,43,.06)}.character-button{display:flex;width:100%;min-height:210px;border:0;background:var(--paper);cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.character{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;line-height:1;font-size:100px}.play-mark{font-size:15px;font-weight:700;color:#765f4e}
.character-button:hover,.character-button:focus-visible,.quick-button:hover,.quick-button:focus-visible,.word-button:hover,.word-button:focus-visible{background:#fff8e9;outline:3px solid #f6cf72;outline-offset:-3px}
.download{display:block;padding:15px;text-align:center;text-decoration:none;color:#3f6296;font-weight:750;border-top:1px solid var(--line)}.download:hover{background:#f5f8fc}
dialog{width:min(92vw,720px);border:0;border-radius:24px;padding:0;box-shadow:0 30px 90px #28231c55;background:white}dialog::backdrop{background:#27221dbd}.dialog-top{display:flex;align-items:center;justify-content:space-between;padding:18px 22px}.dialog-top>div{display:flex;align-items:baseline;gap:12px}.small{color:var(--muted)}#current-word:empty{display:none}#current-char{font-family:"Kaiti TC","BiauKai","DFKai-SB",serif;font-size:28px}#close{border:0;background:#f1eee7;border-radius:50%;width:44px;height:44px;font-size:30px;cursor:pointer}
video{display:block;width:100%;aspect-ratio:1;background:var(--paper)}.dialog-actions{display:flex;gap:12px;padding:16px 20px 20px}.dialog-actions>*{flex:1;padding:14px;border-radius:12px;border:1px solid var(--line);background:white;color:var(--ink);text-align:center;text-decoration:none;font-size:16px;font-weight:750;cursor:pointer}
@media(max-width:650px){header{padding-top:34px}.character-grid,.word-grid{grid-template-columns:repeat(2,1fr);gap:12px}.character-button{min-height:170px}.character{font-size:80px}.word{font-size:38px}.quick-button{width:72px;height:72px;font-size:38px}.word-button{width:56px;height:56px;font-size:28px}main{padding-inline:14px}.dialog-actions{flex-direction:column}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}'''

JS = r'''(function(){
const dialog=document.querySelector('#player');
const video=document.querySelector('#video');
const charLabel=document.querySelector('#current-char');
const wordLabel=document.querySelector('#current-word');
const download=document.querySelector('#dialog-download');
function stop(){video.pause();video.currentTime=0;}
function start(){const played=video.play();if(played&&played.catch)played.catch(function(){});}
function open(button){
  stop();
  const src=button.dataset.video;const char=button.dataset.char;
  charLabel.textContent=char;
  wordLabel.textContent=button.dataset.word||'';
  video.src=src;
  download.href=src;
  download.setAttribute('download',char+'字彩色筆順動畫.mp4');
  if(!dialog.open)dialog.showModal();
  start();
}
document.addEventListener('click',function(event){
  const target=event.target.closest&&event.target.closest('[data-video]');
  if(target)open(target);
});
document.querySelector('#replay').addEventListener('click',function(){video.currentTime=0;start();});
document.querySelector('#close').addEventListener('click',function(){dialog.close();});
dialog.addEventListener('click',function(event){if(event.target===dialog)dialog.close();});
dialog.addEventListener('close',stop);
})();'''
