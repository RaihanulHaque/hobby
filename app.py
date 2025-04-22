import uvicorn
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
import shutil
import os
from uuid import uuid4
# from classify_image import classify_image


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with your Flutter app URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    # Save the file
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    # file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # Perform classification (replace with your actual ML model logic)
    # prediction = classify_image(file_path)  # Example: "Real" or "Fake"
    confidence = 0.95  # Example confidence score

    return {
        "message": "Image uploaded successfully.",
        "prediction": "Human",
        "confidence": confidence,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
#     scan_barcodes()
