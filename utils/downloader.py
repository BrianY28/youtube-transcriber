
import yt_dlp
import re
import pathlib
from typing import Tuple

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()

def download_audio(url: str, out_dir: str) -> Tuple[str, str]:
    """Download best audio from YouTube and convert to mp3.
    Returns (audio_path, title)
    """
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = sanitize_filename(info.get("title", "audio"))
        audio_path = out_dir / f"{title}.mp3"
        if not audio_path.exists():
            candidates = list(out_dir.glob(f"{title}.*"))
            if candidates:
                audio_path = candidates[0]
        return str(audio_path), title
