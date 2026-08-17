from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np

from app.schemas.prediction import PredictionResponse
from app.services.gesture_service import GestureService


router = APIRouter(
    prefix="/gesture",
    tags=["Gesture"]
)

gesture_service = GestureService()


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    image = cv2.imdecode(
        np.frombuffer(contents, np.uint8),
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format."
        )

    return gesture_service.predict(image)