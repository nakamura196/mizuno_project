from PIL import Image, ImageFilter

#前処理
def filter_image(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]
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
