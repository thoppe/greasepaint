import pixelhouse as ph
import cv2
import numpy as np
import json, os
from scipy.signal import convolve2d
import imutils

from greasepaint import face_finder
from greasepaint.utils import chaikins_corner_cutting


np.random.seed(44)

def compute_centroids(coords):
    for key, val in list(coords.items()):
        coords[f"{key}_centroid"] = np.array(val).mean(axis=0)




def cutbox(canvas, pts, pixel_buffer=0, n_bbox_smoothing=0):
    pts = np.array(pts)

    if n_bbox_smoothing:
        pts = chaikins_corner_cutting(pts, n_bbox_smoothing).astype(np.int64)

    hull = cv2.convexHull(pts)

    bbox = np.array(
        [[pts[:, 1].min(), pts[:, 1].max()], [pts[:, 0].min(), pts[:, 0].max()]]
    )
    bbox[:, 0] -= pixel_buffer
    bbox[:, 1] += pixel_buffer

    mask = np.zeros((*canvas.img.shape[:2], 3), canvas.img.dtype)

    cv2.fillConvexPoly(mask, hull, color=[255] * 3)

    img = canvas.img[bbox[0, 0] : bbox[0, 1], bbox[1, 0] : bbox[1, 1]]
    mask = mask[bbox[0, 0] : bbox[0, 1], bbox[1, 0] : bbox[1, 1]]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.dilate(mask, kernel, iterations=13)

    img = img[:, :, :3]
    return img, mask


def pastebox(canvas, img, mask, location):
    canvas.img[:, :, :3] = cv2.seamlessClone(
        img[:, :, :3], canvas.img[:, :, :3], mask, tuple(location), cv2.NORMAL_CLONE
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

#intensity = regions_of_high_intensity(C.img, blocksize=7, kernel_size=3)
#org.img = np.dstack([intensity] * 3)
#org.show()

C.copy().resize(0.5).save("docs/images/tessa1_third_eye.png")

C.show()
