import os

import cv2
import face_recognition
import numpy as np
from fastapi import UploadFile
from numpy import ndarray


# Folder where the known images are stored
KNOWN_IMAGES_FOLDER_PATH = "./images"


# Load all the known images and get their paths and file names
def load_images() -> tuple[str, str]:
    image_files = os.listdir(KNOWN_IMAGES_FOLDER_PATH)
    images_path: list[str] = []

    for file in image_files:
        images_path.append(f"{KNOWN_IMAGES_FOLDER_PATH}/{file}")

    return (image_files, images_path)


# Get the encondings for all of the known images
def encode_images(paths: list[str]) -> list[ndarray]:
    encodings: list[ndarray] = []

    for image in paths:
        img = cv2.imread(image)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_econding = face_recognition.face_encodings(rgb_img)[0]
        encodings.append(img_econding)

    return encodings


# Get the matches in the results array
def get_matches(results: list[bool], image_files: list[str]) -> list[str]:
    matches: list[str] = []

    for i, match in enumerate(image_files):
        if results[i]:
            matches.append(match)

    return matches


# Do the face recognition given an image uploaded by the user
async def recognize_by_image_file(person_image: UploadFile):
    images, paths = load_images()
    encodings = encode_images(paths)

    img_bytes = await person_image.read()
    img_array = np.fromstring(img_bytes, np.uint8)

    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_econding = face_recognition.face_encodings(rgb_img)

    # If no faces are found return the error dict
    if not len(img_econding):
        return {"error": "No faces found!"}

    results = face_recognition.compare_faces(encodings, img_econding[0])

    matches = get_matches(results, images)

    matches_urls = []

    for match in matches:
        matches_urls.append(f"http://127.0.0.1:8000/images/{match}")

    return {
        "image": person_image.filename,
        "foundMatch": any(results),
        "matches": matches_urls,
        "resultsArray": results,
        "numberOfImagesCompared": len(results),
        "images": matches
    }


# Wrapper class for the service
class FaceRecognitionService:
    def recognize_by_image(image: UploadFile):
        return recognize_by_image_file(image)
