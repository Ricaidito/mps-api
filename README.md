# Missing person recognition system

API created for the purpose of serving a missing persons oriented web page with the ability to detect missing persons through facial recognition.

## How to run the API

**_Note: It is highly recommended that you create and use a Python virtual environment before installing packages and dependencies._**

1. Make sure you have the C++ Desktop Development tools (CMake)

2. Run `pip install cmake` in order to install the CMake Python dependencies

3. Run `pip install dlib` in order to install the dlib machine learning models

4. Run `pip install -r requirements.txt` to install the rest of the requierements

5. Run the `main.py` file

---

You can also run the API with the following command: `uvicorn main:app --reload`.
