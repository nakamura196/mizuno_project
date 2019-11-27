import numpy as np
import os
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

#前処理
def preprocess_image(hojo_name):
    boundary = 400

    im = Image.open("./input/{}.jpg".format(hojo_name)).convert("RGB").filter(ImageFilter.MedianFilter(size=3))
    w, h = im.size

    #画素値がboundary以下を黒にする
    for x in range(w):
        for y in range(h):
            px = sum(im.getpixel((x, y)))
            if px < boundary:
                im.putpixel((x, y), (0, 0, 0))

    im.save("./intermediates/pp_{}.jpg".format(hojo_name))

#とりあえず黒地に白文字のものを対象とする
#各行を切った画像を入力する必要がある
def move_measure(hojo_name):
    letter_size = 80
    around_diff_limit = 6.8

    #準備
    im = Image.open("./intermediates/pp_{}.jpg".format(hojo_name))
    width, height = im.size
    n = letter_size
    center_x = int(width/2)

    print("measuring rgb_vals")
    #画素値をリストに保存する
    pixel_list = []
    for y in range(height):
        y_list = []
        for x in range(width):
            rgb_vals = []
            r, g, b = im.getpixel((x, y))
            rgb_vals.append(r)
            rgb_vals.append(g)
            rgb_vals.append(b)
            y_list.append(rgb_vals)
        pixel_list.append(y_list)

    print("calculating gravity point")
    #各yの重心を決定
    cx = []
    for y0 in range(height):
        cx_y_above = 0
        cx_y_below = 0
        for y in range(max(y0-n, 0), min(height, y0+n)):
            for x in range(width):
                cx_y_above += sum(pixel_list[y][x]) * x
                cx_y_below += sum(pixel_list[y][x])
        cx.append(int(cx_y_above/cx_y_below))

    around_diff = [0 for _ in range(height)]

    for y0 in range(height):
        for y in range(max(y0-n, 0), min(height, y0+n)):
            around_diff[y0] += cx[y] - center_x

    print("moving pixels")
    #重心に基づいて画素を動かす
    for y in range(height):
        if center_x > cx[y] and abs(around_diff[y]) >= around_diff_limit*width:
            x_max = width - center_x + cx[y]
            for x in range(x_max):
                r = pixel_list[y][x][0]
                g = pixel_list[y][x][1]
                b = pixel_list[y][x][2]
                im.putpixel((x + center_x - cx[y], y), (r, g, b))
            for x in range(center_x - cx[y]):
                im.putpixel((x, y), (0, 0, 0))
        elif center_x < cx[y] and abs(around_diff[y]) >= around_diff_limit*width:
            x_max = width - cx[y] + center_x
            for x in range(x_max):
                r = pixel_list[y][x + cx[y] - center_x][0]
                g = pixel_list[y][x + cx[y] - center_x][1]
                b = pixel_list[y][x + cx[y] - center_x][2]
                im.putpixel((x, y), (r, g, b))
            for x in range(x_max, width):
                im.putpixel((x, y), (0, 0, 0))

    im.save("./output/revised_measured_{}.jpg".format(hojo_name))


preprocess_image("resized")
move_measure("resized")
