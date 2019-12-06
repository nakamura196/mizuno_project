import detect_divideline
import filter_backprocess
import get_interval
import resize
import os, json
from multiprocessing import Pool
from PIL import Image

if __name__ == "__main__":
    hojo_name = "偽絳帖 三 [A005936-03]"
    characterIsBlack = False
    contents    = os.listdir("../../input/images/{}/".format(hojo_name))
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-1 #hojo.txtを数えないことに注意！

    #画像をリサイズ（関数内でマルチプロセス化）
    #resize.resize_hojo(hojo_name)

    #GCPから文字サイズを取得
    #もうあったらやらない
    if not os.path.exists("../../output/{}/rintervals.json".format(hojo_name)):
        get_interval.generate_rintervals(hojo_name)

    #中央値フィルターをかける
    ##まず準備
    with open("../../output/{}/rintervals.json".format(hojo_name)) as f:
        rintervals = json.load(f)

    iter_ = []
    for page in range(1, page_leng+1):
        im = Image.open("../../input/images/{}/p{}/resized.jpg".format(hojo_name, page))
        width, height = im.size
        iter_.append((hojo_name, page, width*rintervals["p{}".format(page)]))

    with Pool(processes=3) as pool:
        pool.map(filter_backprocess.filter_image, iter_)

    #背景処理
    with Pool(processes=3) as pool:
        pool.map(filter_backprocess.make_back_black, iter_)

    #行探知
    line_place = []
    for page in range(1, page_leng+1):
        lines_in_page = detect_divideline.detect_divideline(hojo_name, page, rintervals["p{}".format(page)], characterIsBlack)
        line_place.append({"p{}".format(page):lines_in_page})

    line_place_js = line_place.json.dumps(line_place)
    with open("../../output/{}/line_place.json", "w") as f:
        f.write(line_place_js)
