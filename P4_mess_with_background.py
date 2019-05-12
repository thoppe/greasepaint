import pixelhouse as ph
import numpy as np
import h5py
import os
import cv2

# Light phantom, 20x on 0.1 gaussian blur, ~mask, MIXED_CLONE
#f_image = "data/source_images/obama-600x587.jpg"
#mask_dir = 'data/masks'

#f_image = "data/source_images/John_Cena_2012.jpg"
#f_image = "data/source_images/emilia-clarke-no-makeup-blonde-brown-ftr.jpg"

#f_image = 'movies/000587.jpg'
f_image = 'movies/000750.jpg'
mask_dir = 'data/movie_mask/'


f_h5 = os.path.join(mask_dir, os.path.basename(f_image))+'.h5'

mask = None
with h5py.File(f_h5) as h5:
    for key in h5:
        if h5[key].attrs['label'] != 'person':
            continue

        #if h5[key].attrs['label'] == 'person':
        #    continue

        if mask is None:
            mask = h5[key]['mask'][...]
        else:
            mask += h5[key]['mask'][...]

C = ph.load(f_image)
print(C.shape, C.img.shape)


def pastebox(canvas, img, fmask, location):
    mask = np.zeros((*canvas.img.shape[:2], 3), canvas.img.dtype)
    mask[fmask] = [255]*3
    
    #mask[:,:] = [255,255,255]
    #canvas.img[fmask] = 0
    #print(loc)
    #print(canvas.shape)
    #canvas.show()
    #exit()

    print(mask.shape, canvas.img.shape, img.shape)

    canvas.img[:, :, :3] = cv2.seamlessClone(
        img[:, :, :3], canvas.img[:, :, :3], mask, tuple(location),
        #cv2.NORMAL_CLONE
        cv2.MIXED_CLONE
        #cv2.MONOCHROME_TRANSFER
    )


#C.img[mask] = 155
#C.show()
#exit()



#loc = C.shape[1]//2, C.shape[0]//2
loc = C.shape[1]//2, C.shape[0]//2
#mask[0,0] = True
#mask[0,-1] = True
#mask[-1,0] = True
#mask[-1,-1] = True

C.show()
org = C.copy()

for i in range(2000):
    print(i)
    C2 = C.copy()
    C2 += ph.filters.gaussian_blur(0.1,0.1)

    #pastebox(C, C2.img, mask, loc)
    pastebox(C, C2.img, ~mask, loc)
    
    C.show()
