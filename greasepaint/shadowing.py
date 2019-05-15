import pixelhouse as ph
from .utils import chaikins_corner_cutting
import numpy as np


def shadowing(C, coords, color="r", n=5, dx=1.0, dy=1.0, n_refinements=2):
    """
    Shadows around a set of "coords" onto a canvas.
    Used for eye liner or eye shadow.

    n: number of times to diffuse the glow outwards (succesive applications)
    dx, dy: Glow in the x and y directions
    color: shadow color
    n_refinements: Number of times to smooth the points
    """

    # Smooth the coordinates a bit if requested
    coords = chaikins_corner_cutting(coords, refinements=n_refinements)

    ex, ey = zip(*coords)

    # Scale glow based of the extent in the x direction
    box_extent = coords.max(axis=0) - coords.min(axis=0)
    x_extent = box_extent[0]
    ratio = box_extent[0] / box_extent[1]

    dx *= x_extent
    dy *= x_extent / ratio

    # Make a copy of the image with a transparent mask
    C2 = C.copy()
    C2.alpha = 255

    # 'Glow' around the mask
    mask = ph.polyline(ex, ey, is_filled=1, color=color)
    C2 += ph.filters.glow(mask, glow_x=dx, glow_y=dy, n=n)

    # Erase the mask
    C2 += ph.polyline(ex, ey, is_filled=1, color=[0, 0, 0, 0])

    # Overlay the glow
    C += C2

    return C


def eye_makeup(canvas, landmarks, color="k", opacity=0.6, n_blend=10, blur=0.3):

    # Adjust color to have specified opacity
    color = ph.color.matplotlib_colors(color)[:3]
    liner_color = list(color) + [np.clip(opacity * 255, 0, 255)]

    right_eye = landmarks["right_eye"]
    left_eye = landmarks["left_eye"]

    args = {"color": liner_color, "dx": blur, "dy": blur / 2, "n": n_blend}

    C = canvas.copy()
    shadowing(C, right_eye, **args)
    shadowing(C, left_eye, **args)

    return C
