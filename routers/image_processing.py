from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from db.mongo import users_collection, fs
from utils.image_ops import process_image
import io

router = APIRouter()

@router.post("/echo/")
async def echo(message: str = Form(...)):
    return {"echo": message}

@router.post("/process-images/")
async def process_images(username: str = Form(...), files: list[UploadFile] = File(...)):
    user = users_collection.find_one({"$or": [{"username": username}, {"email": username}]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    processed_ids = []
    for file in files:
        image_bytes = await file.read()
        if not image_bytes:
            continue
        original_id = fs.put(image_bytes, filename=file.filename, metadata={"type": "original", "uploaded_by": username})
        processed_bytes = process_image(image_bytes)
        processed_id = fs.put(processed_bytes, filename="processed_" + file.filename, metadata={"type": "processed", "uploaded_by": username, "original_id": str(original_id)})
        processed_ids.append(str(processed_id))
    return {"processed_ids": processed_ids}