from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from deepface import DeepFace
import shutil
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verify-face")
async def verify_face(
    stored_image: UploadFile = File(...),
    live_image: UploadFile = File(...)
):
    stored_path = None
    live_path = None

    try:
        stored_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{stored_image.filename}"
        live_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{live_image.filename}"

        # Save images
        with open(stored_path, "wb") as f:
            shutil.copyfileobj(stored_image.file, f)

        with open(live_path, "wb") as f:
            shutil.copyfileobj(live_image.file, f)

        stored_image.file.close()
        live_image.file.close()

        # Face verification
        result = DeepFace.verify(
            img1_path=stored_path,
            img2_path=live_path,
            model_name="ArcFace",
            detector_backend="mtcnn",
            distance_metric="cosine",
            enforce_detection=False  # 🔥 IMPORTANT
        )

        return {
            "success": bool(result.get("verified", False)),
            "distance": float(result.get("distance", 1.0))
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

    finally:
        # Always cleanup
        if stored_path and os.path.exists(stored_path):
            os.remove(stored_path)
        if live_path and os.path.exists(live_path):
            os.remove(live_path)
