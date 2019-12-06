#1つのmanifestに1つのselection
#1つのselectionに各行の情報を入力する
import detect_divideline
import get_interval
import json, os
import hashlib

def create_manifest(iter_):
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
        #identifier   = hojo_info[1].replace("\n", "")
    identifier = hashlib.sha256(hojo_name.encode()).hexdigest()

    #出力の場所
    output_path = "../../output/{}/".format(hojo_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    #全体の大枠を作る
    iiif_json = {}
    iiif_json["@context"]   = ["http://iiif.io/api/presentation/2/context.json", "http://codh.rois.ac.jp/iiif/curation/1/context.json"]
    iiif_json["@id"]        = "https://mp.ex.nii.ac.jp/api/curation/json/" + identifier
    iiif_json["@type"]      = "cr:Curation"
    iiif_json["label"]      = "https://mp.ex.nii.ac.jp/api/curation/json/" + identifier
    iiif_json["selections"] = []

    #共通のselectionを作る
    selection = {}
    selection["@id"]       = "{}/range1".format(iiif_json["@id"])
    selection["@type"]     = "sc:Range"
    selection["label"]     = "Manual curation by IIIF Curation Viewer"
    selection["members"]   = []
    selection["within"] = {"@id":manifest_url, "@type":"sc:Manifest", "label":hojo_name}

    #ページごとにmemberを作る
    #rintervalsを読み込む
    with open("../../output/{}/rintervals.json".format(hojo_name), "r") as f:
        rintervals = json.load(f)

    #行探知
    for page in range(1, page_leng+1):
        print("Page {} line detection began".format(page))
        #準備
        canvas_id_path = hojo_path+"canvas_id.txt"
        relative_line_interval = rintervals["p{}".format(page)]
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
            member["metadata"].append({"label":"備考", "value"})
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
