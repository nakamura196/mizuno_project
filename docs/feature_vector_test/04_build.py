import numpy
import glob
from annoy import AnnoyIndex
from scipy import spatial
import json

# config
dims = 2048
# n_nearest_neighbors = 1000
trees = 100

t = AnnoyIndex(dims, metric='angular')

image_vectors_path = "output/image_vectors"
files = glob.glob(image_vectors_path+"/*.npy")

map = {}

for file_index in range(len(files)):
    # print(file_index)
    file = files[file_index]

    id = file.split("/")[-1].split(".")[0]

    file_vector = numpy.load(files[file_index])
    t.add_item(file_index, file_vector)
    map[file_index] = id

t.build(trees)
t.save('data/index.ann')

f2 = open('data/file_index_map.json', 'w')
json.dump(map, f2)
