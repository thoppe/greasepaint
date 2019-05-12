import glob, os, json, sys
import h5py
from tqdm import tqdm
import numpy as np

save_dest = "../data/masks"
os.system(f"mkdir -p {save_dest}")

clf = None


if __name__ == "__main__":

    F_JPG = sorted(glob.glob(f"../data/source_images/*.jpg"))[::-1][1:]

    for f in tqdm(F_JPG):
        f_save = os.path.join(save_dest, os.path.basename(f))+'.h5'
        if os.path.exists(f_save):
            continue

        print(f_save)

        if not clf:
            from API import Masker
            clf = Masker()
        
        res = clf(f)

        print(res.keys())
        with h5py.File(f_save, 'w') as h5:

            for k in range(len(res['class_labels'])):
                
                g = h5.create_group(f'mask{k}')
                g['mask'] = res['masks'][:, :, k]
                
                g.attrs['label'] = res['class_labels'][k]
                g.attrs['score'] = res['scores'][k]

                label = res['class_labels'][k]

                print(f"{f_save} {label}")
