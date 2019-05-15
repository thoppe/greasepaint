import numpy as np
import pixelhouse as ph
import cv2


def compute_centroids(coords):
    """
    Return the centroids of each object in the dict by adding to the dict
    a {key}_centroid with a single vector.
    """
    for key, val in list(coords.items()):
        coords[f"{key}_centroid"] = np.array(val).mean(axis=0)


def cutbox(canvas, pts, pixel_buffer=0):
    """
    Given a set of points, cuts out of the canvas a bounding box with
    pixel_buffer number of pixels outside of the bbox. Returns both the bbox
    image and a mask of the points within the bbox.
    """

    pts = np.array(pts)

    y0 = pts[:, 0].min() - pixel_buffer
    y1 = pts[:, 0].max() + pixel_buffer

    x0 = pts[:, 1].min() - pixel_buffer
    x1 = pts[:, 1].max() + pixel_buffer

    mask = np.zeros(canvas.shape[:2], canvas.img.dtype)

    hull = cv2.convexHull(pts)
    cv2.fillConvexPoly(mask, hull, color=255)

    img = canvas.img[x0:x1, y0:y1]
    submask = mask[x0:x1, y0:y1]

    return ph.Canvas(img=img), submask, mask


def transform(canvas, coords):
    """
    Transforms a dict of values within pixel space to canvas space.
    """

    for key, val in coords.items():
        val = [
            (canvas.inverse_transform_x(x), canvas.inverse_transform_y(y))
            for x, y in val
        ]
        coords[key] = np.array(val)


def chaikins_corner_cutting(coords, refinements=1):
    """
    Smooths an input set of coordinates by applying Chaikins.
    """

    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * 0.75 + R * 0.25

    return coords
