import os
from fastapi import UploadFile


IMAGES_FOLDER_PATH = "./images/"


def save_picture(picture: UploadFile):
    file_location = IMAGES_FOLDER_PATH + picture.filename
    with open(file_location, "wb+") as f:
        f.write(picture.file.read())


def get_all_known_images():
    images = []
    image_names = os.listdir(IMAGES_FOLDER_PATH)
    for img_name in image_names:
        img_obj = {
            "fileName": img_name,
            "imagePath": f"http://127.0.0.1:8000/images/{img_name}"
        }
        images.append(img_obj)
    return images


# Test
def main():
    print(get_all_known_images())


# Wrapper class for the service
class ImageService:
    def save_image(picture: UploadFile):
        save_picture(picture)

    def get_all_images():
        return get_all_known_images()


if __name__ == "__main__":
    main()
