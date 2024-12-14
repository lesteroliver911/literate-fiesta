from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .services.video_service import VideoService
from .models import ChatMessage

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app = FastAPI(title="Video Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))

video_service = VideoService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        video_path = await video_service.save_video(file)
        return JSONResponse({
            "status": "success",
            "video_path": video_path
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/analyze")
async def analyze_video(message: ChatMessage):
    try:
        response = await video_service.analyze_video(
            message.video_path, 
            message.prompt
        )
        return JSONResponse({
            "status": "success",
            "response": response
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 