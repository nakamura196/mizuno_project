from PIL import Image, ImageFilter
import os

#前処理
def filter_image(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]

    if os.path.exists("../../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page)):
        print("Filtering {} page {} has already done".format(hojo_name, page))
        return

    print("Page {} filtering started".format(page))

    im = Image.open("../../input/images/{}/p{}/resized.jpg".format(hojo_name, page)).convert("RGB").filter(ImageFilter.MedianFilter(size=3))
    w, h = im.size

    #画像サイズが十分大きかったらフィルターをかける
    #多分ここも最終的にはline_intervalに応じて変わることになる
    if line_interval >= 150:
        im.filter(ImageFilter.MedianFilter(size=5))
    elif line_interval >= 90:
        im.filter(ImageFilter.MedianFilter(size=3))

    im.save("../../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page))

    print("finished filtering page {}".format(page))

def make_back_black(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]

    if os.path.exists("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page)):
        print("Backprocessing {} page {} has already done".format(hojo_name, page))
        return

    print("Page {} background processing started".format(page))

    #最終的にはline_intervalに応じてboundaryを変えるかもしれない
    im = Image.open("../../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height = im.size
    boundary = 100
    im = im.convert("L")

    #画素値がboundary以下を黒にする
    for x in range(width):
        for y in range(height):
            brightness = im.getpixel((x, y))
            if brightness < boundary:
                im.putpixel((x, y), 0)

    im.save("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))

    print("finished background processing page {}".format(page))
