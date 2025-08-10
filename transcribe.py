
#!/usr/bin/env python3
import argparse
import pathlib
from utils.downloader import download_audio
from utils.transcriber import transcribe_file, write_srt_from_result

def main():
    parser = argparse.ArgumentParser(description="YouTube to text (CN/EN) via Whisper")
    parser.add_argument("input", help="YouTube URL or local audio/video file path")
    parser.add_argument("--model", default="small", help="Whisper model: base|small|medium|large")
    parser.add_argument("--task", default="transcribe", choices=["transcribe", "translate"], help="Task mode")
    parser.add_argument("--language", default=None, help="Force language code, e.g., zh or en")
    parser.add_argument("--srt", action="store_true", help="Also write .srt subtitles")
    parser.add_argument("--outputs", default="outputs", help="Output directory")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.outputs)
    out_dir.mkdir(exist_ok=True, parents=True)

    # Determine input type
    if args.input.startswith("http://") or args.input.startswith("https://"):
        audio_path, title = download_audio(args.input, out_dir=str(out_dir))
    else:
        # Local file
        p = pathlib.Path(args.input)
        if not p.exists():
            raise FileNotFoundError(f"Input file not found: {p}")
        audio_path = str(p.resolve())
        title = p.stem

    # Transcribe
    result = transcribe_file(
        audio_path,
        model_name=args.model,
        task=args.task,
        language=args.language,
    )

    # Write text
    txt_path = out_dir / f"{title}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result.get("text", ""))
    print(f"[OK] Text written: {txt_path}")

    # Optionally SRT
    if args.srt:
        srt_path = write_srt_from_result(result, title=title, out_dir=str(out_dir))
        print(f"[OK] SRT written: {srt_path}")

if __name__ == "__main__":
    main()
