#1つのmanifestに1つのselection
#1つのselectionに各行の情報を入力する
import json, os
import hashlib

def generate_line_place(page, lines, RESIZE_RATIO):
    line_description = []
    for line in lines:
        x1, x2, y1, y2 = line[0], line[1], line[2], line[3]
        w = x2 - x1
        h = y2 - y1
        line_description.append("#xywh={},{},{},{}".format(RESIZE_RATIO*x1, y1, RESIZE_RATIO*w, RESIZE_RATIO*h))

    return line_description


def create_manifest(hojo_name, characterIsBlack=False):
    RESIZE_RATIO = 3

    #読み込み準備
    hojo_path   = "../../input/images/{}/".format(hojo_name)

    #法帖についての情報をゲット
    with open(hojo_path+"hojo_info.txt", "r") as f:
        hojo_info    = f.readlines()
        manifest_url = hojo_info[0].replace("\n", "")
        #identifier   = hojo_info[1].replace("\n", "")
    identifier = hashlib.sha1(hojo_name.encode()).hexdigest()

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
    with open("../../output/{}/line_place.json".format(hojo_name), "r") as f:
        line_place = json.load(f)

    page_leng = len(line_place)
    #行探知
    for page in range(1, page_leng+1):
        #準備
        canvas_id_path = hojo_path+"p{}/canvas_id.txt".format(page)
        with open(canvas_id_path, "r") as f:
            canvas_id = f.readlines()[0]
        lines = line_place["p{}".format(page)]

        #memberを作成
        line_description = generate_line_place(page, lines, RESIZE_RATIO)
        for i in range(len(line_description)):
            member = {"@type":"sc:Canvas"}
            member["@id"]   = canvas_id+line_description[i]
            member["label"] = "Page-{} Pixel-base line {}".format(page, i)
            member["metadata"] = []
            member["metadata"].append({"label":"作品名", "value":""})
            member["metadata"].append({"label":"行", "value":""})
            member["metadata"].append({"label":"備考", "value":""})
            selection["members"].append(member)

    iiif_json["selections"].append(selection)

    #出力
    output = json.dumps(iiif_json)
    with open("../../output/{}/{} curation.json".format(hojo_name, hojo_name), "w") as f:
        f.write(output)

    with open("/Users/aquan/git/mizuno_project/docs/curation/{} curation.json".format(hojo_name), "w") as f:
        f.write(output)
