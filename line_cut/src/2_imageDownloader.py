import urllib.request, json, os, time

#各作品のマニフェストファイルから、画像URLやページごとのCanvasタイプ情報などを抽出し、
#infoと名付けたリストで整理
def manifest2info(hojo_name):
    json_path = "../input/manifest/{}.json".format(hojo_name)
    with open(json_path) as f:
        manifest = json.load(f)

    #infoの構造：info={"@id":"hoge", "identifier":"fuga", "sequences":{}(後述)}
    info = {}

    info["identifier"]  = ""
    for data in manifest["metadata"]:
        if data["label"] == "identifier":
            info["identifier"]  = data["value"]
    info["@id"] = manifest["@id"]

    #{sequence_id: [[canvas1, image_url, width, height], [canvas2. image_url, width, height], ...]}という形
    #canvasはCanvasタイプのURI
    #UPARLはImage APIの形じゃないので、Thumbnailから持ってくる
    print("Is the file from Uparl? (y/n)")
    ans = input()
    utokyo = False
    if ans == "y":
        utokyo = True
    sequence_num = 1
    for sequence in manifest["sequences"]:
        info["sequence_{}".format(sequence_num)] = []
        for canvas in sequence["canvases"]:
            canvas_info = []
            canvas_info.append(canvas["@id"])
            if utokyo:
                canvas_info.append(canvas["thumbnail"]["@id"].replace("200,/0/default.jpg", "full/0/default.jpg"))
            else:
                for content in canvas["images"]:
                    canvas_info.append(content["resource"]["@id"])
            canvas_info.append(canvas["images"][0]["resource"]["width"])
            canvas_info.append(canvas["images"][0]["resource"]["height"])

            info["sequence_{}".format(sequence_num)].append(canvas_info)
        sequence_num += 1

    return info

#個別の法帖に関する基本データと画像保存場所を作成
def make_hojodir(info, hojo_name):
    hojodir = "../input/images/{}/".format(hojo_name)
    if not os.path.exists(hojodir):
        os.mkdir(hojodir)
    with open(hojodir+"hojo_info.txt", "w") as f:
        f.write("{}\n".format(info["@id"]))
        f.write("{}\n".format(info["identifier"]))
        f.write("{}\n".format(info["sequence_1"][0][2]))
        f.write("{}\n".format(info["sequence_1"][0][3]))

#画像のダウンロード
#画像サイズは(1000, *)で指定
def get_iiif_images(info, hojo_name):
    sequence_num = len(info)-2 #@idとidentifierを除いた数
    page = 1
    for number in range(1, sequence_num+1):
        for sequence in info["sequence_{}".format(number)]:
            canvas, image_url = sequence[0], sequence[1]
            pagedir = "../input/images/{}/p{}/".format(hojo_name, page)
            if not os.path.exists(pagedir):
                os.mkdir(pagedir)

            #canvas_idを保存するためのファイルを作成
            with open(pagedir+"canvas_id.txt", "w") as f:
                f.write(canvas)

            #画像サイズ指定
            image_url = image_url.replace("full/0/default.jpg", "1000,/0/default.jpg")
            #画像ダウンロード
            image_name = hojo_name+"-p{}".format(page)
            urllib.request.urlretrieve(image_url, pagedir+"{}.jpg".format(image_name))

            #諸々の手続き的事項
            print("downloaded {}".format(image_name))
            page += 1
            time.sleep(3)

if __name__ == "__main__":
    hojos = os.listdir("../input/manifest/")
    if ".DS_Store" in hojos:
        hojos.remove(".DS_Store")
    for hojo in hojos:
        hojo = hojo.replace(".json", "")
        print(hojo)
        info = manifest2info(hojo)
        make_hojodir(info, hojo)
        get_iiif_images(info, hojo)
