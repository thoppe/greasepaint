import pixelhouse as ph
import numpy as np
import h5py
import os, random
import cv2, glob
from tqdm import tqdm

mask_dir = "data/movie_mask/"
save_dest = "data/person_glow"

os.system(f"mkdir -p {save_dest}")


def load_mask(f_image):

    f_h5 = os.path.join(mask_dir, os.path.basename(f_image)) + ".h5"

    if not os.path.exists(f_h5):
        print(f"Missing mask for {f_image}")
        return None

    mask = None
    with h5py.File(f_h5) as h5:
        for key in h5:
            if h5[key].attrs["label"] != "person":
                continue

            if mask is None:
                mask = h5[key]["mask"][...]
            else:
                mask += h5[key]["mask"][...]

    return mask


def pastebox(canvas, img, fmask, location):
    mask = np.zeros((*canvas.img.shape[:2], 3), canvas.img.dtype)
    mask[fmask] = [255] * 3
    canvas.img[:, :, :3] = cv2.seamlessClone(
        img[:, :, :3], canvas.img[:, :, :3], mask, tuple(location), cv2.MIXED_CLONE
    )


def person_ghost(f_image):
    loc = C.shape[1] // 2, C.shape[0] // 2
    
    for i in tqdm(range(20)):
        C2 = C.copy()
        C2 += ph.filters.gaussian_blur(0.1, 0.1)
        pastebox(C, C2.img, ~mask, loc)

    return C


f_image = "movies/000750.jpg"

F_IMAGE = sorted(glob.glob('movies/*.jpg'))
random.shuffle(F_IMAGE)


for f in tqdm(F_IMAGE):
    f_final = os.path.join(save_dest, os.path.basename(f))
    mask = load_mask(f)
    
    if mask is None:
        continue

    C = ph.load(f)   
    C = person_ghost(f)
    #C.show()
    C.save(f_final)
    print(f_final)





