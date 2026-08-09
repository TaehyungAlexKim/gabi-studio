# Gabi Studio QR mini-poster — build & credits

`gabi-qr-poster.png` — 6×8" @ 300dpi (1800×2400). Rebuild:
```bash
/tmp/qrvenv/bin/python build_poster.py   # needs Pillow + segno (venv)
```
Matches the site: ivory + soft ink + dusty-blue accent, Sempé logo (../assets/logo.png).
Background = grand piano + oil-paint canvas as a soft blue-grey duotone band fading up.
QR encodes https://www.gabistudio.ca/ (decode-verified with OpenCV).

## Image sources (both CC0 / public domain — no attribution required)
- `assets/piano_a.jpg` — "Grand Piano" (MET), CC0, via Wikimedia Commons
  https://commons.wikimedia.org/wiki/File:Grand_Piano_MET_DP300941.jpg
- `assets/palette.jpg` — "Closeup of brush and palette", CC0, via Flickr
