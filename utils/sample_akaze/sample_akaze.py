import numpy as np
import cv2
import os, time
from PIL import Image, ImageFilter

def generate_sameness(hojo_name1, hojo_name2):
    img1 = cv2.imread('{}.jpg'.format(hojo_name1),0)
    img2 = cv2.imread('./cmp_image/{}.jpg'.format(hojo_name2),0)
    #特徴抽出機の生成
    detector = cv2.AKAZE_create()
    #kpは特徴的な点の位置 destは特徴を現すベクトル
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    return kp1, des1
    #特徴点の比較機
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    #割合試験を適用
    good = []
    match_param = 0.7
    point = 0
    for m,n in matches:
        if m.distance < match_param*n.distance:
            good.append([m])
            point += 1
    #cv2.drawMatchesKnnは適合している点を結ぶ画像を生成する
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good, None,flags=2)
    output_name = "cmp_{}_and_{}".format(hojo_name1, hojo_name2)
    cv2.imwrite("./output/shift_result_{}_{}_{}.png".format(point, hojo_name1, hojo_name2), img3)

def query_formatting(hojo_name):
    im = Image.open("{}.jpg".format(hojo_name))
    im = im.convert("L").filter(ImageFilter.MedianFilter())
    w, h = im.size
    for x in range(w):
        for y in range(h):
            brightness = im.getpixel((x, y))
            if brightness <= 100:
                im.putpixel((x, y), 0)

    im.save("{}_q.jpg".format(hojo_name))
    return "{}_q".format(hojo_name)


def time_check(hojo_name1, hojo_name2):
    start = time.time()
    img1 = cv2.imread('{}.jpg'.format(hojo_name1),0)
    img1_time = time.time()
    img2 = cv2.imread('{}.jpg'.format(hojo_name2),0)
    img2_time = time.time()
    #特徴抽出機の生成
    detector = cv2.AKAZE_create()
    detector_time = time.time()
    #kpは特徴的な点の位置 destは特徴を現すベクトル
    kp1, des1 = detector.detectAndCompute(img1, None)
    kpdes1_time = time.time()
    kp2, des2 = detector.detectAndCompute(img2, None)
    kpdes2_time = time.time()

    #特徴点の比較機
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    cmpgene_time = time.time()

    #割合試験を適用
    good = []
    match_param = 0.7
    point = 0
    for m,n in matches:
        if m.distance < match_param*n.distance:
            good.append([m])
            point += 1
    cmp_time = time.time()

    print("img1_time: {}".format(img1_time- start))
    print("img2_time: {}".format(img2_time - img1_time))
    print("detector_time: {}".format(detector_time - img2_time))
    print("kpdes1_time: {}".format(kpdes1_time-detector_time))
    print("kpdes2_time: {}".format(kpdes2_time-kpdes1_time))
    print("cmpgene_time: {}".format(cmpgene_time-kpdes2_time))
    print("cmp_time: {}".format(cmp_time-cmpgene_time))

time_check("sample1", "sample2")

"""
hojos = os.listdir("./cmp_image/")
if ".DS_Store" in hojos:
    hojos.remove(".DS_Store")

for hojo in hojos:
    hojo = hojo.replace(".jpg", "")
    generate_sameness("hojo5", hojo)
    kp1, des1 = generate_sameness(query_formatting("hojo5"), hojo)
    print(len(kp1))
    print(len(des1))
    break
"""
