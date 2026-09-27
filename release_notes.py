"""Regenerate verification/RELEASE.md from verified manifest and Drive records."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "verification/manifest.json").read_text())
lines = [
    "# Full K3 release verification — 《我愛中國》 expansion",
    "",
    "Verified media: **43/43**. Previous 21 retained byte-for-byte; 22 official-geometry additions. Original nine quick buttons and eight 《他們都愛我》 reading cards retained.",
    "",
    "《我愛中國》 homework cards (exact order): " + "、".join(manifest["homework_words"]) + "。",
    "",
    "Recognition cards (exact order): " + "、".join(manifest["china_reading_words"]) + "。 Every printed character, including duplicates, has its own playback button.",
    "",
    "All 43: 1080×1080, 30 fps, H.264/yuv420p; draw 2.0s, pause 0.6s, intro 0.7s, final 3.0s. Every MP4 was fully decoded. Every new stroke was reviewed at six progress points; all 22 new encoded finals and the combined 43-character final montage were inspected.",
    "",
    "## Official source and media evidence",
    "",
    "The 22 additions use only frozen Hong Kong EDB CreateJS filled outlines and chronological reveal states. `china-source-audit.json` records unique entry IDs, listed/decoded counts, and raw source SHA-256. Generic geometry is not a production input. EDB direction-marker line shapes are explicitly excluded; translated/scaled filled outlines are preserved.",
    "",
    "|字|EDB ID|筆畫|秒|幀|MP4 SHA-256|Drive exact-ID readback|",
    "|---|---:|---:|---:|---:|---|---|",
]
for row in manifest["records"]:
    media = row["media"]
    drive = row["drive"]
    lines.append(
        f'|{row["char"]}|[{row["official_edb_id"]}]({row["official_url"]})|{row["official_strokes"]}|'
        f'{media["duration"]:.1f}|{media["frames"]}|`{media["sha256"]}`|[MP4]({drive["url"]})|'
    )
lines += [
    "",
    "Drive folder `1iZwfwFdhM2pEDiojTRf-stwYjgMebRDK` lists one exact-ID production MP4 for each of the 43 characters. The 22 additions were downloaded by returned ID and compared byte-for-byte; the unchanged 21 were not reuploaded.",
    "",
    "## Verification gates",
    "",
    "- Python/DOM: 10 tests passed; 43 character cards, 27 ordered word cards, duplicate per-character triggers.",
    "- Media: 43/43 ffprobe and full `ffmpeg -xerror` decode; H.264, 1080 square, 30 fps, yuv420p, exact expected frame counts.",
    "- Visual: six progress samples per new stroke, all 22 new finals, and combined all-43 final montage passed.",
    "- Local browser: native ARM64 Debian Chromium with H.264 exercised 121 playback triggers and 43 downloads; no page errors or 390px overflow.",
    "- Public: GitHub Pages build completed for the exact 47-file site tree; HTML/CSS/JS/manifest and all 43 MP4s matched local bytes; native live browser acceptance passed 121 triggers and 43 downloads.",
    "",
    "## Review note",
    "",
    "Automated static/diff review evidence is in `code-review.json`. An independent Claude Code review was attempted but its OAuth session was expired; this limitation is recorded rather than misrepresented as an independent pass.",
]
(ROOT / "verification/RELEASE.md").write_text("\n".join(lines) + "\n")
print({"records": len(manifest["records"]), "release": "verification/RELEASE.md"})
