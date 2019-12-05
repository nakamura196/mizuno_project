from PIL import Image
import os

def resize_hojo(hojo_name, page):
    RESIZE_RATIO = 3

    hojo_path = "../../input/images/{}/p{}/".format(hojo_name, page)
    hojo_img_path = hojo_path + "{}-p{}.jpg".format(hojo_name, page)

    hojo = Image.open(hojo_img_path)
    weight, height = hojo.size
    resized_hojo = hojo.resize((int(weight/RESIZE_RATIO),int(height/RESIZE_RATIO)))
    resized_hojo.save(hojo_path+"resized.jpg")

    print("Resized {} Page {}".format(hojo_name, page))


if __name__ == "__main__":
    hojo_name = "泉州本淳化閣帖 八 [A006099-05]"
    hojo_folder_path = "../../input/images/{}/".format(hojo_name)
    contents    = os.listdir(hojo_folder_path)
    if ".DS_Store" in contents:
        contents.remove(".DS_Store")
    page_leng   = len(contents)-1 #hojo.txtを数えないことに注意！

    for page in range(1, page_leng+1):
        resize_hojo(hojo_name, page)
