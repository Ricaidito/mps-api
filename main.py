import pprint
from face_recognition_helper import recognize_by_image_path


def main():
    results = recognize_by_image_path("unknown.jpg")
    pprint.pprint(results)


if __name__ == "__main__":
    main()
