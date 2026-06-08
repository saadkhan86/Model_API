import app.controller.video_controller as video_controller
from fastapi import APIRouter, UploadFile, File
video_upload_router = APIRouter(prefix="/video", tags=["Video"])

@video_upload_router.post("/")
async def upload(file: UploadFile = File(...)):
    result = video_controller.create(file)
    return {
        "success": True, "message": "video uploaded", "data": result
    }
