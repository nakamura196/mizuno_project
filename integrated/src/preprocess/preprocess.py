import detect_divideline
import filter_backprocess
import get_interval
import resize
import os, json
from multiprocessing import Pool
from PIL import Image

if __name__ == "__main__":
    #準備
    hojo_name = "泉州本淳化閣帖 八 [A006099-05]"
    characterIsBlack = False
    contents    = os.listdir("../../input/images/{}/".format(hojo_name))
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-1 #hojo.txtを数えないことに注意！

    #場所整理
    if not os.path.exists("../../output/{}".format(hojo_name)):
        os.mkdir("../../output/{}".format(hojo_name))
    if not os.path.exists("../../output/{}/preprocessed/filtered/".format(hojo_name)):
        os.makedirs("../../output/{}/preprocessed/filtered/".format(hojo_name))
    if not os.path.exists("../../output/{}/preprocessed/back_black/".format(hojo_name)):
        os.mkdir("../../output/{}/preprocessed/back_black/".format(hojo_name))

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
        iter_.append((hojo_name, page, int(width*rintervals["p{}".format(page)]), characterIsBlack))

    with Pool(processes=3) as pool:
        pool.map(filter_backprocess.filter_image, iter_)

    #背景処理
    with Pool(processes=3) as pool:
        pool.map(filter_backprocess.make_back_black, iter_)

    #行探知
    with Pool(processes=3) as pool:
        hojo_lines = pool.map(detect_divideline.detect_divideline, iter_)

    line_place = {}
    for i in range(len(hojo_lines)):
        page = hojo_lines[i][0]
        page_lines = hojo_lines[i][1]
        line_place["p{}".format(page)] = page_lines

    line_place_js = json.dumps(line_place)
    with open("../../output/{}/line_place.json".format(hojo_name), "w") as f:
        f.write(line_place_js)
