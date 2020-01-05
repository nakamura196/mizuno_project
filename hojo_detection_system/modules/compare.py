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

def compare_image():
    #検索画像の読み込み
    img = cv2.imread("./query/preprocessed.jpg")
    detector = cv2.AKAZE_create()

    kp_q, des_q = detector.detectAndCompute(img, None)

    hojo_features = os.listdir("./feature_vecs_csv")
    if ".DS_Store" in hojo_features:
        hojo_features.remove(".DS_Store")

    #検索開始
    ranking = []
    hojo_count = {}

    #feature_vecs_csv/にある各法帖の各ページ各行の特徴量と比較
    for hojo_name in hojo_features:
        csv_names = os.listdir("./feature_vecs_csv/{}".format(hojo_name))
        if ".DS_Store" in csv_names:
            csv_names.remove(".DS_Store")

        #検索結果で同じ法帖が多すぎないようにするための保持変数
        hojo_count[hojo_name] = {"shown_count": 0}

        #各行のAKAZE特徴量を比較
        for csv in csv_names:
            des = read_des("./feature_vecs_csv/{}/{}".format(hojo_name, csv))
            if np.sum(des) == 0:
                continue

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des, des_q, k=2)

            point = 0
            match_param = 0.65
            for m, n in matches:
                if m.distance < match_param*n.distance:
                    point += 1

            #検索結果がかぶらないようにする準備
            data = csv.replace(".csv", "").split("_")
            hojo_name   = data[0]
            page        = data[1]
            line_num    = data[2] -1 #画像やCSVファイルの名前は1-indexed, 処理上は0-indexed
            hojo_count[hojo_name][page] = 0

            ranking.append([point, hojo_name, page, line_num])

    ranking.sort()
    ranking.reverse()

    #被りすぎないように検索結果を表示
    idx = 0
    top5 = []

    while True:
        hojo_name = ranking[idx][1]
        page = ranking[idx][2]

        #同一法帖は3つまで、同一法帖の同一ページは2つまで
        if hojo_count[hojo_name][page] < 2 and hojo_count[hojo_name]["shown_count"] < 3:
            hojo_count[hojo_name][page] += 1
            hojo_count[hojo_name]["shown_count"] += 1
            top5.append(ranking[idx])
            idx += 1
        else:
            idx += 1

        if len(top5) == 5:
            break

    return top5
