import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException

from bird_model import analyze_bird


app = FastAPI(
    title="AI Bird Server"
)


UPLOAD_FOLDER = "input"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/")
def home():
    return {
        "message": "AI Bird Server працює"
    }


@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...)
):
    try:
        file_path = os.path.join(
            UPLOAD_FOLDER,
            "uploaded_bird.jpg"
        )

        with open(
            file_path,
            "wb"
        ) as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        results = analyze_bird(
            file_path
        )

        predictions = []

        for result in results:
            predictions.append({
                "species": result["label"],
                "confidence": result["score"]
            })

        return {
            "image_name": file.filename or "uploaded_bird.jpg",
            "predictions": predictions
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )