#1つのmanifestに1つのselection
#1つのselectionに各行の情報を入力する
import cut
import centernormalize
import json, os
from PIL import Image

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
        rinterval_arg  = "." + hojo_path+"{}-p{}.jpg".format(hojo_name, page)
        relative_line_interval = rintervals[rinterval_arg]

        #前処理
        centernormalize.preprocess_image(hojo_name, page)

        #行探知と上下の決定
        print("detecting lines")
        hojo_img_path = "./intermediates/{}/pp_{}_p{}.jpg".format(hojo_name, hojo_name, page)
        color_x, color_y, line_interval, height = cut.hojo_init(hojo_img_path, relative_line_interval)
        y1, y2 = cut.detect_horizon(color_y, height)
        x_line_list = cut.detect_vertical(color_x, line_interval)

        print("Page {} centering began".format(page))
        for i in range(len(x_line_list)-1):
            print("Page {} line {} centering began".format(page, i+1))

            #画像の複製
            x1, x2 = x_line_list[i], x_line_list[i+1]
            im = Image.open(hojo_img_path)
            copied_im = im.copy()
            cropped_im = copied_im.crop((x1, y1, x2, y2))
            cropped_im.save("./intermediates/{}/{}-p{}-line_{}.jpg".format(hojo_name, hojo_name, page, i+1))

            #中心位置正規化
            centernormalize.move_to_center(hojo_name, page, i+1)
            print("Moved center")

        print("--------------------------------------------------------")

hojo_line_centering("偽絳帖 三 [A005936-03]")
