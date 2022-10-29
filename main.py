from fastapi import FastAPI, UploadFile
from face_recognition_helper import recognize_by_image_path, recognize_by_image_file


app = FastAPI()
TEST_PATH = "unknown.jpg"


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/recon")
async def recon():
    results = recognize_by_image_path(TEST_PATH)
    return {"result": results["foundMatch"]}


@app.post("/recon-by-file")
async def recon_by_file(file: UploadFile):
    results = await recognize_by_image_file(file)
    return {"result": results["foundMatch"]}
