import os
import uuid
import shutil
from fastapi import UploadFile
from app.error_handler.custom_exception import CustomException
from app.utils.process_and_record import process_and_record


def create(file: UploadFile):
    if file.content_type not in ["video/mp4", "video/webm", "video/mov", "video/mvi"]:
        raise CustomException("invalid file type", 400)
    os.makedirs("media/videos", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = f"media/videos/{file_id}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(e)
        raise CustomException("video upload failed", 500)
    output_path = process_and_record(file_path)
    os.remove(file_path)
    return output_path
