
import whisper
from whisper.utils import get_writer
import pathlib
from typing import Optional, Dict, Any

_model_cache: dict[str, Any] = {}

def get_model(model_name: str = "small"):
    model_name = model_name or "small"
    if model_name not in _model_cache:
        _model_cache[model_name] = whisper.load_model(model_name)
    return _model_cache[model_name]

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
    model = get_model(model_name)
    result = model.transcribe(
        audio_path,
        task=task,
        language=language,
        verbose=False,
    )
    return result

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
