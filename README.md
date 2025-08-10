# YouTube Transcriber

A Python tool to download YouTube videos and transcribe them using OpenAI Whisper.

## Features

- Download audio from YouTube videos using yt-dlp
- Transcribe audio using OpenAI Whisper
- Multiple Whisper model options (tiny, base, small, medium, large)
- Save transcripts to file or display in terminal
- Optional audio file cleanup

## Requirements

- Python 3.8+
- FFmpeg (for audio processing)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/BrianY28/youtube-transcriber.git
   cd youtube-transcriber
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg (if not already installed):
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - Windows: Download from https://ffmpeg.org/

## Usage

Basic usage:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

With options:
```bash
# Use a different Whisper model
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --model small

# Save transcript to file
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --output transcript.txt

# Keep the downloaded audio file
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio
```

### Available Whisper Models

- `tiny`: Fastest, least accurate
- `base`: Good balance of speed and accuracy (default)
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

## License

MIT License
