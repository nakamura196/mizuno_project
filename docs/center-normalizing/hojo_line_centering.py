#1つのmanifestに1つのselection
#1つのselectionに各行の情報を入力する
import cut
import json, os

def hojo_line_centering(hojo_name):
    #読み込み準備
    hojo_path   = "./images/{}/".format(hojo_name)
    contents    = os.listdir(hojo_path)
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-2 #hojo_info.txt, rintervals.jsonを除くことに注意！

    #出力の場所
    output_path = "./output/{}/".format(hojo_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    #Google Cloud Visionからゲットした結果を利用
    with open("./images/{}/rintervals.json".format(hojo_name), "r") as f:
        rintervals = json.load(f)

    #行探知
    for page in range(1, page_leng+1):
        print("Page {} line detection began".format(page))
        #準備
        hojo_path   = "./images/{}/p{}/".format(hojo_name, page)
        hojo_img_path  = "." + hojo_path+"{}-p{}.jpg".format(hojo_name, page)
        relative_line_interval = rintervals[hojo_img_path]
        color_x, color_y, line_interval = cut.hojo_init(hojo_path, relative_line_interval)
        y1, y2 = cut.detect_horizon(color_y)
        x_line_list = cut.detect_vertical(color_x, line_interval)
        print("detected lines")


        print("--------------------------------------------------------")
