import cv2
import os
import numpy as np
import pandas as pd
import time
from PIL import Image, ImageFilter

#csvから特徴量を読み込む
def read_des(csv_path):
    try:
        des_int64 = pd.read_csv(csv_path).values
    #空ファイルならスキップ用の目印出力
    except pd.io.common.EmptyDataError:
        return np.array(0)
    des = des_int64.astype(np.uint8)

    return des

def query_formatting(hojo_name):
    im = Image.open("./query/{}.jpg".format(hojo_name))
    im = im.convert("L").filter(ImageFilter.MedianFilter())
    w, h = im.size
    for x in range(w):
        for y in range(h):
            brightness = im.getpixel((x, y))
            if brightness <= 100:
                im.putpixel((x, y), 0)

    im.save("./query/{}_q.jpg".format(hojo_name))
    return "{}_q".format(hojo_name)

def compare_image(query_name):
    #検索画像の読み込み
    img = cv2.imread("./query/{}.jpg".format(query_name))
    detector = cv2.AKAZE_create()

    kp_q, des_q = detector.detectAndCompute(img, None)

    search_targets = os.listdir("./feature_vecs_csv")
    if ".DS_Store" in search_targets:
        search_targets.remove(".DS_Store")

    #検索開始
    ranking = []
    search_start = time.time()
    #feature_vecs_csv/にある各法帖の各ページ各行の特徴量と比較
    for target in search_targets:
        csv_names = os.listdir("./feature_vecs_csv/{}".format(target))
        if ".DS_Store" in csv_names:
            csv_names.remove("DS_Store")

        for csv in csv_names:
            des = read_des("./feature_vecs_csv/{}/{}".format(target, csv))
            if np.sum(des) == 0:
                continue

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des, des_q, k=2)

            point = 0
            match_param = 0.65
            for m, n in matches:
                if m.distance < match_param*n.distance:
                    point += 1
            ranking.append([point, csv])

    search_end = time.time()
    ranking.sort()
    ranking.reverse()
    for i in range(10):
        print(ranking[i])

    print(search_end-search_start)


if __name__ == "__main__":
    compare_image(query_formatting("hojo5"))
