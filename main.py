from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.face_recognition_service import FaceRecognitionService
from services.image_service import ImageService


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


@app.get("/")
def index():
    return {"swagger": "http://127.0.0.1:8000/docs"}


@app.get("/get-images")
def get_all_images():
    images = ImageService.get_all_images()
    return images


@app.post("/upload-person")
def upload_person(person_picture: UploadFile):
    ImageService.save_image(person_picture)
    return {"imageFileName": person_picture.filename, "extension": person_picture.content_type}


@app.get("/recon-test")
def recognize_face_test():
    result = FaceRecognitionService.recognize_by_image_path()
    return {"result": result["foundMatch"]}


@app.post("/recon-by-file")
async def recognize_face_by_file(person_picture: UploadFile):
    result = await FaceRecognitionService.recognize_by_image(person_picture)
    if "error" in result.keys():
        return result
    return {"result": result["foundMatch"]}
