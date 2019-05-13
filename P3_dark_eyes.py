import pixelhouse as ph
import cv2
import numpy as np
import json, os
from scipy.signal import convolve2d
import imutils

np.random.seed(44)


def transform(C, coords):
    for key, val in coords.items():
        val = [(C.inverse_transform_x(x), C.inverse_transform_y(y)) for x, y in val]
        coords[key] = np.array(val)


def compute_centroids(coords):
    for key, val in list(coords.items()):
        coords[f"{key}_centroid"] = np.array(val).mean(axis=0)


def cutbox(canvas, pts, pixel_buffer=0, n_bbox_smoothing=0):
    pts = np.array(pts)

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
        img[:, :, :3], canvas.img[:, :, :3], mask, tuple(location),
        cv2.NORMAL_CLONE
    )

f_jpg = "data/source_images/tessa1.jpg"

name = os.path.basename(f_jpg)
f_json = os.path.join(f"data/landmarks/{name}.json")

with open(f_json) as FIN:
    js = json.load(FIN)[0]
compute_centroids(js)

C = ph.load(f_jpg)

img0, mask0 = cutbox(C, js["right_eye"], 10)
img1, mask1 = cutbox(C, js["left_eye"], 10)

C += ph.filters.instafilter("Reyes")
C += ph.filters.instafilter("Reyes")

pastebox(C, img0, mask0, np.array(js['right_eye_centroid']).astype(int))
pastebox(C, img1, mask1, np.array(js['left_eye_centroid']).astype(int))

#C.save("docs/images/third_eye.png")
C.show()
