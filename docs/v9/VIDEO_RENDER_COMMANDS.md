# V9 Delta Video Render Commands

The checked-in MP4 is already rendered. Use these commands only if you need to
regenerate the V9 delta proof video from the repo.

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

