from PIL import Image, ImageFilter
import os
import numpy as np
from scipy import signal

#中央値フィルタリング
def filter_image(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]

    if os.path.exists("../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page)):
        print("Filtering {} page {} has already done".format(hojo_name, page))
        return

    print("Page {} filtering started".format(page))

    im = Image.open("../input/images/{0}/p{1}/{0}-p{1}.jpg".format(hojo_name, page)).convert("RGB").filter(ImageFilter.MedianFilter(size=3))
    w, h = im.size

    #画像サイズが十分大きかったらフィルターをかける
    if line_interval >= 150:
        im.filter(ImageFilter.MedianFilter(size=5))
    elif line_interval >= 90:
        im.filter(ImageFilter.MedianFilter(size=3))

    im.save("../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page))

    print("finished filtering page {}".format(page))

#背景処理（閾値以下の画素を真っ黒にする）
def make_back_black(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    boundary = iter_[3]

    if os.path.exists("../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page)):
        print("Backprocessing {} page {} has already done".format(hojo_name, page))
        return

    print("Page {} background processing started".format(page))

    #開いてグレースケール化
    im = Image.open("../output/{}/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height = im.size
    im = im.convert("L")

    #画素値がboundary以下を黒にする
    for x in range(width):
        for y in range(height):
            brightness = im.getpixel((x, y))
            if brightness < boundary:
                im.putpixel((x, y), 0)

    im.save("../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))

    print("finished background processing page {}".format(page))

#極小となるところに目印をつける
def detect_divideline(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]

    #準備
    im              = Image.open("../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height   = im.size
    color           = [0 for i in range(width)]
    print("{} page {}: loaded image".format(hojo_name, page))

    #行ごとにRGB平均値（明るさ）を計算しリストに格納
    print("{} page {}: calculating RGB values...".format(hojo_name, page))
    for x in range(width):
        for y in range(height):
            color[x] += im.getpixel((x, y))
    print("{} page {}: finished calculating brightness of each pixel".format(hojo_name, page))

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

if __name__ == "__main__":
    #法帖のリスト読み込み
    hojos = os.listdir("../input/manifest")
    if ".DS_Store" in hojos:
        hojos.remove(".DS_Store")

    #個別法帖について処理
    for hojo in hojos:
        #下準備
        hojo_name = hojo.replace(".json", "")
        contents = os.listdir("../input/images/{}".format(hojo_name))
        if ".DS_Store" in contents:
            contents.remove(".DS_Store")
        page_leng = len(contents)-1
        print("--------------line detection for {}--------------".format(hojo_name))

        print("--------------")
        print("boundary value for {}?".format(hojo_name))
        boundary = int(input())
        print("--------------")

        #場所整理
        if not os.path.exists("../output/{}".format(hojo_name)):
            os.mkdir("../output/{}".format(hojo_name))
        if not os.path.exists("../output/{}/preprocessed/filtered/".format(hojo_name)):
            os.makedirs("../output/{}/preprocessed/filtered/".format(hojo_name))
        if not os.path.exists("../output/{}/preprocessed/back_black/".format(hojo_name)):
            os.mkdir("../output/{}/preprocessed/back_black/".format(hojo_name))
        if not os.path.exists("../output/{}/line_place".format(hojo_name)):
            os.mkdir("../output/{}/line_place".format(hojo_name))

        #中央値フィルターをかける
        ##まず準備
        with open("../output/{}/rintervals.json".format(hojo_name)) as f:
            rintervals = json.load(f)

        iter_ = []
        for page in range(1, page_leng+1):
            im = Image.open("../input/images/{0}/p{1}/{0}-p{1}.jpg".format(hojo_name, page))
            width, height = im.size
            iter_.append((hojo_name, page, int(width*rintervals["p{}".format(page)]), boundary))

        with Pool(processes=3) as pool:
            pool.map(filter_image, iter_)

        #背景処理
        with Pool(processes=3) as pool:
            pool.map(make_back_black, iter_)

        #行探知
        with Pool(processes=3) as pool:
            hojo_lines = pool.map(detect_divideline, iter_)

        line_place = {}
        for i in range(len(hojo_lines)):
            page = hojo_lines[i][0]
            page_lines = hojo_lines[i][1]
            line_place["p{}".format(page)] = page_lines

        line_place_js = json.dumps(line_place)
        with open("../output/{}/line_place/line_place.json".format(hojo_name), "w") as f:
            f.write(line_place_js)

        print("----------saved line_place-----------")
