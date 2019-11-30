from PIL import Image, ImageFilter
from multiprocessing import Pool

"""
def generate_filtered_image(iter_):
    hojo_name = iter_[0]
    im_copy = iter_[1]
    i = iter_[2]

    if i%2 == 1:
        return
    print("kernel {} filtering...".format(i+1))
    im_copy.filter(ImageFilter.MedianFilter(size=i+1))
    im_copy.save("./output/{}_k{}filter.jpg".format(hojo_name, i+1))
    print("kernel size {} filtering finished".format(i+1))
"""

hojo_name = input()
im = Image.open("./input/{}.jpg".format(hojo_name))
width, height = im.size

im.filter(ImageFilter.MedianFilter(size=123))
im.save("./output/{}_k{}filter.jpg".format(hojo_name, 123))

"""
print(width)
im_copies = [im.copy() for _ in range(5)]
print("copy finished")

iter_ = []
for i in range(5):
    iter_.append([hojo_name, im_copies[i], i*10+20])

with Pool(processes=3) as pool:
    pool.map(generate_filtered_image, iter_)
"""
