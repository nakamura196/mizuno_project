import cut
import centernormalize
import img_info
import preprocessing
import json, os
from PIL import Image
from multiprocessing import Pool

def hojo_line_centering(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]

    print("Page {} line detection began".format(page))

    #切り出し行の決定
    print("at Page {}: detecting lines...".format(page))
    hojo_img_path = "./intermediates/{}/pp/pp_{}_p{}.jpg".format(hojo_name, hojo_name, page)
    color_x, color_y, height = img_info.calculate_hojo_brightness(hojo_img_path)
    y1, y2 = cut.detect_horizon(color_y, height)
    x_line_list = cut.detect_vertical(color_x, line_interval)

    print("Page {} centering began".format(page))
    for i in range(len(x_line_list)-1):
        #1、2、最後の部分は文字がないから飛ばしちゃう
        if i == 0 or i > len(x_line_list)-3:
            print("Page {} line {} is skipped".format(page, i+1))
            continue

        print("Page {} line {} centering".format(page, i+1))

        #画像の複製
        x1, x2 = x_line_list[i+1], x_line_list[i] #縦書きの行に合わせるためx_line_listを逆ソートしてるので、これも逆になる
        im = Image.open(hojo_img_path)
        copied_im = im.copy()
        cropped_im = copied_im.crop((x1, y1, x2, y2))
        cropped_im.save("./intermediates/{}/lines/{}-p{}-line_{}.jpg".format(hojo_name, hojo_name, page, i+1))

        #中心位置正規化
        centernormalize.move_to_center(hojo_name, page, i+1)
        print("at Page {} line {}: Moved center".format(page, i+1))


def main(hojo_name):
    #読み込み準備
    cont_path   = "./images/{}/".format(hojo_name)
    contents    = os.listdir(cont_path)
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-2 #hojo_info.txt, rintervals.jsonを除くことに注意！

    #場所整理
    #中間生成物の場所
    if not os.path.exists("./intermediates/{}/".format(hojo_name)):
        os.mkdir("./intermediates/{}/".format(hojo_name))
    if not os.path.exists("./intermediates/{}/pp/".format(hojo_name)):
        os.mkdir("./intermediates/{}/pp/".format(hojo_name))
    if not os.path.exists("./intermediates/{}/lines/".format(hojo_name)):
        os.mkdir("./intermediates/{}/lines/".format(hojo_name))
    #出力の場所
    output_path = "./output/{}/".format(hojo_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    #前処理
    iter_ = []
    for page in range(1, page_leng+1):
        iter_.append((hojo_name, page, img_info.generate_letter_size(hojo_name, page)))

    with Pool(processes=3) as pool:
        pool.map(filter.filter_image, iter_)

    return

    #行検知と中心位置正規化
    with Pool(processes=3) as pool:
        pool.map(hojo_line_centering, iter_)

if __name__ == "__main__":
    main("星鳳楼帖 寅 [A005935-03]")
