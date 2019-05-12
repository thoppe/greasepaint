import pixelhouse as ph
import numpy as np
import h5py
import os
import cv2

#f_image = "data/source_images/obama-600x587.jpg"
f_image = "data/source_images/John_Cena_2012.jpg"
#f_image = "data/source_images/emilia-clarke-no-makeup-blonde-brown-ftr.jpg"
f_h5 = os.path.join('data/masks/', os.path.basename(f_image))+'.h5'

with h5py.File(f_h5) as h5:
    mask = h5['mask0']['mask'][...]

C = ph.load(f_image)
print(C.shape, C.img.shape)


def pastebox(canvas, img, fmask, location):
    mask = np.zeros((*canvas.img.shape[:2], 3), canvas.img.dtype)
    mask[fmask] = [255]*3

    canvas.img[:, :, :3] = cv2.seamlessClone(
        img[:, :, :3], canvas.img[:, :, :3], mask, tuple(location),
        #cv2.NORMAL_CLONE
        cv2.MIXED_CLONE
    )


#C.img[mask] = 155
#C.show()
#exit()



#loc = C.shape[1]//2, C.shape[0]//2
loc = C.shape[1]//2, C.shape[0]//2
C.show()

for i in range(200):
    print(i)
    C2 = C.copy()
    C2 += ph.filters.gaussian_blur(2,2)

    #pastebox(C, C2.img, mask, loc)
    pastebox(C, C2.img, ~mask, loc)
    C.show()
