import pixelhouse as ph
import numpy as np
import json, os


def transform(C, coords):
    for key, val in coords.items():
        val = [(C.inverse_transform_x(x), C.inverse_transform_y(y))
               for x, y in val]
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


'''
def glitch(C, coords, color="r", n=5, dx=1.0, dy=1.0, refinements=2):

    # Smooth the eye coordinates a bit
    coords = chaikins_corner_cutting(coords, refinements=refinements)
    ex, ey = zip(*coords)
    
    # Scale glow based of the extent in the x direction
    box_extent = coords.max(axis=0) - coords.min(axis=0)
    x_extent = box_extent[0]
    ratio = box_extent[0]/box_extent[1]

    dx *= x_extent/15
    wl = 2.5
    # Make a copy of the image with a transparent mask
    C2 = C.copy()
    C2.img[:, :, 3] = 255
    C2 += ph.transform.elastic.wave(amplitude=3*dx,wavelength=wl)
    C2 += ph.transform.elastic.wave(amplitude=dx,wavelength=wl/7)
    #C2 += ph.transform.elastic.wave(amplitude=dx,wavelength=wl/14,offset=0.2)
    # Cutout the eyeballs
    C += C2

    
    C.show()
    exit()
'''

def shadowing(C, coords, color="r", n=5, dx=1.0, dy=1.0, refinements=2):

    # Smooth the eye coordinates a bit
    coords = chaikins_corner_cutting(coords, refinements=refinements)

    ex, ey = zip(*coords)

    # Scale glow based of the extent in the x direction
    box_extent = coords.max(axis=0) - coords.min(axis=0)
    x_extent = box_extent[0]
    ratio = box_extent[0]/box_extent[1]

    dx *= x_extent
    dy *= x_extent/ratio/2

    #print(dx)

    # Make a copy of the image with a transparent mask
    C2 = C.copy()
    C2.img[:, :, 3] = 255

    # 'Glow' around the mask
    eye = ph.polyline(ex, ey, is_filled=1, color=color)
    C2 += ph.filters.glow(eye, glow_x=dx, glow_y=dy, n=n)

    # Erase the mask
    C2 += ph.polyline(ex, ey, is_filled=1, color=[0, 0, 0, 0])

    '''
    # Optionally erase everything below the centroid
    pts = np.where(C2.img[:,:,3]<255)
    x_pts = C.inverse_transform_x(pts[1].astype(float))
    y_pts = C.inverse_transform_y(pts[0].astype(float))

    ey = np.array(ey)
    idx = y_pts < np.array(ey).mean()
    x_idx = pts[1][idx]
    y_idx = pts[0][idx]
    C2[pts[0][idx], pts[1][idx]] = C[pts[0][idx], pts[1][idx]]
    '''
    
    # Overlay the glow
    C += C2


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


name = os.path.basename(f_jpg)
f_json = os.path.join(f"data/landmarks/{name}.json")

with open(f_json) as FIN:
    js = json.load(FIN)[0]

#print(js.keys())
#exit()

C = ph.load(f_jpg)
transform(C, js)

def find_check_center(eye_label):
    
    # Find cheek, estimate a surface
    eye = js[eye_label]
    eye_centroid = eye.mean(axis=0)


    if eye_label == 'left_eye':
        idx = np.argmin(js['top_lip'][:,0])
    else:
        idx = np.argmax(js['top_lip'][:,0])
        
    lip = js['top_lip'][idx]
    cheek_center = (eye_centroid + lip)/2
    eye_extent = (eye.max(axis=0) - eye.min(axis=0))[0]

    return cheek_center, eye_extent
    

'''
cheek_center, eye_extent = find_check_center('left_eye')
n_pts = 1000
scale = np.array([eye_extent, eye_extent])/3
pts = np.random.normal(loc=cheek_center, scale=scale, size=[n_pts,2])

color = [155,55,55,155]

with C.layer() as C2:
    for pt in pts:
        C2 += ph.circle(pt[0], pt[1], r=0.01, color=color)
    #C2 += ph.filters.gaussian_blur(blur_x=.35, blur_y=.35)

cheek_center, eye_extent = find_check_center('right_eye')
n_pts = 1000
scale = np.array([eye_extent, eye_extent])/3
pts = np.random.normal(loc=cheek_center, scale=scale, size=[n_pts,2])


with C.layer() as C2:
    for pt in pts:
        C2 += ph.circle(pt[0], pt[1], r=0.01, color=color)
''' 

glitch(C, js['right_eye'])
exit()

compute(C, color="k", n_blend=10, blur=0.4, opacity=0.6).show()

for p in pal:
    compute(C, color=p, n_blend=10, blur=0.4, opacity=0.6).show()
