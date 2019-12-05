import os
import urllib.request
import sys
import time

def get_iiif_images(info, hojo_name):
    #法帖に関する基本データと収納場所を作成
    path1 = "../../../input/images/{}/".format(hojo_name)
    if not os.path.exists(path1):
        os.mkdir(path1)
    with open(path1+"hojo_info.txt", "w") as f:
        f.write("{}\n".format(info["@id"]))
        f.write("{}\n".format(info["identifier"]))

    sequence_num = len(info)-2 #@idとidentifierを除いた数
    page = 1
    for number in range(1, sequence_num+1):
        for sequence in info["sequence_{}".format(number)]:
            canvas, image_url = sequence[0], sequence[1]
            path2 = path1 + "p{}/".format(page)
            if not os.path.exists(path2):
                os.mkdir(path2)

            #canvas_idを保存するためのファイルを作成
            with open(path2+"canvas_id.txt", "w") as f:
                f.write(canvas)

            #画像ダウンロード
            image_name = hojo_name.replace(".json", "")+"-p{}".format(page)
            urllib.request.urlretrieve(image_url, path2+"{}.jpg".format(image_name))

            #諸々の手続き的事項
            print("downloaded {}".format(image_name))
            page += 1
            time.sleep(3)
