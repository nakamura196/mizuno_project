import json

def manifest2info(hojo_name):
    json_path = "../../../input/manifest/{}.json".format(hojo_name)

    with open(json_path) as f:
        manifest = json.load(f)

    info = {}

    info["identifier"]  = ""
    for data in manifest["metadata"]:
        if data["label"] == "identifier":
            info["identifier"]  = data["value"]
    info["@id"] = manifest["@id"]


    #{sequence_id: [[canvas1, image_url], [canvas2. image_url], ...]}という形
    sequence_num = 1
    for sequence in manifest["sequences"]:
        info["sequence_{}".format(sequence_num)] = []
        for canvas in sequence["canvases"]:
            canvas_info = []
            canvas_info.append(canvas["@id"])
            for image in canvas["images"]:
                canvas_info.append(image["resource"]["@id"])

            info["sequence_{}".format(sequence_num)].append(canvas_info)
        sequence_num += 1

    return info

#print(manifest2info("医方大成論 [A006464].json"))
