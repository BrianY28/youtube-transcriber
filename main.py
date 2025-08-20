
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils.downloader import download_audio
from utils.transcriber import transcribe_file, write_srt_from_result
import pathlib

app = FastAPI(title="YouTube Transcriber (CN/EN)")

BASE_DIR = pathlib.Path(__file__).parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class TranscribeBody(BaseModel):
    url: str
    model: str | None = "small"          # base | small | medium | large
    task: str | None = "transcribe"      # transcribe | translate
    language: str | None = None          # e.g., "zh" | "en"; None = auto
    write_srt: bool | None = True
    
    # Authentication options for membership videos
    cookies: str | None = None           # Path to cookies file
    cookies_from_browser: str | None = None  # Browser name (chrome, firefox, safari, edge)
    username: str | None = None          # YouTube username/email
    password: str | None = None          # YouTube password

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/transcribe")
async def api_transcribe(body: TranscribeBody):
    try:
        # Prepare authentication options
        auth_opts = {}
        if body.cookies:
            auth_opts['cookies'] = body.cookies
        if body.cookies_from_browser:
            auth_opts['cookies_from_browser'] = body.cookies_from_browser
        if body.username:
            auth_opts['username'] = body.username
        if body.password:
            auth_opts['password'] = body.password
            
        audio_path, title = download_audio(body.url, out_dir=str(OUTPUTS_DIR), auth_opts=auth_opts)
        result = transcribe_file(
            audio_path,
            model_name=body.model or "small",
            task=body.task or "transcribe",
            language=body.language,
        )
        srt_path = None
        if body.write_srt:
            srt_path = write_srt_from_result(result, title=title, out_dir=str(OUTPUTS_DIR))

        response = {
            "title": title,
            "language": result.get("language", None),
            "text": result.get("text", ""),
            "segments": [
                {"start": float(s["start"]), "end": float(s["end"]), "text": s["text"]}
                for s in result.get("segments", [])
            ],
            "srt_path": str(srt_path) if srt_path else None,
        }
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download")
async def download(file: str):
    # basic safe download (files only within outputs/)
    file_path = (OUTPUTS_DIR / file).resolve()
    if OUTPUTS_DIR not in file_path.parents:
        return JSONResponse({"error": "Invalid path"}, status_code=400)
    if not file_path.exists():
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(str(file_path), filename=file_path.name)
