#1つのmanifestに1つのselection
#1つのselectionに各行の情報を入力する
import detect_divideline
import get_interval
import json, os

def create_iiif_desc(iter_):
    characterIsBlack = False
    hojo_name = iter_[0]
    characterIsBlack = iter_[1]

    #読み込み準備
    hojo_path   = "../images/{}/".format(hojo_name)
    contents    = os.listdir(hojo_path)
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-1 #hojo_info.txtを除くことに注意！

    #法帖についての情報をゲット
    with open(hojo_path+"hojo_info.txt", "r") as f:
        hojo_info    = f.readlines()
        manifest_url = hojo_info[0].replace("\n", "")
        identifier   = hojo_info[1].replace("\n", "")

    #出力の場所
    output_path = "../curation/{}/".format(hojo_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    #全体の大枠を作る
    iiif_json = {}
    iiif_json["@context"]   = ["http://iiif.io/api/presentation/2/context.json", "http://codh.rois.ac.jp/iiif/curation/1/context.json"]
    iiif_json["@id"]        = "https://mp.ex.nii.ac.jp/api/curation/json/" + hojo_name#identifier
    iiif_json["@type"]      = "cr:Curation"
    iiif_json["label"]      = "https://mp.ex.nii.ac.jp/api/curation/json/" + hojo_name#identifier
    iiif_json["selections"] = []

    #共通のselectionを作る
    selection = {}
    selection["@id"]       = "{}/range1".format(iiif_json["@id"])
    selection["@type"]     = "sc:Range"
    selection["label"]     = "Manual curation by IIIF Curation Viewer"
    selection["members"]   = []
    selection["within"] = {"@id":manifest_url, "@type":"sc:Manifest", "label":hojo_name}

    #ページごとにmemberを作る
    #前にGoogle Cloud Visionから結果をゲットしてたらそれを利用
    if os.path.exists("../curation/{}/rintervals.json".format(hojo_name)):
        with open("../curation/{}/rintervals.json".format(hojo_name), "r") as f:
            rintervals = json.load(f)
    else:
        #保存結果がなかったらGoogle Cloud VisionにAPIで問合せ
        rintervals = {}
        for page in range(1, page_leng+1):
            print("Page {} request".format(page))
            hojo_path = "../images/{}/p{}/".format(hojo_name, page)
            hojo_img_path = hojo_path+"{}-p{}.jpg".format(hojo_name, page)
            relative_line_interval = get_interval.calculate_line_interval(hojo_path, hojo_img_path)
            rintervals[hojo_img_path] = relative_line_interval
            print("--------------------------------------------------------")
        with open("../curation/{}/rintervals.json".format(hojo_name), "w") as f:
            rint_json = json.dumps(rintervals)
            f.write(rint_json)

    #行探知
    for page in range(1, page_leng+1):
        print("Page {} line detection began".format(page))
        #準備
        hojo_path   = "../images/{}/p{}/".format(hojo_name, page)
        hojo_img_path  = hojo_path+"{}-p{}.jpg".format(hojo_name, page)
        canvas_id_path = hojo_path+"canvas_id.txt"
        relative_line_interval = rintervals[hojo_img_path]
        detected_lines = detect_divideline.detect_divideline(hojo_path, relative_line_interval, characterIsBlack)
        print("detected lines")

        with open(canvas_id_path, "r") as f:
            canvas_id = f.readlines()[0]

        #memberを作成
        for i in range(len(detected_lines)):
            member = {"@type":"sc:Canvas"}
            member["@id"]   = canvas_id+detected_lines[i]
            member["label"] = "Page-{} Pixel-base line {}".format(page, i)
            member["metadata"] = []
            member["metadata"].append({"label":"作品名", "value":""})
            member["metadata"].append({"label":"行", "value":""})
            selection["members"].append(member)
        print("added members")

        print("--------------------------------------------------------")

    iiif_json["selections"].append(selection)

    #出力
    output = json.dumps(iiif_json)
    with open(output_path+"{} curation.json".format(hojo_name), "w") as f:
        f.write(output)

    with open("/Users/aquan/git/mizuno_project/docs/curation/{} curation.json".format(hojo_name), "w") as f:
        f.write(output)
