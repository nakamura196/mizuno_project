import numpy as np
import pandas as pd
import cv2
import os

def generate_des(image_path):
    img = cv2.imread(image_path, 0)
    detector = cv2.AKAZE_create()
    kp, des = detector.detectAndCompute(img, None)

    return des

def create_csv(hojo_name):
    images = os.listdir("./{}".format(hojo_name))
    if ".DS_Store" in images:
        images.remove(".DS_Store")

    #あとでコードの場所を変える
    if not os.path.exists("./feature_vecs_csv/{}".format(hojo_name)):
        os.makedirs("./feature_vecs_csv/{}".format(hojo_name))

    for image in images:
        des = generate_des("./{}/{}".format(hojo_name, image))
        df = pd.DataFrame(des)
        df.to_csv("./feature_vecs_csv/{}/{}".format(hojo_name, image.replace(".jpg", ".csv")), header=False, index=False)

if __name__ == "__main__":
    create_csv("偽絳帖 三 [A005936-03]")
