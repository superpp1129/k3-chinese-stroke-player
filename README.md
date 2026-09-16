# K3 中文筆順播放器

Live: https://superpp1129.github.io/k3-chinese-stroke-player/

21 individual characters: 我、有、爸、媽、姐、妹、弟、哥、和、祖、父、母、老、師、消、防、員、警、察、醫、生。

Eight reading cards: 爸爸、媽媽、祖父、祖母、老師、消防員、警察、醫生。Each printed character has its own playback button. Original nine quick-access buttons, individual cards and MP4 downloads remain available. Playback is silent (not text-to-speech).

## Approved timing

Every stroke draws for 2 seconds, then pauses 0.6 seconds. Intro 0.7 seconds; final hold 3 seconds. All videos: 1080×1080, 30 fps, H.264/yuv420p, fast-start MP4. Fixed red → blue → black → green cycle, pale ghost character and 米字格.

## Sources and regional correctness

Hong Kong EDB 《香港小學學習字詞表》 official 1080 animation sources are frozen under `sources/`, with entry IDs, SHA-256 and chronological stroke states. The 12 additions use the **official filled outlines and reveal states**, not assumed generic Hanzi Writer data. This matters especially for 防 (7 strokes) and 警 (20 strokes), where generic segmentation differs.

The existing nine keep their previously approved filled geometry, frozen under `sources/geometry`, checked against EDB and rendered again at the approved slower speed. `verification/manifest.json` records every mapping and output hash. `comparison.jpg`/`mapping.json` are diagnostic automated overlap comparisons, **not authoritative production remaps**; production mappings and manual dispositions are in the consolidated manifest and visual-review report.

## Build and test

Requirements: Python, Node, ffmpeg/ffprobe, macOS `sips`, NumPy, Pillow, SciPy. On the current Mac, uv is `/Users/claudeuser/.hermes/bin/uv`.

```sh
uv venv .venv
uv pip install --python .venv/bin/python3 numpy pillow scipy
source .venv/bin/activate
npm ci
npm test
python -c 'import build; build.write_site(render_videos=False)'
python -m http.server 8877 --directory site
```

`python build.py` renders all videos. Durable batches: `python render_batch.py 祖父母老師消`; existing verified files: `python render_batch.py 防警 --verify-only`. `python consolidate.py` asserts all21 coverage, timings, current SHA-256 and visual approvals.

Native browser acceptance: install Python Playwright and an H.264-capable browser, then run `python browser_acceptance.py [url]`. Set `BROWSER_EXECUTABLE` to use an explicit installed browser (for example `/usr/bin/chromium`). The verified fallback for a headless macOS service is native ARM64 Debian Chromium in Docker, with CJK fonts; a bundled Chromium headless shell may lack H.264 support, and x86 emulation is not a reliable substitute. Native acceptance exercises all47 playback triggers and all21 download links at desktop and phone sizes. See `verification/ui-local.json` / `ui-live.json`; failed browser launches or unsupported-codec errors are not UI passes.

## Evidence and publication

- `verification/<字>/media.json`: ffprobe, full decode, frame count, output hash, visual disposition.
- `verification/<字>/progress-sheet.jpg`: six samples for every stroke; `decoded-final.png` and `decoded-progress.png`: actual encoded video frames.
- `verification/visual-review.json`: all21 visual review decisions.
- `verification/parent-independent-review.json`, `parent-independent-media.json`: independent review/test/media checks.
- `verification/drive/*.json`: exact Drive IDs and full downloaded-byte equality to local videos. Theme folder: https://drive.google.com/drive/folders/1iZwfwFdhM2pEDiojTRf-stwYjgMebRDK
- `publish_drive.py`: uses the existing authorized Claude Tools connector, never credential copies; same-name replacement and exact-ID readback.

The source branch is `develop`; existing GitHub Pages uses `gh-pages` at repository root. Publish the verified `site/` tree only after media, visual, code and browser gates pass, then compare all21 public MP4 bytes to the local hashes. No framework or third-party runtime API is needed by the site.
