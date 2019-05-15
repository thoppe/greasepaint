import pixelhouse as ph
import cv2

from . import shadowing
from .utils import transform
from .landmarks import FaceFinder
from .shadowing import eye_makeup

face_finder = FaceFinder("hog")


def _apply_eye_makeup(image, **kwargs):

    # Load the image in, transform the coordinates to the shape of the canvas
    if isinstance(image, str):
        canvas = ph.load(image)
        landmarks = face_finder(image)[0]
    elif isinstance(image, ph.Canvas):
        canvas = image
        landmarks = face_finder(canvas.img[:, :, :3])[0]
    else:
        print(f"Unknown type {type(image)}")

    transform(canvas, landmarks)
    return eye_makeup(canvas, landmarks, **kwargs)


def eyeliner(image, color="k", n_blend=10, blur=0.4, opacity=1.0):
    return _apply_eye_makeup(
        image, color=color, n_blend=n_blend, blur=blur, opacity=opacity
    )


def eyeshadow(image, color, n_blend=40, blur=0.8, opacity=0.6):
    return _apply_eye_makeup(
        image, color=color, n_blend=n_blend, blur=blur, opacity=opacity
    )
