# YouTube Membership Video Authentication Guide

This guide explains how to transcribe YouTube membership-only videos that you have purchased access to.

## Prerequisites

1. You must be a paying member of the YouTube channel
2. You must be logged into YouTube in your browser
3. The video must be accessible to your account

## Authentication Methods

### Method 1: Browser Cookies (Recommended)

This is the most secure and convenient method:

```bash
# Using Chrome (most common)
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --cookies-from-browser chrome --model small --srt

# Using Firefox
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --cookies-from-browser firefox --model small --srt

# Using Safari (macOS)
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --cookies-from-browser safari --model small --srt

# Using Edge
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --cookies-from-browser edge --model small --srt
```

### Method 2: Cookies File

If you prefer to use a cookies file:

```bash
# First, export your browser cookies to a file (using browser extension or manual export)
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --cookies youtube_cookies.txt --model small --srt
```

### Method 3: Username and Password (Less Secure)

```bash
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" --username your@email.com --password yourpassword --model small --srt
```

## Testing Cookie Extraction

Before trying to download membership videos, test that cookie extraction works:

```bash
python extract_cookies.py --browser chrome
```

This will verify that your browser cookies can be extracted properly.

## Troubleshooting

### "Cookies are no longer valid" Warning

This is normal. The warning appears even when cookies work correctly. If you get actual download errors:

1. Make sure you're logged into YouTube in your browser
2. Try closing and reopening your browser
3. Clear YouTube cookies and log in again
4. Try a different browser

### "Video unavailable" Error

- Verify you have active membership to the channel
- Check that the video URL is correct
- Make sure the video is actually a membership video (not age-restricted or region-blocked)

### Permission Errors

- On macOS, you may need to grant terminal access to your browser data
- On Windows, make sure your browser is closed when extracting cookies

## Web API Usage

You can also use authentication through the web interface at `http://127.0.0.1:8000/`:

1. Paste your membership video URL
2. Expand "Authentication (for membership videos)"
3. Select your authentication method:
   - **Browser cookies**: Choose your browser
   - **Cookies file**: Enter path to cookies file
   - **Username/Password**: Enter your credentials
4. Click "Transcribe"

## Security Notes

- Browser cookie extraction is the safest method
- Avoid using username/password in shared environments
- Your authentication data is only used to download the video, not stored
- The tool runs locally on your machine

## Legal Considerations

- Only use this for content you have legitimate access to
- Respect YouTube's Terms of Service
- Don't redistribute membership-only content
- This tool is for personal transcription use only

## Example: Full Workflow

```bash
# 1. Test cookie extraction
python extract_cookies.py --browser chrome

# 2. Transcribe membership video
python transcribe.py "https://www.youtube.com/watch?v=MEMBERSHIP_VIDEO_ID" \
    --cookies-from-browser chrome \
    --model medium \
    --srt

# 3. Files will be created in outputs/
# - VIDEO_TITLE.txt (full transcription)
# - VIDEO_TITLE.srt (subtitle file with timestamps)
```

That's it! You should now be able to transcribe YouTube membership videos you have access to.
