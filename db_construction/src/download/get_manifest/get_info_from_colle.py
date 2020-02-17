import json

def collection2list():
    with open("../../../input/collection.json") as f:
        collection_list = json.load(f)

    colle = []

    for work in collection_list["manifests"]:
        colle.append({"url":work["@id"], "label":work["label"]})

    return colle
