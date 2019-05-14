import numpy as np

def transform(C, coords):
    for key, val in coords.items():
        val = [
            (C.inverse_transform_x(x),
             C.inverse_transform_y(y)) for x, y in val]
        coords[key] = np.array(val)


def chaikins_corner_cutting(coords, refinements=1):
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
