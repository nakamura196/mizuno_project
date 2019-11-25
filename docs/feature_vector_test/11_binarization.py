import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json

import cv2
import numpy as np



files = glob.glob("data/original/*.jpg")

for file in files:
    print(file)

    # 入力画像の読み込み
    img = cv2.imread(
        file)

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 方法2 （OpenCVで実装）
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    # 結果を出力
    cv2.imwrite(
        file.replace("original", "binarized").replace(".jpg", "_b.jpg"), th)
