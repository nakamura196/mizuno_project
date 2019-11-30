#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json
import os




file_index_map = {}
with open("data/file_index_map.json") as f:
    file_index_map = json.load(f)

########

# config
dims = 2048

t = AnnoyIndex(dims, metric='angular')
t.load('data/index.ann')

########

n_nearest_neighbors = 200

image_vectors_path = "output/image_vectors"
files = glob.glob(image_vectors_path+"/*.npy")


result_map = {}

for file_index in range(len(files)):

    file = files[file_index]

    id = file.split("/")[-1].split(".")[0]

    master_vector = numpy.load(file)

    nearest_neighbors = t.get_nns_by_vector(master_vector, n_nearest_neighbors)
    

    arr = []

    for j in range(0, len(nearest_neighbors)):

        neighbor_file_name = file_index_map[str(j)]

        neighbor_file_vector = numpy.load(image_vectors_path+"/"+neighbor_file_name+".jpg.npy")

        similarity = 1 - \
            spatial.distance.cosine(master_vector, neighbor_file_vector)
        rounded_similarity = int((similarity * 10000)) / 10000.0

        obj = {
            "id" : neighbor_file_name,
            "score": rounded_similarity
        }

        arr.append(obj)

    arr = sorted(arr, key=lambda x:x['score'], reverse=True)

    '''
    result_arr.append({
        "id" : id,
        "arr": arr
    })
    '''
    result_map[id] = {
        "id" : id,
        "arr": arr
    }

result_arr = []
for id in sorted(result_map):
    result_arr.append(result_map[id])

fw = open("data/predict/result.json", 'w')
json.dump(result_arr, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
