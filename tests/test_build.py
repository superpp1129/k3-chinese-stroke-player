import json
import tempfile
import unittest
from pathlib import Path

import build
import ui


class StrokeSiteTests(unittest.TestCase):
    def test_theme_has_exact_requested_character_order(self):
        self.assertEqual(
            [item["char"] for item in build.CHARACTERS],
            list("我有爸媽姐妹弟哥和祖父母老師消防員警察醫生們中國是人在香港北京長城鳥巢故宮慶節煙花萬里玉米真美味益的白菜一起吃飯早睡跳舞跑步游泳踢球踏單車馬路旁邊公園朋玩耍友善居鄰社區學校圖書好館喜歡結交海洋裏豚鯨魚要保護動物大象虎熊貓獅子猴"),
        )
        self.assertEqual(len(build.CHARACTERS), 113)

    def test_frame_count_uses_approved_k3_timing(self):
        self.assertEqual(build.frame_count(6), 579)
        self.assertEqual(build.frame_count(8), 735)

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
            self.assertEqual(page.count('class="character-card"'), 113)
            self.assertEqual(page.count('class="word-card"'), 73)
            self.assertEqual(page.count('download='), 113)
            self.assertIn("他們都愛我", page)
            self.assertIn("我愛中國", page)
            self.assertIn("起飛吧！得得", page)
            self.assertIn("拯救小海豚", page)
            self.assertIn("巴特一家的新生活", page)
            self.assertIn("aria-label=\"播放「我」字筆順\"", page)

    def test_new_theme_has_exact_homework_and_reading_card_order(self):
        page = build.page_html()
        self.assertEqual(ui.HOMEWORK_WORDS, (
            "我們", "中國", "我們是中國人", "在", "香港", "我們在香港", "北京", "有",
            "長城", "北京有長城", "鳥巢", "故宮", "北京有故宮",
        ))
        self.assertEqual(ui.CHINA_READING_WORDS, ("國慶節", "煙花", "中國", "北京", "故宮", "萬里長城"))
        self.assertLess(page.index('data-word="我們"'), page.index('data-word="中國"'))
        self.assertEqual(page.count('data-word="我們是中國人"'), 7)  # card plus six playable characters

    def test_takeoff_theme_has_exact_homework_and_reading_card_order(self):
        page = build.page_html()
        self.assertEqual(ui.TAKEOFF_HOMEWORK_WORDS, (
            "玉米", "真", "美味", "玉米真美味",
            "有益", "的", "白菜", "有益的白菜",
            "一起", "吃", "米飯", "我們一起吃米飯",
        ))
        self.assertEqual(ui.TAKEOFF_READING_WORDS, ("早睡早起", "跳舞", "跑步", "游泳", "踢球", "踏單車"))
        homework = page.index('id="takeoff-homework-words"')
        reading = page.index('id="takeoff-reading-words"')
        self.assertLess(homework, reading)
        self.assertLess(page.index('data-word="玉米"', homework), page.index('data-word="我們一起吃米飯"', homework))
        self.assertLess(page.index('data-word="早睡早起"', reading), page.index('data-word="踏單車"', reading))
        self.assertNotIn("Animal", page)
        self.assertNotIn("識字冊", page)

    def test_bart_theme_uses_updated_homework_and_reading_order(self):
        page = build.page_html()
        self.assertEqual(ui.BART_HOMEWORK_WORDS, ("馬路", "旁邊", "公園", "朋友", "玩耍", "我和朋友玩耍", "喜歡", "結交"))
        self.assertEqual(ui.BART_READING_WORDS, ("友善", "鄰居", "我們", "好朋友", "公園", "社區", "學校", "圖書館"))
        homework = page.index('id="bart-homework-words"')
        reading = page.index('id="bart-reading-words"')
        self.assertLess(homework, reading)
        self.assertLess(page.index('data-word="馬路"', homework), page.index('data-word="結交"', homework))
        self.assertLess(page.index('data-word="友善"', reading), page.index('data-word="圖書館"', reading))
        self.assertNotIn('data-word="喜歡"', page[reading:])
        self.assertNotIn('data-word="結交"', page[reading:])
        bart = page[page.index('id="bart-theme-title"'):page.index('id="all-title"')]
        self.assertNotIn("大象和老虎", bart)
        self.assertNotIn("waterfall", page)

    def test_dolphin_theme_has_exact_homework_and_reading_card_order(self):
        page = build.page_html()
        self.assertEqual(ui.DOLPHIN_HOMEWORK_WORDS, (
            "海洋裏", "海豚", "鯨魚", "我們要保護海洋",
        ))
        self.assertEqual(ui.DOLPHIN_READING_WORDS, ("動物園", "大熊貓", "獅子", "大象", "老虎", "猴子", "海洋", "海豚"))
        homework = page.index('id="dolphin-homework-words"')
        reading = page.index('id="dolphin-reading-words"')
        self.assertLess(page.index("起飛吧！得得"), page.index("拯救小海豚"))
        self.assertLess(page.index("拯救小海豚"), page.index("巴特一家的新生活"))
        self.assertLess(homework, reading)
        self.assertLess(page.index('data-word="海洋裏"', homework), page.index('data-word="我們要保護海洋"', homework))
        self.assertLess(page.index('data-word="動物園"', reading), page.index('data-word="海豚"', reading))
        self.assertNotIn("noodles", page)
        self.assertNotIn("識字冊", page)

    def test_manifest_records_edb_source_for_every_character(self):
        for item in build.CHARACTERS:
            self.assertRegex(item["edb_id"], r"^\d{4}$")
            self.assertEqual(item["strokes"], len(item["stroke_order"]))


if __name__ == "__main__":
    unittest.main()
