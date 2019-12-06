#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from statistics import mean
from PIL import Image

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def calculate_line_interval(hojo_name, page):

    #ファイルを調達
    with open("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page), 'rb') as ff:
        content = ff.read()

    #Google Cloud Visionから物体検出してもらう
    print("Requesting to Google Cloud Vision...")
    request1 = get_prediction(content, "479921589070", "IOD7660926431366479872") #kanji-datasetの方
    request2 = get_prediction(content, "479921589070", "IOD9206927740949757952") #gray-kanji-datasetの方
    print("Response returned")

    print("Calculating line_interval...")

    #それぞれのレスポンスからbboxのx方向の長さを取得
    line_interval_candidates = []
    for payload in request1.payload:
        x_min = float(payload.image_object_detection.bounding_box.normalized_vertices[0].x)
        x_max = float(payload.image_object_detection.bounding_box.normalized_vertices[1].x)
        diff = x_max - x_min
        line_interval_candidates.append(diff)

    for payload in request2.payload:
        x_min = float(payload.image_object_detection.bounding_box.normalized_vertices[0].x)
        x_max = float(payload.image_object_detection.bounding_box.normalized_vertices[1].x)
        diff = x_max - x_min
        line_interval_candidates.append(diff)

    #物体検出できなかった場合はデフォルトのline_intervalにする
    if len(line_interval_candidates) == 0:
        line_interval_candidates.append(0.02)
        print("\tSet line_interval as default")

    #bboxのx方向の長さの平均値をrelative_line_intervalとする（あとでx方向の解像度と掛け算する）
    relative_line_interval = mean(line_interval_candidates)
    print("Finished calculating line_interval")

    return relative_line_interval

#法帖ごとにpredictionを実行
def generate_rintervals(hojo_name):
    contents = os.listdir("../../output/{}/preprocessed/back_black/".format(hojo_name))
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng = len(contents)-1 #hojo.txtを除くことに注意！

    for page in range(1, page_leng+1):
        print("Page {} request".format(page))
        relative_line_interval = calculate_line_interval(hojo_name, page)
        rintervals["p{}".format(page)] = relative_line_interval
        print("--------------------------------------------------------")
    with open("../../output/{}/rintervals.json".format(hojo_name), "w") as f:
        rint_json = json.dumps(rintervals)
        f.write(rint_json)

    print("Calculated relative_line_interval")
