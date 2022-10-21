import os
import cv2
import face_recognition
from typing import Any
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
def enconde_images(paths: list[str]) -> list[ndarray]:
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


# Do the face recognition given an image and it's path to compare
def recognize_by_image_path(image_to_compare_path: str) -> dict[str, Any]:
    images, paths = load_images()
    encodings = enconde_images(paths)

    img = cv2.imread(image_to_compare_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_econding = face_recognition.face_encodings(rgb_img)[0]

    results = face_recognition.compare_faces(encodings, img_econding)

    matches = get_matches(results, images)

    recognition = {
        "image": image_to_compare_path,
        "foundMatch": any(results),
        "matches": matches,
        "resultsArray": results,
        "numberOfImagesCompared": len(results)

    }

    return recognition


def main():
    result = recognize_by_image_path("unknown.jpg")
    print(result)


if __name__ == "__main__":
    main()
