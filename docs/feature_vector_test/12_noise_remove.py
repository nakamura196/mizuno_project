import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json

import cv2
import numpy as np



files = glob.glob("data/binarized/*.jpg")

for file in files:
    print(file)

    # 入力画像の読み込み
    img = cv2.imread(
        file)

    '''
    # 近傍の定義
    neiborhood = np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]],
                np.uint8)
    #膨張
    img_dilate = cv2.dilate(img,neiborhood,iterations=10)
    #収縮
    img_erode = cv2.erode(img_dilate,neiborhood,iterations=10)
    '''

    ksize=9
    #中央値フィルタ
    img_mask = cv2.medianBlur(img,ksize)

    # 結果を出力
    cv2.imwrite(
        file.replace("binarized", "noise_removed").replace("_b.jpg", "_nr.jpg"), img_mask)
