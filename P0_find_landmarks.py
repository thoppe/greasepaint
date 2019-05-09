import face_recognition
import os, json

save_dest = "data/landmarks"
os.system(f"mkdir -p {save_dest}")


def f_image_to_landmark_file(f_image):
    name = os.path.basename(f_image) + ".json"
    return os.path.join(save_dest, name)


def locate_landmarks(f_image, save_data=False, model="hog"):

    
    if save_data:
        f_json = f_image_to_landmark_file(f_image)
        if os.path.exists(f_json):
            return False
    
    
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(f_image)

    faces = face_recognition.face_locations(image, model=model)   
    landmarks = face_recognition.face_landmarks(image, face_locations=faces)


    if len(landmarks) == 0:
        landmarks = {}

    if save_data:
        js = json.dumps(landmarks)

        with open(f_json, "w") as FOUT:
            FOUT.write(js)

        print(f"Saved {len(landmarks)} faces to {f_json}")

    return landmarks


if __name__ == "__main__":
    from tqdm import tqdm
    import glob
    import joblib, sys

    JPG = sorted(glob.glob(f"data/source_images/*.jpg"))
    func = joblib.delayed(locate_landmarks)
    ITR = tqdm(JPG)

    with joblib.Parallel(1, batch_size=2) as MP:
        MP(func(x, save_data=True) for x in ITR)
