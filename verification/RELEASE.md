# Full K3 release verification — 《我愛中國》 expansion

Verified media: **43/43**. Previous 21 retained byte-for-byte; 22 official-geometry additions. Original nine quick buttons and eight 《他們都愛我》 reading cards retained.

《我愛中國》 homework cards (exact order): 我們、中國、我們是中國人、在、香港、我們在香港、北京、有、長城、北京有長城、鳥巢、故宮、北京有故宮。

Recognition cards (exact order): 國慶節、煙花、中國、北京、故宮、萬里長城。 Every printed character, including duplicates, has its own playback button.

All 43: 1080×1080, 30 fps, H.264/yuv420p; draw 2.0s, pause 0.6s, intro 0.7s, final 3.0s. Every MP4 was fully decoded. Every new stroke was reviewed at six progress points; all 22 new encoded finals and the combined 43-character final montage were inspected.

## Official source and media evidence

The 22 additions use only frozen Hong Kong EDB CreateJS filled outlines and chronological reveal states. `china-source-audit.json` records unique entry IDs, listed/decoded counts, and raw source SHA-256. Generic geometry is not a production input. EDB direction-marker line shapes are explicitly excluded; translated/scaled filled outlines are preserved.

|字|EDB ID|筆畫|秒|幀|MP4 SHA-256|Drive exact-ID readback|
|---|---:|---:|---:|---:|---|---|
|我|[1460](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1460.js)|7|21.9|657|`666e10dbb4c787d46c9d5cc2725b5f490d63be6c0eaec26dd48d29ceb2f21959`|[MP4](https://drive.google.com/file/d/1mVo6SjRtfThChJKEK0MnN-BPCEQ6oAhN/view)|
|有|[1828](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1828.js)|6|19.3|579|`132a66988020389b58147e31a9be3fad9d8aec0906bd672b5dce26564d8f9574`|[MP4](https://drive.google.com/file/d/1P4kyhLPNsCsYHQA27AAmRM0uInueu8pv/view)|
|爸|[2456](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2456.js)|8|24.5|735|`80899b458747c7addcd2b1dd809cf497882c95331f0c7b322fce8cdfe8324139`|[MP4](https://drive.google.com/file/d/1M0jRnzWtLZ6yKxks9YFMxNhtC3B_suC_/view)|
|媽|[0948](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0948.js)|13|37.5|1125|`33952edaa80dfa6dfc9dc04dfcb6ca1c9b5e9bebf08762b9de081efa74fe4535`|[MP4](https://drive.google.com/file/d/1LdvvToggTja8PzhUBmutpDkX6098WEsJ/view)|
|姐|[0892](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0892.js)|8|24.5|735|`b5c07b676028fa0405a10370013307b26c08f3f50710fbc4d98f8c04c46e8497`|[MP4](https://drive.google.com/file/d/1jDzzTVuZOtK1gqOvJU66aUouRsjs0DY-/view)|
|妹|[0889](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0889.js)|8|24.5|735|`5eee2b491c70f43cdd177a8d548d44ff1a013467062cc2bf4e4d94f4c8caa5c4`|[MP4](https://drive.google.com/file/d/1_K8AwwsteOqGIjRjBgNjqzvLXI7KS_pM/view)|
|弟|[1238](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1238.js)|7|21.9|657|`05bce7ed69f2c961dda4c3f35d3f3229243f2678a0ab51aaaf2b860354edd270`|[MP4](https://drive.google.com/file/d/1hCTHAn6bU-h0SD7SnquT_1yUI14KCfTa/view)|
|哥|[0581](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0581.js)|10|29.7|891|`c2c6e1bc6c5d88063a9b3ca9d18a9578ddb2434b39ec0e7f3ac312c18b70b878`|[MP4](https://drive.google.com/file/d/1rW0EgHGkbB6LzGzdcfKUd91JDNcMfGGy/view)|
|和|[0551](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0551.js)|8|24.5|735|`a97f24e9025fe4f0b1687976ce14c25a8f79d0fb80cd79d61d245445078e845b`|[MP4](https://drive.google.com/file/d/1qZ3rK93i_bBfNrFCZGLkpxTtDDDvP5Ki/view)|
|祖|[2870](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2870.js)|9|27.1|813|`280efeaf617db892a4b3e52121363226e46bd874d70f72e76a525ce67ef5a675`|[MP4](https://drive.google.com/file/d/1sskFAG1_c0MQLrqz496Q8LmOKoMRDZ9m/view)|
|父|[2455](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2455.js)|4|14.1|423|`957bbae854b1cd250ee7cbabb81325802f70c6ed1cd1616cc6ec4a4f4a40a5ed`|[MP4](https://drive.google.com/file/d/1F67HDctsIg2TM5o_1k45DhXrPlVNkiz5/view)|
|母|[2082](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2082.js)|5|16.7|501|`021a1a6019870d418e294e7f5e2f2b37f3c7716a819230ada5a29a8cfb3cc3ed`|[MP4](https://drive.google.com/file/d/1ES6_3KBFcGfzD2UtpZFt9FWLXSOuysEa/view)|
|老|[3230](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/3001-4000/3230.js)|6|19.3|579|`561dd823e24cd01a18b1c34396afd85735a7081879de0606a810220a12c152f0`|[MP4](https://drive.google.com/file/d/1ghgYXNgIwLaJ8yd1SFZXGqIlk_nPD6Ug/view)|
|師|[1161](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1161.js)|10|29.7|891|`7161fc426002edefa96afdc8ecc87327874805cd26b3ee150589df898bf1356a`|[MP4](https://drive.google.com/file/d/1ElkjIs5uNHjh4WqmbVUDEzYBcRj2UrRn/view)|
|消|[2190](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2190.js)|10|29.7|891|`34c8a955892eb2a3755f5d8b7be2c776c0d4f47ef8846179f825b11d10904449`|[MP4](https://drive.google.com/file/d/1THgAa_Ho8Z7AnENWEdAKFVykJc_2s-Kq/view)|
|防|[4365](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4365.js)|7|21.9|657|`46e32abfa633c16d4a5f77adcbdfca4b11b62ee1770e3d29c7874b0a19ffea3e`|[MP4](https://drive.google.com/file/d/1SvviHqh-PEaf_qFmHEJJmyjrYdBNX3cN/view)|
|員|[0590](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0590.js)|10|29.7|891|`6608c36ba9fdfaf4db22c17b3296a7f08c4cb432fb8d21c9ab36acc5464f25d0`|[MP4](https://drive.google.com/file/d/1S485cLYX1Nt2sUhADeVNnFEzp6AeQVDP/view)|
|警|[3861](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/3001-4000/3861.js)|20|55.7|1671|`5b3054a91faf40d188e4a823cce994f742c8a7d07d5d7e9824b1d5b6412a1c7d`|[MP4](https://drive.google.com/file/d/1hoDMQTk-mEqFXfy2e9W1CNyqrFmNOtBF/view)|
|察|[1038](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1038.js)|14|40.1|1203|`fea2044bed8e773451ec612ce109f7af56b8febf83fd168648516a26ed805f0a`|[MP4](https://drive.google.com/file/d/16-X0tJzh8ZYdqLL6_e5VhfkFcMkUY7oW/view)|
|醫|[4217](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4217.js)|18|50.5|1515|`f3177aa9fe03a6ab0590b3d8aefe17309c99e7b47a8ef37fe11e23cedfa9041a`|[MP4](https://drive.google.com/file/d/19FVLLqVH_SXO-SSjYK6tSdpJemS0gJyL/view)|
|生|[2605](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2605.js)|5|16.7|501|`06857b4ed27fc5c28d0dfb954bdfc7cea765a591ab2bd4107ddedbded4f58a58`|[MP4](https://drive.google.com/file/d/13D6uDBnoRTE8OlGwrTDHAUgqlenY4yPq/view)|
|們|[0182](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0182.js)|10|29.7|891|`00add9ebfbb69f8c78e619d6ce5ebb7da81341881505ff1f0b93f6e1a65fe2c6`|[MP4](https://drive.google.com/file/d/1TY39aStqeAC4bUMOs2wLNfaGMUDlTv1Q/view)|
|中|[0020](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0020.js)|4|14.1|423|`f14902a8a36c15268618fc6636c5d2e0fec160fa652cdd2e01c08213ca4364f5`|[MP4](https://drive.google.com/file/d/1upvU8hFAsHOqd_qBUvUsPdZP4c9hypnh/view)|
|國|[0729](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0729.js)|11|32.3|969|`7c98fca0b7b978a329b323f4b22c6e8757ff5b77f1bd83c1a7c1b53a1a89fd29`|[MP4](https://drive.google.com/file/d/1O7fa1PQluuoIKsLAq2Zuli3xwB36nmou/view)|
|是|[1776](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1776.js)|9|27.1|813|`0575314bf409eed8945c41b61f8b4b5057924fa3740b6cc0df036eaca58133f8`|[MP4](https://drive.google.com/file/d/1tQFp8dTBAhtL11FjJQtvb3K-Vl8uFgPZ/view)|
|人|[0067](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0067.js)|2|8.9|267|`d67b7016fade105a1f2dd3c5f9202d6bcd24b925c07000541e2df6bb1ee73758`|[MP4](https://drive.google.com/file/d/1NIUNtwnnNtc8h2btxepVG_hbme0CfsiA/view)|
|在|[0737](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0737.js)|6|19.3|579|`12aaf05b5c5c2b38251b17ff20451ff350119b27d288887bd816f7e624fdb777`|[MP4](https://drive.google.com/file/d/1rsH3Neb6iIbIienrlZNkdiSXa3MJ6-BP/view)|
|香|[4575](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4575.js)|9|27.1|813|`1b78ceec67c3e4b9a9e2123d217cf729270a4baa70629bc3047ba978ec4436d1`|[MP4](https://drive.google.com/file/d/19RgBRjx4croek2P5hs024lNxC5udvfrK/view)|
|港|[2238](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2238.js)|12|34.9|1047|`248a426cdd4833bf0864c989b514cf50b727835c41ad010e1cf9cba2c9f0bef4`|[MP4](https://drive.google.com/file/d/12bHVz0y87jJ9xhFW-_z1rguHRd1PtpjU/view)|
|北|[0411](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0411.js)|5|16.7|501|`466cc8d5b1ce9c84a7542cb20c552b051bcb89ab60e7a2a55845ee5c324b0c43`|[MP4](https://drive.google.com/file/d/12C8v2osPQOiWO6TrLaZPqAUAluyGroYE/view)|
|京|[0064](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0064.js)|8|24.5|735|`60fdc4ae9940f1f7d4febc6c0b1d4157567145274bbfb82e89f792bbc1e1037a`|[MP4](https://drive.google.com/file/d/1fXWgoFvvra-AGfSmxUpaMMoFmK0CaBga/view)|
|長|[4331](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4331.js)|8|24.5|735|`3532fb9faddd9c5ec077c06b5d6fe47eb7072ce5932390d7cbf73440310f8c57`|[MP4](https://drive.google.com/file/d/1qQcwB8-O3gadkj0u2RFgPwFXyTwDji4Z/view)|
|城|[0765](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/0001-1000/0765.js)|9|27.1|813|`0f9b1cf03a478ea2eaa0a81f37f3e6b8896bc00916d51e76702deda9109b2dbd`|[MP4](https://drive.google.com/file/d/1ykM-vRHQZJmvznyHQnCC24CeiMyistdV/view)|
|鳥|[4671](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4671.js)|11|32.3|969|`6f7b527bc62e75a3097af669133c8aeaa5af0528b4a1cbb5b28e8fc75338c5c1`|[MP4](https://drive.google.com/file/d/1jOzkZnFD5BvfzTXskAtPZxHmtSO2kPcc/view)|
|巢|[1134](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1134.js)|11|32.3|969|`58b80499d6a81db8324ea509c647197d34777f88779663b3dfad5dc9e3e93f35`|[MP4](https://drive.google.com/file/d/1WqhiFATXgbr8JtkI-z0ua8KMXvozbekU/view)|
|故|[1707](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1707.js)|9|27.1|813|`1c7b488a391282f4dc6c7a46f2940d408dbb2a32ec8f54eb6bfa78feb1fd3dda`|[MP4](https://drive.google.com/file/d/1Cz5Gx0FPHjlCegOZ3jbH8FrggD797635/view)|
|宮|[1016](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1016.js)|10|29.7|891|`2cb2088ca33b0393a2efb153bbdc6b60eaebdf70a91bf5240a3dbf0ed1effeb5`|[MP4](https://drive.google.com/file/d/19gRH4qG1SRVpDKK7WlVb-FI0Tgtdv9jo/view)|
|慶|[1412](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/1001-2000/1412.js)|15|42.7|1281|`6796d7ae4932f02b15aae154f393782d867ff79c86c78f871cb5e2c3c853fc4d`|[MP4](https://drive.google.com/file/d/1SLB6FvKNvoop921I-jzVtmQFKsJqf4aq/view)|
|節|[2989](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2989.js)|13|37.5|1125|`637a452293d8617117936f3a4b41d84b4285f14ef84138d72d69d001a65f8422`|[MP4](https://drive.google.com/file/d/1nDnxhq_wFhlq8SmmZKv2k8W4JaghdEk8/view)|
|煙|[2403](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2403.js)|13|37.5|1125|`bf2a9dfbc5b22445548a8278c4123ea5670c519c9477199477fc4bdf2916cd37`|[MP4](https://drive.google.com/file/d/1eo9kurwlP2IOraVHj0E6Q9czCPUrGWVz/view)|
|花|[3415](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/3001-4000/3415.js)|8|24.5|735|`f7ef89c07ae0f77196a226f951cc659bd74992241726057722b9ea6dc916274d`|[MP4](https://drive.google.com/file/d/1SAfGy_KCHbvWjJpUO7N0kK8whLx16PP9/view)|
|萬|[2891](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/2001-3000/2891.js)|13|37.5|1125|`ef42070b70c3bc553c262e1a371aca7c0cd8a78f00490f1fbf0ecb0bed08f0e3`|[MP4](https://drive.google.com/file/d/1R_uvUqAEdrtwwH67E5jNHVse59ecrLtM/view)|
|里|[4225](https://www.edbchinese.hk/EmbziciwebRes/stkdemo_js/4001-ZC/4225.js)|7|21.9|657|`728d34b1df274f953710b0488420cf2857b8afffb8dbdb9d995fc06040166b39`|[MP4](https://drive.google.com/file/d/12QmUFN-M9IMVgdTroOETiTPAa1ynW_Ih/view)|

Drive folder `1iZwfwFdhM2pEDiojTRf-stwYjgMebRDK` lists one exact-ID production MP4 for each of the 43 characters. The 22 additions were downloaded by returned ID and compared byte-for-byte; the unchanged 21 were not reuploaded.

## Verification gates

- Python/DOM: 10 tests passed; 43 character cards, 27 ordered word cards, duplicate per-character triggers.
- Media: 43/43 ffprobe and full `ffmpeg -xerror` decode; H.264, 1080 square, 30 fps, yuv420p, exact expected frame counts.
- Visual: six progress samples per new stroke, all 22 new finals, and combined all-43 final montage passed.
- Local browser: native ARM64 Debian Chromium with H.264 exercised 121 playback triggers and 43 downloads; no page errors or 390px overflow.
- Public browser/readback fields are updated only after gh-pages deployment and live verification.

## Review note

Automated static/diff review evidence is in `code-review.json`. An independent Claude Code review was attempted but its OAuth session was expired; this limitation is recorded rather than misrepresented as an independent pass.
