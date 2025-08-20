#!/usr/bin/env python3
"""
Helper script to extract YouTube cookies from your browser.
This is the most secure way to authenticate for membership videos.
"""

import argparse
import pathlib
import sys

def main():
    parser = argparse.ArgumentParser(description="Extract YouTube cookies from browser")
    parser.add_argument("--browser", 
                       choices=["chrome", "firefox", "safari", "edge"], 
                       default="chrome",
                       help="Browser to extract cookies from")
    parser.add_argument("--output", 
                       default="youtube_cookies.txt",
                       help="Output file for cookies (Netscape format)")
    
    args = parser.parse_args()
    
    try:
        import yt_dlp
        
        ydl_opts = {
            'cookiesfrombrowser': (args.browser, None, None, None),
            'quiet': True,
        }
        
        print(f"Extracting cookies from {args.browser}...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Try to extract cookies by attempting to get info from a YouTube page
            try:
                ydl.extract_info('https://www.youtube.com', download=False)
                print(f"✅ Successfully extracted cookies from {args.browser}")
                print(f"You can now use: --cookies-from-browser {args.browser}")
                print("\nExample usage:")
                print(f'python transcribe.py "YOUR_MEMBERSHIP_VIDEO_URL" --cookies-from-browser {args.browser} --model small --srt')
                
            except Exception as e:
                print(f"❌ Failed to extract cookies: {e}")
                print("\nTroubleshooting:")
                print("1. Make sure you're logged into YouTube in your browser")
                print("2. Try closing and reopening your browser")
                print("3. Make sure the browser is not running when extracting cookies")
                print(f"4. Try a different browser with --browser [chrome|firefox|safari|edge]")
                sys.exit(1)
                
    except ImportError:
        print("❌ yt-dlp is required for cookie extraction")
        print("Install it with: pip install yt-dlp")
        sys.exit(1)

if __name__ == "__main__":
    main()
