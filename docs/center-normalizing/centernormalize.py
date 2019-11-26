import numpy as np
import os
from PIL import Image

boundary = 450

#とりあえず黒地に白文字のものを対象とする
#各行を切った画像を入力する必要がある
def detect_center():
    #準備
    im = Image.open()
    n = SIZE_OF_LETTER
    center_x = int(width/2)

    #画素値をリストに保存する
    pixel_list = []
    for y in range(height):
        rgb_vals = []
        for x in range(width):
            px = im.getpixel((x, y))
            rgb_vals.append(px)
        pixel_list.append(rgb_vals)

    #各yの重心を決定
    cx = []
    for y0 in range(height):
        cx_y_above = 0
        cx_y_below = 0
        for y in range(max(y0-n, 0), min(height, y0+n)):
            for x in range(width):
                cx_y_above += pixel_list[y][x] * x
                cx_y_below += pixel_list[y][x]
        cx.append(int(cx_y_above/cx_y_below))

    #重心に基づいて画素を動かす
    for y in range(height):
        for x in range(width):
            if center_x > cx[y]:
                func()
            elif center_x < cx[y]:
                func()

def preprocess_image(image_name):
    im = Image.open("./{}.jpg".format(image_name))
    w, h = im.size　

    #画素値がboundary以下を黒にする
    for x in range(w):
        for y in range(h):
            px = im.getpixel((x, y))
            if px < boundary:
                im.putpixel((x, y), (0, 0, 0))

    #グレイスケール変換
    im = im.convert("L")
    im.save("./output/pp_{}.jpg".format(image_name))

    return im
