#!/usr/bin/env python3
"""
YouTube Transcriber
A tool to download YouTube videos and transcribe them using OpenAI Whisper
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path
import yt_dlp
import whisper


def download_youtube_audio(url, output_dir=None):
    """Download audio from YouTube video"""
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown')
        
    # Find the downloaded file
    for file in os.listdir(output_dir):
        if file.endswith('.mp3'):
            return os.path.join(output_dir, file), title
    
    raise FileNotFoundError("Downloaded audio file not found")


def transcribe_audio(audio_path, model_name="base"):
    """Transcribe audio using OpenAI Whisper"""
    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)
    
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path)
    
    return result["text"]


def main():
    parser = argparse.ArgumentParser(description="Transcribe YouTube videos using Whisper")
    parser.add_argument("url", help="YouTube URL to transcribe")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model to use (default: base)")
    parser.add_argument("--output", "-o", help="Output file for transcript")
    parser.add_argument("--keep-audio", action="store_true", 
                       help="Keep downloaded audio file")
    
    args = parser.parse_args()
    
    try:
        # Download audio
        print(f"Downloading audio from: {args.url}")
        audio_path, title = download_youtube_audio(args.url)
        print(f"Downloaded: {title}")
        
        # Transcribe
        transcript = transcribe_audio(audio_path, args.model)
        
        # Output transcript
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"Transcript saved to: {args.output}")
        else:
            print("\n" + "="*50)
            print("TRANSCRIPT:")
            print("="*50)
            print(transcript)
        
        # Cleanup
        if not args.keep_audio:
            os.remove(audio_path)
            print(f"Cleaned up audio file: {audio_path}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()