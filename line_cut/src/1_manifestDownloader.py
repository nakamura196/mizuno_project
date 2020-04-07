import urllib.request, json, os

#collectionタイプからmanifest情報を入手
def collection2list(json_name):
    with open("../input/collection/{}.json".format(json_name)) as f:
        collection_list = json.load(f)

    colle = []
    #作品URL（マニフェストのURL）とマニフェスト名をcollection.jsonから入手
    for work in collection_list["manifests"]:
        colle.append({"url":work["@id"], "label":work["label"]})

    return colle

#指定されたURL先のマニフェストファイルを、作品名.jsonとしてダウンロード
def get_json(json_url, label):
    urllib.request.urlretrieve(json_url, "../input/manifest/{}.json".format(label))

    return "{}.json".format(label)

if __name__ == "__main__":
    #マニフェストファイルのダウンロード
    print("Enter the name of collection list")
    json_name = input()
    colle = collection2list(json_name)
    for col in colle:
        downloaded_name = get_json(col["url"], col["label"])
        print("downloaded " + downloaded_name)
