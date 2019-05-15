import os
import face_recognition


class FaceFinder:
    def __init__(self, model_name="hog"):
        self.model_name = model_name

    def __call__(self, image):

        if isinstance(image, str):
            assert os.path.exists(image)
            image = face_recognition.load_image_file(image)

        faces = face_recognition.face_locations(image, model=self.model_name)
        landmarks = face_recognition.face_landmarks(image, face_locations=faces)

        return landmarks
