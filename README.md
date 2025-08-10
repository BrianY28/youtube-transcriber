
# YouTube Transcriber (CN/EN)
Turn any YouTube URL into text (and SRT subtitles). Supports Chinese and English automatically via Whisper.

## Features
- Paste a YouTube URL → auto-download audio → transcribe with Whisper
- Auto language detection (Chinese/English/mixed)
- CLI tool and FastAPI web server
- Outputs: full text, segments (with timestamps), and optional `.srt`
- Simple web UI in `/`

## Tech stack
- Python 3.10+
- yt-dlp for audio download
- openai-whisper for transcription (runs locally)
- FastAPI + Uvicorn for the API/web UI

## Install (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Tip: For speed, install PyTorch with CUDA if you have an NVIDIA GPU. On Apple Silicon, Whisper runs on CPU by default; you can also try `pip install torch==2.*` which supports MPS (`export PYTORCH_ENABLE_MPS_FALLBACK=1`).

## Quick start — CLI
```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"   --model small            # base | small | medium | large
  --task transcribe        # transcribe (same language) | translate (to English)
  --srt                    # also write .srt subtitles
```
Outputs: `./outputs/<video_title>.txt` and optionally `.srt`

Transcribe a local file:
```bash
python transcribe.py ./sample.mp3 --model small --srt
```

## Quick start — Web server
```bash
uvicorn main:app --reload --port 8000
```
Open: http://127.0.0.1:8000/

### API
`POST /api/transcribe`
```json
{
  "url": "https://youtu.be/VIDEO_ID",
  "model": "small",
  "task": "transcribe",
  "language": null,
  "write_srt": true
}
```
Response (truncated):
```json
{
  "title": "Video Title",
  "language": "zh",
  "text": "full transcription ...",
  "segments": [{"start":0.0, "end":3.2, "text":"..."}],
  "srt_path": "outputs/Video Title.srt"
}
```

## Project layout
```
youtube-transcriber/
├── main.py                 # FastAPI app & web UI
├── transcribe.py           # CLI entry
├── utils/
│   ├── downloader.py       # download audio via yt-dlp
│   └── transcriber.py      # whisper wrapper
├── templates/
│   └── index.html          # minimal UI
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

## Notes
- This tool is for personal/educational use. Respect copyright and YouTube ToS.
- Whisper `large` is the most accurate but slow/heavy. `small`/`medium` are good trade-offs.
- If you see `ffmpeg not found`, install ffmpeg (macOS: `brew install ffmpeg`).

## License
MIT
