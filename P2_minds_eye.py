import pixelhouse as ph
import cv2
import numpy as np
import json, os
from scipy.signal import convolve2d
import imutils

from greasepaint import face_finder
from greasepaint.utils import compute_centroids, cutbox

np.random.seed(44)


def pastebox(canvas, source, mask, location):
    canvas.rgb = cv2.seamlessClone(
        source.rgb, canvas.rgb, mask, tuple(location), cv2.NORMAL_CLONE
    )


def regions_of_high_intensity(canvas, blocksize=3, kernel_size=5):

    # If color, remove the alpha channel and covert (assume BGR!)
    img = cv2.cvtColor(canvas.rgb, cv2.COLOR_RGB2GRAY)

    # Compute the an adaptive Threshold
    lap = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, 4)

    kernel = np.ones([kernel_size] * 2)
    sig = convolve2d(255 - lap, kernel, mode="full", boundary="symm")
    sig /= kernel.sum()
    sig = sig.astype(lap.dtype)

    return ph.Canvas(img=sig)


def transform_image(
    img, scale=1.0, flip_horizontal=False, flip_vertical=False, rotate_angle=0
):
    if scale != 1:
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

    if flip_horizontal:
        img = cv2.flip(img, 1)

    if flip_vertical:
        img = cv2.flip(img, 0)

    if rotate_angle:
        img = imutils.rotate(img, rotate_angle)

    return img


f_jpg = "data/source_images/tessa1.jpg"

landmarks = face_finder(f_jpg)[0]
compute_centroids(landmarks)

C = ph.load(f_jpg)#.resize(0.5).save("docs/images/tessa1.jpg")
org = C.copy()

eye, mask, full_mask = cutbox(C, landmarks["right_eye"], 50)

# Blow out the mask a bit
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.dilate(mask, kernel, iterations=10)

minds_eye = landmarks["right_eye_centroid"] + landmarks["left_eye_centroid"]
minds_eye /= 2

minds_eye[1] -= 100
minds_eye = minds_eye.round().astype(int)


#avg = C.img[full_mask>0].mean(axis=0).astype(np.uint8)
#C[full_mask>0] = avg
#C.show()
#pastebox(C, eye, mask, minds_eye)
#exit()

C.rgb = cv2.seamlessClone(eye.rgb, C.rgb, mask, tuple(minds_eye), cv2.NORMAL_CLONE)

#intensity = regions_of_high_intensity(org, blocksize=7, kernel_size=3)
#intensity.show()
#exit()

C.copy().resize(0.5).save("docs/images/tessa1_third_eye.png")

C.show()
