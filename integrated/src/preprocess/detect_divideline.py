import os
import numpy as np
from scipy import signal
from PIL import Image, ImageDraw

def detect_divideline(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]
    characterIsBlack = iter_[3]

    #準備
    im              = Image.open("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height   = im.size
    color           = [0 for i in range(width)]
    print("{} page {}: loaded resized image".format(hojo_name, page))

    #行ごとにRGB平均値（明るさ）を計算しリストに格納
    print("{} page {}: calculating RGB values...".format(hojo_name, page))
    for x in range(width):
        for y in range(height):
            color[x] += im.getpixel((x, y))
    print("{} page {}: finished calculating brightness of each pixel".format(hojo_name, page))

    #白背景の場合はリスト内で実質的な色反転
    if characterIsBlack:
        for x in range(width):
            color[x] = 255 - color[x]

    #離散データである明るさから極小となる部分を探索
    show_color      = np.array(color)
    localmins       = signal.argrelmin(show_color, order=line_interval)
    color_line_list = localmins[0].tolist()
    print("{} page {}: finished finding local minimums".format(hojo_name, page))

    color_line_list.append(0) #左端が切れないようにする
    color_line_list.sort()
    color_line_list = color_line_list[::-1]

    #出力はリサイズしたものであることに注意！
    output = []
    for i in range(len(color_line_list)-1):
        x1 = color_line_list[i+1]
        x2 = color_line_list[i]
        y1 = 0
        y2 = height
        output.append([x1, x2, y1, y2])

    return page, output
