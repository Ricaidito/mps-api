from fastapi import FastAPI
from face_recognition_helper import recognize_by_image_path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/recon")
async def recon():
    results = recognize_by_image_path("unknown.jpg")
    return {"result": results["foundMatch"]}
