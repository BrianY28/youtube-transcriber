
import yt_dlp
import re
import pathlib
from typing import Tuple

def sanitize_filename(name: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    # Remove invalid characters and limit length
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    name = re.sub(r'\s+', " ", name).strip()
    # Limit length to avoid filesystem issues
    if len(name) > 200:
        name = name[:200].strip()
    return name

def download_audio(url: str, out_dir: str, auth_opts: dict = None) -> Tuple[str, str]:
    """Download best audio from YouTube and convert to mp3.
    Returns (audio_path, title)
    
    Args:
        url: YouTube URL
        out_dir: Output directory
        auth_opts: Authentication options dict with keys:
            - cookies: Path to cookies file
            - cookies_from_browser: Browser name to extract cookies from
            - username: YouTube username/email
            - password: YouTube password
    """
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if auth_opts is None:
        auth_opts = {}

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": False,  # Enable some output for debugging
        "no_warnings": False,
        # Add these for better compatibility
        "extractaudio": True,
        "audioformat": "mp3",
        "prefer_ffmpeg": True,
    }
    
    # Add authentication options
    if auth_opts.get('cookies'):
        ydl_opts['cookiefile'] = auth_opts['cookies']
    
    if auth_opts.get('cookies_from_browser'):
        ydl_opts['cookiesfrombrowser'] = (auth_opts['cookies_from_browser'], None, None, None)
    
    if auth_opts.get('username'):
        ydl_opts['username'] = auth_opts['username']
    
    if auth_opts.get('password'):
        ydl_opts['password'] = auth_opts['password']

    print(f"Downloading audio from: {url}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            raw_title = info.get("title", "audio")
            title = sanitize_filename(raw_title)
            
            print(f"Downloaded: {title}")
            
            # Look for the downloaded file
            audio_path = out_dir / f"{title}.mp3"
            
            # If exact match not found, look for similar files
            if not audio_path.exists():
                # Look for MP3 files that might match
                candidates = list(out_dir.glob("*.mp3"))
                if candidates:
                    # Get the most recently modified file
                    audio_path = max(candidates, key=lambda p: p.stat().st_mtime)
                    print(f"Using file: {audio_path}")
                else:
                    # Look for any audio files
                    audio_extensions = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]
                    for ext in audio_extensions:
                        candidates = list(out_dir.glob(f"*{ext}"))
                        if candidates:
                            audio_path = max(candidates, key=lambda p: p.stat().st_mtime)
                            break
            
            if not audio_path.exists():
                raise FileNotFoundError(f"Downloaded audio file not found in {out_dir}")
                
            return str(audio_path), title
            
        except Exception as e:
            print(f"Download error: {e}")
            raise
