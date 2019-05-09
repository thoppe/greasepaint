import pixelhouse as ph
import cv2
import numpy as np
import json, os


def transform(C, coords):
    for key, val in coords.items():
        val = [(C.inverse_transform_x(x), C.inverse_transform_y(y))
               for x, y in val]
        coords[key] = np.array(val)

def compute_centroids(coords):
    for key, val in list(coords.items()):
        coords[f'{key}_centroid'] = np.array(val).mean(axis=0)


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



def compute(canvas,
            color=[0, 0, 0], opacity=0.6, n_blend=10, blur=0.3, n_applications=1
):
    C = canvas.copy()
    
    # Adjust color to have specified opacity
    color = ph.color.matplotlib_colors(color)[:3]
    liner_color = list(color) + [np.clip(opacity * 255, 0, 255)]

    for k in range(n_applications):

        right_eye = js['right_eye']
        left_eye = js['left_eye']
        
        shadowing(C, right_eye, color=liner_color, dx=blur, n=n_blend)
        shadowing(C, left_eye, color=liner_color, dx=blur, n=n_blend)

        #shadowing(C, js["top_lip"], color=liner_color, dx=blur, n=n_blend)
        #shadowing(C, js["bottom_lip"], color=liner_color, dx=blur, n=n_blend)

        
    return C

pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]

f_jpg = "data/source_images/tessa1.jpg"
#f_jpg = 'data/source_images/emilia-clarke-no-makeup-blonde-brown-ftr.jpg'
#f_jpg = 'data/source_images/obama-600x587.jpg'
#f_jpg = 'data/source_images/000360.jpg'

def cutbox(canvas, pts, pixel_buffer=0, n_bbox_smoothing=2):
    pts = np.array(pts)
    #pts = chaikins_corner_cutting(pts, n_bbox_smoothing).astype(np.int64)

    hull = cv2.convexHull(pts)
    
    bbox = np.array([
        [pts[:,1].min(),pts[:,1].max()],
        [pts[:,0].min(),pts[:,0].max()]
    ])
    bbox[:,0] -= pixel_buffer
    bbox[:,1] += pixel_buffer

    mask = np.zeros((*canvas.img.shape[:2],3), canvas.img.dtype)

    cv2.fillConvexPoly(mask, hull,color=[255,]*3)
    #cv2.fillPoly(mask, hull,color=[255,]*3)

    #mask[:,:] = [255,]*3
    #mask = 255 * np.ones(canvas.img.shape, canvas.img.dtype)
    #mask = mask[:,:,:3]

    img = canvas.img[bbox[0,0]:bbox[0,1], bbox[1,0]:bbox[1,1]]
    mask = mask[bbox[0,0]:bbox[0,1], bbox[1,0]:bbox[1,1]]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    mask = cv2.dilate(mask,kernel,iterations = 13)

    img = img[:,:,:3]
    return img, mask


def pastebox(canvas, img, mask, location):
    

    canvas.img[:,:,:3] = cv2.seamlessClone(
        img[:,:,:3],
        canvas.img[:,:,:3],
        mask, tuple(location), cv2.NORMAL_CLONE)


name = os.path.basename(f_jpg)
f_json = os.path.join(f"data/landmarks/{name}.json")

with open(f_json) as FIN:
    js = json.load(FIN)[0]
compute_centroids(js)

C = ph.load(f_jpg)
org = C.copy()

img, mask = cutbox(C, js['right_eye'],50)
minds_eye = (js['right_eye_centroid'] + js['left_eye_centroid'])/2

np.random.seed(44)

minds_eye = (js['right_eye_centroid'] + js['left_eye_centroid'])/2
minds_eye[1] -= 100
minds_eye = minds_eye.round().astype(int)

dx = 0.75
img = cv2.resize(img, (0,0), fx=dx, fy=dx)
mask = cv2.resize(mask, (0,0), fx=dx, fy=dx) 



pastebox(C, img, mask, minds_eye)
C.show()
