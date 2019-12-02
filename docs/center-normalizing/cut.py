from PIL import Image
import numpy as np
from scipy import signal
import json

#黒地の法帖限定
def calculate_hojo_brightness(hojo_img_path):
    im = Image.open(hojo_img_path)
    width, height = im.size

    color_x = [0 for i in range(width)]
    color_y = [0 for i in range(height)]

    for x in range(width):
        for y in range(height):
            brightness = im.getpixel((x, y))
            color_x[x] += brightness
            color_y[y] += brightness

    return color_x, color_y, height

def generate_letter_size(hojo_name, page):
    #Google Cloud Visionからゲットした結果を利用
    with open("./images/{}/rintervals.json".format(hojo_name), "r") as f:
        rintervals = json.load(f)

    rinterval_arg  = "../images/{}/p{}/{}-p{}.jpg".format(hojo_name, page, hojo_name, page)
    relative_line_interval = rintervals[rinterval_arg]

    im = Image.open("./intermediates/{}/pp/pp_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height = im.size

    line_interval = int(width*relative_line_interval)

    return line_interval

def detect_horizon(color_y, height):
    #y方向の切り出し座標y1, y2を見つける
    y1, y2 = 0, 0
    divide_val = int(sum(color_y)/len(color_y))

    for i in range(height-1):
        if color_y[i] > divide_val and color_y[i+1] < divide_val:
            y1 = i+1
        elif color_y[i] < divide_val and color_y[i+1] > divide_val:
            y2 = i
            break

    return y1, y2

def detect_vertical(color_x, line_interval):
    #x方向の行切り出しを見つける
    color_x_np = np.array(color_x)
    localmins  = signal.argrelmin(color_x_np, order=line_interval)
    x_line_list = localmins[0].tolist()
    x_line_list.append(0)
    x_line_list.sort()
    x_line_list.reverse()

    return x_line_list
