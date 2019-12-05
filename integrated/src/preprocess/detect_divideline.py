import os
from scipy import signal
from PIL import Image, ImageOps, ImageDraw

def detect_divideline(hojo_name, hojo_path, relative_line_interval, characterIsBlack):
    #準備
    RESIZE_RATIO = 3
    im              = Image.open("../../input/{}/p{}/resized.jpg".format(hojo_name, page))
    width, height   = im.size
    color           = [0 for i in range(width)]
    print("\tloaded resized image")

    #行ごとにRGB平均値（明るさ）を計算しリストに格納
    print("\tcalculating RGB values...")
    for x in range(width):
        for y in range(height):
            color[x] += im.getpixel((x, y))
    print("\tfinished calculating brightness of each pixel")

    #白背景の場合はリスト内で実質的な色反転
    if characterIsBlack:
        for x in range(width):
            color[x] = 255 - color[x]

    #極小値をどのくらいの幅でとるかを確定
    line_interval   = int(relative_line_interval*width)

    #離散データである明るさから極小となる部分を探索
    show_color      = np.array(color)
    localmins       = signal.argrelmin(show_color, order=line_interval)
    color_line_list = localmins[0].tolist()
    print("\tfinished finding local minimums")

    color_line_list.append(0) #左端が切れないようにする
    color_line_list.sort()

    """
    detected_lines  = []
    for i in range(len(color_line_list)-1):
        retangle_w  = int(5*(color_line_list[i+1]-color_line_list[i]))
        retangle    = "#xywh={},{},{},{}".format(int(RESIZE_RATIO*color_line_list[i]), 0, retangle_w, RESIZE_RATIO*height)
        detected_lines.append(retangle)

    return detected_lines
    """
