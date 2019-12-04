import numpy as np
from PIL import Image

#とりあえず黒地に白文字のものを対象とする
#各行を切った画像を入力する必要がある
def move_to_center(hojo_name, page, line):
    #準備
    im = Image.open("./intermediates/{}/lines/{}-p{}-line_{}.jpg".format(hojo_name, hojo_name, page, line))
    width, height = im.size
    n = around_letter_size
    center_x = int(width/2)

    around_letter_size = width
    around_diff_limit = 6.8

    print("at Page {} line {}: Measuring rgb_vals".format(page, line))
    #画素値をリストに保存する
    pixel_list = []
    for y in range(height):
        y_list = []
        for x in range(width):
            brightness_vals = []
            brightness = im.getpixel((x, y))
            brightness_vals.append(brightness)
            y_list.append(brightness)
        pixel_list.append(y_list)

    print("at Page {} line {}: Calculating gravity point".format(page, line))
    #各yの重心を決定
    cx = []
    for y0 in range(height):
        cx_y_above = 0
        cx_y_below = 0
        for y in range(max(y0-n, 0), min(height, y0+n)):
            for x in range(width):
                cx_y_above += pixel_list[y][x] * x
                cx_y_below += pixel_list[y][x]
        if cx_y_below == 0:
            cx_y_above = center_x
            cx_y_below = 1

        cx.append(int(cx_y_above/cx_y_below))

    #周辺の中心位置からの距離を保存
    around_diff = [0 for _ in range(height)]

    for y0 in range(height):
        for y in range(max(y0-n, 0), min(height, y0+n)):
            around_diff[y0] += cx[y] - center_x

    print("at Page {} line {}: Moving pixels".format(page, line))
    #重心に基づいて画素を動かす
    #周りがあまり中心から離れていないことがaround_diffからわかる場合は処理は行わない
    for y in range(height):
        if center_x > cx[y] and abs(around_diff[y]) >= around_diff_limit*width:
            x_max = width - center_x + cx[y]
            for x in range(x_max):
                brightness = pixel_list[y][x]
                im.putpixel((x + center_x - cx[y], y), brightness)
            for x in range(center_x - cx[y]):
                im.putpixel((x, y), 0)
        elif center_x < cx[y] and abs(around_diff[y]) >= around_diff_limit*width:
            x_max = width - cx[y] + center_x
            for x in range(x_max):
                brightness = pixel_list[y][x + cx[y] - center_x]
                im.putpixel((x, y), brightness)
            for x in range(x_max, width):
                im.putpixel((x, y), 0)

    im.save("./output/{}/centered_{}-p{}-line_{}.jpg".format(hojo_name, hojo_name, page, line))
