from annoy import AnnoyIndex
import os
import numpy
import glob
import json

# config
dims = 2048
trees = 100

t = AnnoyIndex(dims, metric='angular')

image_vectors_path = "data/center_output/image_vectors"
files = glob.glob(image_vectors_path+"/*.npy")

file_index_map = {}

for file_index in range(len(files)):
    filepath = files[file_index]

    file_vector = numpy.load(filepath)
    t.add_item(file_index, file_vector)

    filename = os.path.basename(filepath)
    filename_wo_ext = os.path.splitext(filename)[0]
    file_index_map[file_index] = filename_wo_ext

t.build(trees)
t.save('data/index.ann')


f2 = open('data/file_index_map.json', 'w')
json.dump(file_index_map, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))