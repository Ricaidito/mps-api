from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from services.face_recognition_service import FaceRecognitionService
from services.image_service import ImageService
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/get-images")
def get_all_images():
    images = ImageService.get_all_images()
    return images


@app.post("/upload-person")
def upload_person(person_picture: UploadFile):
    ImageService.save_image(person_picture)
    return {"imageFileName": person_picture.filename, "extension": person_picture.content_type}


@app.post("/recon-by-file")
async def recognize_face_by_file(person_picture: UploadFile):
    result = await FaceRecognitionService.recognize_by_image(person_picture)
    if "error" in result.keys():
        return result
    return {"result": result["foundMatch"], "matches": result["matches"], "images": result["images"]}


@app.delete("/delete-image/{fileName}")
def delete_person_image(fileName: str):
    result = ImageService.delete_image(fileName)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
