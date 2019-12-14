import cv2
import os
import numpy as np
import pandas as pd
import time

def read_des(csv_path):
    des = pd.read_csv(csv_path).values

    return des

def compare_image(query_name, hojo_name):
    img = cv2.imread("./query/{}.jpg".format(query_name))
    detector = cv2.AKAZE_create()

    kp_q, des_q = detector.detectAndCompute(img, None)

    images = os.listdir("./{}".format(hojo_name))
    if ".DS_Store" in images:
        images.remove(".DS_Store")


    ranking = []
    search_start = time.time()
    for image in images:
        img_t = cv2.imread("./{}/{}".format(hojo_name, image))
        kp, des = detector.detectAndCompute(img_t, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des, des_q, k=2)

        point = 0
        match_param = 0.7
        for m, n in matches:
            if m.distance < match_param*n.distance:
                point += 1
        ranking.append([point, image])
    search_end = time.time()

    """
    print(len(des_q[0]))
    print(type(des_q))

    search_targets = os.listdir("./feature_vecs_csv")
    if ".DS_Store" in search_targets:
        search_targets.remove(".DS_Store")

    ranking = []
    for target in search_targets:
        csv_names = os.listdir("./feature_vecs_csv/{}".format(target))
        if ".DS_Store" in csv_names:
            csv_names.remove("DS_Store")

        for csv in csv_names:
            des = read_des("./feature_vecs_csv/{}/{}".format(target, csv))
            print(len(des[0]))
            print(type(des))

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des, des_q, k=2)

            point = 0
            match_param = 0.7
            for m, n in matches:
                if m.distance < match_param*n.distance:
                    point += 1
            ranking.append([point, csv])

    """
    ranking.sort()
    ranking.reverse()
    for i in range(5):
        print(ranking[i])

    print(search_end-search_start)

if __name__ == "__main__":
    compare_image("hojo4", "偽絳帖 三 [A005936-03]")
