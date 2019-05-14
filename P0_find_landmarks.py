from greasepaint import FaceFinder
import os, json, glob
from tqdm import tqdm

save_dest = "data/landmarks"
os.system(f"mkdir -p {save_dest}")

clf = FaceFinder()

def f_image_to_landmark_file(f_image):
    name = os.path.basename(f_image) + ".json"
    return os.path.join(save_dest, name)


def locate_landmarks(f_image):

    f_json = f_image_to_landmark_file(f_image)
    if os.path.exists(f_json):
        return False

    # Load the jpg file into a numpy array
    landmarks = clf(f_image)

    js = json.dumps(landmarks)

    with open(f_json, "w") as FOUT:
        FOUT.write(js)

    print(f"Saved {len(landmarks)} faces to {f_json}")
    return landmarks


if __name__ == "__main__":   

    JPG = sorted(glob.glob(f"data/source_images/*.jpg"))
    for f in tqdm(JPG):
        locate_landmarks(f)
