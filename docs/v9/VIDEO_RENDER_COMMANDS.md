# V9 Video Render Commands

The checked-in MP4 files are already rendered. Use these commands only if you
need to regenerate them from the repo.

## 16-Chapter Audited Build Video

```bash
python3 -m pip install -r scripts/video/requirements.txt
python3 scripts/video/render_bidintel_v9_16_chapter_build_video.py
ffprobe -v error -show_entries format=duration,size -show_entries stream=index,codec_type,width,height -of json docs/v9/BidIntel_V9_16_Chapter_Audited_Build_Video.mp4
python3 -m json.tool docs/v9/BidIntel_V9_16_Chapter_Audited_Build_Video_manifest.json >/dev/null
```

Expected proof:

- MP4 has one video stream and one audio stream.
- Manifest parses as valid JSON.
- Generated frame files appear under `docs/v9/v9_16_chapter_frames/`.

## Delta Proof Video

```bash
python3 -m pip install -r scripts/video/requirements.txt
python3 scripts/video/render_bidintel_v9_delta_video.py
ffprobe -v error -show_entries format=duration,size -show_entries stream=index,codec_type,width,height -of json docs/v9/BidIntel_ZeroToBuild_Masterclass_v9_delta_proof.mp4
python3 -m json.tool docs/v9/BidIntel_ZeroToBuild_Masterclass_v9_delta_manifest.json >/dev/null
```

Expected proof:

- MP4 has one video stream and one audio stream.
- Manifest parses as valid JSON.
- Generated frame files appear under `docs/v9/v9_delta_frames/`.
