import json, os
import hashlib
import time

#同じキーを持つ辞書のリストから適切な値を取り出す
def getValue(target, items):
    values = [x['value'] for x in items if 'label' in x and 'value' in x and x['label'] == target]
    return values[0] if values else None

def generate_curationList(ranking_top5_hojo):
    #準備としてcurationを全部持っておく
    curations = os.listdir("../curation")
    if ".DS_Store" in curations:
        curations.remove(".DS_Store")

    curation_of_search_target = {}
    for curation in curations:
        hojo_name = curation.replace(".json", "")
        with open("../curation/{}".format(curation), "r") as f:
            curation_of_search_target[hojo_name] = json.load(f)

    #なんか必要なやつ
    identifier = hashlib.sha1(time.time().encode()).hexdigest()

    #全体の大枠を作る
    curationList = {}
    curationList["@context"]   = ["http://iiif.io/api/presentation/2/context.json", "http://codh.rois.ac.jp/iiif/curation/1/context.json"]
    curationList["@id"]        = "https://mp.ex.nii.ac.jp/api/curation/json/" + identifier
    curationList["@type"]      = "cr:Curation"
    curationList["label"]      = "https://mp.ex.nii.ac.jp/api/curation/json/" + identifier
    curationList["selections"] = []

    #法帖ごとのselectionを作る
    range_num = 1
    sel_dic = {}

    for list_ in ranking_top5_hojo:
        #point = list_[0]
        hojo_name   = list_[1]
        page        = list_[2]
        line_num    = list_[3]

        if not hojo_name in sel_dic.keys():
            selection = {}
            selection["@id"]       = "{}/range{}".format(curationList["@id"], range_num)
            selection["@type"]     = "sc:Range"
            selection["label"]     = "Curation by Hojo Search System"
            selection["members"]   = []
            selection["within"] = curation_of_search_target[hojo_name]["selections"]["within"]

            #該当するmemberを探す（あとで関数にしよう）
            members = curation_of_search_target[hojo_name]["selections"]["members"]
            for member in members:
                p = getValue("Page", member["metadata"])
                if p == page:
                    l = getValue("Pixel line", member["metadata"])
                    if l == line_num:
                        selection["members"].append(member)

            sel_dic[hojo_name] = selection
            range_num += 1
        else:
            selection = sel_dic[hojo_name]
            #該当するmemberを探す（あとで関数にしよう）
            members = curation_of_search_target[hojo_name]["selections"]["members"]
            for member in members:
                p = getValue("Page", member["metadata"])
                if p == page:
                    l = getValue("Pixel line", member["metadata"])
                    if l == line_num:
                        selection["members"].append(member)

    for key in sel_dic.keys():
        curationList["selections"].append(sel_dic[key])


    return curationList
