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

    #特徴点の比較機
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    #return matches

    #割合試験を適用
    good = []
    match_param = 0.8
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
    if os.path.exists("./{}_q.jpg".format(hojo_name)):
        return "{}_q".format(hojo_name)
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

hojo = "泉州本淳化閣帖 八 [A006099-05]_p17_line3"
generate_sameness(query_formatting("gihou_saikiku"), hojo)


"""hojos = os.listdir("./cmp_image/")
if ".DS_Store" in hojos:
    hojos.remove(".DS_Store")

for hojo in hojos:
    hojo = hojo.replace(".jpg", "")
    if hojo == "淳化閣帖第1-10。[8]_p15_line8":
        print(generate_sameness(query_formatting("marusai"), hojo))
"""
