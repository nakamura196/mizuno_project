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
    if os.path.exists("./query/{}_q.jpg".format(hojo_name)):
        return "{}_q".format(hojo_name)

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

def call_image(hojo_name, page, line):
    im_path = "./{}/{}_{}_{}.jpg".format(hojo_name, hojo_name, page, line)
    im = Image.open(im_path)
    return im

def connect_image(im1, im2):
    img = Image.new('L', (im1.width + im2.width, max(im1.height, im2.height)))
    img.paste(im1, (0, 0))
    img.paste(im2, (im1.width, 0))
    return img

def compare_image(query_name):
    #検索画像の読み込み
    img = cv2.imread("./query/{}.jpg".format(query_name))
    detector = cv2.AKAZE_create()

    kp_q, des_q = detector.detectAndCompute(img, None)

    hojo_features = os.listdir("./feature_vecs_csv")
    if ".DS_Store" in hojo_features:
        hojo_features.remove(".DS_Store")

    #検索開始
    ranking = []
    hojo_count = {}
    search_start = time.time()

    #feature_vecs_csv/にある各法帖の各ページ各行の特徴量と比較
    for hojo_name in hojo_features:
        csv_names = os.listdir("./feature_vecs_csv/{}".format(hojo_name))
        if ".DS_Store" in csv_names:
            csv_names.remove("DS_Store")

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
            line_num    = data[2]
            hojo_count[hojo_name][page] = 0

            ranking.append([point, hojo_name, page, line_num])

    search_end = time.time()
    ranking.sort()
    ranking.reverse()

    #被りすぎないように検索結果を表示
    current_num = 0
    total_show_count = 0

    #検索を画像で表示
    im_right = Image.new("L", (1, 900), 0)
    while True:
        point       = ranking[current_num][0]
        hojo_name   = ranking[current_num][1]
        page        = ranking[current_num][2]
        line_num    = ranking[current_num][3]

        #同一法帖は3つまで、同一法帖の同一ページは2つまで
        if hojo_count[hojo_name][page] < 2 and hojo_count[hojo_name]["shown_count"] < 3:
            hojo_count[hojo_name][page] += 1
            hojo_count[hojo_name]["shown_count"] += 1
            print("Resembleness: {}".format(point))
            print("Hojo: {}".format(hojo_name))
            print("Page: {}".format(page.replace("p", "")))
            print("Line: {}".format(line_num.replace("line", "")))
            print("------------------------------------------")

            #結果画像を作成
            im_left = call_image(hojo_name, page, line_num)
            im_right = connect_image(im_left, im_right)

            current_num += 1
            total_show_count += 1
        else:
            current_num += 1

        if total_show_count == 5:
            break

    print("Search time: {}".format(search_end-search_start))
    im_right.save("search_result_by_{}.jpg".format(query_name))
    im_right.show()


if __name__ == "__main__":
    print("Select query name: saikiku, kokonoka, marusai, or marukyu")
    query_name = input()
    compare_image(query_formatting(query_name))
