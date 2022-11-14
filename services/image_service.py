import os
from fastapi import UploadFile


# Folder where the known images are stored
IMAGES_FOLDER_PATH = "./images/"


# Save the picture the user uploads on the images folder
def save_picture(picture: UploadFile):
    file_location = IMAGES_FOLDER_PATH + picture.filename
    with open(file_location, "wb+") as f:
        f.write(picture.file.read())


# Get the images json array with the name of the file and it's link to get it
def get_all_known_images():
    images = []
    image_names = os.listdir(IMAGES_FOLDER_PATH)
    for img_name in image_names:
        img_obj = {
            "fileName": img_name,
            "imagePath": f"http://127.0.0.1:8000/images/{img_name}",
            "personName": img_name.split(".")[0]
        }
        images.append(img_obj)
    return images


# Delete the image from its filename
def delete_image_from_path(image_path: str):
    path = f"{IMAGES_FOLDER_PATH}/{image_path}"
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


# Test
def main():
    print(get_all_known_images())


# Wrapper class for the service
class ImageService:
    def save_image(picture: UploadFile):
        save_picture(picture)

    def get_all_images():
        return get_all_known_images()

    def delete_image(path):
        return delete_image_from_path(path)


if __name__ == "__main__":
    main()
