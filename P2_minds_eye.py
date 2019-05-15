import pixelhouse as ph
import cv2
import numpy as np
import json, os
from scipy.signal import convolve2d
import imutils

from greasepaint import face_finder
from greasepaint.utils import compute_centroids

np.random.seed(44)


def cutbox(canvas, pts, pixel_buffer=0):
    '''
    Given a set of points, cuts out of the canvas a bounding box with
    pixel_buffer number of pixels outside of the bbox,
    '''
    
    pts = np.array(pts)

    y0 = pts[:, 0].min() - pixel_buffer
    y1 = pts[:, 0].max() + pixel_buffer

    x0 = pts[:, 1].min() - pixel_buffer
    x1 = pts[:, 1].max() + pixel_buffer
    
    mask = np.zeros(canvas.shape[:2], canvas.img.dtype)

    hull = cv2.convexHull(pts)
    cv2.fillConvexPoly(mask, hull, color=255)

    img = canvas.rgb[x0:x1, y0:y1]
    mask = mask[x0:x1, y0:y1]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.dilate(mask, kernel, iterations=13)

    return img, mask


def pastebox(canvas, img, mask, location):
    canvas.rgb = cv2.seamlessClone(
        img, canvas.rgb, mask, tuple(location), cv2.MIXED_CLONE
    )


def regions_of_high_intensity(img, blocksize=3, kernel_size=5):

    # If color, remove the alpha channel and covert (assume BGR!)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)

    # Compute the an adaptive Threshold
    lap = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, 4
    )

    kernel = np.ones([kernel_size] * 2)
    sig = convolve2d(255 - lap, kernel, mode="full", boundary="symm")
    sig /= kernel.sum()
    sig = sig.astype(lap.dtype)

    return sig


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

C = ph.load(f_jpg)
org = C.copy()

minds_eye = landmarks["right_eye_centroid"] + landmarks["left_eye_centroid"]
minds_eye /= 2

minds_eye[1] -= 100
minds_eye = minds_eye.round().astype(int)

img, mask = cutbox(C, landmarks["right_eye"], 50)
dx = .9
args = {
    "scale": dx,
    "flip_horizontal": False,
    "flip_vertical": False,
    "rotate_angle": 0,
}

img = transform_image(img, **args)
mask = transform_image(mask, **args)

pastebox(C, img, mask, minds_eye)

intensity = regions_of_high_intensity(C.img, blocksize=7, kernel_size=3)
org.img = np.dstack([intensity] * 3)
org.show()

C.copy().resize(0.5).save("docs/images/tessa1_third_eye.png")

C.show()
