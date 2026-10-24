# K3 中文筆順播放器

Live: https://superpp1129.github.io/k3-chinese-stroke-player/

The site now contains **109 distinct characters**. It preserves the earlier themes, then adds visually distinct 《拯救小海豚》 and 《小巴的願望》 sections.

## 《我愛中國》 cards

Homework cards, exact order: 我們、中國、我們是中國人、在、香港、我們在香港、北京、有、長城、北京有長城、鳥巢、故宮、北京有故宮。

Recognition cards, exact order: 國慶節、煙花、中國、北京、故宮、萬里長城。

## 《起飛吧！得得》 cards

Homework cards, exact order: 玉米、真、美味、玉米真美味、有益、的、白菜、有益的白菜、一起、吃、米飯、我們一起吃米飯。

Recognition cards, exact order: 早睡早起、跳舞、跑步、游泳、踢球、踏單車。

## 《拯救小海豚》 cards

Homework cards follow the verified 2026-2027 final plan, in order: 海洋裏、海豚、鯨魚、我們要保護海洋。

Recognition cards follow the parent handbook, in order: 動物園、大熊貓、獅子、大象、老虎、猴子、海洋、海豚。

## 《小巴的願望》 cards

Homework cards follow the verified final plan, not the superseded 「大象和老虎」 wording. Exact order: 馬路、旁邊、公園、朋友、玩耍、我和朋友玩耍。

Recognition cards, exact order: 友善、鄰居、我們、好朋友、公園、社區、學校、圖書館。

English words, workbook names and number-book page ranges are not stroke cards. Every printed Chinese character in every word card is an individual playback button. All 109 character cards have playback and MP4 download controls. Playback is silent.

## Approved animation format

Every stroke draws for 2.0 seconds, then pauses 0.6 seconds. Intro 0.7 seconds; final hold 3.0 seconds. All videos are 1080×1080, 30 fps, H.264/yuv420p, fast-start MP4. The fixed colour cycle is red → blue → black → green, with a pale ghost character and 米字格.

## Hong Kong EDB authority

Hong Kong EDB 《香港小學學習字詞表》 sources are frozen under `sources/`. The 22 《我愛中國》 additions use the official CreateJS full filled outlines and chronological reveal states only—not generic Hanzi geometry. Acquisition records the exact EDB entry ID, official listed stroke count, source URL, and raw JavaScript SHA-256. `verification/china-source-audit.json` confirms that every listed count equals the decoded chronological timeline count and that every filled source state reconstructs exactly.

The previous 12 official-geometry additions remain unchanged. The original nine retain their previously approved frozen outlines and mappings.

## Build and test

Requirements: Python, Node, ffmpeg/ffprobe, macOS `sips`, NumPy, Pillow, SciPy. On this Mac, uv is `/Users/claudeuser/.hermes/bin/uv`.

```sh
uv venv .venv
uv pip install --python .venv/bin/python3 numpy pillow scipy
source .venv/bin/activate
npm ci
PATH="$PWD/.venv/bin:$PATH" npm test
python -c 'import build; build.write_site(render_videos=False)'
```

`python build.py` renders all videos. Durable new-character batches:

```sh
python render_batch.py 們中國是人在香港北京長
python render_batch.py 城鳥巢故宮慶節煙花萬里
```

`python consolidate.py` fails closed unless all 43 media files, visual approvals, official metadata, current hashes, and Drive records agree.

## Browser acceptance

`browser_acceptance.py [url]` checks actual H.264 playback advancement, all 121 playback triggers, all 43 downloads, modal controls, phone layout, and page errors. A bundled ARM headless shell may omit H.264, so the verified fallback is native ARM64 Debian Chromium with Noto CJK fonts:

```sh
docker build -t k3-browser-acceptance /Users/claudeuser/projects/k3-browser-acceptance
docker run --rm --platform linux/arm64 \
  -v "$PWD:/work:ro" \
  -v "$PWD/verification:/work/verification" \
  -v /Users/claudeuser/projects/k3-browser-acceptance/run.py:/runner.py:ro \
  k3-browser-acceptance /runner.py
```

Pass the public URL after `/runner.py` for the live check. The external Docker helper directory is intentionally not committed.

## Evidence and publication

- `verification/<字>/media.json`: ffprobe, complete decode, frame count, output hash, visual disposition.
- `verification/<字>/progress-sheet.jpg`: six samples for every stroke; `decoded-final.png` and `decoded-progress.png` are decoded MP4 frames.
- `verification/china-progress-1.jpg` … `china-progress-6.jpg`: all new progress sheets at review resolution.
- `verification/china-final22-review.jpg`, `encoded-all43-review.jpg`: new and combined final-state reviews.
- `verification/manifest.json`: consolidated source, media, Drive, cards, timings, and hashes.
- `verification/drive/*.json`: returned Drive IDs and exact downloaded-byte equality. Folder: https://drive.google.com/drive/folders/1iZwfwFdhM2pEDiojTRf-stwYjgMebRDK
- `publish_drive.py`: authorized connector upload/replacement plus exact-ID download; the unchanged previous 21 were not reuploaded.
- `verification/ui-local.json`, `ui-live.json`, `public-readback.json`: native browser and exact public-byte acceptance.

Source development uses `develop`; GitHub Pages serves the exact `site/` tree from `gh-pages` at repository root.
