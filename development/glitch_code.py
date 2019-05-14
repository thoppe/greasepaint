
"""

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
"""
