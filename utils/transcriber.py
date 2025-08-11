
import whisper
from whisper.utils import get_writer
import pathlib
import subprocess
import tempfile
import shutil
import os
from typing import Optional, Dict, Any

_model_cache: dict[str, Any] = {}

def get_model(model_name: str = "small"):
    model_name = model_name or "small"
    if model_name not in _model_cache:
        _model_cache[model_name] = whisper.load_model(model_name)
    return _model_cache[model_name]

def preprocess_audio(audio_path: str) -> str:
    """Preprocess audio to ensure compatibility with Whisper."""
    audio_path = pathlib.Path(audio_path)
    
    # If it's already a WAV file, return as-is
    if audio_path.suffix.lower() == '.wav':
        return str(audio_path)
    
    # Convert to WAV using FFmpeg for better compatibility
    temp_dir = tempfile.mkdtemp()
    wav_path = pathlib.Path(temp_dir) / f"{audio_path.stem}.wav"
    
    try:
        # Use FFmpeg to convert to a clean WAV format
        cmd = [
            'ffmpeg', '-i', str(audio_path),
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-ar', '16000',          # 16kHz sample rate (Whisper default)
            '-ac', '1',              # Mono
            '-y',                    # Overwrite output
            str(wav_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return str(wav_path)
        
    except subprocess.CalledProcessError as e:
        # If conversion fails, try the original file
        print(f"Warning: Audio conversion failed, using original file: {e}")
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        return str(audio_path)

def transcribe_file(
    audio_path: str,
    model_name: str = "small",
    task: str = "transcribe",
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Transcribe or translate an audio file with Whisper.
    - task: "transcribe" (same language) or "translate" (to English)
    - language: ISO 639-1 code, e.g., "zh" or "en"; None = auto
    """
    print(f"Loading Whisper model: {model_name}")
    model = get_model(model_name)
    
    print(f"Preprocessing audio: {audio_path}")
    processed_audio_path = preprocess_audio(audio_path)
    
    try:
        print(f"Transcribing audio...")
        result = model.transcribe(
            processed_audio_path,
            task=task,
            language=language,
            verbose=False,
        )
        return result
    
    finally:
        # Clean up temporary file if we created one
        if processed_audio_path != audio_path and os.path.exists(processed_audio_path):
            temp_dir = pathlib.Path(processed_audio_path).parent
            if temp_dir.name.startswith('tmp'):
                shutil.rmtree(temp_dir, ignore_errors=True)

def write_srt_from_result(result: Dict[str, Any], title: str, out_dir: str) -> str:
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    srt_path = out_dir / f"{title}.srt"
    writer = get_writer("srt", str(out_dir))
    # writer expects the original audio path for naming, but we override name by moving
    writer(result, audio_path=str(srt_path.with_suffix(".dummy")))
    srts = sorted(out_dir.glob("*.srt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if srts and srts[0] != srt_path:
        srts[0].rename(srt_path)
    return str(srt_path)
