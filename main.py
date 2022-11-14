import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from services.face_recognition_service import FaceRecognitionService
from services.image_service import ImageService

app = FastAPI()

# CORS configuration
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static folder for images
app.mount("/images", StaticFiles(directory="images"), name="images")


# Redirect to swagger docs
@app.get("/", description="Redirect to the swagger docs")
def swagger_redirect():
    return RedirectResponse("http://127.0.0.1:8000/docs")


# Get all images in the images folder
@app.get("/get-images", description="Get all of the images in the images static folder")
def get_all_images():
    return ImageService.get_all_images()


# Upload a picture of a person
@app.post("/upload-person", description="Upload the picture of the person given by the user")
def upload_person(person_picture: UploadFile):
    ImageService.save_image(person_picture)
    return {"imageFileName": person_picture.filename, "extension": person_picture.content_type}


# Do the face recognition with a given image uploaded by the user
@app.post("/recon-by-file", description="Do the face recognition and get the results and matches")
async def recognize_face_by_file(person_picture: UploadFile):
    result = await FaceRecognitionService.recognize_by_image(person_picture)
    if "error" in result.keys():
        return result
    return {"result": result["foundMatch"], "matches": result["matches"], "images": result["images"]}


# Delete an image by the file name
@app.delete("/delete-image/{fileName}", description="Delete an image based on the file name")
def delete_person_image(fileName: str):
    return ImageService.delete_image(fileName)


# Run the API in reload mode
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
