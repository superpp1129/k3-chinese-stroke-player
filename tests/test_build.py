import json
import tempfile
import unittest
from pathlib import Path

import build


class StrokeSiteTests(unittest.TestCase):
    def test_theme_has_exact_requested_character_order(self):
        self.assertEqual([item["char"] for item in build.CHARACTERS], list("我有爸媽姐妹弟哥和"))

    def test_frame_count_uses_approved_k3_timing(self):
        self.assertEqual(build.frame_count(6), 333)
        self.assertEqual(build.frame_count(8), 417)

    def test_colour_cycle_repeats_every_four_strokes(self):
        self.assertEqual([build.colour_for(i) for i in range(9)], [
            "#E53935", "#1E63D5", "#111111", "#16A34A",
            "#E53935", "#1E63D5", "#111111", "#16A34A", "#E53935",
        ])

    def test_optical_translation_places_bounds_on_edb_target(self):
        tx, ty = build.optical_translation((100, 200, 700, 800), (550, 535))
        self.assertEqual((tx, ty), (150, 35))

    def test_generated_site_has_one_card_and_download_per_character(self):
        with tempfile.TemporaryDirectory() as tmp:
            build.write_site(Path(tmp), render_videos=False)
            page = (Path(tmp) / "index.html").read_text()
            self.assertEqual(page.count('class="character-card"'), 9)
            self.assertEqual(page.count('download='), 9)
            self.assertIn("他們都愛我", page)
            self.assertIn("aria-label=\"播放「我」字筆順\"", page)

    def test_manifest_records_edb_source_for_every_character(self):
        for item in build.CHARACTERS:
            self.assertRegex(item["edb_id"], r"^\d{4}$")
            self.assertEqual(item["strokes"], len(item["stroke_order"]))


if __name__ == "__main__":
    unittest.main()
