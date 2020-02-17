from PIL import Image
import os
from multiprocessing import Pool

def resize_page(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    RESIZE_RATIO = 3

    hojo_path = "../../input/images/{}/p{}/".format(hojo_name, page)
    hojo_img_path = hojo_path + "{}-p{}.jpg".format(hojo_name, page)

    hojo = Image.open(hojo_img_path)
    weight, height = hojo.size
    resized_hojo = hojo.resize((int(weight/RESIZE_RATIO),int(height/RESIZE_RATIO)))
    resized_hojo.save(hojo_path+"resized.jpg")

    print("Resized {} Page {}".format(hojo_name, page))

def resize_hojo(hojo_name):
    contents    = os.listdir("../../input/images/{}/".format(hojo_name))
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-1 #hojo.txtを数えないことに注意！

    iter_ = []
    for page in range(1, page_leng+1):
        iter_.append((hojo_name, page))

    with Pool(processes=3) as pool:
        pool.map(resize_page, iter_)
